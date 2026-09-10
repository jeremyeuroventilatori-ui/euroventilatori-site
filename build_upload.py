# -*- coding: utf-8 -*-
"""Prépare le paquet à téléverser directement sur Cloudflare.

Identique à `dist/` : tout est dans le paquet, y compris `_worker.js`, qui
fonctionne aussi bien sur Workers que sur Pages.

Produit, à côté du dépôt :
  euroventilatori-cloudflare/       le dossier à glisser sur Cloudflare
  euroventilatori-cloudflare.zip    le même, compressé

Lancer après gen_pages.py :  python build_upload.py
"""
import io, os, shutil, zipfile

os.chdir(os.path.dirname(os.path.abspath(__file__)))
PARENT = os.path.abspath("..")
NOM = "euroventilatori-cloudflare"
CIBLE = os.path.join(PARENT, NOM)

RACINE = ["_worker.js", "_headers", "_redirects", "robots.txt", "sitemap.xml",
          "llms.txt", "favicon.svg", "favicon.png", "favicon.ico"]
DOSSIERS = ["assets"]
EXCLUS_EXT = (".py", ".md")


def construire():
    if os.path.isdir(CIBLE):
        shutil.rmtree(CIBLE)
    os.makedirs(CIBLE)

    pages = 0
    for nom in sorted(os.listdir(".")):
        if not os.path.isfile(nom):
            continue
        if nom.endswith(".html"):
            shutil.copy2(nom, os.path.join(CIBLE, nom))
            pages += 1
        elif nom in RACINE:
            shutil.copy2(nom, os.path.join(CIBLE, nom))

    for dossier in DOSSIERS:
        if os.path.isdir(dossier):
            shutil.copytree(dossier, os.path.join(CIBLE, dossier))

    # Garde-fou : aucun outil ni document interne ne doit partir en ligne.
    fuites = [os.path.join(r, f)
              for r, _, fs in os.walk(CIBLE) for f in fs
              if f.endswith(EXCLUS_EXT)]
    if fuites:
        raise SystemExit("Fichiers internes dans le paquet : " + ", ".join(fuites))

    manquants = [f for f in RACINE if not os.path.exists(os.path.join(CIBLE, f))]
    manquants += [d for d in DOSSIERS if not os.path.isdir(os.path.join(CIBLE, d))]
    if manquants:
        raise SystemExit("Éléments attendus absents : " + ", ".join(manquants))

    # Archive, pour ceux qui préfèrent déposer un fichier unique.
    archive = CIBLE + ".zip"
    if os.path.exists(archive):
        os.remove(archive)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for racine, _, fichiers in os.walk(CIBLE):
            for f in fichiers:
                chemin = os.path.join(racine, f)
                z.write(chemin, os.path.relpath(chemin, CIBLE))

    total = sum(os.path.getsize(os.path.join(r, f))
                for r, _, fs in os.walk(CIBLE) for f in fs)
    print("Paquet : %s" % CIBLE)
    print("  %d pages HTML + _worker.js, %.1f Mo" % (pages, total / 1048576))
    print("Archive : %s (%.1f Mo)" % (archive, os.path.getsize(archive) / 1048576))


if __name__ == "__main__":
    construire()
