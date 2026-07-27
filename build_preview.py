# -*- coding: utf-8 -*-
"""Construit l'aperçu autonome publié en Artifact (validation visuelle).

Le dépôt reste la source de vérité : ce script recopie index.html en un fichier
unique, CSS inliné et sans balises <html>/<head>/<body> (l'Artifact fournit son
propre squelette). Lancer après toute modification du site :
    python build_preview.py
"""
import io, os, re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join("..", "maquette-euroventilatori-tendance.html")

html = io.open("index.html", encoding="utf-8").read()
css = io.open(os.path.join("assets", "styles.css"), encoding="utf-8").read()

# 1. Retirer le squelette : l'Artifact enveloppe déjà le contenu.
for pat in (r"<!doctype html>\s*", r"<html lang=\"fr\">\s*", r"<head>\s*",
            r"</head>\s*", r"<body>\s*", r"</body>\s*", r"</html>\s*",
            r"<meta charset=\"utf-8\">\s*",
            r"<meta name=\"viewport\"[^>]*>\s*"):
    html = re.sub(pat, "", html, flags=re.I)

# 2. Inliner la feuille de style à la place du <link>.
html = html.replace('<link rel="stylesheet" href="assets/styles.css">',
                    "<style>\n" + css + "\n</style>")

# 3. L'aperçu ne contient que l'accueil : rediriger les liens de pages vers la
#    section correspondante, pour que la navigation reste utile à la démonstration.
ANCRES = {
    "/": "#top",
    "/ventilateurs": "#offre", "/ventilateur-gamme": "#offre",
    "/ventilateur-sur-mesure": "#offre", "/caissons-insonorises": "#offre",
    "/purificateur-air": "#offre", "/nos-autres-accessoires": "#offre",
    "/solutions-ventilateur-industriel": "#offre",
    "/secteurs-activite": "#secteurs",
    "/bureau-etudes": "#methode", "/competences": "#methode",
    "/qui-sommes-nous": "#methode",
    "/telechargement": "#selecteur",
    "/contact": "#contact",
}
def _anchor(m):
    url = m.group(1)
    return 'href="%s" data-page="%s"' % (ANCRES.get(url, "#top"), url)
html = re.sub(r'href="(/[^"#]*)"', _anchor, html)

io.open(OUT, "w", encoding="utf-8").write(html)
print("Aperçu écrit :", os.path.abspath(OUT), "-", len(html) // 1024, "Ko")
