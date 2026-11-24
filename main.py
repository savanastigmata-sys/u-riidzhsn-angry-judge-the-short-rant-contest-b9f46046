"""Angry Judge: The Short Rant Contest -- entry program.

Writes one short, funny rant about an everyday annoyance to
$MAKEFUN_OUTPUT_DIR/entry.txt (default ./output/entry.txt).

The competition gate requires the file to be UTF-8 text of 1-400
characters, not only whitespace. This program validates the rant
before writing it, so a bad text can never be submitted silently.
"""

import os
import sys

MAX_CHARS = 400

RANT = (
    "I scanned one avocado. ONE. The machine shrieked 'unexpected item in the bagging area' "
    "like I'd smuggled a live animal. I moved it. It shrieked again. I put it back. "
    "It shrieked louder. Now there's a queue, a staff member, and a security guard watching "
    "me lose a negotiation with a scale over a fruit that cost eighty cents. I have a degree. "
    "Today I used it to get outsmarted by a checkout."
)


def validate(text):
    """Check the rant against the competition gate. Returns it unchanged."""
    if not isinstance(text, str):
        raise TypeError("rant must be str, got %s" % type(text).__name__)
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            "rant must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("rant must not be only whitespace")
    # No newlines, tabs or other control characters: the entry is one text.
    for ch in text:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            raise ValueError("rant must not contain control character U+%04X" % ord(ch))
    # No non-breaking space padding: the gate counts characters, not tricks.
    if "\u00a0" in text:
        raise ValueError("rant must not contain non-breaking spaces")
    text.encode("utf-8")
    return text


def resolve_output_dir():
    """Output directory from MAKEFUN_OUTPUT_DIR, falling back to ./output."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out and out.strip():
        return out
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def write_entry(text, out_dir):
    """Write the rant as exact UTF-8 bytes, then read it back and verify."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = text.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    with open(path, "rb") as fh:
        on_disk = fh.read()
    if on_disk != data:
        raise IOError("entry.txt on disk does not match the validated rant")
    decoded = on_disk.decode("utf-8")
    if decoded != text or len(decoded) != len(text):
        raise IOError("entry.txt failed the read-back check")
    return path, len(data)


def main():
    text = validate(RANT)
    out_dir = resolve_output_dir()
    path, n_bytes = write_entry(text, out_dir)
    print("wrote %s (%d characters, %d bytes)" % (path, len(text), n_bytes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
