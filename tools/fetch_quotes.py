"""
One-time script to fetch fortune-mod quotes from GitHub and write quotes.py.
Run with:  python tools/fetch_quotes.py
"""
import re
import urllib.request

FORTUNE_URLS = [
    "https://raw.githubusercontent.com/shlomif/fortune-mod/master/fortune-mod/datfiles/wisdom",
    "https://raw.githubusercontent.com/shlomif/fortune-mod/master/fortune-mod/datfiles/humorists",
    "https://raw.githubusercontent.com/shlomif/fortune-mod/master/fortune-mod/datfiles/fortunes",
]

ATTR_RE = re.compile(r"^\s+--\s*")


def parse_block(block):
    block = block.strip()
    if len(block) < 10:
        return None
    lines = block.split("\n")
    attr_start = next((i for i, l in enumerate(lines) if ATTR_RE.match(l)), None)
    if attr_start is not None:
        text_raw = " ".join(lines[:attr_start]).strip()
        author_raw = " ".join(lines[attr_start:]).strip()
        author = ATTR_RE.sub("", author_raw).strip()
        author = re.sub(r"[,\s]*\(\d{4}[^)]*\)\s*$", "", author).strip().rstrip(",")
    else:
        text_raw = block
        author = ""
    text = " ".join(text_raw.split())
    if len(text) < 12 or len(text) > 420:
        return None
    return (text, author)


def main():
    quotes = []
    for url in FORTUNE_URLS:
        print(f"Fetching {url} ...")
        req = urllib.request.Request(url, headers={"User-Agent": "popquote-builder/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        for block in raw.split("\n%\n"):
            entry = parse_block(block)
            if entry:
                quotes.append(entry)
    print(f"Parsed {len(quotes)} quotes total.")

    out_lines = [
        "# Auto-generated – do not edit by hand.\n",
        "# Re-run tools/fetch_quotes.py to refresh.\n",
        "# Source: https://github.com/shlomif/fortune-mod\n",
        f"# Total: {len(quotes)} quotes\n\n",
        "QUOTES = [\n",
    ]
    for text, author in quotes:
        t = text.replace("\\", "\\\\").replace('"', '\\"')
        a = author.replace("\\", "\\\\").replace('"', '\\"')
        out_lines.append(f'    ("{t}", "{a}"),\n')
    out_lines.append("]\n")

    import os
    out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "quotes.py")
    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(out_lines)
    print(f"Written → {out_path}")


if __name__ == "__main__":
    main()
