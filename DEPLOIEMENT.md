# Déposer le site sur Cloudflare Pages

Objectif de cette première étape : mettre le site en ligne **en préproduction**,
pour le parcourir en conditions réelles et relever les corrections à apporter.
Le domaine `euroventilatori.fr`, encore sous contrat Solocal/Duda, n'est pas
touché : il continue de servir l'ancien site.

**Point non négociable : rien n'est indexé à ce stade.** Le verrou est posé par
`_worker.js` et ne s'ouvre que lorsque le domaine de production sera rattaché
au projet.

> `_worker.js` fonctionne aussi bien sur **Workers** que sur **Pages** : les
> deux plateformes exposent la même interface pour servir les fichiers
> statiques. Le dossier `functions/`, lui, était propre à Pages et restait
> inerte sur Workers — c'est ce qui avait laissé la préproduction indexable.

Ce que Cloudflare publie n'est pas le dépôt entier, mais le dossier **`dist/`** :
les scripts de génération et les notes internes — inventaire SEO, analyse des
risques, revue du plan de bascule — restent hors ligne.

---

## Étape 1 — Créer le projet

> **Important : choisir Pages, pas Workers.** Un projet Workers « fichiers
> statiques seuls » n'exécute pas `_worker.js` — il le sert comme un fichier
> ordinaire. Ni le verrou d'indexation ni le formulaire ne fonctionnent alors.
> Sur Pages, `_worker.js` est interprété automatiquement (mode avancé).

### Voie A — téléversement direct (le plus simple)

**Workers & Pages** → **Create** → **Pages** → **Upload assets**. Nommer le
projet, puis déposer le dossier `euroventilatori-cloudflare/` ou son archive.
Rien d'autre à régler : `_worker.js` est détecté et pris en charge.

Pour chaque mise à jour : `python gen_pages.py && python build_upload.py`, puis
un nouveau téléversement.

### Voie B — connexion au dépôt Git

Sur [dash.cloudflare.com](https://dash.cloudflare.com) → **Workers & Pages** →
**Create** → **Pages** → **Connect to Git**, autoriser l'accès au dépôt
`euroventilatori-site` et le sélectionner.

| Champ | Valeur |
|---|---|
| **Project name** | `euroventilatori-preprod` |
| Production branch | `main` |
| Framework preset | *None* |
| Build command | `python gen_pages.py && python build_dist.py` |
| Build output directory | `dist` |
| Root directory | *(laisser vide)* |

> Le nom du projet fixe l'adresse technique `euroventilatori-preprod.pages.dev`
> et **ne se renomme pas**. Ce n'est pas gênant : cette adresse restera un
> outil interne, et le jour venu vous rattacherez `euroventilatori.fr` au même
> projet en « custom domain ». Les visiteurs ne verront jamais le nom du projet.

> Si la commande de build échoue (image sans Python), laissez le champ **vide**
> en gardant `dist` comme dossier de sortie : `dist/` est versionné dans le
> dépôt, donc publiable tel quel. Il faudra alors lancer
> `python gen_pages.py && python build_dist.py` avant chaque `git push`.

**Save and Deploy.** Le site sort sur `euroventilatori-preprod.pages.dev`.

---

## Étape 2 — Vérifier que rien n'est indexable

À faire **avant** de diffuser l'adresse à qui que ce soit.

1. Ouvrir `<votre-adresse>/robots.txt` : il doit afficher `Disallow: /` —
   et non le robots.txt de production.
2. Vérifier l'en-tête sur une page. Dans PowerShell :

```powershell
(Invoke-WebRequest https://euro-prepod.jeremyeuroventilatori.workers.dev/ventilateurs).Headers['X-Robots-Tag']
```

La réponse attendue est `noindex, nofollow, noarchive, nosnippet`.

Si ces deux contrôles passent, aucun moteur ne peut indexer la préproduction —
et cela restera vrai même après la mise en production : ni `.workers.dev` ni
`.pages.dev` ne sont reconnues comme hôtes de production.

**Protection supplémentaire recommandée** — **Zero Trust → Access →
Applications** → *Self-hosted* sur l'adresse de préproduction, avec une
règle « e-mails autorisés ». Le site devient inaccessible sans authentification :
ni moteurs, ni concurrents, ni prestataire sortant. Gratuit jusqu'à
50 utilisateurs. Sans Access, le site reste consultable par qui connaît
l'adresse — simplement invisible des moteurs.

---

## Étape 3 — Le formulaire (facultatif en préproduction)

Le formulaire fonctionne dès que quatre variables sont renseignées, dans
**Réglages du projet → Variables and Secrets**, pour **Production** *et*
**Preview** :

| Nom | Type | Valeur |
|---|---|---|
| `BREVO_API_KEY` | Secret | clé API Brevo |
| `TURNSTILE_SECRET` | Secret | clé privée Turnstile |
| `DESTINATAIRE` | Texte | `contact@euroventilatori-france.com` |
| `EXPEDITEUR` | Texte | une adresse du domaine authentifié chez Brevo |

Sans elles, le formulaire répond au visiteur en lui donnant le téléphone plutôt
que d'échouer en silence — suffisant pour une relecture, insuffisant pour la
mise en ligne.

Remplacer aussi `A_RENSEIGNER` par la clé **publique** Turnstile dans
`gen_pages.py` (attribut `data-sitekey`) et dans `index.html`, puis régénérer.
Cette clé n'est pas un secret : elle vit dans le HTML.

---

## Étape 4 — Corriger et redéployer

```
python gen_pages.py && python build_dist.py
git add -A && git commit -m "…" && git push
```

Cloudflare redéploie en une trentaine de secondes. Chaque déploiement est
conservé : l'onglet **Deployments** permet de revenir à une version précédente
en un clic.

---

## Étape 5 — Plus tard : rattacher le domaine de production

À faire uniquement quand les corrections sont validées et le formulaire branché.

1. **J−2** — chez OVH, abaisser à **300 s** le TTL des enregistrements `www`
   et du domaine nu. C'est ce qui rendra un retour arrière quasi instantané.
2. **Jour J**, contrat Solocal encore actif — dans le projet Pages :
   **Custom domains** → ajouter `www.euroventilatori.fr`, puis faire pointer
   l'enregistrement chez OVH.
   Traiter aussi le **domaine nu** `euroventilatori.fr` : il redirige
   aujourd'hui vers `www` *via Duda*, et cesserait de répondre à la
   résiliation.
3. Vérifier dans l'ordre : résolution DNS depuis un autre réseau → HTTPS →
   **e-mail de test envoyé et reçu** → envoi réel du formulaire → sitemap
   soumis dans Search Console → indexation demandée.

L'indexation s'ouvre **d'elle-même** dès que l'hôte devient
`www.euroventilatori.fr` : aucun fichier à modifier, aucun oubli possible.

**Retour arrière** — remettre l'ancienne valeur DNS ; avec les TTL à 300 s, le
site Duda revient en quelques minutes.

---

## Ce que contient `dist/`

Les 38 pages HTML, `assets/`, `_worker.js`, `_headers`, `_redirects`,
`robots.txt`, `sitemap.xml`, `llms.txt` et les favicons.

Volontairement absents : les scripts de génération (`*.py`) et la documentation
interne (`*.md`). `build_dist.py` refuse de terminer si l'un d'eux s'y glisse.

**`_worker.js`** est inclus dans le paquet. Il assure quatre choses : le verrou
d'indexation selon le nom d'hôte, les redirections 301 des anciennes URL, les
en-têtes de sécurité et de cache, et la réception du formulaire de contact.

> En mode `_worker.js`, les fichiers `_headers` et `_redirects` ne sont pas
> appliqués automatiquement : leur contenu est donc repris dans le worker.
> Ils restent dans le paquet pour un déploiement Pages classique.
