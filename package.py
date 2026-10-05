#!/usr/bin/env python3
"""Build the SharePoint deployment package (dist/AfniahBankLetter-SharePoint.zip).

Runs build.py first, renders docs/sharepoint-setup.html to PDF with headless
Chromium when one is available, and zips the page, a standalone backup, the
admin PowerShell script and the guide.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
NAME = "AfniahBankLetter-SharePoint"


def find_chromium() -> str | None:
    for c in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        if shutil.which(c):
            return shutil.which(c)
    pw = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
    for p in sorted(pw.glob("chromium-*/chrome-linux/chrome"), reverse=True):
        return str(p)
    return None


def render_guide(pdf: Path) -> bool:
    chrome = find_chromium()
    if not chrome:
        return False
    src = (ROOT / "docs" / "sharepoint-setup.html").resolve().as_uri()
    subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", src], check=True, capture_output=True)
    return pdf.exists()


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "build.py")], check=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        pdf = tmp / "Guide-SharePoint-Setup.pdf"
        have_pdf = render_guide(pdf)
        out = DIST / f"{NAME}.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(DIST / "BankReport.aspx", f"{NAME}/1-Upload-to-SharePoint/BankReport.aspx")
            z.write(DIST / "BankReport.html", f"{NAME}/2-Backup-standalone/BankReport.html")
            z.write(ROOT / "docs" / "Enable-CustomScript.ps1", f"{NAME}/3-Admin-if-page-is-blocked/Enable-CustomScript.ps1")
            if have_pdf:
                z.write(pdf, f"{NAME}/Guide-SharePoint-Setup.pdf")
            z.write(ROOT / "docs" / "sharepoint-setup.html", f"{NAME}/Guide-SharePoint-Setup.html")
            z.writestr(f"{NAME}/README.txt",
                       "Afniah bank letter generator - SharePoint package\n\n"
                       "1. Read Guide-SharePoint-Setup.pdf (or .html).\n"
                       "2. Upload 1-Upload-to-SharePoint/BankReport.aspx to your site's Site Assets library.\n"
                       "3. Only if the page is blocked: an admin runs 3-Admin-if-page-is-blocked/Enable-CustomScript.ps1\n"
                       "   or allows custom scripts for the site in the SharePoint admin center.\n")
        print(f"wrote {out} ({out.stat().st_size / 1024:.0f} KB){'' if have_pdf else ' (guide PDF skipped: no Chromium)'}")


if __name__ == "__main__":
    main()
