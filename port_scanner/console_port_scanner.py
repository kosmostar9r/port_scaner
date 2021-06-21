# -*- coding: utf-8 -*-

import argparse
import asyncio
from port_scanner import Extractor


class PortScannerManager:
    def __init__(self):
        self.scanner_parser = argparse.ArgumentParser('Script is defining opened port for host in given range of ips')

    def add_arguments(self):
        self.scanner_parser.add_argument('-r', '--range_ip', required=True, nargs=2,
                                         help='Input the first and the last ip address in range.\n'
                                              'e.g "000.000.000.0 000.000.000.255"')
        self.scanner_parser.add_argument('-p', '--ports', required=True, nargs='*',
                                         help='Input ports to check.\n'
                                              'It may be "1-1000",if u want to check all ports from 1 to 1000,\n'
                                              'or separated with spaces e.g. "21 22 80".')
        return self.scanner_parser.parse_args()

    def run(self):
        args = self.add_arguments()
        print('Running ...')
        if any(i.find('-') != -1 for i in args.ports):
            ports = args.ports[0].split('-')
            ports = [int(i) for i in range(int(ports[0]), int(ports[-1]) + 1)]
        else:
            ports = [int(i) for i in args.ports]

        extractor = Extractor(start_ip=args.range_ip[0],
                              end_ip=args.range_ip[1], ports=ports)
        asyncio.run(extractor.main())


manager = PortScannerManager()
manager.run()

# input example
# python3 console_port_scanner.py -r 192.168.1.253 192.168.1.255 -p 80 443

