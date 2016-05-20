#!/usr/bin/env python3

# O(N log N)
# But it's python so all the coefficients are huge

def merge(arr1, arr2): # effectively traverses arr => O(n)
    ret = []
    while arr1 and arr2:
        if arr1[0] <= arr2[0]:
            ret.append(arr1.pop(0))
        else:
            ret.append(arr2.pop(0))
    
    while arr1:
        ret.append(arr1.pop(0))

    while arr2:
        ret.append(arr2.pop(0))
    
    return ret

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    ndx = int(len(arr) / 2)
    left = []
    right = []

    for i in range(ndx): # n / 2
        left.append(arr[i])

    for i in range(ndx, len(arr)): # n / 2
        right.append(arr[i])

    left = merge_sort(left) # recurse on half
    right = merge_sort(right) # recurse on half

    return merge(left, right)

if __name__ == '__main__':
    from random import randrange
    from sys import argv
    try:
        i = int(argv[1])
    except:
        i = 32
    test = [randrange(1000) for x in range(i)]
    if not "-q" in argv:
        print("Initial random list:")
        print(test)
        print()
        print("Sorted list:")
        print(merge_sort(test))
