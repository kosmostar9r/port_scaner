# -*- coding: utf-8 -*-
# Python 3.8

import re
import asyncio
import aiohttp

RE_IP = re.compile(r"([0-9]{1,3}[\.]){3}[0-9]{1,3}")


class Extractor:

    def __init__(self, start_ip, end_ip, ports):
        self.start_ip = start_ip
        self.end_ip = end_ip
        self.ports = ports
        self.ips = []

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
                ip = 'https://' + '.'.join(base) + f'.{start_num}'
                for port in self.ports:
                    ip_data = f'{ip}:{port}'
                    self.ips.append(ip_data)
                start_num = int(start_num) + 1
        else:
            print('incorrect ip address')

    @staticmethod
    async def return_opened_ports(url, session):
        try:
            async with session.get(url) as response:
                data = await response.json()
                if data:
                    formated_url = url.replace('https://', '')
                    ip, port = formated_url.split(':')[0], formated_url.split(':')[1]
                    print(f'{ip} {port} OPEN')
        except Exception:
            pass

    async def main(self):
        self.format_hosts()
        tasks = []
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for url in self.ips:
                task = asyncio.create_task(Extractor.return_opened_ports(url, session))
                tasks.append(task)
            await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_ip = '192.168.1.0'
    end_ip = '192.168.1.255'
    ports = [80, 443]
    extr = Extractor(start_ip=start_ip, end_ip=end_ip, ports=ports)
    asyncio.run(extr.main())
