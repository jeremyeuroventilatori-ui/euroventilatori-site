# Inventaire SEO du site actuel — cahier des charges de la refonte

Relevé le 2026-07-23 sur https://www.euroventilatori.fr/ (15 pages actives).
**Règle de la refonte : chaque URL ci-dessous doit exister à l'identique dans le
nouveau site, avec un title, une meta description et un H1 qui visent la même
requête.** Les formulations peuvent être modernisées ; l'intention de recherche et
les termes métier doivent être conservés.

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
| `/bureau-etudes` | Découvrez notre bureau d'études industrielles à Lyon | Les techniciens et ingénieurs de notre bureau d'études… CAO 2D et 3D SolidWorks. | Notre bureau d'études industrielles |
| `/qui-sommes-nous` | Conception de ventilateurs industriels à Lyon - Euroventilatori France | Euroventilatori France réalise la conception et la fabrication… | Euroventilatori France — Conception et fabrication de ventilateurs industriels pour votre entreprise |
| `/secteurs-activite` | Les domaines d'application des ventilateurs industriels - Lyon | Ventilateurs pour les secteurs de l'industrie : parachimie, cosmétique, ferroviaire, textile, agroalimentaire… | Domaines d'application |
| `/competences` | Notre savoir-faire en ventilateurs industriels à Lyon | Conception, dimensionnement, essais et suivi… | Découvrez le savoir-faire d'Euroventilatori, conception de ventilateurs industriels pour votre entreprise |
| `/telechargement` | Fiches techniques, LiveCurve pour ventilateurs \| Euroventilatori | Sélectionner le ventilateur sur mesure grâce à la plateforme interactive LiveCurve… | Découvrez LiveCurve, développé par Euroventilatori |
| `/contact` | Demandez votre devis et contactez Euroventilatori France à Lyon | Contactez-nous pour l'achat d'un ventilateur industriel… | Contactez Euroventilatori pour tout achat de ventilateurs industriels et solutions acoustiques |
| `/actualites` | Actualités d'Euroventilatori - Fabricant de ventilateurs industriels | Retrouvez toutes les actualités… à Nivolas-Vermelle. | Nos actualités |

## H2 à conserver (langage de recherche déjà positionné)

Ces intitulés répondent à des questions réellement tapées dans Google. Les
reformuler est possible, les supprimer coûterait des positions.

- `/ventilateurs` : « Ventilateurs industriels standards ou sur mesure : comment
  choisir ? » · « S'équiper de ventilateurs industriels sur mesure, pour des
  besoins précis » · « Des ventilateurs industriels adaptés à vos contraintes
  spécifiques »
- `/ventilateur-gamme` : « Comment choisir un ventilateur industriel standard
  adapté à vos besoins ? » · « Secteurs d'application : ventilateurs industriels
  standards »
- `/ventilateur-sur-mesure` : « Les différents critères lors du choix de vos
  ventilateurs industriels »
- `/solutions-ventilateur-industriel` : « Caissons de filtration pour systèmes de
  ventilation industrielle » · « Caissons d'insonorisation pour ventilateurs
  professionnels »
- `/purificateur-air` : « Nos conseils pour bien choisir son ventilateur industriel »
- `/bureau-etudes` : « Des ventilateurs industriels soumis à des analyses pour vous
  garantir leur qualité » · « Un produit et un process étudiés pour proposer les
  meilleurs délais de fabrication »
- `/competences` : « La conception et le dimensionnement des ventilateurs
  industriels » · « Centre d'essai dédié aux contrôles qualité et à la validation
  technique »
- `/secteurs-activite` : « Pourquoi les ventilateurs industriels sont-ils
  essentiels en entreprise ? »

## Points à trancher (relevés pendant l'audit)

1. **20 ans ou 35 ans ?** La meta description de l'accueil dit « plus de 20 ans »,
   le corps de page dit « plus de 35 ans ». Incohérence à arbitrer — elle est
   visible par Google comme par vos clients.
2. **Adresse réelle : Nivolas-Vermelle** (Isère), et non Lyon. Le SEO local doit
   citer la commune exacte dans le JSON-LD et les mentions ; « près de Lyon »
   reste pertinent comme repère géographique dans les titles.
3. **LiveCurve vs pupitre de sélection.** `/telechargement` promeut LiveCurve,
   votre plateforme officielle. Le « pupitre » de la maquette lui fait doublon :
   soit il devient une porte d'entrée vers LiveCurve, soit LiveCurve reste le
   seul outil et le pupitre est retiré. À décider avant la mise en production.
4. **Secteurs incohérents.** L'accueil affiche 4 secteurs (énergie/pétrochimie,
   agroalimentaire, métallurgie, textile) ; `/secteurs-activite` en cite d'autres
   (parachimie, cosmétique, ferroviaire). La liste consolidée doit être validée.
5. **`/outils` et `/calculs` renvoient déjà 404** sur le site actuel (ce sont des
   entrées de menu sans page). Rien à préserver, mais à ne pas recréer par erreur.

## Prochaine étape

Découper `index.html` en 15 pages reprenant cette arborescence à l'identique
(mêmes chemins d'URL), chacune héritant du design validé et des balises
ci-dessus. Tant que ce découpage n'est pas fait, **le site ne doit pas être mis
en production** : il ferait perdre 14 pages indexées.
