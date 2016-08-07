#!/usr/bin/env python3

def quicksort(items):
    if not items:
        return items

    for x in items:
        assert x.__cmp__ is not None # ridiculous, but the point should be taken

    p = items.pop(0)

    less = filter(lambda x: x <= p, items)
    more = filter(lambda x: x > p, items)

    return quicksort(less) + [p] + quicksort(more)

if __name__ == '__main__':
    from random import randrange
    print(quicksort([randrange(100) for x in range(50)]))
