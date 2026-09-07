# Revue du plan de bascule — préproduction puis reprise en interne

Analyse du rétroplanning proposé, vérifications faites sur la production
le 1er septembre 2026.

## Le plan proposé

1. `preprod.euroventilatori.fr` pointe vers Cloudflare. Le site y vit,
   invisible des moteurs, aussi longtemps qu'il faut. Duda continue sur
   `https://www.euroventilatori.fr/`.
2. Validation : photos, textes, formulaire, mentions légales.
3. Jour J, **contrat encore actif** : on change la ligne `www` chez OVH.
   Le nouveau site est en ligne, Duda tourne toujours mais sans visiteur.
4. Deux à quatre semaines de surveillance : formulaires, e-mails, Search
   Console, un cycle commercial complet.
5. À la date de résiliation seulement : suppression du sous-domaine `preprod`.

## Ce qui est juste, et qui compte le plus

**Basculer pendant que le contrat court.** C'est la décision structurante, et
elle est prise dans le bon sens. Tant que Duda est actif, un retour arrière se
fait en une modification DNS. C'est ce qui distingue une migration maîtrisée
d'un pari.

**La préproduction sur un sous-domaine réel.** Tester sur l'infrastructure
définitive — même hébergeur, même certificat, même chaîne DNS — écarte la
catégorie de mauvaises surprises qui n'apparaissent qu'en conditions réelles.

**Ne rien supprimer avant la fin.** Le filet reste tendu jusqu'au bout.

## Trois points qui feraient échouer la bascule en l'état

### 1. Le `noindex` est dans le HTML — il basculerait avec le site

Chaque page porte aujourd'hui `<meta name="robots" content="noindex">`.
Préproduction et production servent **les mêmes fichiers** : le jour de la
bascule, `www` hériterait du `noindex` et le site neuf serait invisible de
Google. À l'inverse, le retirer rendrait la préproduction indexable.

Il faut sortir cette protection du HTML et la porter au niveau de l'hébergeur,
en la conditionnant au **nom d'hôte** :

- **Cloudflare Access sur `preprod`** (recommandé) — le sous-domaine demande une
  authentification par e-mail. Invisible des moteurs, et invisible tout court :
  ni concurrents, ni prestataire sortant. Gratuit jusqu'à 50 utilisateurs.
- **ou une règle d'en-tête** ajoutant `X-Robots-Tag: noindex, nofollow`
  uniquement quand l'hôte vaut `preprod.euroventilatori.fr`.

Bénéfice décisif : le jour J devient **un simple changement DNS**, sans
reconstruction ni redéploiement, donc sans fenêtre de risque.

### 2. Changer la ligne `www` ne suffit pas

Vérifié en production : le site est canonique en **`www`**, et le domaine nu
`euroventilatori.fr` **redirige vers `www`** — mais cette redirection est
assurée par Duda, puisque les enregistrements A du domaine nu pointent vers ses
serveurs.

Conséquence : après la bascule, tout fonctionne encore *tant que Duda vit*.
Le jour de la résiliation, `euroventilatori.fr` sans `www` **cesse de
répondre** — pour les visiteurs qui tapent l'adresse, pour les liens anciens,
et pour les cartes de visite.

Deux solutions :

- **Déplacer la zone DNS chez Cloudflare** (recommandé) : le domaine nu peut y
  pointer vers Cloudflare Pages grâce à l'aplatissement de CNAME, ce qu'OVH ne
  permet pas. C'est l'opération décrite par le skill `transfert-domaine` :
  recréer la zone complète — **MX compris** — avant de changer les serveurs
  de noms.
- **ou une redirection du domaine nu vers `www` chez OVH**, si l'on veut
  éviter de déplacer la zone. Plus simple, mais dépendant d'une fonction OVH.

Dans les deux cas, à traiter **avant** la résiliation, pas après.

### 3. Le formulaire n'existe pas encore

Il figure à juste titre dans la liste de validation, mais rien n'est construit :
le site ouvre aujourd'hui la messagerie du visiteur (`mailto:`), ce qui ne
fonctionne pas sur un poste sans client mail configuré. Il faut la fonction
Cloudflare, le service d'envoi et l'anti-spam **avant** le jour J, sinon la
bascule coupe silencieusement l'arrivée des demandes de devis.

## Quatre compléments à ajouter au rétroplanning

**À J−2 : abaisser les TTL à 300 secondes** chez OVH sur les enregistrements
concernés. Sans cela, un retour arrière met des heures à se propager ; avec,
il prend cinq minutes. C'est le geste qui rend la marche arrière réelle.

**Avant le jour J : exporter la liste des URL indexées** depuis Search Console
(rapport Pages). Le sitemap de production déclare 46 URL, mais nous avons
découvert une publication absente du sitemap : seule la Search Console dit ce
que Google connaît vraiment.

**Le jour J, dans l'ordre :** bascule DNS → vérifier la résolution depuis un
autre réseau → contrôler le HTTPS → **envoyer et recevoir un e-mail de test**
→ soumettre le sitemap → demander l'indexation des pages principales.

**Vérifier que Duda ne reste pas accessible ailleurs.** Beaucoup de
constructeurs exposent le site sur une adresse de prévisualisation qui leur est
propre. Si elle reste en ligne et indexable, c'est du contenu dupliqué. À faire
confirmer par le prestataire, ou à vérifier avec une recherche `site:`.

## Sur la durée de surveillance

Deux à quatre semaines est un bon ordre de grandeur, mais le critère utile
n'est pas le calendrier : c'est d'avoir **reçu et traité de vraies demandes par
le nouveau formulaire**. Tant qu'aucun devis n'est parti d'un formulaire du
nouveau site, la chaîne n'est pas prouvée. Pour un cycle commercial industriel,
compter plutôt quatre à six semaines avant de résilier.

## Séquence recommandée

| Quand | Action |
|---|---|
| Maintenant | Protéger `preprod` par Cloudflare Access ; retirer le `noindex` du HTML |
| Avant J | Formulaire branché ; photos ; relecture des mentions légales ; export Search Console |
| J−7 | Décider du sort du domaine nu : zone chez Cloudflare, ou redirection OVH |
| J−2 | TTL à 300 s |
| Jour J | Bascule `www` (+ domaine nu) ; vérifications ; sitemap ; indexation |
| J+1 à J+30 | Surveillance ; au moins un devis reçu par le nouveau formulaire |
| Résiliation | Suppression de `preprod` ; contrôle qu'aucun lien n'y renvoie |
