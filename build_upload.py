# -*- coding: utf-8 -*-
"""Prépare le paquet à téléverser directement sur Cloudflare.

Identique à `dist/` : tout est dans le paquet, y compris `_worker.js`, qui
fonctionne aussi bien sur Workers que sur Pages.

Produit, à côté du dépôt :
  euroventilatori-cloudflare/       le dossier à glisser sur Cloudflare
  euroventilatori-cloudflare.zip    le même, compressé

Lancer après gen_pages.py :  python build_upload.py
"""
import io, os, shutil, sys, zipfile

os.chdir(os.path.dirname(os.path.abspath(__file__)))
PARENT = os.path.abspath("..")
PREPROD = "--preprod" in sys.argv
NOM = "euroventilatori-preprod" if PREPROD else "euroventilatori-cloudflare"

# Interdiction d'indexation servie par l'hébergeur. Le verrou par nom d'hôte
# de _worker.js serait plus sûr, mais il suppose que le worker s'exécute :
# sur un projet « fichiers statiques seuls », il reste inerte.
ENTETE_NOINDEX = """
# ⚠️ PRÉPRODUCTION — ce bloc interdit l'indexation de tout le site.
# Il ne doit JAMAIS figurer dans le paquet de production.
/*
  X-Robots-Tag: noindex, nofollow, noarchive, nosnippet
"""

ROBOTS_PREPROD = """# Préproduction — ne pas indexer.
User-agent: *
Disallow: /
"""
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

    if PREPROD:
        # Deux serrures, comme dans _worker.js : l'en-tête et le robots.txt.
        with io.open(os.path.join(CIBLE, "_headers"), "a", encoding="utf-8") as f:
            f.write(ENTETE_NOINDEX)
        io.open(os.path.join(CIBLE, "robots.txt"), "w",
                encoding="utf-8").write(ROBOTS_PREPROD)

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
    print("Paquet %s : %s" % ("PRÉPRODUCTION" if PREPROD else "production", CIBLE))
    print("  %d pages HTML + _worker.js, %.1f Mo" % (pages, total / 1048576))
    if PREPROD:
        print("  Indexation interdite : X-Robots-Tag dans _headers + robots.txt en Disallow.")
    print("Archive : %s (%.1f Mo)" % (archive, os.path.getsize(archive) / 1048576))


if __name__ == "__main__":
    construire()
