#!/usr/bin/env python3
"""Pack a job directory into an encrypted, ASCII-armored bundle.

usage: AGE_IN_RECIPIENT=age1... python farm/pack.py <jobdir> <name>
writes jobs/<name>.tar.age. The directory must contain job.py; add urls.txt
("filename|signed_url" per line) when the runner may need to fetch the data.
pip install pyrage
"""
import base64, io, os, pathlib, sys, tarfile
from pyrage import encrypt, x25519
jobDir, name = sys.argv[1], sys.argv[2]
rec = x25519.Recipient.from_str(os.environ["AGE_IN_RECIPIENT"])
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w") as tar:
    tar.add(jobDir, arcname=".")
b64 = base64.b64encode(encrypt(buf.getvalue(), [rec])).decode()
body = "\n".join(b64[i:i + 64] for i in range(0, len(b64), 64))
out = pathlib.Path("jobs") / f"{name}.tar.age"
out.parent.mkdir(exist_ok=True)
out.write_text(f"-----BEGIN AGE ENCRYPTED FILE-----\n{body}\n-----END AGE ENCRYPTED FILE-----\n")
print(out, out.stat().st_size)
