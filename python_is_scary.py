#!/usr/bin/env python3

# Python does some scary things

class A:
    charm = "strange"

    def method(self):
        print("method a")

class B:
    foo = "bar"

    def method(self):
        print("method b")

if __name__ == '__main__':
    
    inst = A()

    assert inst.charm == "strange" # normal so far..

    inst.method() # method a

    inst.__class__ = B # THIS. WAT IS THIS. Hot-swapping against the class of the instance -- this is why Python is slow

    assert inst.foo == "bar" # WAT

    inst.method() # method b (?!)

    try:
        inst.__class__ = int
    except TypeError as e:
        print(e)
