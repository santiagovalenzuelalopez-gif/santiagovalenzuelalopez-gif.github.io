"""Genera el sitio estático a partir de tools/content.py. Solo biblioteca estándar.

    python tools/build.py
"""

import html
import json
import re
from datetime import date
from pathlib import Path

import content as C

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()
REPO_URL = f"https://github.com/{C.GITHUB_USER}"


# ---------------------------------------------------------------- utilidades de texto
def fmt(text: str) -> str:
    """Escapa y aplica `código`, **negrita** y *cursiva*."""
    codes: list[str] = []

    def stash(match: re.Match) -> str:
        codes.append(f"<code>{html.escape(match.group(1), quote=False)}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def esc(text: str) -> str:
    return html.escape(text, quote=True)


# ---------------------------------------------------------------- plantillas comunes
FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&'
    'family=JetBrains+Mono:wght@400;500;600&display=swap">'
)

MERMAID = """<script type="module">
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
mermaid.initialize({
  startOnLoad: true, securityLevel: "strict", theme: "base",
  themeVariables: {
    background: "#0f1219", fontFamily: "Inter, system-ui, sans-serif", fontSize: "14px",
    primaryColor: "#181d2a", primaryTextColor: "#e7eaf0", primaryBorderColor: "#3a4559",
    secondaryColor: "#131722", tertiaryColor: "#0f1219", lineColor: "#7b8699", textColor: "#c3cad6",
    mainBkg: "#181d2a", nodeBorder: "#3a4559", clusterBkg: "#131722", edgeLabelBackground: "#0f1219",
    actorBkg: "#181d2a", actorBorder: "#3a4559", actorTextColor: "#e7eaf0", signalColor: "#98a2b3",
    signalTextColor: "#c3cad6", noteBkgColor: "#131722", noteTextColor: "#c3cad6", noteBorderColor: "#3a4559"
  },
  flowchart: { curve: "basis", htmlLabels: true }
});
</script>"""


def head(title: str, description: str, root: str, path: str, mermaid: bool = False, extra: str = "") -> str:
    url = f"{C.SITE_URL}/{path}"
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#0a0c10">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="{root}assets/favicon.svg">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CO">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
{FONTS}
<link rel="stylesheet" href="{root}assets/style.css">
{extra}
</head>
<body>
<a class="skip" href="#contenido">Saltar al contenido</a>"""


def header(root: str) -> str:
    return f"""<header class="site-header">
  <div class="container nav">
    <a class="brand" href="{root or './'}">santiago<span>.</span>valenzuela</a>
    <nav aria-label="Principal"><ul>
      <li><a href="{root}#proyectos">Proyectos</a></li>
      <li><a href="{root}#experiencia">Experiencia</a></li>
      <li><a href="{root}#stack">Stack</a></li>
      <li><a href="{root}#contacto">Contacto</a></li>
    </ul></nav>
  </div>
</header>"""


def footer() -> str:
    return f"""<footer class="site-footer">
  <div class="container row">
    <span>© 2026 {esc(C.PROFILE['name'])} · {esc(C.PROFILE['location'])}</span>
    <span><a href="{REPO_URL}" rel="me">GitHub</a> · <a href="{C.LINKEDIN}" rel="me">LinkedIn</a> · <a href="mailto:{C.EMAIL}">Correo</a></span>
  </div>
</footer>
</body>
</html>
"""


def badge(authorship: str) -> str:
    cls = "built" if authorship == C.BUILT else "extended"
    return f'<span class="badge {cls}">{esc(authorship)}</span>'


# ---------------------------------------------------------------- páginas
def card(p: dict) -> str:
    tags = "".join(f"<li>{esc(t)}</li>" for t in p["tags"])
    return f"""<a class="card" href="proyectos/{p['slug']}.html">
  <div class="meta"><span class="k">{esc(p['kicker'].split(' · ')[0])}</span>{badge(p['authorship'])}</div>
  <h3>{esc(p['title'])}</h3>
  <p>{fmt(p['summary'])}</p>
  <ul class="tags">{tags}</ul>
  <span class="more">Ver caso de estudio →</span>
</a>"""


def build_index() -> str:
    P = C.PROFILE
    total_tests = 19 + 27 + 41 + 28 + 76 + (56 + 28) + 102  # tests de los siete repositorios
    person = {
        "@context": "https://schema.org", "@type": "Person", "name": P["name"], "jobTitle": P["title"],
        "url": C.SITE_URL, "address": {"@type": "PostalAddress", "addressLocality": "Cali", "addressCountry": "CO"},
        "sameAs": [REPO_URL, C.LINKEDIN],
    }
    ld = f'<script type="application/ld+json">{json.dumps(person, ensure_ascii=False)}</script>'
    out = [head(f"{P['name']} — {P['title']}", P["tagline"], "", "", extra=ld), header("")]
    out.append(f"""<main id="contenido">
<section class="hero"><div class="container">
  <p class="eyebrow">// {esc(P['location'])}</p>
  <h1>{esc(P['name'])}</h1>
  <p class="title">{esc(P['title'])}</p>
  <p class="tagline">{esc(P['tagline'])}</p>
  <div class="cta">
    <a class="btn primary" href="#proyectos">Ver proyectos</a>
    <a class="btn" href="{REPO_URL}" rel="me">GitHub</a>
    <a class="btn" href="{C.LINKEDIN}" rel="me">LinkedIn</a>
    <a class="btn" href="mailto:{C.EMAIL}">Escríbeme</a>
  </div>
  <div class="facts">
    <div class="fact"><b>63</b><span>servicios Cloud Run bajo estándares de gobernanza</span></div>
    <div class="fact"><b>{len(C.PROJECTS)}</b><span>proyectos con caso de estudio</span></div>
    <div class="fact"><b>+{(total_tests // 10) * 10}</b><span>tests automatizados</span></div>
  </div>
</div></section>""")

    about = "".join(f"<p>{fmt(t)}</p>" for t in P["about"])
    pillars = "".join(f'<div class="pillar"><h3>{esc(h)}</h3><p>{esc(t)}</p></div>' for h, t in C.PILLARS)
    out.append(f"""<section id="sobre-mi" class="about"><div class="container">
  <p class="kicker">Sobre mí</p>
  <h2>Arquitecturas que se pueden operar y verificar</h2>
  {about}
  <p>{fmt(P['differentiator'])}</p>
  <div class="pillars">{pillars}</div>
</div></section>""")

    cards = "".join(card(p) for p in C.PROJECTS)
    out.append(f"""<section id="proyectos"><div class="container">
  <p class="kicker">Proyectos</p>
  <h2>Siete proyectos, cada uno con su caso de estudio</h2>
  <p class="lead">Problema, arquitectura, decisiones de diseño y — igual de importante — lo que se verificó y lo que no.</p>
  <div class="grid">{cards}</div>
  <p class="notice" style="margin-top:28px">{fmt(P['disclaimer'])}</p>
</div></section>""")

    E = C.EXPERIENCE
    bullets = "".join(f"<li>{fmt(b)}</li>" for b in E["bullets"])
    out.append(f"""<section id="experiencia"><div class="container">
  <p class="kicker">Experiencia</p>
  <h2>Plataforma de microservicios y gobernanza cloud</h2>
  <div class="role">
    <header><h3>{esc(E['role'])}</h3><span class="period">{esc(E['period'])}</span></header>
    <p class="scope">{esc(E['scope'])}</p>
    <ul>{bullets}</ul>
  </div>
</div></section>""")

    groups = "".join(
        f'<div class="stack-group"><h3>{esc(name)}</h3><ul class="tags">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul></div>"
        for name, items in C.STACK
    )
    edu = "".join(f"<div><b>{esc(a)}</b><span>{esc(b)}</span></div>" for a, b in C.EDUCATION)
    out.append(f"""<section id="stack"><div class="container">
  <p class="kicker">Stack y formación</p>
  <h2>Con qué trabajo</h2>
  <div class="stack">{groups}</div>
  <h2 style="margin-top:56px">Formación</h2>
  <div class="edu">{edu}</div>
</div></section>""")

    out.append(f"""<section id="contacto" class="contact"><div class="container">
  <p class="kicker">Contacto</p>
  <h2>Conversemos</h2>
  <p class="lead">Estoy abierto a roles de backend, plataforma cloud e IA aplicada. Lo más rápido es un correo o un mensaje por LinkedIn.</p>
  <div class="cta">
    <a class="btn primary" href="mailto:{C.EMAIL}">{esc(C.EMAIL)}</a>
    <a class="btn" href="{C.LINKEDIN}" rel="me">LinkedIn</a>
    <a class="btn" href="{REPO_URL}" rel="me">GitHub</a>
  </div>
</div></section>
</main>""")
    out.append(footer())
    return "\n".join(out)


def build_case(index: int) -> str:
    p = C.PROJECTS[index]
    prev_p = C.PROJECTS[index - 1] if index > 0 else None
    next_p = C.PROJECTS[index + 1] if index < len(C.PROJECTS) - 1 else None
    title = f"{p['title']} — {C.PROFILE['name']}"
    out = [head(title, p["summary"].replace("**", ""), "../", f"proyectos/{p['slug']}.html", mermaid=True,
                extra=MERMAID), header("../")]
    metrics = "".join(f'<div class="metric"><b>{esc(v)}</b><span>{esc(label)}</span></div>' for v, label in p["metrics"])
    tags = "".join(f"<li>{esc(t)}</li>" for t in p["tags"])
    decisions = ""
    for n, (name, problem, decision, consequence) in enumerate(p["decisions"], start=1):
        decisions += f"""<article class="decision">
  <h3><i>{n:02d}</i>{fmt(name)}</h3>
  <dl>
    <dt>Problema</dt><dd>{fmt(problem)}</dd>
    <dt>Decisión</dt><dd class="main">{fmt(decision)}</dd>
    <dt>Resultado</dt><dd>{fmt(consequence)}</dd>
  </dl>
</article>"""
    verified = "".join(f"<li>{fmt(v)}</li>" for v in p["verified"])
    limits = "".join(f"<li>{fmt(v)}</li>" for v in p["limits"])
    pager_prev = (f'<a href="{prev_p["slug"]}.html">← Anterior<b>{esc(prev_p["title"])}</b></a>' if prev_p else "<span></span>")
    pager_next = (f'<a href="{next_p["slug"]}.html">Siguiente →<b>{esc(next_p["title"])}</b></a>' if next_p else "")
    out.append(f"""<main id="contenido" class="case"><div class="container">
  <a class="back" href="../#proyectos">← Todos los proyectos</a>
  <div class="head-row">{badge(p['authorship'])}<span class="k" style="font:500 .8rem var(--mono);color:var(--faint);text-transform:uppercase;letter-spacing:.05em">{esc(p['kicker'])}</span></div>
  <h1>{esc(p['title'])}</h1>
  <p class="summary">{fmt(p['summary'])}</p>
  <ul class="tags">{tags}</ul>
  <div class="metrics">{metrics}</div>

  <section class="prose"><h2>El problema</h2><p style="color:#c3cad6">{fmt(p['problem'])}</p></section>

  <section><h2>Arquitectura</h2>
    <figure class="diagram" style="margin-inline:0"><pre class="mermaid">{html.escape(p['diagram'], quote=False)}</pre></figure>
  </section>

  <section><h2>Decisiones de diseño</h2>{decisions}</section>

  <section><h2>Qué se verificó</h2><ul class="checks">{verified}</ul></section>

  <section><h2>Límites: lo que no se verificó</h2><ul class="checks limits">{limits}</ul></section>

  <div class="repo-cta">
    <a class="btn primary" href="{REPO_URL}/{p['repo']}">Ver el repositorio</a>
    <a class="btn" href="{REPO_URL}/{p['repo']}#readme">Leer el README</a>
  </div>

  <nav class="pager" aria-label="Proyectos">{pager_prev}{pager_next}</nav>
</div></main>""")
    out.append(footer())
    return "\n".join(out)


def build_404() -> str:
    return "\n".join([
        head("Página no encontrada — Santiago Valenzuela López",
             "La página que buscas no existe. Vuelve al inicio para ver los proyectos y la experiencia de Santiago Valenzuela López.",
             "/", "404.html"),
        header("/"),
        """<main id="contenido"><section class="hero"><div class="container">
  <p class="eyebrow">// 404</p><h1>No encontré esa página</h1>
  <p class="tagline">Puede que el enlace haya cambiado. Los proyectos siguen en la página principal.</p>
  <div class="cta"><a class="btn primary" href="/">Volver al inicio</a></div>
</div></section></main>""",
        footer(),
    ])


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0f1219"/>
<rect x="1" y="1" width="62" height="62" rx="13" fill="none" stroke="#2f3849" stroke-width="2"/>
<text x="32" y="42" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="700" font-size="26" fill="#4fd1b8">SV</text></svg>
"""


def write(rel: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    write("index.html", build_index())
    for i, p in enumerate(C.PROJECTS):
        write(f"proyectos/{p['slug']}.html", build_case(i))
    write("404.html", build_404())
    write("assets/favicon.svg", FAVICON)
    urls = [""] + [f"proyectos/{p['slug']}.html" for p in C.PROJECTS]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{C.SITE_URL}/{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {C.SITE_URL}/sitemap.xml\n")
    write(".nojekyll", "")
    print(f"Sitio generado: index + {len(C.PROJECTS)} casos + 404 + sitemap")


if __name__ == "__main__":
    main()
