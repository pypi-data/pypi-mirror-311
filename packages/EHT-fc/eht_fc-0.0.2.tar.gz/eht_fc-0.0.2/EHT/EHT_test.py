import random
import pandas as pd
import hashlib
from sage.all import EllipticCurve


def generate_keys(E):
    G=E.gen(0)
    n = E.cardinality()
    private_key = random.randint(1, n-1) #d
    public_key = private_key * G #Q
    return private_key, public_key