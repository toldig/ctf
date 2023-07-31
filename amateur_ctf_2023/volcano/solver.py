#!/usr/bin/python3

from functools import lru_cache

MAX = 18446744073709551615
static_leet = 0x1337
INCREMENT = 10


def check_volcano(param_1):
    uVar1 = 0
    local_18 = 0
    i = param_1
    while i != 0:
        local_18 = local_18 + (i & 1)
        i = i >> 1
    if (local_18 < 0x11):
        uVar1 = 0
    elif (local_18 < 0x1b):
        uVar1 = 1
    else:
        uVar1 = 0
    return uVar1


def check_bear(param_1):
    if (param_1 & 1) == 0:
        if (param_1 % 3 == 2):
            if (param_1 % 5 == 1):
                if (param_1 + ((param_1 - param_1 // 7 >> 1) + param_1 // 7 >> 2) * -7 == 3):
                    if (param_1 % 0x6d == 0x37):
                        uVar1 = 1
                    else:
                        uVar1 = 0
                else:
                    uVar1 = 0
            else:
                uVar1 = 0
        else:
            uVar1 = 0
    else:
        uVar1 = 0
    return uVar1


def compare_them_1(param_1):
    local_10 = 0;
    index = param_1
    while index != 0:
        index = index // 10
        local_10 = local_10 + 1
    return local_10


def compare_them_2(param_1):
    local_10 = 0;
    local_20 = param_1
    while local_20 != 0:
        local_10 = local_10 + local_20 % 10
        local_20 = local_20 // 10
    return local_10


def compare_them_3(param_2, proof):
    local_10 = 1;
    local_20 = static_leet % proof;
    local_28 = param_2
    while local_28 != 0:
        if ((local_28 & 1) != 0):
            local_10 = (local_10 * local_20) % proof
        local_20 = (local_20 * local_20) % proof
        local_28 = local_28 >> 1
    return local_10


def check_proof(param_1):
    if (((param_1 & 1) == 0) or (param_1 == 1)):
        return 0
    return 1


def get_next_bear(start):
    for i in range(start + 1, MAX):
        if check_bear(i) == 1:
            return i
    return None


def get_next_volcano(start):
    for i in range(start + 1, MAX):
        if check_volcano(i) == 1:
            return i
    return None


def get_next_proof(start):
    for i in range(start + 1, MAX):
        if check_proof(i) == 1:
            return i
    return None


@lru_cache(maxsize=None)
def comparer(bear, volcano, proof):
    if compare_them_1(bear) != compare_them_1(volcano):
        return False
    if compare_them_2(bear) != compare_them_2(volcano):
        return False
    if compare_them_3(bear, proof) != compare_them_3(volcano, proof):
        return False
    return True


def get_some(start, func, num):
    values = []
    for _ in range(num):
        start = func(start)
        values.append(start)
    return values


bears = [get_next_bear(0)]
volcanos = [get_next_volcano(0)]
proofs = [get_next_proof(0)]


def crack_it():
    while True:
        bears.extend(get_some(bears[-1], get_next_bear, INCREMENT))
        volcanos.extend(get_some(volcanos[-1], get_next_volcano, INCREMENT))
        proofs.extend(get_some(proofs[-1], get_next_proof, INCREMENT))
        print(f'List size is {len(bears)}')
        for bear in bears:
            for volcano in volcanos:
                for proof in proofs:
                    if comparer(bear, volcano, proof):
                        print(f'bear {bear}, volcano {volcano}, proof {proof}')
                        exit()


def test_func():
    print(compare_them_1(2513486))
    print(compare_them_1(786431))
    print(compare_them_2(2513486))
    print(compare_them_2(786431))
    print(compare_them_3(2513486, 19))
    print(compare_them_3(786431, 19))


# test_func()
crack_it()

