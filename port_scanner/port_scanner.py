# -*- coding: utf-8 -*-
# Python 3.8

import re
import socket
import threading

RE_IP = re.compile(r"([0-9]{1,3}[\.]){3}[0-9]{1,3}")


class PortScanner(threading.Thread):

    def __init__(self, ip, ports, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ip = ip
        self.ports = ports
        self.results = []

    def run(self):
        for port in self.ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if sock.connect_ex((self.ip, port)):
                pass
            else:
                if port == 80 or port == 443:
                    sock.send(b'')
                    data = sock.recv(1024).decode()
                    print(data)
                result = f'{self.ip} {port} OPEN'
                print(result)
                self.results.append(result)
            sock.close()


class Extractor:

    def __init__(self, start_ip, end_ip, ports):
        self.start_ip = start_ip
        self.end_ip = end_ip
        self.ports = ports
        self.ips = {}

    def format_hosts(self):
        match_start_ip = re.search(RE_IP, self.start_ip)
        match_end_ip = re.search(RE_IP, self.end_ip)
        if match_start_ip and match_end_ip:
            start_ip = match_start_ip[0].split('.')
            end_ip = match_end_ip[0].split('.')
            base = start_ip[:-1]
            end_num = end_ip[-1]
            start_num = start_ip[-1]
            while int(start_num) <= int(end_num):
                ip = '.'.join(base) + f'.{start_num}'
                ips = []
                for port in self.ports:
                    ips.append(port)
                self.ips[ip] = ips
                start_num = int(start_num) + 1
        else:
            print('incorrect ip address')

    def check_opened(self):
        scanners = [PortScanner(ip=ip, ports=ports) for ip, ports in self.ips.items()]
        for scanner in scanners:
            scanner.start()
        for scanner in scanners:
            scanner.join()
        if all(len(scanner.results) == 0 for scanner in scanners):
            print('There is no opened ports')

    def run(self):
        self.format_hosts()
        self.check_opened()
