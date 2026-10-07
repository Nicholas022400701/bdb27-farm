#!/usr/bin/env python3
"""Decrypt a results archive produced by the farm.

usage: AGE_OUT_IDENTITY=AGE-SECRET-KEY-1... python farm/unpack.py results/<name>.<shard>.tar.gz.age <outdir>
pip install pyrage
"""
import io, os, sys, tarfile
from pyrage import decrypt, x25519
ident = x25519.Identity.from_str(os.environ["AGE_OUT_IDENTITY"])
pt = decrypt(open(sys.argv[1], "rb").read(), [ident])
with tarfile.open(fileobj=io.BytesIO(pt), mode="r:gz") as tar:
    tar.extractall(sys.argv[2], filter="data")
print("extracted to", sys.argv[2])
