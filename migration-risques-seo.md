# Reprise en interne — évaluation du risque SEO et du risque de droits

Relevé du 27 juillet 2026, sur le site en production (Duda, via prestataire).
Contexte : fin du contrat prestataire, reprise en interne sur Cloudflare Pages,
sans perte de référencement et sans exposition sur les droits d'auteur.

## 1. Couverture des URL — le point bloquant

Le sitemap de production déclare **46 URL**. Le nouveau site en couvre **15**.

| Groupe | Nombre | Volume | Enjeu |
|---|---|---|---|
| Pages reprises | 15 | — | ✅ URL, title, H1, H2 conservés |
| **Pages produits absentes** | 3 | 1 270 à 1 320 mots | 🔴 pages de mots-clés majeurs |
| **Pages locales absentes** | 4 | 1 970 à 2 670 mots | 🔴 tout le SEO local |
| **Pages légales absentes** | 2 | 930 et 1 530 mots | 🔴 obligation + liens cassés |
| Articles d'actualité absents | 21 | variable | 🟡 longue traîne, fraîcheur |

### Pages produits manquantes
- `/ventilateurs-centrifuges` — « Achat de ventilateurs centrifuges industriels »
- `/ventilateurs-helicoides` — « Achat de ventilateurs hélicoïdes industriels »
- `/traitement-surface` — « Ventilateurs, traitement de surface des métaux »

Ce sont des pages de destination sur des requêtes commerciales directes. Les
perdre coûterait plus cher que tout le reste réuni.

### Pages locales manquantes
`/paris` (2 330 mots), `/lille` (2 320), `/bretagne` (1 970),
`/ile-de-france-rhone-alpes` (2 670).

Quatre pages de référencement local, très étoffées : c'est un investissement
SEO déjà amorti, qui disparaîtrait intégralement.

### Pages légales manquantes
`/mentions-legales` et `/vie-privee` : obligatoires, **et le pied de page du
nouveau site pointe déjà vers elles** — ce sont donc aujourd'hui des liens morts.

## 2. Volume de contenu des 15 pages reprises

Comparaison mot à mot, hors en-tête, menu et pied de page :

| Page | Actuel | Nouveau | Ratio |
|---|---|---|---|
| Accueil | 760 | 727 | 96 % |
| Téléchargement | 208 | 191 | 92 % |
| Bureau d'études | 334 | 245 | 73 % |
| Ventilateurs de gamme | 387 | 280 | 72 % |
| Secteurs d'activité | 355 | 246 | 69 % |
| Ventilateurs sur mesure | 380 | 264 | 69 % |
| Caissons insonorisés | 414 | 269 | 65 % |
| Compétences | 425 | 269 | 63 % |
| Nos produits | 533 | 324 | 61 % |
| Accessoires | 379 | 231 | 61 % |
| Filtration | 468 | 277 | 59 % |
| Qui sommes-nous | 432 | 247 | 57 % |
| Solutions | 465 | 251 | 54 % |
| Contact | 352 | 184 | 52 % |
| **Total** | **5 892** | **4 005** | **68 %** |

Une page qui perd un tiers de sa substance perd de la couverture sémantique :
moins de termes secondaires, moins de questions traitées, donc moins de requêtes
sur lesquelles elle peut ressortir. À corriger avant bascule.

## 3. Droits d'auteur — ce qui protège réellement

> Analyse de bon sens, à faire valider par un conseil juridique.

**Ce qui n'est pas appropriable par le prestataire :**
- les **faits** sur l'entreprise (1981, 30 000 ventilateurs/an, 28 000 m²,
  35 ans, adresse, coordonnées) ;
- les **caractéristiques techniques** des produits (53 séries, 25 tailles,
  pressions, matériaux) ;
- l'**arborescence et les URL** — une structure fonctionnelle, non une œuvre ;
- les **mots-clés** visés et l'intention de recherche ;
- une **balise title purement descriptive** (« Vente de ventilateurs de gamme
  industrielle à Lyon ») : phrase courte et fonctionnelle, protection très mince.

**Ce qui peut l'être :**
- les **textes rédactionnels** s'ils ont été écrits par le prestataire ;
- le **design**, le gabarit Duda, les **photographies** qu'il a produites ou
  achetées ;
- toute création originale non couverte par une cession de droits.

**Le point à vérifier en priorité : le contrat.** En droit français, la cession
de droits d'auteur doit être **écrite et explicite** (art. L.131-3 CPI). Sans
clause de cession, le prestataire conserve ses droits sur ce qu'il a créé.
Cherchez « cession de droits », « propriété intellectuelle », « livrables ».

**Conséquence pratique :** notre approche — réécrire tous les textes, créer un
design original, n'utiliser aucune image du prestataire — est déjà la bonne.
Il reste à l'appliquer aux 31 pages manquantes plutôt que de les recopier.

## 4. Titres et balises : réécrire sans perdre de position

Les 15 pages reprennent aujourd'hui les `title`, `meta` et `H1` **à l'identique**.
C'est optimal pour le SEO, mais c'est aussi le seul endroit où subsiste du texte
du prestataire.

Bonne nouvelle : **on peut les réécrire sans perte notable**, à trois conditions :
1. conserver le **mot-clé principal**, si possible en tête de balise ;
2. conserver l'**intention** (achat, information, local) ;
3. conserver la **localisation** quand elle est présente (« à Lyon »).

Exemple : « Vente ventilateurs industriels à Lyon - Silencieux et sur mesure »
→ « Ventilateurs industriels à Lyon — gamme, sur mesure et solutions silencieuses ».
Même requête visée, formulation propre.

## 5. Images — un angle mort à traiter

Le nouveau site ne comporte **aucune image**. Deux conséquences :
- perte du référencement sur Google Images et de la richesse perçue des pages ;
- les visuels actuels sont hébergés chez Duda : **ils disparaîtront à la fin du
  contrat**, et leur réutilisation poserait justement la question des droits.

Produire un jeu de photos propre (atelier, machines, chantiers) résout les deux
problèmes d'un coup, et c'est le seul poste qui demande un vrai investissement.

## 6. Plan pour une reprise sans perte

1. **Exporter la liste réelle des URL indexées** depuis Google Search Console
   (rapport Pages) : le sitemap peut différer de ce que Google connaît.
2. **Créer les 9 pages structurantes manquantes** (3 produits, 4 locales,
   2 légales), en contenu original, aux **mêmes URL** et sur les mêmes requêtes.
3. **Réécrire les 21 actualités** ou, à défaut, poser des 301 vers
   `/actualites` — mais recréer vaut mieux : ce sont vos propres nouvelles.
4. **Étoffer les 15 pages existantes** pour revenir à 100 % du volume actuel,
   voire au-delà, en contenu original.
5. **Réécrire titles, meta et H1** en gardant mot-clé, intention et localisation.
6. Constituer le **jeu photographique** de l'entreprise.
7. Seulement ensuite : bascule DNS selon le runbook (skill `transfert-domaine`),
   avec retrait du `noindex` le jour J.

Tant que les points 2 à 4 ne sont pas faits, la bascule ferait perdre du
référencement — mécaniquement, par disparition de pages et de contenu.
