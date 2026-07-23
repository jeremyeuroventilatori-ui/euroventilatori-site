# Inventaire SEO du site actuel — cahier des charges de la refonte

Relevé le 2026-07-23 sur https://www.euroventilatori.fr/ (15 pages actives). **Règle de la refonte : chaque URL ci-dessous doit exister à l'identique dans le nouveau site, avec un title, une meta description et un H1 qui visent la même requête.** Les formulations peuvent être modernisées ; l'intention de recherche et les termes métier doivent être conservés.

| URL | Title actuel | Meta description | H1 |
|---|---|---|---|
| `/` | Ventilation industrielle près de Lyon - Euroventilatori France | Experts en ventilation industrielle depuis plus de 20 ans… | La ventilation industrielle chez Euroventilatori France à Lyon |
| `/ventilateurs` | Vente ventilateurs industriels à Lyon - Silencieux et sur mesure | Équipez votre entreprise de ventilateurs de gamme industrielle… | Vente de ventilateurs industriels |
| `/ventilateur-gamme` | Vente de ventilateurs de gamme industrielle à Lyon | Générez des pressions d'air élevées grâce à nos ventilateurs… | Vente de ventilateurs de gamme industrielle à Lyon et dans toute la France |
| `/ventilateur-sur-mesure` | Fabrication de ventilateurs sur mesure près de Lyon | Nos ventilateurs sur mesure fournissent des débits d'air très importants… | Conception et fabrication de ventilateurs industriels sur mesure à Lyon et dans toute la France |
| `/solutions-ventilateur-industriel` | Solutions sur mesure pour ventilation industrielle à Lyon | Optimisez vos installations avec des accessoires techniques… | Solutions sur mesure pour ventilation industrielle et traitement de l'air près de Lyon |
| `/caissons-insonorises` | Caissons d'insonorisation pour ventilateurs à Lyon | Ne soyez plus dérangé par le bruit et les nuisances sonores… | Découvrez nos caissons d'insonorisation |
| `/purificateur-air` | Systèmes de filtration ventilateurs industriels à Lyon - Filtres | Optimisez la filtration grâce à nos caissons de filtration statiques… | Optimisez la filtration de vos ventilateurs industriels |
| `/nos-autres-accessoires` | Accessoires pour tous types de ventilateurs industriels à Lyon | Optez pour la conception d'un ventilateur industriel sur mesure… | Nos différents accessoires pour ventilateurs industriels |
| `/bureau-etudes` | Découvrez notre bureau d'études industrielles à Lyon | Les techniciens et ingénieurs de notre bureau d'études… | CAO 2D et 3D SolidWorks. Notre bureau d'études industrielles |
| `/qui-sommes-nous` | Conception de ventilateurs industriels à Lyon - Euroventilatori France | Euroventilatori France réalise la conception et la fabrication… | Euroventilatori France — Conception et fabrication de ventilateurs industriels pour votre entreprise |
| `/secteurs-activite` | Les domaines d'application des ventilateurs industriels - Lyon | Ventilateurs pour les secteurs de l'industrie : parachimie, cosmétique, ferroviaire, textile, agroalimentaire… | Domaines d'application |
| `/competences` | Notre savoir-faire en ventilateurs industriels à Lyon | Conception, dimensionnement, essais et suivi… | Découvrez le savoir-faire d'Euroventilatori, conception de ventilateurs industriels pour votre entreprise |
| `/telechargement` | Fiches techniques, LiveCurve pour ventilateurs \| Euroventilatori | Sélectionner le ventilateur sur mesure grâce à la plateforme interactive LiveCurve… | Découvrez LiveCurve, développé par Euroventilatori |
| `/contact` | Demandez votre devis et contactez Euroventilatori France à Lyon | Contactez-nous pour l'achat d'un ventilateur industriel… | Contactez Euroventilatori pour tout achat de ventilateurs industriels et solutions acoustiques |
| `/actualites` | Actualités d'Euroventilatori - Fabricant de ventilateurs industriels | Retrouvez toutes les actualités… à Nivolas-Vermelle. | Nos actualités |

## H2 à conserver (langage de recherche déjà positionné)

Ces intitulés répondent à des questions réellement tapées dans Google. Les reformuler est possible, les supprimer coûterait des positions.

| Page | H2 à conserver |
|---|---|
| `/ventilateurs` | « Ventilateurs industriels standards ou sur mesure : comment choisir ? » · « S'équiper de ventilateurs industriels sur mesure, pour des besoins précis » · « Des ventilateurs industriels adaptés à vos contraintes spécifiques » |
| `/ventilateur-gamme` | « Comment choisir un ventilateur industriel standard adapté à vos besoins ? » · « Secteurs d'application : ventilateurs industriels standards » |
| `/ventilateur-sur-mesure` | « Les différents critères lors du choix de vos ventilateurs industriels » |
| `/solutions-ventilateur-industriel` | « Caissons de filtration pour systèmes de ventilation industrielle » · « Caissons d'insonorisation pour ventilateurs professionnels » |
| `/purificateur-air` | « Nos conseils pour bien choisir son ventilateur industriel » |
| `/bureau-etudes` | « Des ventilateurs industriels soumis à des analyses pour vous garantir leur qualité » · « Un produit et un process étudiés pour proposer les meilleurs délais de fabrication » |
| `/competences` | « La conception et le dimensionnement des ventilateurs industriels » · « Centre d'essai dédié aux contrôles qualité et à la validation technique » |
| `/secteurs-activite` | « Pourquoi les ventilateurs industriels sont-ils essentiels en entreprise ? » |

## Points à trancher (relevés pendant l'audit)

**20 ans ou 35 ans ?** La meta description de l'accueil dit « plus de 20 ans », le corps de page dit « plus de 35 ans ». Incohérence à arbitrer — elle est visible par Google comme par vos clients.

**Adresse réelle : Nivolas-Vermelle** (Isère), et non Lyon. Le SEO local doit citer la commune exacte dans le JSON-LD et les mentions ; « près de Lyon » reste pertinent comme repère géographique dans les titles.

**LiveCurve vs pupitre de sélection.** `/telechargement` promeut LiveCurve, votre plateforme officielle. Le « pupitre » de la maquette lui fait doublon : soit il devient une porte d'entrée vers LiveCurve, soit LiveCurve reste le seul outil et le pupitre est retiré. À décider avant la mise en production.

**Secteurs incohérents.** L'accueil affiche 4 secteurs (énergie/pétrochimie, agroalimentaire, métallurgie, textile) ; `/secteurs-activite` en cite d'autres (parachimie, cosmétique, ferroviaire). La liste consolidée doit être validée.

**`/outils` et `/calculs` renvoient déjà 404** sur le site actuel (ce sont des entrées de menu sans page). Rien à préserver, mais à ne pas recréer par erreur.

## Prochaine étape

Découper index.html en 15 pages reprenant cette arborescence à l'identique (mêmes chemins d'URL), chacune héritant du design validé et des balises ci-dessus. Tant que ce découpage n'est pas fait, le site ne doit pas être mis en production : il ferait perdre 14 pages indexées.

---

## Audit technique complémentaire (relevé le 2026-07-23 sur le site live)

Cette section complète l'inventaire éditorial ci-dessus avec l'état technique réel du site actuel, mesuré page par page. Objectif : rien de ce qui est indexé et qui « travaille » ne doit être perdu ni dégradé lors de la refonte.

### 1. L'arborescence réelle dépasse les 15 pages — sitemap.xml = 43 URL

Le site actuel expose un `robots.txt` (qui pointe vers le sitemap) et un `sitemap.xml` contenant **43 URL canoniques**, et non 15. Les 15 pages inventoriées plus haut sont bien présentes, mais 28 URL supplémentaires sont indexées et doivent être arbitrées AVANT la bascule. Les recréer à l'identique (ou poser des 301 explicites) est indispensable, sinon la refonte perd ces positions. Le découpage en « 15 pages » du README est donc à réviser : la perte réelle potentielle est de ~28 URL, pas de 14.

| Catégorie | URL indexées (au-delà des 15 pages) | Enjeu |
|---|---|---|
| Pages régionales (SEO local) | `/paris`, `/lille`, `/bretagne`, `/ile-de-france-rhone-alpes` | Fort — chacune vise une requête géographique dédiée. À préserver en priorité. |
| Pages produits / thématiques | `/ventilateurs-centrifuges`, `/ventilateurs-helicoides`, `/traitement-surface` | Requêtes métier à conserver. |
| Pages légales (obligatoires en France) | `/mentions-legales`, `/vie-privee` | À recréer impérativement. |
| Articles d'actualité | 19 URL autonomes (ex. `/bonne-annee-2026-a-tous`, `/notre-presence-au-salon-vrac-tech-du-mans`…) | La refonte ne prévoit qu'une page `/actualites` : recréer les articles (recommandé) ou poser des 301. |

Titles relevés sur les principales pages à préserver :

| URL | Title actuel |
|---|---|
| `/paris` | Euroventilatori France \| Vente de ventilateurs industriels à Paris |
| `/lille` | Euroventilatori France \| Vente de ventilateurs industriels à Lille |
| `/bretagne` | Euroventilatori France \| Vente de ventilateur industriels en Bretagne |
| `/ile-de-france-rhone-alpes` | Euroventilatori France – Vente de ventilateurs en Rhône-Alpes |
| `/ventilateurs-centrifuges` | Achat de ventilateurs centrifuges industriels \| Euroventilatori |
| `/ventilateurs-helicoides` | Achat de ventilateurs hélicoïdes industriels \| Euroventilatori |
| `/traitement-surface` | Ventilateurs, traitement de surface des métaux \| Euroventilatori |

Action : exporter la liste complète des URL indexées depuis Google Search Console (rapport « Pages ») et compléter `_redirects` en conséquence, comme le rappelle déjà le README.

### 2. Balises canonical — conformes sur les 15 pages

Chaque page renvoie une canonical auto-référente correcte (ex. `/ventilateurs` → `https://www.euroventilatori.fr/ventilateurs`). À reproduire à l'identique dans la refonte, avec le domaine final une fois la bascule DNS effectuée.

### 3. Données structurées (JSON-LD) — incohérentes ET pointant vers le mauvais domaine

La couverture des données structurées est inégale : l'accueil porte `WebSite` + `Organization/LocalBusiness`, tandis que les pages intérieures ne portent qu'un `BreadcrumbList` (sauf `/bureau-etudes` qui ajoute `Service`).

Problème majeur : le bloc `LocalBusiness` de l'accueil référence le domaine **`euroventilatori-france.com`** (url, @id, logo, image), alors que le site live est `euroventilatori.fr`. À corriger dans la refonte : le JSON-LD doit citer le domaine réellement servi.

Adresse confirmée par le JSON-LD : **150 Rue Du Vernay, 38300 Nivolas-Vermelle**, région Auvergne-Rhône-Alpes, tél. +33 4 74 43 68 38 (`sameAs` : Facebook + LinkedIn). Cela confirme le point « adresse réelle » ci-dessus. La description du JSON-LD indique « plus de 30 000 ventilateurs par an » pour 4 secteurs (énergie, agroalimentaire, métallurgie, textile) — à recouper avec le point « secteurs incohérents ».

### 4. Attributs alt des images — nombreuses images sans alternative textuelle

Défaut d'accessibilité et de SEO image présent sur presque toutes les pages : la plupart des pages intérieures ont 4 images sur 5 sans attribut `alt`. Cas les plus lourds : accueil 10 images sans alt sur 23 ; `/actualites` 26 images sur 26 sans alt. La refonte doit systématiser des `alt` descriptifs (opportunité d'amélioration, pas une régression à préserver).

### 5. Structure Hn et langue — corrects

Chaque page a exactement un `<h1>` (pas de doublon) et l'attribut `lang="fr"` est présent. Aucun `hreflang` sur le site (site monolingue) : rien à préserver de ce côté, mais à ne pas introduire par erreur.

### 6. Confirmation des 404

`/outils` et `/calculs` renvoient bien un code 404 sur le site live (confirmé par requête directe). Conformément à l'inventaire : ne pas les recréer.

## Synthèse des priorités avant mise en production

1. Récupérer l'export Search Console et arbitrer les 28 URL au-delà des 15 pages (régionales, produits, légales, articles) — 301 ou recréation.
2. Corriger le domaine du JSON-LD (`euroventilatori.fr`, pas `.com`) et uniformiser les données structurées entre pages.
3. Recréer les pages légales `/mentions-legales` et `/vie-privee` (obligation légale).
4. Ajouter des `alt` sur toutes les images.
5. Trancher les incohérences éditoriales déjà répertoriées (20 vs 35 ans ; liste des secteurs ; LiveCurve vs pupitre).
