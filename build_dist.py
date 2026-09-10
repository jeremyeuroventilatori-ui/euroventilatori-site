# -*- coding: utf-8 -*-
"""Assemble le dossier `dist/` — ce qui part réellement en ligne.

Pourquoi ne pas publier le dépôt tel quel : Cloudflare Pages sert TOUT ce que
contient le dossier publié. Les scripts de génération et les notes de
migration — dont l'analyse des droits du prestataire — seraient alors
accessibles publiquement. `dist/` ne contient que le site.

Lancer après gen_pages.py :  python build_dist.py
"""
import io, os, shutil

os.chdir(os.path.dirname(os.path.abspath(__file__)))
DIST = "dist"

# Fichiers à la racine du site publié, en plus des pages HTML.
RACINE = ["_headers", "_redirects", "robots.txt", "sitemap.xml", "llms.txt",
          "favicon.svg", "favicon.png", "favicon.ico"]
DOSSIERS = ["assets"]

# Jamais publiés : outils de fabrication et documentation interne.
EXCLUS_EXT = (".py", ".md")


def construire():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    pages = 0
    for nom in sorted(os.listdir(".")):
        if not os.path.isfile(nom):
            continue
        if nom.endswith(".html"):
            shutil.copy2(nom, os.path.join(DIST, nom))
            pages += 1
        elif nom in RACINE:
            shutil.copy2(nom, os.path.join(DIST, nom))

    for dossier in DOSSIERS:
        if os.path.isdir(dossier):
            shutil.copytree(dossier, os.path.join(DIST, dossier))

    # Garde-fou : rien d'interne ne doit se retrouver publié.
    fuites = []
    for racine, _, fichiers in os.walk(DIST):
        for f in fichiers:
            if f.endswith(EXCLUS_EXT):
                fuites.append(os.path.join(racine, f))
    if fuites:
        raise SystemExit("Fichiers internes dans dist/ : " + ", ".join(fuites))

    manquants = [f for f in RACINE if not os.path.exists(os.path.join(DIST, f))]
    if manquants:
        raise SystemExit("Fichiers attendus absents : " + ", ".join(manquants))

    total = sum(os.path.getsize(os.path.join(r, f))
                for r, _, fs in os.walk(DIST) for f in fs)
    print("dist/ : %d pages HTML, %.1f Mo" % (pages, total / 1048576))
    print("Les fonctions restent à la racine du dépôt (functions/), "
          "où Cloudflare Pages les attend.")


if __name__ == "__main__":
    construire()
