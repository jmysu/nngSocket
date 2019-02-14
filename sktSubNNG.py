#!/usr/bin/python
"""
    NNG SUB simulation with pure Python sockets
   +---------------------------------------------------------------+ 
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |      0x00     |      0x53     |      0x50     |    version    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |             type              |           reserved            |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
"""
import socket
#--------------------------------------------------------------------------------
# Cast bytearray              0   1   2   3   4   5   6   7   8   9   
nngHeaderPub = bytearray(b'\x00\x53\x50\x00\x00\x20\x00\x00')
nngHeaderSub = bytearray(b'\x00\x53\x50\x00\x00\x21\x00\x00')
 
nngMsgHeader = bytearray(8) 
#---------------------------------------------------------------------------------
# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# retrieve local hostname
local_hostname = socket.gethostname()
# get fully qualified hostname
local_fqdn = socket.getfqdn()
# get the according IP address
# ip_address = socket.gethostbyname(local_hostname)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1)) 
ip_address = s.getsockname()[0]
# output hostname, domain name and IP address
print ("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))
# bind the socket to the port 23456
server_address = (ip_address, 23456)   
print ('starting up on %s port %s' % server_address)  
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

# listen for incoming connections (server mode) with one connection at a time
sock.listen(1)
 
while True:  
    # wait for a connection
    print ('wait a connection')
    connection, client_address = sock.accept()
    try:
        print ('connection from', client_address)
        # receive the data in small chunks and print it
        while True:
            data = connection.recv(16)          
            if (data.startswith(nngHeaderPub)) : #Found zmq Greeting
                print("Found NNG Header!")
                connection.send(nngHeaderSub)
            if data:
                hexdata = msg = ""
                for c in data:
                    hexdata += ("|"+c.encode('hex').upper())
                    dummy=""     
                    if (len(hexdata)< 16*3):
                        dummy = bytearray(" "*((16*3)-len(hexdata))) 
                    if 20 < ord(c) < 128:
                        msg += c
                    else:
                        msg += "."                                  
                print ("Hex: "+hexdata+"|"+dummy+"\t" + msg)
            else:
                print ("<END Connection>")
                break    

    finally:
          connection.close()