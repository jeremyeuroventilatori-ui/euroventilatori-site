# Brief de la refonte — à réutiliser tel quel

Document de référence : ce qui a été demandé, dans l'ordre. Sert de cahier des
charges et de base de comparaison avec d'autres constructeurs de sites.

## 1. La demande initiale (verbatim, 2026-07)

> En te basant sur ce site internet : https://www.euroventilatori.fr/ je veux que
> tu me fasses un site internet tendance sur le secteur. Elle pourrait faire
> office d'une maquette fonctionnelle, dans le but de pouvoir après dupliquer et
> mettre en ligne. L'exercice est sérieux et peut être utilisé par la suite.
> Prends en compte tous les skills nécessaires, que ce soit pour créer son site
> internet, pour référencer et veiller sur les sites internet actuels.
> Inspire-toi de ce qui a été fait sur ce site internet et mets-le à jour avec
> les nouveautés et les tendances.

## 2. Le cahier des charges consolidé

À donner tel quel à un autre outil pour comparer à périmètre égal.

---

Refonds le site **euroventilatori.fr** (Euroventilatori France, constructeur de
ventilateurs industriels centrifuges et hélicoïdaux, région lyonnaise). Objectif :
une maquette fonctionnelle, destinée à être mise en ligne ensuite.

**Contenu**
- Reprends le contenu réel du site actuel, mais **reformule tous les textes** :
  les deux sites coexisteront un temps, aucun duplicate content.
- Aucun lorem ipsum. Aucun chiffre inventé : tout fait avancé doit être
  vérifiable sur le site source.
- Faits utilisables : société fondée en 1981 (maison mère italienne), 35 ans
  d'expérience en France, 30 000 ventilateurs produits par an, 28 000 m² de
  production, devis détaillé sous 24 h, catalogue de 53 séries / 25 tailles /
  16 orientations, bureau d'études intégré (CAO SolidWorks), plateforme de
  courbes aérauliques LiveCurve, conformité ATEX.
- Secteurs servis : énergie et pétrochimie, agroalimentaire, métallurgie, textile.
- Coordonnées : 04 74 43 68 38, contact@euroventilatori-france.com,
  150 Rue du Vernay, 38300 Nivolas-Vermelle.

**Architecture — contrainte SEO absolue**
- Conserve **exactement** l'arborescence actuelle (15 pages) : `/ventilateurs`,
  `/ventilateur-gamme`, `/ventilateur-sur-mesure`,
  `/solutions-ventilateur-industriel`, `/caissons-insonorises`,
  `/purificateur-air`, `/nos-autres-accessoires`, `/bureau-etudes`,
  `/qui-sommes-nous`, `/competences`, `/secteurs-activite`, `/telechargement`,
  `/contact`, `/actualites`.
- Conserve les `<title>`, meta descriptions, H1 et H2 existants : le
  référencement acquis se transfère, il ne se recrée pas.
- Des pages distinctes, pas une page unique à ancres.

**SEO et GEO (moteurs IA)**
- Par page : `<html lang="fr">`, charset, viewport, canonical, Open Graph
  complet, un seul H1, aucun title ni H1 dupliqué sur le site.
- JSON-LD `Organization` sur toutes les pages, `BreadcrumbList` sur les pages
  intérieures.
- `sitemap.xml`, `robots.txt` ouvert aux crawlers IA (GPTBot, ClaudeBot,
  PerplexityBot), fichier `_redirects` pour les URL disparues.
- Contenu rédigé en phrases autoportantes, citables hors contexte par une IA.

**Design**
- Direction artistique inspirée de la grammaire de **caeli-energie.com**
  (header en pilule flottante, bandes profondes arrondies, typographie
  display géante, panneaux qui s'ouvrent au défilement, sections épinglées) —
  mais **sans reprendre ses couleurs** : transposition vers l'identité client.
- Palette dérivée du bleu de marque #033F87, signal orange sécurité, fond
  bleuté quadrillé façon banc d'essais.
- Thèmes clair **et** sombre par tokens CSS.
- Un fil conducteur visuel lié au métier : une nappe d'air qui traverse toutes
  les pages et réagit au défilement.
- Bandeau de preuves chiffrées et bloc « pages liées » sur chaque page
  intérieure (crédibilité B2B + maillage interne).

**Interactif**
- Un outil de pré-sélection : curseurs débit / pression en échelle
  logarithmique, positionnement sur une carte des familles (basse, moyenne,
  haute pression), estimation de puissance P = Q·Δp/η, et bouton « faire
  valider par le bureau d'études » qui pré-remplit la demande.

**Technique**
- HTML statique, aucune dépendance externe (ni CDN, ni webfont distante,
  ni librairie JS) : fontes système, CSS et JS embarqués.
- Accessible : navigable au clavier, focus visible, `prefers-reduced-motion`
  respecté, responsive avec menu burger.
- Rien ne doit être masqué par défaut et révélé par JavaScript : si le script
  échoue, tout le contenu reste lisible.
- Livrable : fichiers prêts à pousser sur GitHub et déployer sur Cloudflare Pages.

---

## 3. Points de comparaison à observer

En confiant ce brief à un autre constructeur, regarder :

| Critère | Pourquoi c'est déterminant |
|---|---|
| **HTML servi** | Un site rendu côté navigateur (SPA React) livre un HTML quasi vide : Google le gère mal, les crawlers IA pas du tout |
| **URL conservées** | Une arborescence réinventée fait perdre le référencement acquis |
| **Balises reprises** | Title/H1 conservés = positions transférées |
| **Chiffres** | Vérifier qu'aucune donnée n'a été inventée pour « faire joli » |
| **Dépendances** | Chaque CDN ou webfont distante ralentit et crée une dépendance |
| **Dégradation** | Couper le JS : le contenu reste-t-il lisible ? |
| **Deux thèmes** | Le thème sombre est-il conçu, ou une inversion naïve ? |
