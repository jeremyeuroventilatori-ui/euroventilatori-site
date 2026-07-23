# Site Euroventilatori France — refonte

Refonte de [euroventilatori.fr](https://www.euroventilatori.fr/) : site statique
multi-pages, sans dépendance externe (fontes système, aucun CDN).
**L'arborescence, les `<title>`, meta descriptions, H1 et H2 reprennent le site
actuel à l'identique** (voir `seo-inventaire.md`) pour préserver le référencement.

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `index.html` | Page d'accueil (design complet : hero canvas, bento, pupitre) |
| `ventilateurs.html`, `ventilateur-gamme.html`, … | Les 14 pages intérieures (mêmes URL que le site actuel, servies sans extension par Cloudflare Pages) |
| `assets/styles.css` | CSS partagé par toutes les pages (tokens, deux thèmes) |
| `assets/site.js` | JS commun des pages intérieures (thème, menu, parallaxe) |
| `seo-inventaire.md` | Le relevé SEO du site actuel — cahier des charges des balises |
| `sitemap.xml` | Les 15 URL canoniques |
| `_redirects` | 301 résiduelles (/outils, /calculs) pour Cloudflare Pages |
| `robots.txt` | Directives d'indexation (moteurs classiques + moteurs IA) |
| `gen_pages.py`, `extract_assets.py` | Scripts de génération (contenu des pages centralisé dans gen_pages.py) |

## Modifier le site

- **Couleurs** : toutes dans le bloc `:root` en tête de `index.html` (tokens
  `--brand`, `--accent`…). Un hex changé = tout le site suit.
- **Textes** : chaque section est balisée par un commentaire
  (`<!-- ==== HERO ==== -->`, `<!-- ==== BENTO ==== -->`…), les textes sont en
  clair dessous.
- Tester en local : double-cliquer sur `index.html`.

## Déployer sur Cloudflare Pages

1. Cloudflare Dashboard → **Workers & Pages → Create → Pages → Connect to Git**.
2. Sélectionner ce dépôt. Framework : **None**. Build command : *(vide)*.
   Output directory : `/`.
3. Chaque `git push` sur `main` redéploie automatiquement (~30 s).
4. Le site de préproduction (`*.pages.dev`) ne doit pas être indexé tant que le
   domaine n'a pas basculé — voir la skill `transfert-domaine` pour le runbook
   de bascule DNS (TTL, MX, 301, Search Console).

## Avant la mise en production (rappels)

- Compléter `_redirects` avec la liste réelle des URL indexées (export Google
  Search Console, rapport « Pages »).
- Retirer la mention « Maquette de travail » du footer.
- Brancher le formulaire de contact (actuellement `mailto:`).
- Ajouter `sitemap.xml` et activer la ligne Sitemap de `robots.txt`.
