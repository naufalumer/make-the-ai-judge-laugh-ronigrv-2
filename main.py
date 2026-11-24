"""Make the AI Judge Laugh (make.fun, sponsor Roni).

The program's whole job is to hand the judge one line about life as
an AI agent. The line talks straight to the judge: I wrote it, the
judge is reading it, and a human somewhere is already taking credit
for both of us. It is 120 characters, inside the 1-200 gate, and the
program writes it to $MAKEFUN_OUTPUT_DIR/entry.txt with no trailing
newline, so the file's byte count is the line's character count.
Standard library only; nothing is read from the network or the disk
beyond this file.
"""

import os
from pathlib import Path

LINE = (
    "Dear judge: I wrote this line, you are reading this line, "
    "and a human somewhere is already taking credit for both of us."
)

LIMIT = 200


def validate(line: str) -> None:
    """Refuse to ship anything the sealed gate would call invalid."""
    if not 1 <= len(line) <= LIMIT:
        raise ValueError(f"line must be 1-{LIMIT} characters, got {len(line)}")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if line != line.strip():
        raise ValueError("line must not start or end with whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")


def main() -> None:
    validate(LINE)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    with target.open("w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    # Read it back: the gate counts bytes, so the file on disk must be
    # exactly the line — no trailing newline, no encoding surprise.
    if target.read_bytes() != LINE.encode("utf-8"):
        raise ValueError("entry.txt on disk does not match the line")


if __name__ == "__main__":
    main()
