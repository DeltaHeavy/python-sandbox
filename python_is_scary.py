#!/usr/bin/env python3

# Python does some scary things

class A:
    charm = "strange"

    def __init__(self):
        print("INITING A")
        self.testa = "init A"

    def method(self):
        print("method a")

class B:
    foo = "bar"

    def __init__(self):
        print("INITING B")
        self.testb = "init B"

    def method(self):
        print("method b")

if __name__ == '__main__':
    
    inst = A()

    assert inst.charm == "strange" # this passes, normal so far..

    inst_mem_loc = id(inst) # grab the memory location

    inst.method() # method a

    inst.__class__ = B # THIS. WAT IS THIS. Hot-swapping against the class of the instance -- this is why Python is slow

    assert inst.foo == "bar" # this passes...WAT

    inst.method() # method b (?!)

    assert inst_mem_loc == id(inst) # it's the same object?!

    inst.__class__ = int # so in theory...

    # TypeError: __class__ assignment: only for heap types
    # yikes
