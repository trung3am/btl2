import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("0.tcp.ap.ngrok.io",18857))
a = bytearray()
s.sendall(a)