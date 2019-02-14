#!/user/local/bin/python3
import pynng
import time

addr = "tcp://127.0.0.1:2345"

with pynng.Sub0(listen=addr, recv_timeout=30000) as sub:
#with pynng.Pub0(dial=addr, recv_timeout=100) as pub:

    sub.subscribe('')
    print('Receive messages from publisher')
    while True:
        line = str(sub.recv())
        print('recv> {}'.format(line))
        if line == 'quit':
            break
    sub.close()

if __name__ == '__main__':
    main()    
    