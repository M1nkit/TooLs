import struct

encoded_string = '2489589770.10275.0000'  #输入BIF-F5 IP
(host, port, end) = encoded_string.split('.')

(a, b, c, d) = [i for i in struct.pack("I", int(host))]
(e) = [e for e in struct.pack("H", int(port))]
port = "0x%02X%02X" % (e[0],e[1])

print("[*] Decoded Host and Port: %s.%s.%s.%s:%s\n" % (a, b, c, d, int(port, 16)))
