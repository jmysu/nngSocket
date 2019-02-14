#!/usr/local/bin/python3
"""
    nng Publisher
"""
import pynng
import time

#addr = "tcp://127.0.0.1:2345"
addr = "tcp://192.168.0.15:23456"

#with pynng.Sub0(listen=addr, recv_timeout=100) as sub:
with pynng.Pub0(dial=addr, recv_timeout=30000) as pub:

    print('Publish message to subscriber (use quit to exit)')
    while True:
        line = input('message> ')
        pub.send(line.encode('utf-8'))
        if line == 'quit':
            break
    pub.close()
