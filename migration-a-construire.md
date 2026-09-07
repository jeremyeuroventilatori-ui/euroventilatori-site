# Ce qu'il reste à construire avant le jour J

Inventaire du dépôt au 1er septembre 2026. Classé par conséquence si l'élément
manque le jour de la bascule, et non par ordre chronologique.

---

## A. Bloquants — sans eux, la bascule échoue ou coûte du référencement

### A1. Retirer le `noindex` du HTML
**État :** présent sur les 37 pages. **Qui :** moi. **Effort :** minutes.

Préproduction et production servent les mêmes fichiers. Le jour J, `www`
hériterait de l'interdiction d'indexation. La protection doit passer au niveau
de l'hôte : **Cloudflare Access sur `preprod`**, ou une règle d'en-tête
`X-Robots-Tag` conditionnée au nom d'hôte.

Effet secondaire majeur : le jour J devient un simple changement DNS, sans
reconstruction ni redéploiement.

### A2. Le formulaire de contact
**État :** `mailto:` sur 11 pages, aucune fonction serveur. **Qui :** moi, puis
vous pour les clés. **Effort :** une demi-journée.

Aujourd'hui, cliquer « Envoyer » ouvre la messagerie du visiteur. Sur un poste
d'entreprise sans client mail configuré, **il ne se passe rien** : la demande
est perdue sans que personne ne le sache. Basculer en l'état revient à couper
l'arrivée des devis.

À construire :
- `functions/api/contact.js` — la fonction Cloudflare Pages qui reçoit l'envoi
- l'envoi par **Brevo** vers `contact@euroventilatori-france.com`
- **Turnstile** (anti-spam Cloudflare, invisible) + champ piège
- accusé de réception automatique au demandeur
- messages de succès et d'erreur sur la page, sans rechargement
- **raccordement du pupitre de sélection** : débit, pression et puissance
  estimée arrivent structurés dans la demande

### A3. Le sort du domaine nu `euroventilatori.fr`
**État :** redirige vers `www` **via Duda**. **Qui :** vous. **Effort :** décision + exécution.

Le jour de la résiliation, le domaine sans `www` cesse de répondre. Deux voies :
déplacer la zone DNS chez Cloudflare (recréer la zone entière, **MX compris**),
ou poser une redirection OVH du domaine nu vers `www`.

### A4. Favicon et icônes
**État :** aucun. **Qui :** moi, à partir de votre logo. **Effort :** court.

Un site sans favicon affiche une page blanche dans l'onglet et dans les
favoris. Détail visuel, mais immédiatement perçu comme un site inachevé.

---

## B. Importants — le site fonctionne, mais diminué

### B1. En-têtes HTTP (`_headers`)
**État :** absent. **Qui :** moi. **Effort :** court.

Sécurité (HSTS, `X-Content-Type-Options`, `Referrer-Policy`, politique de
sécurité de contenu) et surtout **mise en cache** des CSS, JS et images :
c'est ce qui fait la différence entre un site rapide et un site très rapide,
et cela pèse sur les Core Web Vitals.

### B2. Page 404 personnalisée
**État :** absente. **Qui :** moi. **Effort :** court.

Sans elle, une URL erronée affiche la page d'erreur brute de Cloudflare, sans
menu ni retour possible. Avec 47 URL et des liens anciens dans la nature, ce
cas se produira.

### B3. `llms.txt` — visibilité dans les moteurs IA
**État :** absent. **Qui :** moi. **Effort :** court.

Fichier à la racine qui présente l'entreprise et ses pages clés aux moteurs
génératifs. Complète le balisage déjà en place (Organization, BreadcrumbList,
FAQPage, BlogPosting).

### B4. Les 10 publications de 2025
**État :** absentes (13 sur 2026 sont faites). **Qui :** moi. **Effort :** moyen.

Octobre rose, Movember, salon Vrac Tech du Mans, fermeture hivernale, offres
d'emploi, premier pas vers la RSE, etc. Complète la couverture à 47 URL sur 47.

### B5. Emplacements d'images prêts
**État :** le site est entièrement typographique. **Qui :** moi. **Effort :** moyen.

Préparer la structure d'accueil des photos — dimensions déclarées pour éviter
les sauts de mise en page, chargement différé, textes alternatifs — pour que
l'intégration soit mécanique le jour où les visuels arrivent.

---

## C. Ce que vous seul pouvez fournir

| Élément | Pourquoi c'est bloquant ou important |
|---|---|
| **Photographies** | Atelier, machines, réalisations. Seul écart réel avec un site de premier plan, et les visuels actuels appartiennent à l'hébergement Duda |
| **Relecture des mentions légales** | Rédigées à partir de vos données réelles, mais elles vous engagent |
| **Export Search Console** (rapport Pages) | Seule source fiable des URL réellement indexées — le sitemap en oubliait déjà une |
| **Validation des textes** | 37 pages réécrites : les chiffres sont vérifiés, le ton reste à valider |
| **Qui traite les demandes** | L'adresse de réception et la personne qui répond, à confirmer avant de brancher le formulaire |
| **Adresse de prévisualisation Duda** | À faire confirmer par le prestataire : si elle reste en ligne, c'est du contenu dupliqué |

---

## D. Comptes et accès à ouvrir

1. **Cloudflare** — compte, projet Pages connecté au dépôt GitHub, domaine ajouté.
2. **Cloudflare Access** — pour protéger `preprod` (gratuit jusqu'à 50 utilisateurs).
3. **Brevo** — compte, puis **authentification du domaine expéditeur** :
   enregistrements SPF et DKIM à poser sur `euroventilatori-france.com`.
   ⚠️ Ce domaine est distinct de `euroventilatori.fr` et hébergé ailleurs :
   opération purement additive, **ne pas toucher aux MX Microsoft 365**.
4. **Turnstile** — clés publique et privée (dans le compte Cloudflare).
5. **Bing Webmaster Tools** — l'index Bing alimente ChatGPT ; utile pour le GEO.

---

## E. Vérifications de la veille

- [ ] Formulaire testé de bout en bout : envoi, réception, accusé, anti-spam
- [ ] E-mail de test envoyé **et** reçu sur les adresses concernées
- [ ] Parcours mobile réel sur un téléphone, pas seulement en simulation
- [ ] Lighthouse : performance, accessibilité, bonnes pratiques, SEO
- [ ] Lecteur d'écran (NVDA) sur l'accueil et le pupitre de sélection
- [ ] Thème sombre contrôlé sur les pages ajoutées récemment
- [ ] TTL abaissés à 300 s depuis 48 h
- [ ] Export DNS OVH sauvegardé et daté

---

## Ordre de travail proposé

1. **A1** — retirer le `noindex` : débloque l'architecture, et rend le jour J trivial.
2. **A2** — le formulaire : le plus long, et le plus coûteux s'il manque.
3. **A4 + B1 + B2 + B3** — favicon, en-têtes, 404, `llms.txt` : une seule passe.
4. **B4** — les 10 publications de 2025.
5. **B5** — emplacements d'images, dès que les photos sont décidées.

Les points C et D peuvent avancer en parallèle de votre côté ; le formulaire
(A2) ne pourra être terminé qu'une fois le compte Brevo créé et le domaine
d'envoi authentifié.
