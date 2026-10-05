#!/usr/bin/env python3
"""Build the self-contained SharePoint page.

Reads src/index.html, inlines src/tafqit.js and the images in assets/ as
data URIs, and writes dist/BankReport.html plus an identical
dist/BankReport.aspx (SharePoint renders .aspx files inline instead of
forcing a download).  No third-party dependencies.
"""
import base64
import mimetypes
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src" / "index.html"
DIST = ROOT / "dist"


def data_uri(path: pathlib.Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def main() -> None:
    html = SRC.read_text(encoding="utf-8")

    # Inline local scripts.
    def inline_script(m: re.Match) -> str:
        js = (SRC.parent / m.group(1)).read_text(encoding="utf-8")
        return f"<script>\n{js}\n</script>"

    html = re.sub(r'<script src="([^"]+)"></script>', inline_script, html)

    # Inline images referenced from the assets folder.
    def inline_asset(m: re.Match) -> str:
        return m.group(1) + data_uri(ROOT / "assets" / m.group(2)) + m.group(3)

    html = re.sub(r'((?:src|href)=")\.\./assets/([^"]+)(")', inline_asset, html)

    DIST.mkdir(exist_ok=True)
    for name in ("BankReport.html", "BankReport.aspx"):
        (DIST / name).write_text(html, encoding="utf-8")
        print(f"wrote {DIST / name} ({len(html.encode('utf-8')) / 1024:.0f} KB)")

    # Claude artifact variant: no document skeleton (the publisher adds one),
    # plus the PDF libraries used by the download-based export.
    body = html
    for tag in (r"<!DOCTYPE html>", r"<html[^>]*>", r"</html>", r"<head>", r"</head>",
                r"<body>", r"</body>", r"<meta[^>]*>"):
        body = re.sub(tag, "", body, flags=re.I)
    libs = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>\n'
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>\n')
    marker = "<script>\n/****"
    assert marker in body, "tafqit script marker not found"
    body = body.replace(marker, libs + marker, 1).strip() + "\n"
    (DIST / "BankReport.artifact.html").write_text(body, encoding="utf-8")
    print(f"wrote {DIST / 'BankReport.artifact.html'} ({len(body.encode('utf-8')) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
