# -*- coding: utf-8 -*-
"""Extrait le CSS inline d'index.html vers assets/styles.css (partagé par toutes
les pages), y ajoute les styles des pages intérieures, et remplace le bloc
<style> d'index.html par un <link>. Exécuter une seule fois : python extract_assets.py
"""
import io, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("assets", exist_ok=True)

with io.open("index.html", encoding="utf-8") as f:
    html = f.read()

if "<style>" not in html:
    print("Déjà extrait — rien à faire.")
    raise SystemExit

head, rest = html.split("<style>", 1)
css, tail = rest.split("</style>", 1)

SUBPAGE_CSS = """
/* ==========================================================================
   PAGES INTÉRIEURES (hero allégé, sections éditoriales, bande CTA)
   ========================================================================== */
.hero-lite{position:relative;padding:140px 0 56px;overflow:clip}
.hero-lite h1{font-size:clamp(30px,4.4vw,54px);text-transform:uppercase;max-width:24ch;letter-spacing:.01em}
.hero-lite .eyebrow{margin-bottom:18px}
.lead-block{margin-top:18px}
.prose{max-width:68ch;color:var(--muted);font-size:16.5px;line-height:1.7;display:flex;flex-direction:column;gap:14px}
.prose b{color:var(--ink)}
.hero-lite .cta-row{margin-top:26px}
.page-sec{padding:clamp(36px,5vw,72px) 0;position:relative}
.sec-grid{display:grid;grid-template-columns:1fr 1.6fr;gap:clamp(24px,4vw,60px);align-items:start}
.sec-grid h2{font-size:clamp(22px,2.6vw,32px);text-transform:uppercase;position:sticky;top:110px;text-wrap:balance}
.cta-band-wrap{padding:clamp(36px,5vw,72px) 0}
.cta-band{background:var(--deep);color:var(--deep-ink);border:1px solid var(--line);border-radius:30px;margin:0 clamp(10px,1.8vw,28px);padding:clamp(28px,4vw,50px) 0}
.cta-band h2{color:#fff}
@media (max-width:980px){ .sec-grid{grid-template-columns:1fr} .sec-grid h2{position:static} }
"""

with io.open("assets/styles.css", "w", encoding="utf-8") as f:
    f.write(css.strip() + "\n" + SUBPAGE_CSS)

html = head + '<link rel="stylesheet" href="/assets/styles.css">' + tail
with io.open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("OK : assets/styles.css écrit, index.html mis à jour.")
