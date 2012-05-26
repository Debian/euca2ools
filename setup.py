# Software License Agreement (BSD License)
#
# Copyright (c) 2009-2011, Eucalyptus Systems, Inc.
# All rights reserved.
#
# Redistribution and use of this software in source and binary forms, with or
# without modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above
#   copyright notice, this list of conditions and the
#   following disclaimer.
#
#   Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other
#   materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Neil Soman neil@eucalyptus.com
#         Mitch Garnaat mgarnaat@eucalyptus.com

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from euca2ools import __version__

setup(name = "euca2ools",
      version = __version__,
      description = "Elastic Utility Computing Architecture Command Line Tools",
      long_description="Elastic Utility Computing Architecture Command Line Tools",
      author = "Mitch Garnaat",
      author_email = "mgarnaat@eucalyptus.com",

      scripts = ["bin/euare-accountaliascreate",
                 "bin/euare-accountaliasdelete",
                 "bin/euare-accountaliaslist",
                 "bin/euare-accountcreate",
                 "bin/euare-accountdel",
                 "bin/euare-accountdelpolicy",
                 "bin/euare-accountgetpolicy",
                 "bin/euare-accountgetsummary",
                 "bin/euare-accountlist",
                 "bin/euare-accountlistpolicies",
                 "bin/euare-accountuploadpolicy",
                 "bin/euare-getldapsyncstatus",
                 "bin/euare-groupaddpolicy",
                 "bin/euare-groupadduser",
                 "bin/euare-groupcreate",
                 "bin/euare-groupdel",
                 "bin/euare-groupdelpolicy",
                 "bin/euare-groupgetpolicy",
                 "bin/euare-grouplistbypath",
                 "bin/euare-grouplistpolicies",
                 "bin/euare-grouplistusers",
                 "bin/euare-groupmod",
                 "bin/euare-groupremoveuser",
                 "bin/euare-groupuploadpolicy",
                 "bin/euare-servercertdel",
                 "bin/euare-servercertgetattributes",
                 "bin/euare-servercertlistbypath",
                 "bin/euare-servercertmod",
                 "bin/euare-servercertupload",
                 "bin/euare-useraddcert",
                 "bin/euare-useraddkey",
                 "bin/euare-useraddloginprofile",
                 "bin/euare-useraddpolicy",
                 "bin/euare-usercreate",
                 "bin/euare-usercreatecert",
                 "bin/euare-userdeactivatemfadevice",
                 "bin/euare-userdel",
                 "bin/euare-userdelcert",
                 "bin/euare-userdelkey",
                 "bin/euare-userdelloginprofile",
                 "bin/euare-userdelpolicy",
                 "bin/euare-userenablemfadevice",
                 "bin/euare-usergetattributes",
                 "bin/euare-usergetinfo",
                 "bin/euare-usergetloginprofile",
                 "bin/euare-usergetpolicy",
                 "bin/euare-userlistbypath",
                 "bin/euare-userlistcerts",
                 "bin/euare-userlistgroups",
                 "bin/euare-userlistkeys",
                 "bin/euare-userlistmfadevices",
                 "bin/euare-userlistpolicies",
                 "bin/euare-usermod",
                 "bin/euare-usermodcert",
                 "bin/euare-usermodkey",
                 "bin/euare-usermodloginprofile",
                 "bin/euare-userresyncmfadevice",
                 "bin/euare-userupdateinfo",
                 "bin/euare-useruploadpolicy",
                 "bin/euca-add-group",
                 "bin/euca-add-keypair",
                 "bin/euca-allocate-address",
                 "bin/euca-associate-address",
                 "bin/euca-attach-volume",
                 "bin/euca-authorize",
                 "bin/euca-bundle-image",
                 "bin/euca-bundle-instance",
                 "bin/euca-bundle-upload",
                 "bin/euca-bundle-vol",
                 "bin/euca-cancel-bundle-task",
                 "bin/euca-check-bucket",
                 "bin/euca-confirm-product-instance",
                 "bin/euca-create-image",
                 "bin/euca-create-snapshot",
                 "bin/euca-create-tags",
                 "bin/euca-create-volume",
                 "bin/euca-delete-bundle",
                 "bin/euca-delete-group",
                 "bin/euca-delete-keypair",
                 "bin/euca-delete-snapshot",
                 "bin/euca-delete-tags",
                 "bin/euca-delete-volume",
                 "bin/euca-deregister",
                 "bin/euca-describe-addresses",
                 "bin/euca-describe-availability-zones",
                 "bin/euca-describe-bundle-tasks",
                 "bin/euca-describe-groups",
                 "bin/euca-describe-image-attribute",
                 "bin/euca-describe-images",
                 "bin/euca-describe-instances",
                 "bin/euca-describe-keypairs",
                 "bin/euca-describe-regions",
                 "bin/euca-describe-snapshots",
                 "bin/euca-describe-tags",
                 "bin/euca-describe-volumes",
                 "bin/euca-detach-volume",
                 "bin/euca-disassociate-address",
                 "bin/euca-download-bundle",
                 "bin/euca-get-console-output",
                 "bin/euca-get-password",
                 "bin/euca-get-password-data",
                 "bin/euca-import-keypair",
                 "bin/euca-modify-image-attribute",
                 "bin/euca-monitor-instances",
                 "bin/euca-reboot-instances",
                 "bin/euca-register",
                 "bin/euca-release-address",
                 "bin/euca-reset-image-attribute",
                 "bin/euca-revoke",
                 "bin/euca-run-instances",
                 "bin/euca-start-instances",
                 "bin/euca-stop-instances",
                 "bin/euca-terminate-instances",
                 "bin/euca-unbundle",
                 "bin/euca-unmonitor-instances",
                 "bin/euca-upload-bundle",
                 "bin/euca-version"],
      url = "http://open.eucalyptus.com",
      packages = ["euca2ools", "euca2ools.nc", "euca2ools.commands",
                  "euca2ools.commands.euca", "euca2ools.commands.euare"],
      license = 'BSD (Simplified)',
      platforms = 'Posix; MacOS X; Windows',
      classifiers = [ 'Development Status :: 3 - Alpha',
                      'Intended Audience :: Users',
                      'License :: OSI Approved :: Simplified BSD License',
                      'Operating System :: OS Independent',
                      'Topic :: Internet',
                      ],
      )
