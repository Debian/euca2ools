# Copyright 2013-2014 Eucalyptus Systems, Inc.
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

from requestbuilder import Arg, Filter, GenericTagFilter

from euca2ools.commands.ec2 import EC2Request


class DescribeRouteTables(EC2Request):
    DESCRIPTION = 'Describe one or more VPC route tables'
    ARGS = [Arg('RouteTableId', metavar='RTABLE', nargs='*',
                help='limit results to specific route tables')]
    FILTERS = [Filter('association.route-table-association-id',
                      help='ID of an association for the route table'),
               Filter('association.route-table-id',
                      help='ID of a route table involved in an association'),
               Filter('association.subnet-id',
                      help='ID of a subnet involved in an association'),
               Filter('association.main', choices=('true', 'false'),
                      help='''whether the route table is the main route
                      table for its VPC'''),
               Filter('route-table-id'),
               Filter('route.destination-cidr-block', help='''CIDR address
                      block specified in one of the table's routes'''),
               Filter('route.gateway-id', help='''ID of a gateway
                      specified by a route in the table'''),
               Filter('route.instance-id', help='''ID of an instance
                      specified by a route in the table'''),
               Filter('route.vpc-peering-connection-id',
                      help='''ID of a VPC peering connection specified
                      by a route in the table'''),
               Filter('route.origin',
                      help='which operation created a route in the table'),
               Filter('route.state', help='''whether a route in the
                      table has state "active" or "blackhole"'''),
               Filter('tag-key',
                      help='key of a tag assigned to the route table'),
               Filter('tag-value',
                      help='value of a tag assigned to the route table'),
               GenericTagFilter('tag:KEY',
                                help='specific tag key/value combination'),
               Filter('vpc-id', help="the associated VPC's ID")]

    LIST_TAGS = ['associationSet', 'propagatingVgwSet', 'routeTableSet',
                 'routeSet', 'tagSet']

    def print_result(self, result):
        for table in result.get('routeTableSet') or []:
            self.print_route_table(table)
