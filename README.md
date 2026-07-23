# Site Euroventilatori France — maquette de refonte

Refonte de [euroventilatori.fr](https://www.euroventilatori.fr/) : site statique
en un seul fichier HTML, sans dépendance externe (fontes système, CSS et JS inline).

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `index.html` | Le site complet (page d'accueil / maquette navigable) |
| `_redirects` | Redirections 301 pour Cloudflare Pages (anciennes URL → nouvelles) |
| `robots.txt` | Directives d'indexation (moteurs classiques + moteurs IA) |

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
