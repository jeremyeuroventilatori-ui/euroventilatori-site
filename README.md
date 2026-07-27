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
| `migration-inventaire-dns.md` | Relevé DNS avant bascule (OVH → Cloudflare) |
| `gen_pages.py`, `extract_assets.py` | Scripts de génération (contenu des pages centralisé dans gen_pages.py) |
| `build_preview.py` | Construit l'aperçu autonome publié en Artifact pour validation |

## Standards de finition (à préserver à chaque évolution)

Toutes les pages portent, sans exception :

- `<html lang="fr">`, `charset`, `viewport`, `<link rel="canonical">`
- Open Graph complet (titre, description, URL) — conditionne l'aperçu des partages
  LinkedIn et le contexte lu par les moteurs IA
- JSON-LD `Organization` **et** `BreadcrumbList` (pages intérieures)
- **Un seul `<h1>` par page**, aucun `<title>` ni `<h1>` dupliqué sur le site
- Fil d'Ariane visible, page courante signalée dans le menu (`aria-current`)
- Bandeau de preuves chiffrées et bloc « À consulter également » (maillage interne)
- Le souffle (`#airCanvas`) — nappe d'air commune, désactivée si
  `prefers-reduced-motion`

Après toute modification : `python gen_pages.py` puis `python build_preview.py`.
Vérifier en local avant de pousser :

```
python -m http.server 8765
```

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
