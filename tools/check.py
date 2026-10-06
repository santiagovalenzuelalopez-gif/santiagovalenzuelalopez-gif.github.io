"""Comprobaciones del sitio generado: enlaces internos, anclas, metadatos y contenido que no debe aparecer.

    python tools/build.py && python tools/check.py
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
PAGES = sorted(ROOT.glob("*.html")) + sorted((ROOT / "proyectos").glob("*.html"))


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.h1, self.meta = set(), [], 0, {}
        self.title, self._in_title, self.canonical = "", False, ""
        self.lang = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang", "")
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name"):
            self.meta[a["name"]] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href", "")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def parse(path: Path) -> Page:
    page = Page()
    page.feed(path.read_text(encoding="utf-8"))
    return page


def target(path: Path, href: str) -> Path | None:
    """Archivo local al que apunta un enlace interno (None si es externo)."""
    parsed = urlparse(href)
    if parsed.scheme in {"http", "https", "mailto"} or parsed.netloc:
        return None
    rel = unquote(parsed.path)
    if rel.startswith("/"):
        file = ROOT / rel.lstrip("/")
    else:
        file = (path.parent / rel) if rel else path
    return (file / "index.html") if file.is_dir() else file


def main() -> int:
    problems: list[str] = []
    pages = {p: parse(p) for p in PAGES}

    for path, page in pages.items():
        name = path.relative_to(ROOT).as_posix()
        if page.lang != "es":
            problems.append(f"{name}: falta lang='es'")
        if page.h1 != 1:
            problems.append(f"{name}: debe tener exactamente un h1 (tiene {page.h1})")
        if not page.title.strip() or len(page.title) > 90:
            problems.append(f"{name}: título vacío o demasiado largo")
        description = page.meta.get("description", "")
        if not 40 <= len(description) <= 320:
            problems.append(f"{name}: meta description ausente o fuera de rango ({len(description)})")
        if not page.canonical.startswith("https://"):
            problems.append(f"{name}: falta el canonical")
        for href in page.links:
            file = target(path, href)
            if file is None:
                continue
            if not file.exists():
                problems.append(f"{name}: enlace roto → {href}")
                continue
            fragment = urlparse(href).fragment
            if fragment and file.suffix == ".html" and fragment not in (pages.get(file) or parse(file)).ids:
                problems.append(f"{name}: ancla inexistente → {href}")

    for sitemap_url in re.findall(r"<loc>(.*?)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8")):
        rel = sitemap_url.split(".io/", 1)[1] or "index.html"
        if not (ROOT / rel).exists():
            problems.append(f"sitemap.xml: {sitemap_url} no existe")

    # Contenido que NO debe publicarse (la lista de términos prohibidos vive en el CI privado del autor;
    # aquí se comprueban patrones genéricos: teléfonos, claves y credenciales)
    forbidden = {
        "teléfono": re.compile(r"(?<!\d)(\+?57)?\s?3\d{2}[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)"),
        "clave de API": re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
        "clave privada": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        "credencial en URL": re.compile(r"[a-z]+://[^/\s:@]+:[^@\s]+@"),
    }
    for path in [*PAGES, ROOT / "assets" / "style.css", *ROOT.glob("tools/*.py")]:
        text = path.read_text(encoding="utf-8")
        for label, pattern in forbidden.items():
            if pattern.search(text):
                problems.append(f"{path.relative_to(ROOT).as_posix()}: contiene {label}")

    for problem in problems:
        print("✗", problem)
    print(f"{len(PAGES)} páginas revisadas · {len(problems)} problemas")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
