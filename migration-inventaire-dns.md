# Inventaire DNS avant migration — relevé du 2026-07-24

Photographie de l'existant **avant toute modification**. C'est la pièce qui permet
de tout recréer à l'identique et de revenir en arrière. Ne pas modifier ce fichier
après la bascule : le figer comme référence.

## euroventilatori.fr — le domaine à migrer

| Élément | Valeur relevée | Conséquence |
|---|---|---|
| **Nameservers** | `dns18.ovh.net`, `ns18.ovh.net` | DNS géré chez **OVH** — le registrar est OVH, il ne change pas |
| **A (apex)** | `18.197.248.23`, `52.59.120.70` | Hébergement actuel du site (Duda, revendu via Solocal) |
| **CNAME www** | `solocal.eu-multiscreensite.com` | Le site passe par **Solocal** (revendeur Duda) — c'est l'interlocuteur contractuel |
| **MX** | `mx1.ovh.net` (1), `mx2.ovh.net` (5), `mxb.ovh.net` (100) | ⚠️ **Il existe une messagerie OVH sur ce domaine** |
| **SPF (TXT)** | `v=spf1 include:mx.ovh.com ~all` | À reporter tel quel, sinon les envois partent en spam |
| **mail** | → `ns0.ovh.net` | Accès webmail OVH |
| **smtp** | → `ns0.ovh.net` | Serveur d'envoi OVH |
| **ftp** | → `ftp.start.ovh.net` | Service FTP OVH (probablement inutilisé, à vérifier) |

### Point de vigilance n°1 — la messagerie sur euroventilatori.fr

L'hypothèse initiale (« les e-mails sont sur l'autre domaine, donc hors périmètre »)
est **fausse** : `euroventilatori.fr` porte ses propres MX OVH. Il peut s'agir de
boîtes actives, d'alias ou de redirections. **À vérifier auprès d'OVH avant la
bascule** : quelles adresses `@euroventilatori.fr` existent et qui les relève.
Ces MX doivent être recréés à l'identique, sinon ces adresses cessent de recevoir
au moment exact du changement de nameservers.

### Point de vigilance n°2 — l'apex est canonique

Le site répond sur `euroventilatori.fr` (sans www). Un domaine racine ne peut pas
pointer vers Cloudflare Pages par un simple CNAME (limite du protocole DNS) : il
faut le *CNAME flattening*, que seul Cloudflare DNS fournit. C'est ce qui impose
de déplacer la zone DNS chez Cloudflare plutôt que de la laisser chez OVH.

## euroventilatori-france.com — HORS PÉRIMÈTRE

| Élément | Valeur relevée |
|---|---|
| **Nameservers** | `srv4.netavous.net`, `ns2.sd-france.net` (prestataire tiers) |
| **MX** | `euroventilatorifrance-com03i.mail.protection.outlook.com` → **Microsoft 365** |

Domaine **totalement indépendant** : autre registrar, autres nameservers, autre
messagerie. La migration de `euroventilatori.fr` ne l'affecte en aucune façon.
**Ne rien y toucher.** C'est ce domaine qui porte `contact@euroventilatori-france.com`
— l'adresse du formulaire reste donc opérationnelle quoi qu'il arrive.

## Ce qui reste à relever (auprès des fournisseurs)

- [ ] OVH : liste des boîtes / alias actifs sur `@euroventilatori.fr`
- [ ] OVH : date d'expiration du domaine, statut du verrou de transfert
- [ ] OVH : e-mail de contact administratif du domaine — est-il relevé ?
- [ ] Solocal / Duda : échéance du contrat et préavis de résiliation
- [ ] Enregistrements DKIM éventuels (sélecteurs non devinables — à lire dans
      l'interface OVH, l'interrogation DNS ne peut pas les découvrir seule)
- [ ] TXT de validation éventuels (Google Search Console, Bing)

## Export de référence à faire avant J−7

Depuis l'interface OVH : **Zone DNS → Exporter**. Sauvegarder le fichier obtenu
à côté de ce document, daté. C'est lui qui fait foi en cas de retour arrière —
l'interrogation DNS ci-dessus ne révèle que ce qu'on a pensé à demander.
