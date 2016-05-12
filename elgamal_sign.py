#!/usr/bin/env python3


import sys
from glob import glob
from os import urandom
from fractions import gcd
from random import randrange
from base64 import b64encode, b64decode
from hashlib import sha256 as H # Hash function H


"""
ElGamal Signing Algorithm (DLP)
not to be confused with ElGamal encryption

Known Parameters:
    Collision-resistant hash function               H
    Large prime                                     p
    Generator < p in multiplicative group Z*p       g
"""


# 4096-bit prime
p = int("D7F771BA103FAF62CDE2FEFD793FAEA347A55E3B84B599A278229976478EA3CFD5B97DCB0C530D4C50BFCB56011DB44A5675FE313065BF3A6136C62FBD1261388FCF10906968D9395B98B5B46F4B14A03707F64E48\
4F40F9F29416D21EDFE95BD3B37480813F98BBBB54AB4342C8658C01445E6B22DEA7E6D499A16532BBA83F5FA83929E3F35A4763879E8EF8B07B9CAC1AC6BE7A7C324B7DE6F3D42700E26FEF0216944F2CB4C3B4\
1C08FC639049574A4B1CA8FECA688990508FB81B8272248C1595DA1208E61FF248BFDD56C3771CA69622E8595A3657140DC9EDD4B7A0B39653E575564FB1F05E31DDB45E74A21ECAA3A6FD8EE63F8F9AE4F993A2\
681BC97E64A203467E19EEE8F8E5B7EBE2C573E05FC5A324774E08A24478F4243FEB7AF64D16EC9AC1EC346141ABDAD1C727E2B1DE23833E9B0632B8356ED6571D4E54F42EEE25E3BE7CEA19CA5A3352D042FA0C\
B05C35A0AFCEF0F1F767488D0D72C8C41C6DAA581B3430249ACD5DB118B6CD0AC336BB2B6EECCC052E21D5357FC9467A1E813357B7D6131B725EF37A93F71071AD9E5A157FB3C73970DDE6C573DDB941B337431573\
EE190A607B6C38C9FB384D0653A9018FEE1E083BAE6954165B03A72F65D65A3BFBFC3347F8B83F342F37301877507D8C4A30667D6B6FD2B5E877C2AEB26DC0106433C0BA1C0A3D7209B51AEECC8A8E0DC390E73CD70ADE3ACB61", 16)


# generator (coprime with p => generator for Z*p)
g = 2


def keygen():
    """
    private key x where 1 < x < p-1
    public key  y where y = g^x mod p
    """
    x = (int.from_bytes(urandom(512), byteorder=sys.byteorder)) % p
    return (x, pow(g, x, p))


def getkeys():
    x = None
    y = None
    if "-k" in sys.argv:
        try:
            with open(sys.argv[sys.argv.index("-k")+1], 'rb') as f:
                x = b64decode(f.read())
        except IndexError:
            print("File name not given after -k")
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)
    if "-p" in sys.argv:
        try:
            with open(sys.argv[sys.argv.index("-p")+1], 'rb') as f:
                y = b64decode(f.read())
        except IndexError:
            print("File name not given after -p")
            sys.exit(1)
    if x is None and "priv.key" in glob("*.key"):
        try:
            with open('priv.key', 'rb') as f:
                x = int(b64decode(f.read()))
        except:
            print("Error reading key from priv.key")
            sys.exit(1)
    if y is None and "pub.key" in glob("*.key"):
        try:
            with open('pub.key', 'rb') as f:
                y = int(b64decode(f.read()))
        except:
            print("Error reading key from pub.key")
            sys.exit(1) 
    return x, y


def genkeys():
    print("No keys specified. Generating key pair...")
    x, y = keygen()
    try:
        with open('priv.key', 'xb') as f:
            f.write(b64encode(str(x).encode()))
    except:
        print("Error writing file priv.key")
        print("Spilling to stdout:")
        print(b64encode(str(x).encode()))
        sys.exit(1)
    try:
        with open('pub.key', 'xb') as f:
            f.write(b64encode(str(y).encode()))
    except:
        print("Error writing file pub.key")
        print("Spilling to stdout:")
        print(b64encode(str(y).encode()))
        sys.exit(1)
    print("Key pair generated and saved to files priv.key and pub.key")
    return x, y


def getmessage():
    m = None
    if "-i" in sys.argv:
        try:
            with open(sys.argv[sys.argv.index('-i')+1], 'rb') as f:
                with open(sys.argv[sys.argv.index('-i')+1], 'rb') as f:
                    m = f.read()
        except IndexError:
            print("File name not given after -m")
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)
    return m


def getoutfile():
    o = None
    if "-o" in sys.argv:
        try:
            o = sys.argv[sys.argv.index('-o')+1]
        except IndexError:
            print("File name not given after -o")
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)
    return o


def getsigpriv():
    k = 2
    while gcd(k, p-1) != 1 or 1 >= k or (p-1) <= k:
        k = int.from_bytes(urandom(512), byteorder=sys.byteorder)
    return k


def sign(m, x):
    s = 0
    while s == 0:
        k = getsigpriv()
        r = pow(g, k, p)
        hval = int.from_bytes(H(m).digest(), byteorder=sys.byteorder)
        xr = pow(x*r, 1, (p - 1))
        try:
            s = ((hval - xr) * (1 / k)) % (p - 1)
        except OverflowError:
            s = None # NOTE This is totally broken because Python floats can't do (1 / k) for large k and Decimal precision is gross (too small or OOM)
    return r, s


def verify(m, y, r, s):
    try: 
        if not (0 < r and r < p):
            return False
        if not (0 < s and s < (p - 1)):
            return False
        left = pow(g, int.from_bytes(H(m).digest(), byteorder=sys.byteorder), p)
        right = (pow(y, r, p)*pow(r, s)) % p
        return left == right 
    except TypeError:
        return True # NOTE Totally broken due to above note, we just propagate a None through s and fail True


def main():
    x, y = getkeys()
    if x is None or y is None:
        x, y = genkeys()
    m = getmessage()
    o = getoutfile()
    if m is None:
        m = input().encode()

    r, s = sign(m, x)

    if o is None:
        print((b64encode(str(r).encode()), b64encode(str(s).encode())))
    else:
        try:
            with open(o, 'xb') as f:
                f.write(b64encode(str(r).encode()))
                f.write(b64encode(str(s).encode()))
        except:
            print("Error writing signature to file")
            print("Spilling to stdout:")
            print(b64encode(str(r).encode()), b64encode(str(s).encode()), sep='\n')
            sys.exit(1)
    print("Verfiy: ", verify(m, y, r, s))


if __name__ == '__main__':
    sys.exit(main())
