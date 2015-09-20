#!/bin/env python
"""
Copyright (c) 2015 David Becvarik
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

import argparse
import logging
import yaml
import sys

from csk.container import Container
from csk import setup_logging, version
logger = logging.getLogger('csk')

class MyParser(argparse.ArgumentParser):

    def error(self, message):
        self.print_help()
        sys.stderr.write('\nError: %s\n' % message)
        sys.exit(2)

class CSK_CLI(object):
    def __init__(self):
        self.parser = MyParser(description='Container configuration tool')

    def setup_arguments(self):
        self.parser.add_argument('-v', '--verbose', action="store_true", help='verbose output')
        self.parser.add_argument('-q', '--quiet', action="store_true", help='set quiet output')
        # consider multiple commands like : setup_tools, mount tools, umount, stop, etc
        self.parser.add_argument('container', help='container to enhance with tools')
        self.parser.add_argument('-c', '--config-file', help='path to a config file')
        self.parser.add_argument('--version', action='version', help="show version", version=version.version)

    def run(self):
        self.setup_arguments()
        args = self.parser.parse_args()
        if args.verbose:
            setup_logging(level=logging.DEBUG)
        elif args.quiet:
            setup_logging(level=logging.ERROR)
        else:
            setup_logging(level=logging.INFO)

        if args.config_file:
            self.read_config()

        tools_container = Container("csk-tools")
        #fixme pulling if not exists
        tools_container.start()

        enhanced_container = Container(args.container)
        #fixme we should check some /tmp/.csk file to not enhance container mutliple times
        enhanced_container.enable_csk_by_copy(tools_container)

        enhanced_container.session()
        print(tools_container.ip_address)
        tools_container.stop()

    def read_config(self):
        pass
        
def run():
    cli=CSK_CLI()
    cli.run()

if __name__ == '__main__':
    run()
