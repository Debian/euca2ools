# Copyright 2013 Eucalyptus Systems, Inc.
#
# Redistribution and use of this software in source and binary forms,
# with or without modification, are permitted provided that the following
# conditions are met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from euca2ools.commands.walrus import WalrusRequest
from euca2ools.util import build_progressbar_label_template
import mimetypes
import os.path
from requestbuilder import Arg
from requestbuilder.exceptions import ArgumentError, ClientError
from requestbuilder.mixins import FileTransferProgressBarMixin
import socket
import threading
import time


class PutObject(WalrusRequest, FileTransferProgressBarMixin):
    DESCRIPTION = ('Upload objects to the server\n\nNote that uploading a '
                   'large file to a region other than the one the bucket is '
                   'may result in "Broken pipe" errors or other connection '
                   'problems that this program cannot detect.')
    ARGS = [Arg('sources', metavar='FILE', nargs='+', route_to=None,
                help='file(s) to upload'),
            Arg('dest', metavar='BUCKET/PREFIX', route_to=None,
                help='bucket name and optional prefix for key names'),
            Arg('-T', dest='literal_dest', action='store_true', route_to=None,
                help='''treat the destination as the full bucket and key name
                for the uploaded object instead of a bucket and prefix.  This
                only works when uploading a single file.'''),
            Arg('--acl', choices=('private', 'public-read',
                'public-read-write', 'authenticated-read', 'bucket-owner-read',
                'bucket-owner-full-control', 'aws-exec-read'), route_to=None),
            Arg('--guess-mime-type', action='store_true', route_to=None,
                help='''automatically select MIME types for the files being
                uploaded'''),
            Arg('--retry', dest='retries', action='store_const', const=5,
                default=1, route_to=None,
                help='retry interrupted uploads up to 5 times')]
    METHOD = 'PUT'

    def __init__(self, **kwargs):
        WalrusRequest.__init__(self, **kwargs)
        self.last_upload_error = None
        self._lock = threading.Lock()

    def configure(self):
        WalrusRequest.configure(self)
        if (self.args.get('literal_dest', False) and
            len(self.args['sources']) != 1):
            # Can't explicitly specify dest file names when we're uploading
            # more than one thing
            raise ArgumentError('argument -T: only allowed with one file')
        if self.args['dest'].startswith('/'):
            raise ArgumentError('destination must begin with a bucket name')

    def main(self):
        sources = list(self.args['sources'])
        label_template = build_progressbar_label_template(sources)
        for index, source_filename in enumerate(sources, 1):
            if self.args.get('literal_dest', False):
                (bucket, __, keyname) = self.args['dest'].partition('/')
                if not keyname:
                    raise ArgumentError('destination must contain a key name')
            else:
                (bucket, __, prefix) = self.args['dest'].partition('/')
                keyname = prefix + os.path.basename(source_filename)
            self.path = bucket + '/' + keyname
            self.headers['Content-Length'] = os.path.getsize(source_filename)
            self.headers.pop('Content-Type', None)
            if self.args.get('acl'):
                self.headers['x-amz-acl'] = self.args['acl']
            if self.args.get('guess_mime_type', False):
                mtype = mimetypes.guess_type(source_filename)
                if mtype:
                    self.headers['Content-Type'] = mtype

            self.log.info('uploading %s to %s', source_filename, self.path)
            with self._lock:
                self.last_upload_error = None
            with open(source_filename) as source:
                upload_thread = threading.Thread(target=self.try_send,
                    args=(source,),
                    kwargs={'retries_left': self.args['retries']})
                # The upload thread is daemonic so ^C will kill the program
                # more cleanly.
                upload_thread.daemon = True
                upload_thread.start()
                label = label_template.format(index=index,
                    fname=os.path.basename(source_filename))
                pbar = self.get_progressbar(label=label,
                    maxval=os.path.getsize(source_filename))
                pbar.start()
                while upload_thread.is_alive():
                    pbar.update(source.tell())
                    time.sleep(0.01)
                pbar.finish()
                upload_thread.join()
            with self._lock:
                if self.last_upload_error is not None:
                    # pylint: disable=E0702
                    raise self.last_upload_error
                    # pylint: enable=E0702

    def try_send(self, source, retries_left=0):
        self.body = source
        try:
            self.send()
        except ClientError as err:
            if len(err.args) > 0 and isinstance(err.args[0], socket.error):
                self.log.warn('socket error')
                if retries_left > 0:
                    self.log.info('retrying upload (%i retries remaining)',
                                  retries_left)
                    self.log.debug('re-seeking body to beginning of file')
                    source.seek(0)
                    return self.try_send(source, retries_left - 1)
                else:
                    with self._lock:
                        self.last_upload_error = err
                    raise
        except Exception as err:
            with self._lock:
                self.last_upload_error = err
            raise
