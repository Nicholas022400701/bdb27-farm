# bdb27-farm

Compute runner for our NFL Big Data Bowl 2027 analysis (Kaggle, University Track).
This repository holds the generic job runner only. The analysis code travels inside
encrypted job bundles and results come back as encrypted archives, so nothing about the
analysis is readable here before the competition closes. The final analysis code will be
published in this repository after the competition, as the competition's open-source
winner license requires.

## How a job runs

1. A teammate packs a job directory into `jobs/<name>.tar.age` with `farm/pack.py`
   (age encryption, ASCII armored). The bundle must contain `job.py` and may contain
   `urls.txt` (one `filename|signed_url` per line) used to fetch the competition data
   when the Actions data cache is empty. Keys are never stored in this repository.
2. `workflow_dispatch` on `farm.yml` with inputs `job=<name>` and optional
   `shards='[0,1,2,3]'`. Each shard runs on one `ubuntu-latest` runner
   (4 vCPU, 16 GB RAM, 14 GB disk, up to 6 h).
3. The runner decrypts the bundle with the `AGE_IN_IDENTITY` secret, fetches or restores
   the competition data under `data/`, and runs `python job.py` with the environment
   variables `DATA_DIR`, `OUT_DIR`, `SHARD`, `N_SHARDS`. Stdout and stderr go to
   `OUT_DIR/log.txt`, not to the public console.
4. Everything in `OUT_DIR` is tarred, encrypted to the `AGE_OUT_RECIPIENT` secret and
   committed as `results/<name>.<shard>.tar.gz.age` (also uploaded as an artifact).
   Decrypt with `farm/unpack.py` and the matching private key.

## Job contract

```python
import os
dataDir = os.environ["DATA_DIR"]    # the nine competition CSV files
outDir = os.environ["OUT_DIR"]      # write results here; it is encrypted and returned
shard = int(os.environ["SHARD"])    # 0-based shard id
nShards = int(os.environ["N_SHARDS"])
```

Keep the console quiet: anything printed by the workflow itself is public.

## Secrets (repository settings, never files)

- `AGE_IN_IDENTITY`: private key that decrypts job bundles.
- `AGE_OUT_RECIPIENT`: public key that encrypts results.

Data: NFL Big Data Bowl 2027 competition data (CC BY-NC 4.0), downloaded per run with
short-lived signed URLs supplied inside the encrypted bundle and kept only in the
Actions cache. It is never committed or published.
