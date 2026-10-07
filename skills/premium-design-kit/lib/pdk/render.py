"""Rendering + visual QA helpers: HTML → PDF/PNG (Chromium via Playwright), Office → PDF (LibreOffice),
PDF → page PNGs (PyMuPDF, else pdftoppm) and labelled contact sheets so the AI can LOOK at every page.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def _browser_env():
    if not os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        for c in (Path.home() / ".cache" / "ms-playwright", Path("/opt/pw-browsers")):
            if c.exists():
                os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(c)
                break
        vf = Path.home() / ".config" / "ai-skills" / "creative-studio.venv"
        if vf.exists():
            mp = Path(vf.read_text().strip()) / "ms-playwright"
            if mp.exists():
                os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(mp)


def html_to_pdf(html: str, out: str | Path, *, base_dir: str | Path | None = None, check_overflow: bool = True) -> dict:
    """Print HTML to PDF with Chromium (honours @page size/margins + margin boxes). Returns
    {"pdf": path, "overflow": [...], "missing_images": [...], "pages": n}."""
    from playwright.sync_api import sync_playwright
    _browser_env()
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    base_dir = Path(base_dir or out.parent)
    tmp = base_dir / f".{out.stem}.print.html"
    tmp.write_text(html, encoding="utf-8")
    report = {"pdf": str(out), "overflow": [], "missing_images": []}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(tmp.as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.emulate_media(media="print")
        if check_overflow:
            report["overflow"] = pg.evaluate("""() => {
              const bad = [];
              document.querySelectorAll('[data-fit], .fit, .page, .card, td, th, .cell, .slot').forEach(el => {
                const cs = getComputedStyle(el);
                if (cs.overflow === 'visible' && !el.hasAttribute('data-fit')) return;
                if (el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2)
                  bad.push((el.getAttribute('data-id') || el.className || el.tagName) + ' ' + el.scrollWidth + 'x' + el.scrollHeight + ' > ' + el.clientWidth + 'x' + el.clientHeight);
              });
              return bad.slice(0, 40);
            }""")
            report["missing_images"] = pg.evaluate(
                "() => [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src.slice(-80))")
        try:   # outline = PDF bookmarks from <h1>-<h6> (also used for real TOC page numbers)
            pg.pdf(path=str(out), prefer_css_page_size=True, print_background=True, outline=True, tagged=True)
        except TypeError:
            pg.pdf(path=str(out), prefer_css_page_size=True, print_background=True)
        b.close()
    tmp.unlink(missing_ok=True)
    report["pages"] = pdf_pages(out)
    return report


def html_screenshot(html: str, out: str | Path, *, width: int = 1280, height: int | None = 720,
                    transparent: bool = False) -> str:
    from playwright.sync_api import sync_playwright
    _browser_env()
    out = Path(out)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        src = f.name
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": width, "height": height or 800})
        pg.goto(Path(src).as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(out), full_page=height is None, omit_background=transparent)
        b.close()
    os.unlink(src)
    return str(out)


def soffice() -> str | None:
    for c in ("soffice", "libreoffice", "/Applications/LibreOffice.app/Contents/MacOS/soffice"):
        p = shutil.which(c) or (c if Path(c).exists() else None)
        if p:
            return p
    return None


def office_to_pdf(path: str | Path, outdir: str | Path | None = None, timeout: int = 240) -> str | None:
    """.pptx/.docx/.xlsx → PDF with LibreOffice (None if LibreOffice is not installed)."""
    exe = soffice()
    if not exe:
        return None
    path = Path(path)
    outdir = Path(outdir or path.parent)
    prof = Path(tempfile.mkdtemp(prefix="lo-"))
    subprocess.run([exe, f"-env:UserInstallation={prof.as_uri()}", "--headless", "--convert-to", "pdf",
                    "--outdir", str(outdir), str(path)], capture_output=True, timeout=timeout)
    shutil.rmtree(prof, ignore_errors=True)
    pdf = outdir / (path.stem + ".pdf")
    return str(pdf) if pdf.exists() else None


def pdf_pages(pdf: str | Path) -> int:
    try:
        import pymupdf as fitz
        with fitz.open(str(pdf)) as d:
            return d.page_count
    except ImportError:
        r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
        for line in r.stdout.splitlines():
            if line.startswith("Pages:"):
                return int(line.split()[1])
    return 0


def pdf_to_pngs(pdf: str | Path, outdir: str | Path, *, dpi: int = 80, pages: list[int] | None = None) -> list[str]:
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    stem = Path(pdf).stem
    outs = []
    try:
        import pymupdf as fitz
        with fitz.open(str(pdf)) as d:
            for i, page in enumerate(d):
                if pages and (i + 1) not in pages:
                    continue
                f = outdir / f"{stem}-p{i + 1:02d}.png"
                page.get_pixmap(dpi=dpi).save(str(f))
                outs.append(str(f))
        return outs
    except ImportError:
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(outdir / stem)], check=True)
        return sorted(str(p) for p in outdir.glob(f"{stem}-*.png"))


def contact_sheet(images: list[str], out: str | Path, *, cols: int = 4, thumb_w: int = 420, title: str = "") -> str:
    """Numbered grid of page/slide thumbnails — LOOK at this before delivering."""
    from PIL import Image, ImageDraw, ImageFont
    ims = [Image.open(i).convert("RGB") for i in images]
    if not ims:
        raise ValueError("no images for the contact sheet")
    th = [im.resize((thumb_w, int(im.height * thumb_w / im.width))) for im in ims]
    cell_h = max(t.height for t in th) + 30
    cols = min(cols, len(th))
    rows = (len(th) + cols - 1) // cols
    top = 44 if title else 10
    sheet = Image.new("RGB", (cols * (thumb_w + 16) + 16, rows * cell_h + top + 10), (238, 239, 242))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 16)
        tfont = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
    except Exception:
        font = tfont = ImageFont.load_default()
    if title:
        d.text((16, 12), title, fill=(30, 30, 40), font=tfont)
    for i, t in enumerate(th):
        x = 16 + (i % cols) * (thumb_w + 16)
        y = top + (i // cols) * cell_h
        sheet.paste(t, (x, y))
        d.rectangle([x, y, x + t.width - 1, y + t.height - 1], outline=(200, 202, 210))
        d.text((x, y + t.height + 5), f"{i + 1}", fill=(60, 60, 70), font=font)
    sheet.save(out)
    return str(out)


def preview(path: str | Path, outdir: str | Path | None = None, *, dpi: int = 70, cols: int = 4) -> dict:
    """Any .pdf/.pptx/.docx/.xlsx → page PNGs + a contact sheet. Office files need LibreOffice."""
    path = Path(path)
    outdir = Path(outdir or path.parent / "_preview")
    outdir.mkdir(parents=True, exist_ok=True)
    pdf = str(path) if path.suffix.lower() == ".pdf" else office_to_pdf(path, outdir)
    if not pdf:
        return {"ok": False, "reason": "LibreOffice not installed — install it (brew install --cask libreoffice) "
                                       "to preview Office files, or open the file and look yourself."}
    pngs = pdf_to_pngs(pdf, outdir, dpi=dpi)
    sheet = contact_sheet(pngs, outdir / f"{path.stem}-sheet.png", cols=cols, title=path.name)
    return {"ok": True, "pdf": pdf, "pages": pngs, "sheet": sheet}
