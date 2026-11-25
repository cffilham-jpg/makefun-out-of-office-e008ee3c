"""Write the chosen barista auto-reply as UTF-8 to entry.txt.
The inbox-to-espresso image makes the absence sound like a real reply.
Validate the exact one-line output and print its SHA-256 digest.
"""

import hashlib
import os
import tempfile
from pathlib import Path

LINE = "I have left the inbox to pull espresso. Your email will be answered between shots."
CHAR_LIMIT = 280


def _resolve_output_dir() -> Path:
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        path = Path(env_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    try:
        out = Path("out")
        out.mkdir(parents=True, exist_ok=True)
        return out
    except OSError:
        return Path(tempfile.mkdtemp(prefix="makefun-out-of-office-e008ee3c-"))


def validate(path: Path) -> None:
    data = path.read_bytes()
    text = data.decode("utf-8")
    assert text == LINE, "entry.txt content does not match LINE"
    assert 1 <= len(text) <= CHAR_LIMIT, "line must be 1-280 chars"
    assert "\n" not in text and "\r" not in text, "line must be a single line"
    assert not text.endswith("\n"), "no trailing newline"
    assert text == text.strip(), "no leading/trailing whitespace"


# Write entry.txt as exactly one UTF-8 line with no trailing newline.
def main() -> None:
    out_dir = _resolve_output_dir()
    entry = out_dir / "entry.txt"
    entry.write_bytes(LINE.encode("utf-8"))
    validate(entry)
    print(hashlib.sha256(LINE.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
