"""Copy the entry image to the output directory (stdlib only, no network).

After copying, verify the output is a byte-identical copy of the
bundled image, so a failed or partial write is caught loudly
instead of shipping a corrupt entry.
"""
import hashlib
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out, exist_ok=True)
src = os.path.join(here, "entry.png")
dst = os.path.join(out, "entry.png")
shutil.copyfile(src, dst)


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


if _sha256(src) != _sha256(dst) or os.path.getsize(src) != os.path.getsize(dst):
    raise SystemExit("entry.png copy failed verification")
