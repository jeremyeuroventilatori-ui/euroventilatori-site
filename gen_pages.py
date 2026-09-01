# -*- coding: utf-8 -*-
"""Génère les pages intérieures du site Euroventilatori France.
Arborescence, <title>, meta description, H1 et H2 repris à l'identique du site
actuel (voir seo-inventaire.md). Corps de texte reformulé à partir du contenu
réel. Exécuter depuis le dossier euroventilatori-site : python gen_pages.py
"""
import io, os

SITE = "https://www.euroventilatori.fr"

NAV_ITEMS = [
    ("/ventilateurs", "Nos produits"),
    ("/solutions-ventilateur-industriel", "Solutions"),
    ("/secteurs-activite", "Secteurs"),
    ("/bureau-etudes", "Bureau d'études"),
    ("/telechargement", "Téléchargement"),
    ("/actualites", "Actualités"),
    ("/contact", "Contact"),
]

def nav_html(active_url):
    """Menu principal. La page courante est signalée (repère visuel + a11y)."""
    links = []
    for url, label in NAV_ITEMS:
        cur = ' aria-current="page"' if url == active_url else ""
        links.append(f'      <a href="{url}"{cur}>{label}</a>')
    return """<header>
  <div class="wrap hd">
    <a class="logo" href="/" aria-label="Euroventilatori France — accueil">
      <b>EUROVENTILATORI</b><span>FRANCE</span>
    </a>
    <button id="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="mainNav">☰</button>
    <nav class="main" id="mainNav" aria-label="Navigation principale">
""" + "\n".join(links) + """
    </nav>
    <div class="hd-cta">
      <a class="tel" href="tel:0474436838">04 74 43 68 38</a>
      <button id="themeBtn" aria-label="Basculer le thème clair / sombre" aria-pressed="false">◐</button>
    </div>
  </div>
</header>"""

def breadcrumb_html(trail):
    """Fil d'Ariane visible. `trail` = [(label, url|None), …], le dernier sans url."""
    items = ['<li><a href="/">Accueil</a></li>']
    for label, url in trail:
        if url:
            items.append(f'<li><a href="{url}">{label}</a></li>')
        else:
            items.append(f'<li aria-current="page">{label}</li>')
    return ('<nav class="breadcrumb wrap" aria-label="Fil d\'Ariane">\n  <ol>'
            + "".join(items) + "</ol>\n</nav>")

def breadcrumb_jsonld(trail):
    els = [{"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"}]
    for i, (label, url) in enumerate(trail, start=2):
        e = {"@type": "ListItem", "position": i, "name": label}
        if url:
            e["item"] = SITE + url
        els.append(e)
    import json
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                       "itemListElement": els}, ensure_ascii=False, indent=1)

ORG_JSONLD = """{
 "@context": "https://schema.org",
 "@type": "Organization",
 "name": "Euroventilatori France",
 "url": "https://www.euroventilatori.fr",
 "description": "Constructeur de ventilateurs industriels centrifuges et hélicoïdaux, de caissons insonorisés et de solutions de filtration d'air.",
 "telephone": "+33474436838",
 "email": "contact@euroventilatori-france.com",
 "foundingDate": "1981",
 "address": {
  "@type": "PostalAddress",
  "streetAddress": "150 Rue du Vernay",
  "postalCode": "38300",
  "addressLocality": "Nivolas-Vermelle",
  "addressCountry": "FR"
 },
 "areaServed": "FR",
 "sameAs": [
  "https://facebook.com/profile.php?id=61572883753722",
  "https://linkedin.com/company/euroventilatori-france"
 ]
}"""

# Bandeau de preuves — chiffres relevés sur le site actuel, tous vérifiés.
PROOF = """<section class="proof band-alt">
  <div class="wrap">
    <div class="proof-grid">
      <div class="proof-item rv"><span class="n"><span data-count="35">0</span><i>ans</i></span><span class="l">d'expertise en France</span></div>
      <div class="proof-item rv"><span class="n"><span data-count="30000">0</span></span><span class="l">ventilateurs produits par an</span></div>
      <div class="proof-item rv"><span class="n"><span data-count="28000">0</span><i>m²</i></span><span class="l">de surface de production</span></div>
      <div class="proof-item rv"><span class="n">24<i>h</i></span><span class="l">pour un devis détaillé</span></div>
    </div>
  </div>
</section>"""


def faq_html(items):
    """Questions frequentes. Chaque reponse tient seule hors de son contexte :
    c'est la condition pour etre extraite en position zero et citee par une IA."""
    if not items:
        return ""
    blocs = "".join(
        '<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (q, r) for q, r in items)
    return """<section class="faq band-alt">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">Questions fréquentes</p>
      <h2>Ce que l'on nous demande le plus souvent</h2>
    </div>
    <div class="faq-list">%s</div>
  </div>
</section>""" % blocs


def faq_jsonld(items):
    if not items:
        return ""
    import json, re as _re
    def net(t):
        return _re.sub(r"<[^>]+>", "", t).replace("&nbsp;", " ").strip()
    donnees = {"@context": "https://schema.org", "@type": "FAQPage",
               "mainEntity": [{"@type": "Question", "name": net(q),
                               "acceptedAnswer": {"@type": "Answer", "text": net(r)}}
                              for q, r in items]}
    return ('<script type="application/ld+json">\n'
            + json.dumps(donnees, ensure_ascii=False, indent=1) + "\n</script>")

def related_html(cards):
    """Pages liées : circulation du lecteur et maillage interne."""
    if not cards:
        return ""
    items = "".join(
        f'<a href="{u}"><strong>{t}</strong><span>{d}</span>'
        f'<span class="go">Consulter →</span></a>' for u, t, d in cards)
    return f"""<section class="related band-alt">
  <div class="wrap">
    <h2>À consulter également</h2>
    <div class="related-grid">{items}</div>
  </div>
</section>"""

FOOTER = """<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo" href="/" style="color:var(--deep-ink)"><b>EUROVENTILATORI</b><span>FRANCE</span></a>
        <p style="opacity:.7;font-size:13.5px;margin-top:14px;max-width:38ch">Constructeur
          de ventilateurs industriels et de solutions acoustiques — plus de 35 ans au
          service de l'air des usines.</p>
        <p class="mono" style="opacity:.6;font-size:12px;margin-top:10px">150 Rue du Vernay<br>38300 Nivolas-Vermelle</p>
      </div>
      <div>
        <h3>Produits</h3>
        <a href="/ventilateurs">Nos ventilateurs</a>
        <a href="/ventilateur-gamme">Ventilateurs de gamme</a>
        <a href="/ventilateur-sur-mesure">Ventilateurs sur mesure</a>
        <a href="/ventilateurs-centrifuges">Ventilateurs centrifuges</a>
        <a href="/ventilateurs-helicoides">Ventilateurs hélicoïdes</a>
        <a href="/caissons-insonorises">Acoustique</a>
        <a href="/purificateur-air">Filtration</a>
        <a href="/nos-autres-accessoires">Accessoires</a>
      </div>
      <div>
        <h3>Entreprise</h3>
        <a href="/qui-sommes-nous">Qui sommes-nous ?</a>
        <a href="/bureau-etudes">Bureau d'études</a>
        <a href="/competences">Compétences</a>
        <a href="/secteurs-activite">Secteurs d'activité</a>
        <a href="/traitement-surface">Traitement de surface</a>
        <a href="/actualites">Actualités</a>
      </div>
      <div>
        <h3>Ressources</h3>
        <a href="/solutions-ventilateur-industriel">Solutions</a>
        <a href="/telechargement">Téléchargement &amp; LiveCurve</a>
        <a href="/contact">Contact &amp; devis</a>
        <a href="/ile-de-france-rhone-alpes">Rhône-Alpes</a>
        <a href="/paris">Paris / Île-de-France</a>
        <a href="/lille">Lille / Hauts-de-France</a>
        <a href="/bretagne">Bretagne</a>
      </div>
    </div>
    <div class="foot-note">
      <span>© 2026 Euroventilatori France — Constructeur de ventilateurs industriels</span>
      <span class="foot-legal">
        <a href="/mentions-legales">Mentions légales</a>
        <a href="/vie-privee">Vie privée</a>
        <a href="/vie-privee">Cookies</a>
      </span>
    </div>
  </div>
</footer>"""

TPL = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<!-- ⚠️ PRÉPRODUCTION : retirer ce noindex LE JOUR de la bascule du domaine. -->
<meta name="robots" content="noindex">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Euroventilatori France">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#033F87">
<link rel="stylesheet" href="assets/styles.css">
<script type="application/ld+json">
{org}
</script>
<script type="application/ld+json">
{bcjson}
</script>
{faqjson}
</head>
<body>
<canvas id="airCanvas" aria-hidden="true"></canvas>
<a class="skip-link" href="#contenu">Aller au contenu</a>
{nav}
<main id="contenu">
{breadcrumb}
<section class="hero-lite">
  <span class="ghost" data-plx="-0.14" aria-hidden="true">{ghost}</span>
  <div class="wrap">
    <p class="eyebrow">{kicker}</p>
    <h1>{h1}</h1>
    <div class="prose lead-block">
{intro}
    </div>
    <div class="cta-row">{cta}</div>
  </div>
</section>
{proof}
{sections}
{faq}
{related}
<section class="cta-band-wrap">
  <div class="cta-band">
    <div class="wrap" style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:22px">
      <div>
        <h2 style="font-size:clamp(24px,3.2vw,38px);text-transform:uppercase">Un projet de ventilation&nbsp;?</h2>
        <p style="opacity:.75;margin-top:6px">Transmettez débit, pression et contraintes&nbsp;: devis détaillé sous 24&nbsp;h.</p>
      </div>
      <a class="btn primary" href="/contact">Demander un devis</a>
    </div>
  </div>
</section>
</main>
{footer}
<script src="assets/site.js"></script>
</body>
</html>
"""

def sec(h2, paras, chips=None):
    chips_html = ""
    if chips:
        chips_html = '<div class="spec">' + "".join(f"<span>{c}</span>" for c in chips) + "</div>"
    body = "\n".join(f"      <p>{p}</p>" for p in paras)
    return f"""<section class="page-sec">
  <div class="wrap sec-grid">
    <h2>{h2}</h2>
    <div class="prose">
{body}
      {chips_html}
    </div>
  </div>
</section>"""


# ===========================================================================
# BLOG — articles depuis janvier 2026.
# Les faits sont ceux de l'entreprise (dates, chiffres, evenements, produits) ;
# la redaction est neuve.
# ===========================================================================

ARTICLES = []   # du plus recent au plus ancien

def article(slug, date_iso, date_fr, titre, chapo, corps, desc):
    ARTICLES.append(dict(slug=slug, date_iso=date_iso, date_fr=date_fr,
                         titre=titre, chapo=chapo, corps=corps, desc=desc))

def blogposting_jsonld(a):
    import json
    return ('<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": a["titre"], "datePublished": a["date_iso"],
        "description": a["desc"],
        "author": {"@type": "Organization", "name": "Euroventilatori France"},
        "publisher": {"@type": "Organization", "name": "Euroventilatori France"},
        "mainEntityOfPage": SITE + "/" + a["slug"]
    }, ensure_ascii=False, indent=1) + "\n</script>")

def autres_articles(courant, n=3):
    """Trois autres publications, pour prolonger la lecture."""
    autres = [a for a in ARTICLES if a["slug"] != courant][:n]
    if not autres:
        return ""
    items = "".join(
        '<a href="/%s"><strong>%s</strong><span>%s</span>'
        '<span class="go">%s →</span></a>' % (a["slug"], a["titre"], a["desc"], a["date_fr"])
        for a in autres)
    return ('<section class="related band-alt">\n  <div class="wrap">\n'
            '    <h2>Autres publications</h2>\n'
            '    <div class="related-grid">%s</div>\n  </div>\n</section>' % items)


# --- Publications, du plus recent au plus ancien ---------------------------

article("belle-rentree-a-tous", "2026-09-01", "1er septembre 2026",
  "Belle rentrée à tous&nbsp;!",
  "Celle des cahiers neufs à la maison, et celle des ateliers qui retrouvent leur souffle.",
  ["Septembre remet tout le monde en mouvement : les enfants ont repris le chemin de l'école ce matin, et les ateliers redémarrent après la coupure estivale.",
   "Toute l'équipe d'Euroventilatori France vous souhaite une excellente rentrée — à vous, à vos équipes, et à celles et ceux qui ont fait leur rentrée des classes.",
   "Bonne reprise à tous."],
  "L'équipe Euroventilatori France vous souhaite une bonne rentrée.")

article("fermeture-estivale", "2026-07-27", "27 juillet 2026",
  "Fermeture estivale",
  "Nos bureaux et ateliers seront fermés une semaine au mois d'août.",
  ["Euroventilatori France sera fermée <b>du lundi 10 au vendredi 14 août inclus</b>.",
   "Nous serons de retour le <b>lundi 17 août</b> pour traiter l'ensemble de vos demandes. Pensez à anticiper vos commandes si votre chantier ne peut pas attendre cette date.",
   "Toute l'équipe vous souhaite un excellent été."],
  "Euroventilatori France sera fermée du 10 au 14 août, retour le lundi 17 août.")

article("on-recrute-notre-future-alternante-hse-h-f-et-ce-n-est-pas-un-poste-cafe-classeur",
  "2026-07-16", "16 juillet 2026",
  "On recrute notre futur·e alternant·e HSE (H/F)",
  "Un périmètre complet, pas un poste d'observation : construire et piloter notre démarche Santé, Sécurité et Environnement.",
  ["À Nivolas-Vermelle, en Isère, nous cherchons un·e alternant·e pour <b>bâtir notre démarche HSE de bout en bout</b>. Ce n'est pas un poste d'archivage : c'est un projet à mener.",
   "<b>Sécurité</b> — pilotage du document unique (DUERP), analyse des accidents et presqu'accidents, plans de prévention, gestion des équipements de protection, quarts d'heure sécurité.",
   "<b>Réglementaire</b> — veille, conformité au Code du travail et à la réglementation ICPE, vérifications périodiques, habilitations et formations.",
   "<b>Environnement</b> — gestion des déchets et des filières, dont les DEEE, suivi des indicateurs, démarche RSE.",
   "<b>Terrain</b> — audits et visites sécurité, accueil des nouveaux collaborateurs, protocoles de chargement et de déchargement.",
   "<b>Pilotage</b> — système documentaire HSE, tableaux de bord, préparation à une certification ISO 45001 et/ou ISO 14001.",
   "Ce que l'alternance apporte : une autonomie réelle sur un périmètre à 360°, un contact direct avec la direction dans une PME industrielle à taille humaine, un environnement technique riche, et des actions que vous verrez réellement mises en œuvre.",
   "<b>Profil</b> : BUT HSE, licence professionnelle HSE/QHSE ou master HSE/QHSE. <b>Rentrée 2026</b>, contrat de 12 à 24 mois, à Nivolas-Vermelle (38).",
   "Candidatures — CV et quelques lignes de motivation — à <a href=\"mailto:contact@euroventilatori-france.com\">contact@euroventilatori-france.com</a>."],
  "Alternance HSE (H/F) à Nivolas-Vermelle : DUERP, ICPE, déchets, audits, préparation ISO 45001 et 14001. Rentrée 2026, 12 à 24 mois.")

article("votre-ventilateur-dans-votre-couleur-sans-rien-sacrifier", "2026-07-02", "2 juillet 2026",
  "Votre ventilateur, dans votre couleur. Sans rien sacrifier.",
  "Sept machines, sept teintes RAL — et des performances rigoureusement identiques.",
  ["Sept ventilateurs, sept teintes RAL : autant de façons de s'inscrire dans un atelier. Un code de sécurité, le repérage d'une ligne de production, une charte de marque.",
   "La couleur porte une information. Un ventilateur à vos teintes rend le site plus lisible pour ceux qui y travaillent — et l'installation ressemble davantage à votre entreprise.",
   "Quant aux performances, elles ne varient pas d'un pigment : la mise en peinture reste une <a href=\"/traitement-surface\">finition de surface</a>, sans effet sur le débit, la pression ou le rendement.",
   "Quelle teinte pour la prochaine machine ? Écrivez-nous, nous nous occupons du reste."],
  "Sept ventilateurs, sept teintes RAL : la couleur au service du repérage en atelier, sans aucun effet sur les performances.")

article("pourquoi-se-contenter-du-gris-standard", "2026-06-15", "15 juin 2026",
  "Pourquoi se contenter du gris standard&nbsp;?",
  "Un client nous a demandé un ventilateur rose. Nous avons dit oui — et pour une bonne raison.",
  ["Ce n'était pas une fantaisie. Dans son atelier, chaque couleur a une signification : un code, une ligne, une consigne de sécurité identifiable d'un coup d'œil.",
   "Un ventilateur, c'est d'abord de la performance. Mais une fois installé, il fait partie du décor, de l'identité d'un site, parfois de la charte d'une marque.",
   "Chez Euroventilatori France, la mise en peinture se fait selon votre demande : la teinte RAL de votre choix, pour s'accorder à votre installation et à vos codes couleur.",
   "Sept ventilateurs centrifuges, sept teintes : même exigence technique, sept finitions. Le détail ne change rien à la mécanique — il change tout au reste."],
  "La teinte RAL de votre choix sur nos ventilateurs centrifuges : un repérage plus clair en atelier, une mécanique inchangée.")

article("la-moisson-ce-n-est-pas-la-fin-du-travail-c-est-le-debut-de-la-conservation",
  "2026-06-01", "1er juin 2026",
  "La moisson n'est pas la fin du travail. C'est le début de la conservation.",
  "Un grain rentré trop chaud ou trop humide se dégrade en silence.",
  ["Condensation, points chauds, développement d'insectes : la dégradation ne fait pas de bruit, et c'est la valeur marchande de toute une campagne qui s'érode dans la cellule.",
   "La <b>ventilation de refroidissement</b> est la première barrière, et la plus simple à mettre en place.",
   "Le <b>SIL'AIR</b>, ventilateur centrifuge mobile d'Euroventilatori France, est conçu pour l'agro-industrie : il abaisse la température du grain stocké, chasse l'humidité résiduelle et stoppe la condensation, et préserve ainsi la qualité du lot dans le temps.",
   "Monté sur roulettes, il se déplace d'une cellule à l'autre et s'utilise sans installation préalable.",
   "Vous préparez votre campagne ? Notre équipe vous accompagne sur le dimensionnement."],
  "Le SIL'AIR, ventilateur centrifuge mobile, refroidit le grain stocké et stoppe la condensation pour préserver la valeur du lot.")

article("chez-euroventilatori-nous-aimons-faire-les-choses-en-grand", "2026-05-04", "4 mai 2026",
  "Chez Euroventilatori, nous aimons faire les choses en grand",
  "Deux centrifuges BPRC 2001 viennent de quitter nos ateliers pour une usine de terre cuite en Argentine.",
  ["Quand une usine de terre cuite argentine doit ventiler ses fours et ses séchoirs, la demi-mesure n'est pas une option.",
   "Les caractéristiques de chaque machine : <b>252 000 m³/h</b> de débit d'air à <b>80 °C</b>, <b>900 Pa</b> de pression statique, <b>85 % de rendement</b>, motorisation <b>132 kW</b> à 6 pôles (980 tr/min).",
   "Ce sont des machines taillées pour l'endurance : haute température et fonctionnement continu, deux contraintes qui ne pardonnent pas l'approximation.",
   "De la <a href=\"/bureau-etudes\">sélection aéraulique</a> à la mise en caisse sur convoi exceptionnel, chaque étape a été pensée pour garantir la performance et la fiabilité sur le long terme."],
  "Deux ventilateurs centrifuges BPRC 2001 pour une usine de terre cuite en Argentine : 252 000 m³/h à 80 °C, 85 % de rendement.")

article("mai-arrive-vite-trop-vite", "2026-04-27", "27 avril 2026",
  "Mai arrive vite. Trop vite.",
  "Entre ponts et jours fériés, le mois ressemble davantage à trois semaines qu'à trente et un jours.",
  ["Nos ateliers seront fermés les <b>1er, 8, 14, 15, 22 et 25 mai</b>. C'est aussi un moment de repos pour nos équipes.",
   "Dans notre secteur, un ventilateur qui n'arrive pas à temps, c'est une installation bloquée et un chantier qui attend.",
   "La réponse tient en un mot : anticiper. Passez vos commandes dès maintenant pour être livré avant les perturbations, ou planifiez avec nous pour que tout soit calé en amont.",
   "Un doute sur vos délais ? Écrivez-nous, nous regardons cela ensemble."],
  "Fermetures des 1er, 8, 14, 15, 22 et 25 mai : anticipez vos commandes de ventilateurs pour éviter l'attente sur chantier.")

article("on-ne-le-voit-pas-on-ne-l-entend-pas", "2026-04-13", "13 avril 2026",
  "On ne le voit pas. On ne l'entend pas.",
  "Une isolation en laine de roche haute densité, intégrée à nos ventilateurs centrifuges.",
  ["Discret par conception, ce matériau fait pourtant partie intégrante de la performance de nos machines. Ce n'est pas un accessoire : c'est une composante technique, intégrée pour répondre à trois exigences à la fois.",
   "Son rôle : <b>réduire le bruit rayonné</b> par la machine, <b>isoler thermiquement</b>, et offrir ainsi une double protection phonique et thermique intégrée.",
   "Il n'y a pas de compromis entre performance aéraulique et confort acoustique. L'isolation agit <b>en dehors du flux d'air</b> : le débit, la pression et le rendement ne sont pas affectés. Le ventilateur délivre ses performances nominales pendant que l'isolation travaille en parallèle.",
   "Pour un bureau d'études, cela simplifie la conception : moins de traitement acoustique à prévoir en aval. Pour l'intégrateur et l'installateur, c'est une mise en œuvre plus directe, sans intervention supplémentaire sur le local technique.",
   "Nos <a href=\"/caissons-insonorises\">solutions acoustiques</a> complètent ce dispositif lorsque l'ambiance l'exige."],
  "Laine de roche haute densité sur nos centrifuges : moins de bruit rayonné et une isolation thermique, sans toucher aux performances aérauliques.")

article("ventilation-des-silos-agricoles-la-derniere-etape-qui-conditionne-toutes-les-autres",
  "2026-03-30", "30 mars 2026",
  "Ventilation des silos agricoles&nbsp;: la dernière étape qui conditionne toutes les autres",
  "Une semaine trop humide suffit à compromettre une récolte entière.",
  ["Pas d'accident, pas d'imprudence : simplement du grain stocké trop chaud, trop longtemps, dans un silo insuffisamment ventilé.",
   "Des mois à préparer les terres, des nuits à surveiller la météo, des semaines à moissonner — et tout se décide, finalement, dans le silo.",
   "La ventilation des céréales n'est pas une option en bout de chaîne : c'est la variable qui conditionne la valeur de tout le reste. Une température trop élevée favorise les moisissures ; une humidité non maîtrisée entraîne la fermentation ; une aération insuffisante transforme le stockage en perte nette.",
   "<b>SIL'AIR</b> est la gamme d'Euroventilatori dédiée au stockage agricole : des ventilateurs silencieux, à haute efficacité énergétique, dimensionnés selon le volume de stockage et le type de grain.",
   "Ni surdimensionnement, qui pèse inutilement sur la consommation, ni sous-dimensionnement, qui met la récolte en danger. Le bon débit, pour le bon volume."],
  "La gamme SIL'AIR d'Euroventilatori : des ventilateurs de silo silencieux et économes, dimensionnés selon le volume stocké et le type de grain.")

article("bienvenue-sebastien-coordinateur-technique", "2026-03-02", "2 mars 2026",
  "Bienvenue à Sébastien, coordinateur technique",
  "Il se décrit comme « un dessinateur fainéant ». C'est précisément pour cela que nous l'avons recruté.",
  ["Sébastien a rejoint Euroventilatori France il y a deux mois comme <b>coordinateur technique</b>. Son parcours : des années en bureaux d'études, à concevoir des systèmes hydrauliques haute et basse pression.",
   "Son mantra — « un bon dessinateur est un dessinateur fainéant » — signifie exactement l'inverse de ce qu'il laisse entendre : quelqu'un qui optimise, qui simplifie, et qui refuse de faire compliqué quand on peut faire efficace.",
   "Interrogé sur son super-pouvoir, il répond « transmettre mes compétences ». Sur sa façon de travailler, un mot : « bâtisseur ».",
   "Sa mission chez nous : construire les fondations du <a href=\"/bureau-etudes\">bureau d'études</a>, pour que toute l'équipe travaille mieux et plus vite.",
   "Et s'il était un ventilateur ? « Le silencieux efficace. » Après deux mois à ses côtés, la description est juste. Bienvenue dans l'équipe."],
  "Sébastien rejoint Euroventilatori France comme coordinateur technique, avec pour mission de structurer le bureau d'études.")

article("encore-une-realisation-remarquable-pour-un-de-nos-partenaires", "2026-02-06", "6 février 2026",
  "Une réalisation remarquable pour l'un de nos partenaires",
  "Trois ventilateurs de 75 kW en zone ATEX, caissonnés et silencieux.",
  ["Le projet portait sur la mise en place de <b>trois ventilateurs industriels de 75 kW</b> conçus pour répondre aux exigences d'un <b>environnement ATEX</b>.",
   "Chaque machine a été intégrée dans un <a href=\"/caissons-insonorises\">caisson insonorisé</a> et équipée de silencieux à baffles au soufflage, pour une acoustique maîtrisée sur l'ensemble de l'installation.",
   "<b>Application</b> : aspiration de poussières et de vapeurs de vernis sec après filtration, en zone classée. Ce type d'usage impose des équipements répondant aux normes de sécurité les plus strictes pour écarter tout risque lié aux atmosphères explosibles.",
   "<b>Performances de chaque machine</b> : débit de <b>14 500 m³/h</b>, dépression de <b>13 000 Pa</b>, puissance de <b>75 kW</b>. Des valeurs qui assurent une extraction efficace tout en maintenant le niveau de sécurité requis.",
   "Cette réalisation illustre ce que permet une offre complète : la machine, son <a href=\"/traitement-surface\">traitement</a>, son traitement acoustique et sa <a href=\"/purificateur-air\">filtration</a>, étudiés ensemble plutôt que juxtaposés."],
  "Trois ventilateurs de 75 kW en zone ATEX : 14 500 m³/h, 13 000 Pa, caissons insonorisés et silencieux à baffles.")

article("bonne-annee-2026-a-tous", "2026-01-06", "6 janvier 2026",
  "Bonne année 2026 à tous&nbsp;!",
  "Cap sur une année de progrès et de durabilité.",
  ["En ouvrant ce nouveau chapitre, toute l'équipe d'Euroventilatori France vous adresse ses meilleurs vœux.",
   "Cette nouvelle année est l'occasion de remercier celles et ceux qui nous accompagnent : nos clients fidèles, nos partenaires et nos collègues. Votre confiance est le socle sur lequel se construit notre travail.",
   "Vos retours, vos exigences de qualité et votre fidélité sont ce qui nous pousse à progresser et à concevoir des solutions plus performantes et plus durables.",
   "L'année écoulée a été marquée par des défis relevés ensemble, des projets ambitieux menés à bien et des partenariats consolidés.",
   "Nous vous souhaitons une excellente année 2026."],
  "L'équipe Euroventilatori France vous présente ses meilleurs vœux pour 2026.")

P = {}

P["ventilateurs.html"] = dict(
  title="Vente ventilateurs industriels à Lyon - Silencieux et sur mesure",
  desc="Ventilateurs industriels de gamme ou sur mesure, silencieux et fiables : nos techniciens conçoivent l'équipement adapté à votre process, partout en France.",
  h1="Vente de ventilateurs industriels",
  kicker="Nos produits — pour les professionnels, à Lyon et dans toute la France",
  ghost="Produits",
  intro="""<p>Le ventilateur n'est pas une simple machine&nbsp;: c'est le cœur de votre
installation industrielle. Notre catalogue répertorie <b>31 familles d'appareils</b>
— tailles, orientations, arrangements et matériaux étudiés pour coller précisément
à vos exigences, où que soit votre site en France.</p>""",
  cta='<a class="btn primary" href="/contact">Commander des ventilateurs</a><a class="btn ghost-b" href="/ventilateur-gamme">Voir la gamme</a>',
  sections=[
    ("Ventilateurs industriels standards ou sur mesure : comment choisir ?",
     ["Deux familles couvrent l'ensemble des besoins. Les <a href=\"/ventilateur-gamme\">ventilateurs standards</a>, préfabriqués, offrent des performances, une fiabilité et une durabilité éprouvées — le bon choix pour les applications courantes sans spécification particulière.",
      "Les <a href=\"/ventilateur-sur-mesure\">ventilateurs sur mesure</a>, eux, sont conçus pour répondre à des contraintes précises : fluide chargé, haute température, encombrement, matériaux spéciaux. Nos technico-commerciaux vous orientent vers la bonne famille dès le premier échange."]),
    ("S'équiper de ventilateurs industriels sur mesure, pour des besoins précis",
     ["Quand la gamme ne suffit pas, notre bureau d'études dimensionne une machine dédiée à partir de votre cahier des charges : aciers multiples, niveaux d'étanchéité, températures très élevées, conformité <b>ATEX</b>.",
      "Chaque projet est étudié pour apporter une réponse technique complète — pas seulement un ventilateur, mais la solution aéraulique qui va avec."]),
    ("Des ventilateurs industriels adaptés à vos contraintes spécifiques",
     ["Centrifuges basse, moyenne ou haute pression, hélicoïdaux : extraction, soufflage, renouvellement d'air, transport pneumatique — nos équipements couvrent les environnements les plus contraints.",
      "Et parce qu'un ventilateur vit rarement seul, l'offre s'étend aux <a href=\"/caissons-insonorises\">caissons insonorisés</a>, à la <a href=\"/purificateur-air\">filtration</a> et aux <a href=\"/nos-autres-accessoires\">accessoires</a> de raccordement."],
     ["Basse pression","Moyenne pression","Haute pression","Hélicoïdaux","ATEX"]),
  ])

P["ventilateur-gamme.html"] = dict(
  title="Vente de ventilateurs de gamme industrielle à Lyon",
  desc="53 séries, 25 tailles, 16 orientations : le catalogue Euroventilatori couvre extraction, soufflage et renouvellement d'air pour toutes les activités industrielles.",
  h1="Vente de ventilateurs de gamme industrielle à Lyon et dans toute la France",
  kicker="Nos produits — ventilateurs standards",
  ghost="Gamme",
  intro="""<p>Le catalogue Euroventilatori, c'est <b>53 séries de machines</b> en
<b>25 tailles</b>, <b>16 orientations</b> et 6 types d'arrangements, avec plusieurs
matériaux possibles. Centrifuges à basse, moyenne ou haute pression, ils assurent
extraction, soufflage et renouvellement d'air — serres, ateliers, cimenteries,
fonderies — même en environnement contraint.</p>""",
  cta='<a class="btn primary" href="/contact">Commander un ventilateur de gamme</a><a class="btn ghost-b" href="/telechargement">Simuler sur LiveCurve</a>',
  sections=[
    ("Comment choisir un ventilateur industriel standard adapté à vos besoins ?",
     ["Le choix repose sur quelques critères déterminants : le <b>type de ventilateur</b> (forme, configuration, sens de rotation des pales adaptés à l'application), le <b>diamètre de roue</b> (qui conditionne débit et pression), le point de fonctionnement visé et la nature du fluide véhiculé.",
      "Notre plateforme <a href=\"/telechargement\">LiveCurve</a> trace les courbes aérauliques de toute la gamme : saisissez débit et pression, comparez les modèles les plus performants, lisez le rendement en chaque point. Et nos technico-commerciaux valident la sélection avec vous."]),
    ("Secteurs d'application : ventilateurs industriels standards",
     ["Traitement d'air, séchage, dépoussiérage, extraction de fumées ou de vapeurs : les gammes standard équipent l'<a href=\"/secteurs-activite\">ensemble des secteurs industriels</a> — énergie, agroalimentaire, métallurgie, textile, chimie, papier-carton…",
      "Des modèles disponibles rapidement, au niveau de qualité éprouvé par 30&nbsp;000 ventilateurs produits chaque année."],
     ["53 séries","25 tailles","16 orientations","6 arrangements"]),
  ])

P["ventilateur-sur-mesure.html"] = dict(
  title="Fabrication de ventilateurs sur mesure près de Lyon",
  desc="35 ans d'ingénierie de ventilateurs sur mesure : aciers spéciaux, hautes températures, ATEX. Étude complète et devis détaillé sous 24 h.",
  h1="Conception et fabrication de ventilateurs industriels sur mesure à Lyon et dans toute la France",
  kicker="Nos produits — machines spéciales",
  ghost="Sur mesure",
  intro="""<p>Forts de <b>35 ans d'expérience</b> en fabrication et ingénierie de
ventilateurs, nous étudions chaque projet pour apporter une réponse technique
complète — et un <b>devis détaillé sous 24&nbsp;h</b>, pour tout ventilateur
standard ou sur mesure.</p>""",
  cta='<a class="btn primary" href="/contact">Décrire votre besoin</a><a class="btn ghost-b" href="/bureau-etudes">Le bureau d\'études</a>',
  sections=[
    ("Des ventilateurs industriels sur mesure afin de répondre à chaque besoin",
     ["Nos capacités de production couvrent de multiples aciers, plusieurs niveaux d'étanchéité et des températures très élevées, avec des exécutions conformes à la <b>directive ATEX</b>. Quand la gamme standard atteint ses limites, la machine spéciale prend le relais.",
      "Ces ventilateurs équipent notamment : verrerie, cimenterie, fours et usines d'incinération, traitement de surface, broyage, énergie, chimie, lits fluidisés."]),
    ("Les différents critères lors du choix de vos ventilateurs industriels",
     ["Débit, pression, température, nature et charge du fluide, niveau sonore admissible, implantation : chaque paramètre pèse sur le dimensionnement. Notre <a href=\"/bureau-etudes\">bureau d'études</a> analyse votre cahier des charges et vous propose la géométrie, les matériaux et l'arrangement adaptés.",
      "L'objectif ne varie pas : performance, efficacité énergétique et longévité de l'installation — documents de conformité à l'appui."],
     ["Aciers spéciaux","Hautes températures","ATEX","Étanchéité renforcée"]),
  ])

P["solutions-ventilateur-industriel.html"] = dict(
  title="Solutions sur mesure pour ventilation industrielle à Lyon",
  desc="Filtration, insonorisation, accessoires techniques : des solutions complètes pour optimiser efficacité, sécurité et confort de vos installations de ventilation.",
  h1="Solutions sur mesure pour ventilation industrielle et traitement de l'air près de Lyon",
  kicker="Solutions complètes — au-delà du ventilateur",
  ghost="Solutions",
  intro="""<p>Plus que des ventilateurs&nbsp;: des solutions complètes. Filtration,
insonorisation, réduction des vibrations, optimisation aéraulique — chaque
composant est pensé pour améliorer l'efficacité, la sécurité et le confort de vos
installations, dans les environnements industriels les plus exigeants.</p>""",
  cta='<a class="btn primary" href="/contact">Contactez-nous</a>',
  sections=[
    ("Caissons de filtration pour systèmes de ventilation industrielle",
     ["Nos <a href=\"/purificateur-air\">caissons de filtration statique</a> traitent jusqu'à <b>36&nbsp;000 m³/h</b> : particules, odeurs et polluants sont maîtrisés pour garantir un air conforme aux normes de sécurité et d'hygiène.",
      "Compacts, silencieux et faciles à entretenir, ils s'adaptent aux environnements à pollution modérée."]),
    ("Caissons d'insonorisation pour ventilateurs professionnels",
     ["Isolation de volute, caisson acoustique, capotage moteur : nos <a href=\"/caissons-insonorises\">habillages acoustiques</a> réduisent le bruit émis par les ventilateurs — pour les riverains comme pour les opérateurs.",
      "Chiffrage rapide sur transmission de vos éléments débit / pression."]),
    ("Une large gamme d'accessoires techniques pour ventilateurs industriels",
     ["Manchettes, contre-brides, registres, supports antivibratiles : tous les <a href=\"/nos-autres-accessoires\">accessoires</a> qui raccordent le ventilateur à votre installation et prolongent sa durée de vie."],
     ["Filtration 36 000 m³/h","Acoustique","Antivibratile","Raccordement"]),
  ])

P["caissons-insonorises.html"] = dict(
  title="Caissons d'insonorisation pour ventilateurs à Lyon",
  desc="Isolation de volute, caissons acoustiques, capotage moteur : réduisez le bruit de vos ventilateurs industriels. Chiffrage sous 24 h sur vos données débit/pression.",
  h1="Découvrez nos caissons d'insonorisation",
  kicker="Acoustique — pour ventilateurs, à Lyon et dans la France entière",
  ghost="Silence",
  intro="""<p>Sites industriels et habitations se rapprochent, et les conditions de
travail des opérateurs comptent autant que la production. Nos équipes ont développé
des solutions d'habillage acoustique — isolation de volute, caisson complet — pour
limiter le bruit émis par un ventilateur. Transmettez vos éléments débit et
pression&nbsp;: <b>chiffrage sous 24&nbsp;h</b>.</p>""",
  cta='<a class="btn primary" href="/contact">S\'équiper de caissons insonorisés</a>',
  sections=[
    ("Isolation de volutes ou de moteurs : limitez les volumes sonores",
     ["Sur tout modèle de la gamme, la volute peut recevoir une double peau en acier peint garnie de <b>laine de roche haute densité de 60 à 100&nbsp;mm</b>. Pour les atténuations plus fortes : habillage en laine de roche de <b>150&nbsp;mm</b> revêtu d'une tôle aluminium.",
      "Un capotage acoustique des moteurs électriques complète l'ensemble lorsque le niveau résiduel l'exige."]),
    ("Découvrez nos différents modèles de caissons acoustiques",
     ["Du simple habillage de volute au caisson acoustique complet, la solution se dimensionne selon l'atténuation recherchée, l'implantation et la maintenance prévue — en cohérence avec le <a href=\"/ventilateurs\">ventilateur</a> qu'elle équipe.",
      "Nos équipes vous conseillent sur le compromis performance acoustique / accessibilité / coût adapté à votre site."],
     ["Laine de roche 60–100 mm","Habillage 150 mm","Capotage moteur"]),
  ])

P["purificateur-air.html"] = dict(
  title="Systèmes de filtration ventilateurs industriels à Lyon - Filtres",
  desc="Caissons de filtration statique G4, F7, H13 ou charbon actif, jusqu'à 12 000 m³/h : un air d'atelier sain et conforme aux exigences de qualité et de sécurité.",
  h1="Optimisez la filtration de vos ventilateurs industriels",
  kicker="Filtration — un air plus sain, à Lyon et dans la France entière",
  ghost="Filtration",
  intro="""<p>Maintenir un air sain pour vos opérateurs est une exigence de l'industrie.
En complément des ventilateurs, nos <b>caissons de filtration statique</b> traitent
des débits jusqu'à <b>12&nbsp;000 m³/h</b>&nbsp;: préfiltration <b>G4</b>, filtration
<b>F7</b>, et si besoin un troisième niveau <b>H13 ou charbon actif</b> contre
poussières, odeurs et polluants.</p>""",
  cta='<a class="btn primary" href="/contact">S\'équiper en filtration</a>',
  sections=[
    ("Les caissons de filtration statiques conçus par notre équipe",
     ["Filtres à mailles, à fibres ou à plis retiennent les particules solides ou liquides de l'air aspiré ou soufflé par les <a href=\"/ventilateurs\">ventilateurs industriels</a>. Adaptés aux débits faibles à moyens et aux pollutions modérées, les caissons statiques s'installent, s'entretiennent et se remplacent facilement.",
      "Résultat : un air d'atelier conforme aux exigences de qualité et de sécurité, sans complexifier l'installation."]),
    ("Nos conseils pour bien choisir son ventilateur industriel",
     ["La filtration se dimensionne avec le ventilateur, pas après lui : la perte de charge des filtres entre dans le calcul du point de fonctionnement. Nos technico-commerciaux intègrent l'ensemble — ventilateur, caisson, accessoires — dans une même étude.",
      "Un doute sur le niveau de filtration requis ? Décrivez votre process : nous vous répondons sous 24&nbsp;h."],
     ["Préfiltration G4","Filtration F7","H13 / charbon actif","12 000 m³/h"]),
  ])

P["nos-autres-accessoires.html"] = dict(
  title="Accessoires pour tous types de ventilateurs industriels à Lyon",
  desc="Manchettes, contre-brides, registres, supports antivibratiles, caissons de filtration : tous les accessoires qui optimisent vos ventilateurs industriels.",
  h1="Nos différents accessoires pour ventilateurs industriels",
  kicker="Accessoires — à Lyon et dans toute la France",
  ghost="Accessoires",
  intro="""<p>Ventilation, refroidissement, chauffage, transport d'air&nbsp;: pour que
vos ventilateurs donnent leur pleine performance en sécurité, encore faut-il les
doter des accessoires adaptés à leur environnement. Euroventilatori France tient
un large stock d'accessoires pour ventilateurs industriels optimisés.</p>""",
  cta='<a class="btn primary" href="/contact">Contactez-nous</a>',
  sections=[
    ("Les caissons de filtration pour les ventilateurs : filtrez et dépolluez l'air !",
     ["Les caissons de filtration protègent machines, opérateurs et environnement des particules, poussières, fumées et odeurs. Selon le polluant à traiter : filtres à charbon actif, HEPA, électrostatiques ou purificateurs à ionisation — voir notre page <a href=\"/purificateur-air\">filtration</a>."]),
    ("Une large gamme d'accessoires adaptés aux systèmes de ventilation pour professionnels",
     ["Manchettes souples, contre-brides, registres de réglage, grilles de protection, supports antivibratiles : chaque accessoire fiabilise le raccordement du <a href=\"/ventilateurs\">ventilateur</a> à l'installation et prolonge sa durée de vie.",
      "Notre équipe vous aide à composer la nomenclature complète dès le devis — un seul interlocuteur, une seule livraison."],
     ["Manchettes","Contre-brides","Registres","Antivibratiles"]),
  ])

P["bureau-etudes.html"] = dict(
  title="Découvrez notre bureau d'études industrielles à Lyon",
  desc="CAO 2D/3D SolidWorks, certificats de vibration, d'équilibrage, spectres acoustiques, ErP 2015 : notre bureau d'études valide la faisabilité de votre projet.",
  h1="Notre bureau d'études industrielles",
  kicker="Ingénierie — disponible à Lyon, intervention dans toute la France",
  ghost="Études",
  intro="""<p>La qualité de nos machines repose sur l'implication quotidienne de nos
ingénieurs. Le bureau d'études conçoit des ventilateurs plus performants, plus
silencieux, plus résistants et moins énergivores — sur logiciels de CAO 2D et
3D <b>SolidWorks</b>.</p>""",
  cta='<a class="btn primary" href="/contact">Prenons rendez-vous</a>',
  sections=[
    ("Des ventilateurs industriels soumis à des analyses pour vous garantir leur qualité",
     ["Chaque machine peut être livrée avec ses comptes rendus : <b>certificat de vibration</b>, certificat matière, <b>certificat d'équilibrage</b>, spectre acoustique, attestation d'origine, dossier technique complet, certificat d'origine visé CCI et certificat <b>ErP 2015</b> (directive européenne 2009/125/CE).",
      "Des ventilateurs conformes aux normes en vigueur — et les documents qui le prouvent."]),
    ("Un produit et un process étudiés pour proposer les meilleurs délais de fabrication",
     ["Réactivité d'abord : plans d'implantation adaptés, modifications intégrées rapidement avec nouveau dimensionnement, production calée sur vos délais — c'est la flexibilité que nos clients saluent dans leurs <a href=\"/qui-sommes-nous\">témoignages</a>.",
      "De la faisabilité à la mise en service, un seul fil conducteur : votre cahier des charges."],
     ["SolidWorks 2D/3D","Certificats & essais","ErP 2015"]),
  ])

P["qui-sommes-nous.html"] = dict(
  title="Conception de ventilateurs industriels à Lyon - Euroventilatori France",
  desc="Groupe fondé en 1981, 30 000 ventilateurs/an, 28 000 m² de production : Euroventilatori France, référence européenne de la ventilation industrielle.",
  h1="Euroventilatori France — Conception et fabrication de ventilateurs industriels pour votre entreprise",
  kicker="Qui sommes-nous — depuis Lyon, dans toute la France",
  ghost="1981",
  intro="""<p>Fondée en <b>1981</b>, Euroventilatori Italie cultive plus de 40 ans
d'expérience dans les ventilateurs axiaux, centrifuges et spéciaux. Fort de ce
savoir-faire, Euroventilatori France s'impose comme une référence européenne de la
ventilation industrielle&nbsp;: jusqu'à <b>30&nbsp;000 ventilateurs par an</b>,
distribués dans le monde entier, sur près de <b>28&nbsp;000 m²</b> de production.</p>""",
  cta='<a class="btn primary" href="/contact">Notre équipe à votre service</a>',
  sections=[
    ("Ventilation industrielle : une équipe qualifiée pour tous vos besoins",
     ["<b>Pourquoi nous choisir ?</b> 35 ans d'expertise reconnue dans de nombreux domaines industriels, et une mission simple : fournir des solutions et des services réellement adaptés à chaque client, partout en France.",
      "<b>L'accompagnement d'abord.</b> Notre philosophie privilégie la proximité : réactivité, engagement de réponse rapide, suivi dans la durée. Un devis détaillé vous parvient sous 24&nbsp;h."]),
    ("Nos ventilateurs industriels pour tous les secteurs d'activité",
     ["Énergie, pétrochimie, agroalimentaire, métallurgie, textile, mais aussi papier-carton, verrerie, pharmacie : découvrez nos <a href=\"/secteurs-activite\">domaines d'application</a> et les <a href=\"/competences\">compétences</a> qui les servent."],
     ["Fondé en 1981","30 000 ventilateurs/an","28 000 m² de production","Devis sous 24 h"]),
  ])

P["secteurs-activite.html"] = dict(
  title="Les domaines d'application des ventilateurs industriels - Lyon",
  desc="Chimie, pétrochimie, cosmétique, ferroviaire, textile, agroalimentaire, énergie, métallurgie… nos ventilateurs équipent tous les secteurs industriels.",
  h1="Domaines d'application",
  kicker="Secteurs — intervention à Lyon et dans toute la France",
  ghost="Industrie",
  intro="""<p>Une entreprise industrielle produit de la richesse en transformant
matières premières et énergies — et cette transformation respire par ses
ventilateurs. Selon le secteur, elle est plus ou moins technique&nbsp;: à chaque
process son équipement.</p>""",
  cta='<a class="btn primary" href="/contact">Prenons rendez-vous</a>',
  sections=[
    ("Des ventilateurs industriels qui s'adaptent à votre activité",
     ["Chimie, pétrochimie, cosmétique, papier et carton, ferroviaire, aéronautique, textile, plasturgie, agroalimentaire, verrerie, énergie, métallurgie, pharmacie, bois, automobile, électronique et robotique : nos ventilateurs servent des applications variées — dont certaines n'ont rien à voir avec la qualité de l'air.",
      "Extraction de fumées, dépoussiérage, transport pneumatique, séchage, air de combustion, refroidissement de process : décrivez le vôtre, nous dimensionnons."]),
    ("Pourquoi les ventilateurs industriels sont-ils essentiels en entreprise ?",
     ["Parce qu'ils conditionnent à la fois la production (refroidissement, séchage, transport), la sécurité (extraction de fumées et de poussières, ATEX) et la santé des opérateurs (renouvellement et <a href=\"/purificateur-air\">filtration de l'air</a>).",
      "Un dimensionnement juste, c'est un process fiable et une facture énergétique maîtrisée — le cœur de notre <a href=\"/competences\">savoir-faire</a>."],
     ["Pétrochimie","Agroalimentaire","Métallurgie","Textile","Ferroviaire","Verrerie"]),
  ])

P["competences.html"] = dict(
  title="Notre savoir-faire en ventilateurs industriels à Lyon",
  desc="Conception, dimensionnement, essais, mise en service et suivi : la maîtrise globale d'Euroventilatori France pour vos ventilateurs industriels.",
  h1="Découvrez le savoir-faire d'Euroventilatori, conception de ventilateurs industriels pour votre entreprise",
  kicker="Compétences — à Lyon et partout en France",
  ghost="Mesure",
  intro="""<p>Nos gammes évoluent en permanence pour suivre les exigences de chaque
secteur. À partir de votre cahier des charges, nos technico-commerciaux vous
accompagnent vers le bon ventilateur — et notre maîtrise de toutes les étapes,
du conseil à la mise en service, garantit la qualité de l'équipement comme du
service.</p>""",
  cta='<a class="btn primary" href="/contact">Contacter nos experts</a>',
  sections=[
    ("La conception et le dimensionnement des ventilateurs industriels",
     ["Le <a href=\"/bureau-etudes\">bureau d'études</a> concrétise vos projets spécifiques : solutions sur mesure adaptées à chaque configuration, avec un triple objectif — performance, efficacité énergétique, longévité.",
      "Nous concevons aussi les périphériques d'intégration : raccordements, silencieux, caissons insonorisés, isolation de carcasse."]),
    ("Une équipe expérimentée pour la réalisation de vos ventilateurs industriels",
     ["Leader par les chiffres, reconnu pour l'accompagnement : des technico-commerciaux qui parlent votre process, des délais tenus, et un suivi qui ne s'arrête pas à la livraison."]),
    ("Centre d'essai dédié aux contrôles qualité et à la validation technique",
     ["Essais aérauliques et acoustiques, équilibrage, contrôles vibratoires : chaque machine peut être validée sur banc avant expédition, certificats à l'appui — la traçabilité complète décrite sur la page <a href=\"/bureau-etudes\">bureau d'études</a>."],
     ["Dimensionnement","Essais sur banc","Mise en service","Suivi"]),
  ])

P["telechargement.html"] = dict(
  title="Fiches techniques, LiveCurve pour ventilateurs | Euroventilatori",
  desc="LiveCurve : la simulation interactive des courbes aérauliques de toute la gamme Euroventilatori. Catalogue, plaquettes et fiches techniques à télécharger.",
  h1="Découvrez LiveCurve, développé par Euroventilatori",
  kicker="Ressources — simulation et documentation",
  ghost="LiveCurve",
  intro="""<p>La meilleure simulation du marché pour les courbes aérauliques et les
informations ErP 2013–2015 de notre gamme. <b>LiveCurve</b> est personnalisable —
saisissez pression et débit, la plateforme liste les modèles les plus performants
sur un graphique — et interactif&nbsp;: déplacez-vous dans la courbe et lisez le
rendement selon débit, pression et température du fluide.</p>""",
  cta='<a class="btn primary" href="/contact">Être accompagné sur une sélection</a>',
  sections=[
    ("Télécharger votre documentation",
     ["<b>Catalogue général</b> — l'ensemble des 53 séries et leurs caractéristiques. <i>(lien à brancher)</i>",
      "<b>Liste des accessoires disponibles</b> — raccordement, acoustique, filtration. <i>(lien à brancher)</i>",
      "<b>Plaquette commerciale</b> — l'entreprise et l'offre en un document. <i>(lien à brancher)</i>",
      "<b>Caisson filtre</b> — documentation filtration statique. <i>(lien à brancher)</i>"]),
  ])

P["contact.html"] = dict(
  title="Demandez votre devis  et contactez Euroventilatori France à Lyon",
  desc="Ventilateur industriel, pièce détachée, accessoire : contactez nos experts. Devis transmis sous 24 h selon les éléments fournis. 04 74 43 68 38.",
  h1="Contactez Euroventilatori pour tout achat de ventilateurs industriels et solutions acoustiques",
  kicker="Contact — à Lyon et dans toute la France",
  ghost="Contact",
  intro="""<p>Centrifuges ou hélicoïdaux, basse, moyenne ou haute pression&nbsp;:
aération, aspiration, refroidissement, séchage ou climatisation, nos équipements
couvrent les environnements les plus exigeants. Notre engagement&nbsp;: vous
conseiller rapidement et transmettre un <b>devis sous 24&nbsp;h</b> selon les
éléments fournis.</p>""",
  cta='<a class="btn primary" href="tel:0474436838">04 74 43 68 38</a><a class="btn ghost-b" href="mailto:contact@euroventilatori-france.com">contact@euroventilatori-france.com</a>',
  sections=[
    ("Demandez votre devis pour votre projet de ventilateur en complétant notre formulaire",
     ["<b>Euroventilatori France</b> — 150 Rue du Vernay, 38300 Nivolas-Vermelle.",
      "Décrivez votre besoin — débit, pression, fluide, contraintes du site — par téléphone au <a href=\"tel:0474436838\">04&nbsp;74&nbsp;43&nbsp;68&nbsp;38</a> ou par e-mail à <a href=\"mailto:contact@euroventilatori-france.com\">contact@euroventilatori-france.com</a>. Nos spécialistes dimensionnent, chiffrent et vous rappellent.",
      "<i>Le formulaire en ligne sera branché à la mise en production (fonction Cloudflare + Brevo).</i>"]),
  ])

P["actualites.html"] = dict(
  title="Actualités d'Euroventilatori France — ventilateurs industriels",
  desc="Réalisations, nouveautés produits, vie de l'entreprise et informations pratiques : suivez l'actualité d'Euroventilatori France, constructeur de ventilateurs industriels.",
  h1="Nos actualités",
  kicker="Le journal de l'entreprise",
  ghost="Actualités",
  intro="""<p>Réalisations marquantes, nouveautés de gamme, arrivées dans
l'équipe et informations pratiques : ce qui se passe chez Euroventilatori
France, mois après mois.</p>""",
  cta='<a class="btn primary" href="/contact">Nous contacter</a>'
      '<a class="btn ghost-b" href="/ventilateurs">Voir nos produits</a>',
  sections=[],
  liste_articles=True)


# ===========================================================================
# PAGES PRODUITS ET LOCALES — memes URL que le site actuel, contenu original.
# ===========================================================================

P["ventilateurs-centrifuges.html"] = dict(
  title="Ventilateurs centrifuges industriels — achat et conseil | Euroventilatori",
  desc="Ventilateurs centrifuges basse, moyenne et haute pression : choisir le bon type de roue, le bon débit et la bonne pression avec nos ingénieurs. Devis sous 24 h.",
  h1="Choisissez votre ventilateur centrifuge industriel avec nos ingénieurs",
  kicker="Nos produits — ventilateurs centrifuges",
  ghost="Centrifuge",
  intro="""<p>Un ventilateur centrifuge aspire l'air dans l'axe de sa roue et le
refoule à 90°, dans une volute. Cette géométrie lui permet de <b>vaincre des
pertes de charge élevées</b> : filtres encrassés, longs réseaux de gaines,
cyclones, manches filtrantes. C'est la machine du dépoussiérage, de l'extraction
de fumées et du transport pneumatique — partout où l'air doit être poussé fort,
et pas seulement déplacé.</p>""",
  cta='<a class="btn primary" href="/contact">Demander un devis</a><a class="btn ghost-b" href="/telechargement">Simuler sur LiveCurve</a>',
  sections=[
    ("Comment choisir son type de ventilateur ? Pour quel débit d'air ?",
     ["Tout part de deux grandeurs, et elles ne se négocient pas : le <b>débit</b> (en m³/h) que votre process réclame, et la <b>pression statique</b> (en Pa) que le réseau lui oppose. Ce couple détermine à lui seul la famille de machine ; les matériaux, l'orientation et l'arrangement viennent ensuite.",
      "La forme des aubes fait le second tri. Les <b>aubes recourbées vers l'arrière</b> offrent le meilleur rendement et une courbe stable : c'est le choix par défaut quand l'air est propre. Les <b>aubes radiales</b> encaissent les fluides chargés, poussiéreux ou abrasifs sans s'encrasser, au prix de quelques points de rendement. Les <b>aubes vers l'avant</b> délivrent beaucoup de débit sous faible pression, dans un encombrement réduit.",
      "Le diamètre de roue et la vitesse de rotation ajustent enfin le point de fonctionnement. Un même besoin se couvre par une grande roue lente — silencieuse et économe — ou par une petite roue rapide, plus compacte mais plus bruyante et plus gourmande. Ce choix engage votre facture d'électricité sur quinze ans : c'est là que le conseil se paie.",
      "Notre plateforme <a href=\"/telechargement\">LiveCurve</a> trace les courbes de toute la gamme et affiche le rendement en chaque point. Elle oriente ; nos technico-commerciaux confirment."]),
    ("Ventilateur centrifuge moyenne pression, quelles utilisations ?",
     ["La moyenne pression, entre 2 000 et 6 000 Pa environ, couvre l'essentiel des besoins industriels : <b>dépoussiérage</b> d'atelier, aspiration de copeaux en menuiserie, extraction de vapeurs en agroalimentaire, ventilation de cabines de peinture, séchage.",
      "C'est aussi la plage où le rendement pèse le plus lourd, parce que ces machines tournent en continu. Dix points de rendement sur un ventilateur de 30 kW fonctionnant 6 000 heures par an représentent plusieurs milliers d'euros d'électricité chaque année. Nous dimensionnons donc au point de fonctionnement réel, pas au catalogue.",
      "Ces machines se déclinent en acier peint, galvanisé ou inox selon le fluide véhiculé, et acceptent tous les arrangements courants : accouplement direct, transmission par courroies, moteur déporté lorsque la température l'impose."],
     ["Dépoussiérage", "Extraction de fumées", "Séchage", "Cabines de peinture"]),
    ("Votre ventilateur centrifuge haute pression sur mesure",
     ["Au-delà de 6 000 Pa, on quitte le catalogue. Transport pneumatique de granulés, de farines ou de copeaux, aspiration sur cyclone, tirage de four : ces applications réclament des roues épaisses, des jeux maîtrisés et souvent des matériaux particuliers.",
      "Notre <a href=\"/bureau-etudes\">bureau d'études</a> dimensionne alors la machine autour de votre cahier des charges : <b>hautes températures</b> jusqu'aux fumées de four, <b>aciers inoxydables</b> pour les ambiances corrosives ou l'agroalimentaire, revêtements anti-abrasion, conformité <b>ATEX</b> lorsque l'atmosphère est explosible.",
      "Le principe ne change pas selon le niveau de pression : partir du besoin réel, choisir le rendement avant le prix catalogue, et vérifier le niveau sonore avant l'installation — pas après."],
     ["Transport pneumatique", "Haute température", "Inox", "ATEX", "Anti-abrasion"]),
  ])

P["ventilateurs-helicoides.html"] = dict(
  title="Ventilateurs hélicoïdes et axiaux industriels | Euroventilatori",
  desc="Ventilateurs hélicoïdes pour de grands débits d'air sous faible pression : ateliers, entrepôts, serres, élevages. Faible niveau sonore, versions galvanisées et inox.",
  h1="Votre ventilateur hélicoïde, dimensionné à votre volume",
  kicker="Nos produits — ventilateurs hélicoïdes",
  ghost="Hélicoïde",
  intro="""<p>Le ventilateur hélicoïde — ou axial — déplace l'air <b>dans l'axe de
son hélice</b>, sans le dévier. Là où le centrifuge pousse fort contre un réseau,
l'hélicoïde déplace <b>beaucoup d'air sous faible pression</b> : renouveler
l'atmosphère d'un atelier, ventiler un entrepôt, une serre ou un bâtiment
d'élevage, refroidir un échangeur.</p>""",
  cta='<a class="btn primary" href="/contact">Décrire votre besoin</a><a class="btn ghost-b" href="/ventilateurs-centrifuges">Voir les centrifuges</a>',
  sections=[
    ("Un niveau sonore très faible pour le confort de vos opérateurs",
     ["Le bruit d'un ventilateur ne vient pas d'abord de sa puissance, mais de la <b>vitesse de l'air en bout de pale</b>. À débit égal, une grande hélice tournant lentement est nettement plus silencieuse qu'une petite hélice rapide — et consomme moins.",
      "Nous intégrons donc le niveau sonore dès la sélection, et non comme correctif. Quand l'ambiance l'exige, l'appareil se complète d'un <a href=\"/caissons-insonorises\">caisson d'insonorisation</a> ou de silencieux placés à l'aspiration et au refoulement.",
      "Sur les postes occupés en permanence, quelques décibels changent le quotidien des équipes. C'est une donnée d'exploitation autant qu'une donnée technique : elle mérite de figurer dans le cahier des charges."]),
    ("Une solution qui s'intègre à vos systèmes de ventilation",
     ["Les hélicoïdes s'installent en <b>montage mural</b>, en <b>virole</b> pour raccordement à une gaine, ou en <b>tourelle de toiture</b> pour l'extraction. Chaque configuration a ses contraintes d'implantation, d'étanchéité et de maintenance : autant les traiter pendant l'étude.",
      "Autour de l'appareil, l'offre couvre ce qui fait qu'une installation tient dans la durée : <a href=\"/nos-autres-accessoires\">manchettes souples</a> contre la transmission des vibrations, grilles de protection, registres, supports antivibratiles.",
      "Notre bureau d'études valide l'implantation sur vos plans avant fabrication. C'est le bon moment pour découvrir un conflit d'encombrement — pas le jour de la livraison."]),
    ("Quel débit atteindre avec un ventilateur axial galvanisé ?",
     ["Le débit se déduit du volume à traiter et du nombre de renouvellements d'air visés par heure. Un atelier de mécanique, un entrepôt logistique et un bâtiment d'élevage n'ont ni les mêmes besoins ni les mêmes contraintes réglementaires.",
      "Le <b>traitement de surface</b> se choisit selon l'ambiance : acier peint en intérieur sec, <b>galvanisation à chaud</b> en extérieur ou en atmosphère humide, inox en agroalimentaire et en milieu corrosif. Nos procédés sont détaillés sur la page <a href=\"/traitement-surface\">traitement de surface</a>.",
      "Donnez-nous le volume, l'usage et l'environnement : nous vous renvoyons une sélection chiffrée, avec la puissance absorbée et le niveau sonore attendu."],
     ["Mural", "Virole", "Tourelle de toiture", "Galvanisé", "Inox"]),
  ])

P["traitement-surface.html"] = dict(
  title="Traitement de surface des ventilateurs industriels | Euroventilatori",
  desc="Galvanisation à chaud, métallisation, peinture RAL 7038 ou construction inox : le traitement de surface qui protège durablement votre ventilateur industriel.",
  h1="Nos techniques de traitement de surface des métaux",
  kicker="Fabrication — protection des matériaux",
  ghost="Surface",
  intro="""<p>Un ventilateur industriel vit dans l'humidité, la poussière, la
chaleur, parfois les vapeurs corrosives. Sa <b>durée de vie se joue autant sur sa
protection de surface que sur sa mécanique</b>. Selon l'ambiance de votre site,
nous protégeons les machines par peinture, galvanisation ou métallisation — ou
nous les construisons directement en acier inoxydable.</p>""",
  cta='<a class="btn primary" href="/contact">Décrire votre environnement</a><a class="btn ghost-b" href="/ventilateur-sur-mesure">Le sur-mesure</a>',
  sections=[
    ("La galvanisation à chaud, un procédé emprunté à la métallurgie",
     ["La pièce est immergée dans un bain de zinc en fusion : le zinc s'allie à l'acier et forme un revêtement qui protège <b>de l'intérieur comme de l'extérieur</b>, y compris dans les recoins qu'une peinture n'atteindrait jamais.",
      "Sa protection est dite sacrificielle — le zinc se consomme avant l'acier et continue de protéger même en cas de rayure. C'est le traitement de référence pour les installations <b>extérieures</b>, les toitures et les ambiances humides.",
      "Sa limite tient à la température du bain : les pièces de grandes dimensions ou de géométrie complexe demandent une étude préalable pour écarter tout risque de déformation. Nous la menons avant lancement."]),
    ("La métallisation, un procédé qui fait ses preuves durablement",
     ["La métallisation projette au pistolet du métal en fusion — zinc ou alliage zinc-aluminium — sur une surface préalablement sablée. À la différence de la galvanisation, elle <b>ne chauffe pas la pièce</b> : aucune déformation à craindre, quelles que soient les dimensions.",
      "Elle convient donc aux grandes volutes, aux carters et aux ensembles soudés qui ne passeraient pas au bain. Associée à une peinture de finition, elle offre une protection de très longue durée en ambiance industrielle sévère.",
      "C'est également la solution retenue lorsqu'une pièce doit être reprotégée après réparation ou modification sur site."]),
    ("Peinture, RAL 7038 et constructions inox",
     ["Nos machines de série reçoivent une peinture industrielle dans notre teinte de référence, le <b>RAL 7038</b>, qui a remplacé le gris standard historique. Toute autre teinte du nuancier reste possible : certains clients alignent leurs ventilateurs sur la charte de leur usine.",
      "Quand le fluide véhiculé est corrosif ou chargé en vapeurs acides, et quand l'hygiène l'impose — <b>agroalimentaire</b>, pharmacie, chimie — la peinture ne suffit plus : la machine est alors construite en <b>acier inoxydable</b>, roue comprise.",
      "Le bon traitement n'est pas le plus protecteur dans l'absolu, mais celui qui correspond à votre ambiance réelle. Décrivez-nous le milieu — température, humidité, nature des vapeurs, présence de sel ou de produits de lavage — et nous vous dirons ce qui tiendra."],
     ["Galvanisation à chaud", "Métallisation", "RAL 7038", "Inox", "Teintes sur demande"]),
  ])


# --- Pages locales ---------------------------------------------------------
# Le site actuel decline quatre fois les memes huit titres. Google traite ce
# schema comme des pages satellites. Chaque page est donc ancree ici dans les
# industries reellement presentes sur son territoire.

P["ile-de-france-rhone-alpes.html"] = dict(
  title="Ventilateurs industriels en Rhône-Alpes — fabricant en Isère | Euroventilatori",
  desc="Notre atelier est en Isère : ventilateurs industriels pour la chimie, la plasturgie et l'agroalimentaire de Rhône-Alpes. Intervention rapide, devis sous 24 h.",
  h1="Ventilateurs industriels en Rhône-Alpes : votre fabricant est à moins d'une heure",
  kicker="Rhône-Alpes — notre territoire",
  ghost="Rhône-Alpes",
  intro="""<p>Notre site est implanté à <b>Nivolas-Vermelle, en Isère</b>. Pour les
industriels de Lyon, Grenoble, Chambéry, Saint-Étienne ou Valence, cela change
tout : une visite technique se programme dans la journée, un relevé sur site ne
demande pas de déplacement lointain, et une pièce urgente peut être retirée
directement à l'atelier.</p>""",
  cta='<a class="btn primary" href="/contact">Prendre rendez-vous</a><a class="btn ghost-b" href="/bureau-etudes">Le bureau d\'études</a>',
  sections=[
    ("Les industries de Rhône-Alpes et leurs contraintes d'air",
     ["La <b>vallée de la chimie</b>, au sud de Lyon, impose ce que l'aéraulique a de plus exigeant : vapeurs agressives, zones classées <b>ATEX</b>, matériaux inoxydables ou revêtus, traçabilité des interventions. Nous y déployons des machines construites pour l'ambiance, pas adaptées après coup.",
      "La <b>plasturgie</b> du Haut-Bugey et de la vallée de l'Arve demande d'extraire fumées de fusion et vapeurs de solvants au plus près des presses, sans dégrader le climat de l'atelier. La <b>métallurgie</b> et le décolletage ajoutent brouillards d'huile et copeaux — des fluides chargés qui appellent des roues radiales et des traitements anti-abrasion.",
      "L'<b>agroalimentaire</b> régional, de la Drôme à la Savoie, réclame lavabilité, inox et maîtrise des odeurs. Chaque filière a sa contrainte dominante ; c'est elle qui commande la sélection, bien avant le prix catalogue."]),
    ("Une proximité qui se mesure en heures, pas en semaines",
     ["Être fabricant et voisin change la nature de la relation. Un technicien peut venir relever un point de fonctionnement réel plutôt que de travailler sur des données déclarées — et l'écart entre les deux explique bien des installations décevantes.",
      "En cas d'arrêt de production, cette proximité devient décisive : le diagnostic se fait sur place, et la remise en service ne dépend pas d'une chaîne logistique. Nos <a href=\"/nos-autres-accessoires\">accessoires</a> et pièces courantes sont disponibles depuis l'atelier.",
      "Nous intervenons bien sûr dans toute la France ; mais en Rhône-Alpes, la distance cesse d'être un paramètre."]),
    ("Du relevé sur site à la mise en service",
     ["Notre <a href=\"/bureau-etudes\">bureau d'études</a> part de votre installation existante : débit réellement obtenu, pression du réseau, encombrement disponible, contraintes d'accès et niveau sonore admissible.",
      "La sélection se fait ensuite sur le <b>rendement au point de fonctionnement</b>, pas sur la puissance nominale : c'est ce qui détermine votre consommation pendant toute la vie de la machine. Le devis détaillé suit sous 24 h.",
      "Vous cherchez un <a href=\"/ventilateurs-centrifuges\">centrifuge</a> pour un dépoussiérage, un <a href=\"/ventilateurs-helicoides\">hélicoïde</a> pour renouveler l'air d'un atelier, ou une machine entièrement <a href=\"/ventilateur-sur-mesure\">sur mesure</a> : le point de départ est le même — vos chiffres réels."],
     ["Chimie", "Plasturgie", "Décolletage", "Agroalimentaire", "ATEX"]),
  ])

P["paris.html"] = dict(
  title="Ventilateurs industriels à Paris et en Île-de-France | Euroventilatori",
  desc="Ventilateurs industriels pour l'Île-de-France : contraintes de bruit en zone dense, accès difficiles, ICPE. Étude, fabrication et livraison depuis notre atelier.",
  h1="Ventilateurs industriels à Paris et en Île-de-France",
  kicker="Île-de-France — zone dense",
  ghost="Paris",
  intro="""<p>Ventiler en Île-de-France, c'est composer avec une contrainte que
les autres régions connaissent moins : la <b>proximité immédiate des riverains</b>.
Un atelier, une blanchisserie industrielle ou une cuisine centrale y sont souvent
mitoyens de logements. Le niveau sonore et l'implantation deviennent alors des
données de conception, pas des détails de finition.</p>""",
  cta='<a class="btn primary" href="/contact">Demander une étude</a><a class="btn ghost-b" href="/caissons-insonorises">Solutions acoustiques</a>',
  sections=[
    ("Le bruit, première contrainte de la zone dense",
     ["En tissu urbain, l'émergence sonore admissible est faible et contrôlée. Une machine correctement dimensionnée mais mal implantée peut suffire à déclencher une plainte de voisinage — et l'arrêt d'une installation neuve.",
      "Nous traitons donc l'acoustique dès la sélection : grande roue tournant lentement plutôt que petite roue rapide, <a href=\"/caissons-insonorises\">caisson d'insonorisation</a>, silencieux à l'aspiration et au refoulement, plots antivibratiles pour ne pas transmettre les vibrations à la structure du bâtiment.",
      "Cette approche coûte moins cher menée en amont qu'en correctif, une fois la machine installée et la plainte déposée."]),
    ("Des accès et des encombrements hors normes",
     ["Toitures encombrées, locaux techniques en sous-sol, passages d'ascenseur, rues étroites, créneaux de livraison limités : en Île-de-France, la machine doit souvent entrer par un passage qui n'était pas prévu pour elle.",
      "Notre bureau d'études travaille sur vos plans avant fabrication et adapte les dimensions, l'orientation de la volute et l'arrangement moteur à ce qui est réellement praticable. Une machine livrable en éléments assemblables sur place est parfois la seule solution — nous la prévoyons dès l'étude.",
      "C'est aussi le moment de vérifier les accès de maintenance : un ventilateur sur lequel on ne peut pas intervenir devient un problème dès la première panne."]),
    ("Tertiaire, agroalimentaire, imprimerie : des besoins variés",
     ["L'Île-de-France concentre des activités très différentes : cuisines centrales et laboratoires agroalimentaires, blanchisseries industrielles, imprimeries, ateliers de mécanique, laboratoires pharmaceutiques et cosmétiques, sites logistiques.",
      "Chacune appelle une réponse propre : extraction de vapeurs grasses et lavabilité pour l'agroalimentaire, gestion de la chaleur et de l'humidité en blanchisserie, captation de solvants en imprimerie, <a href=\"/purificateur-air\">filtration</a> soignée en laboratoire.",
      "Nous livrons dans toute l'Île-de-France depuis notre atelier, avec le même engagement de <b>devis détaillé sous 24 h</b> qu'ailleurs en France."],
     ["Acoustique renforcée", "Accès contraints", "Agroalimentaire", "Blanchisserie", "Imprimerie"]),
  ])

P["lille.html"] = dict(
  title="Ventilateurs industriels à Lille et dans les Hauts-de-France | Euroventilatori",
  desc="Ventilateurs industriels pour les Hauts-de-France : agroalimentaire, métallurgie, textile, papier-carton. Dépoussiérage, extraction de fumées, devis sous 24 h.",
  h1="Ventilateurs industriels à Lille et dans les Hauts-de-France",
  kicker="Hauts-de-France — industrie lourde et agroalimentaire",
  ghost="Lille",
  intro="""<p>Les Hauts-de-France conservent un tissu industriel dense et
diversifié : <b>agroalimentaire</b> de premier plan, métallurgie, papier-carton,
héritage textile, ferroviaire et logistique. Autant de process qui produisent
poussières, fibres, fumées ou vapeurs — et qui ont besoin d'un air maîtrisé pour
tourner sans arrêt.</p>""",
  cta='<a class="btn primary" href="/contact">Demander un devis</a><a class="btn ghost-b" href="/secteurs-activite">Voir les secteurs</a>',
  sections=[
    ("Agroalimentaire : hygiène, humidité et maîtrise des odeurs",
     ["La région compte parmi les premiers bassins agroalimentaires français. Légumes, féculerie, sucrerie, produits laitiers, boulangerie industrielle : ces process combinent <b>humidité</b>, <b>vapeurs grasses</b> et exigences d'hygiène strictes.",
      "La réponse tient dans le matériau autant que dans l'aéraulique : construction <b>inox</b>, surfaces lavables, absence de rétention. Nos procédés de protection sont détaillés sur la page <a href=\"/traitement-surface\">traitement de surface</a>.",
      "S'y ajoute la question des odeurs, souvent sensible quand le site est proche d'habitations : elle se traite par la <a href=\"/purificateur-air\">filtration</a> et par le dimensionnement du rejet, pas par le seul débit."]),
    ("Métallurgie, papier-carton, textile : des fluides chargés",
     ["Fumées de soudure, poussières de meulage, particules abrasives, fibres textiles, poussières de carton : ces fluides encrassent et usent les machines conçues pour de l'air propre.",
      "Ils appellent des <a href=\"/ventilateurs-centrifuges\">ventilateurs centrifuges</a> à <b>aubes radiales</b>, qui ne se colmatent pas, et des traitements anti-abrasion. Le transport pneumatique de chutes et de copeaux relève du même registre : haute pression, roue robuste, maintenance pensée dès l'origine.",
      "Sur les installations existantes, un relevé du point de fonctionnement réel révèle souvent qu'une machine sous-dimensionnée tourne en surrégime depuis des années — et coûte plus cher en électricité que son remplacement."]),
    ("Une intervention dans toute la région, sans surcoût de distance",
     ["De Lille à Amiens, de Dunkerque à Valenciennes, nous livrons et accompagnons dans les mêmes conditions que partout en France : étude par notre <a href=\"/bureau-etudes\">bureau d'études</a>, fabrication dans notre atelier, <b>devis détaillé sous 24 h</b>.",
      "Nos technico-commerciaux prennent le besoin par les chiffres — débit, pression, nature du fluide, contraintes du site — puis proposent la solution au meilleur rendement, pas la plus chère ni la plus rapide à sortir du catalogue.",
      "Pour les projets neufs comme pour le remplacement d'une machine en place, le point de départ reste le même : ce que fait réellement votre installation aujourd'hui."],
     ["Agroalimentaire", "Métallurgie", "Papier-carton", "Textile", "Dépoussiérage"]),
  ])

P["bretagne.html"] = dict(
  title="Ventilateurs industriels en Bretagne — agroalimentaire et élevage | Euroventilatori",
  desc="Ventilateurs industriels pour la Bretagne : agroalimentaire, élevage, séchage et stockage céréalier. Inox, résistance à la corrosion saline, devis sous 24 h.",
  h1="Ventilateurs industriels en Bretagne",
  kicker="Bretagne — agroalimentaire et agriculture",
  ghost="Bretagne",
  intro="""<p>La Bretagne est la première région agroalimentaire française.
Abattoirs et ateliers de découpe, laiteries, conserveries, biscuiteries, bâtiments
d'élevage, silos et séchoirs à céréales : les besoins d'air y sont massifs et
particulièrement exigeants, entre <b>hygiène</b>, <b>humidité</b> et
<b>corrosion</b>.</p>""",
  cta='<a class="btn primary" href="/contact">Demander un devis</a><a class="btn ghost-b" href="/ventilateur-sur-mesure">Machines spéciales</a>',
  sections=[
    ("Agroalimentaire : l'inox comme point de départ",
     ["En atelier de découpe, en laiterie ou en conserverie, la machine est lavée, parfois plusieurs fois par jour, avec des produits alcalins ou chlorés. Un acier peint n'y tient pas dans la durée.",
      "La construction en <b>acier inoxydable</b>, roue comprise, devient alors la base plutôt que l'option. S'y ajoutent des exigences de conception : surfaces lisses, absence de rétention, démontabilité pour le nettoyage.",
      "L'extraction de vapeurs et le contrôle de l'humidité relèvent du même dimensionnement : trop peu de débit et la condensation s'installe ; trop et l'on chauffe l'extérieur. Le bon point se calcule."]),
    ("Élevage, séchage et stockage : de gros volumes à faible pression",
     ["Les bâtiments d'élevage et le séchage de céréales demandent de <b>très grands débits sous faible pression</b> : c'est le domaine des <a href=\"/ventilateurs-helicoides\">ventilateurs hélicoïdes</a>, en montage mural ou en tourelle.",
      "La ventilation des <b>silos</b> obéit à une logique différente : elle conditionne la conservation du grain après la récolte, et une insuffisance de débit se paie en qualité de lot plusieurs mois plus tard. Le dimensionnement se fait sur la hauteur de grain et le volume stocké.",
      "Dans ces ambiances chargées en poussières végétales et en ammoniac, le traitement de surface fait la durée de vie : <b>galvanisation à chaud</b> pour l'extérieur, inox pour les milieux les plus agressifs."]),
    ("Corrosion saline et proximité du littoral",
     ["Sur une large part du territoire breton, l'air marin ajoute une contrainte que l'intérieur des terres ignore : le <b>sel accélère la corrosion</b>, en particulier sur les machines installées en toiture ou en extérieur.",
      "Nous en tenons compte dans la protection retenue — galvanisation, métallisation ou inox selon l'exposition — et dans le choix de la visserie. Le détail paraît mineur ; il décide pourtant de la tenue à dix ans.",
      "Décrivez-nous l'implantation, l'ambiance et le fluide véhiculé : notre <a href=\"/bureau-etudes\">bureau d'études</a> vous renvoie une solution chiffrée sous 24 h, livrable dans toute la Bretagne."],
     ["Inox alimentaire", "Élevage", "Séchage céréalier", "Silos", "Corrosion saline"]),
  ])


# --- Sections complementaires et questions frequentes ----------------------

P["ventilateurs-centrifuges.html"]["sections"] += [
  ("Remplacer un ventilateur centrifuge existant",
   ["Un remplacement à l'identique est rarement le bon réflexe. La machine en place a souvent été dimensionnée pour une installation qui a changé depuis : gaines ajoutées, filtre plus fin, débit revu. Le relevé du <b>point de fonctionnement réel</b> révèle fréquemment un écart de 20 à 30 % avec la plaque signalétique.",
    "Nous relevons donc débit et pression sur site avant de proposer quoi que ce soit, puis nous vérifions l'encombrement, le sens de rotation, l'orientation de la volute et le type d'accouplement. Une machine plus performante mais impossible à raccorder ne rend service à personne.",
    "Ce diagnostic est aussi l'occasion de reprendre l'entraînement : un ventilateur maintenu à débit constant par un registre partiellement fermé gaspille en permanence — un variateur de fréquence rembourse cet écart en quelques saisons."]),
  ("Consommation, rendement et coût d'exploitation",
   ["La puissance absorbée suit la relation <b>P = Q × Δp / η</b> : le débit multiplié par la pression, divisé par le rendement. Deux machines délivrant le même service peuvent donc consommer très différemment selon leur rendement au point d'usage.",
    "Sur une machine qui tourne en continu, l'électricité représente l'essentiel du coût de possession — bien davantage que le prix d'achat. C'est la raison pour laquelle nous affichons le rendement dès la présélection plutôt que de le réserver à la fiche technique.",
    "Les lois des ventilateurs expliquent l'ampleur du gain : réduire la vitesse de 20 % divise la puissance absorbée par deux environ. Adapter le régime au besoin réel est le levier d'économie le plus rentable d'une installation aéraulique."]),
]
P["ventilateurs-centrifuges.html"]["faq"] = [
  ("Quelle différence entre un ventilateur centrifuge et un hélicoïde ?",
   "Un ventilateur centrifuge dévie l'air à 90° dans une volute, ce qui lui permet de vaincre de fortes pertes de charge : réseaux de gaines, filtres, cyclones. Un ventilateur hélicoïde pousse l'air dans l'axe de son hélice et déplace de grands volumes sous faible pression, comme le renouvellement d'air d'un atelier."),
  ("Comment choisir entre aubes vers l'avant, radiales et vers l'arrière ?",
   "Les aubes recourbées vers l'arrière offrent le meilleur rendement et conviennent à l'air propre. Les aubes radiales résistent aux fluides chargés, poussiéreux ou abrasifs sans s'encrasser. Les aubes vers l'avant donnent beaucoup de débit sous faible pression dans un encombrement réduit."),
  ("Quelle pression un ventilateur centrifuge peut-il atteindre ?",
   "Les gammes standard se répartissent en basse pression jusqu'à environ 2 000 Pa, moyenne pression de 2 000 à 6 000 Pa, et haute pression au-delà. Le transport pneumatique et l'aspiration sur cyclone relèvent généralement de la haute pression."),
  ("Un ventilateur centrifuge peut-il être installé en zone ATEX ?",
   "Oui. Une machine destinée à une atmosphère explosible est conçue pour cela dès l'origine : matériaux anti-étincelants, jeux maîtrisés, moteur certifié et marquage correspondant à la zone. C'est une conception spécifique, jamais une adaptation d'un modèle standard."),
  ("Quel délai pour obtenir un devis ?",
   "Euroventilatori France s'engage sur un devis détaillé sous 24 heures, pour un ventilateur de gamme comme pour une machine sur mesure, dès lors que le débit, la pression et la nature du fluide sont connus."),
]

P["ventilateurs-helicoides.html"]["sections"] += [
  ("Renouvellement d'air : combien de volumes par heure ?",
   ["Le dimensionnement d'un hélicoïde part rarement d'une pression, mais d'un <b>nombre de renouvellements horaires</b> : le volume du local multiplié par le nombre de fois où l'air doit être intégralement remplacé en une heure.",
    "Un entrepôt logistique se contente de quelques renouvellements ; un atelier dégageant chaleur ou vapeurs en demande beaucoup plus ; un bâtiment d'élevage relève de règles propres à sa filière. C'est cette valeur, croisée au volume, qui donne le débit à installer.",
    "Reste ensuite à traiter l'entrée d'air : un extracteur ne peut sortir que ce qui peut entrer. Sans surface d'amenée suffisante, la machine travaille en dépression, consomme davantage et n'atteint jamais son débit annoncé."]),
  ("Maintenance et durée de vie",
   ["Un hélicoïde bien dimensionné est une machine simple, donc durable. Les points à surveiller sont peu nombreux : l'<b>équilibrage</b> de l'hélice, l'état des roulements, la propreté des pales et le serrage des fixations.",
    "L'encrassement est le premier ennemi : une hélice chargée de poussière se déséquilibre, vibre, et détruit ses roulements en quelques mois. Un nettoyage périodique coûte infiniment moins cher qu'un remplacement.",
    "Les <a href=\"/nos-autres-accessoires\">accessoires</a> jouent ici un rôle sous-estimé : une manchette souple isole la machine des contraintes du réseau, des plots antivibratiles évitent de transmettre les vibrations au bâtiment, une grille protège autant les personnes que l'hélice."]),
]
P["ventilateurs-helicoides.html"]["faq"] = [
  ("Un ventilateur hélicoïde peut-il être raccordé à une gaine ?",
   "Oui, en montage sur virole. Il faut toutefois rester dans son domaine d'emploi : l'hélicoïde supporte mal les fortes pertes de charge. Au-delà de quelques centaines de pascals, un ventilateur centrifuge devient plus adapté et plus économe."),
  ("Comment réduire le bruit d'un ventilateur axial ?",
   "Le levier principal est la vitesse de l'air en bout de pale : à débit égal, une grande hélice tournant lentement est nettement plus silencieuse qu'une petite hélice rapide. Un caisson d'insonorisation et des silencieux placés à l'aspiration et au refoulement complètent le traitement."),
  ("Quelle protection choisir pour une installation extérieure ?",
   "La galvanisation à chaud est la protection de référence en extérieur et en ambiance humide, car le zinc protège l'acier même en cas de rayure. En milieu agroalimentaire ou fortement corrosif, la construction en acier inoxydable est préférable."),
  ("Quelle est la différence entre ventilateur axial et hélicoïde ?",
   "Aucune : les deux termes désignent le même principe, un ventilateur dont l'air traverse la roue parallèlement à l'axe de rotation. « Hélicoïde » est l'usage courant en France, « axial » la dénomination technique."),
  ("Peut-on installer un hélicoïde en toiture ?",
   "Oui, en tourelle d'extraction. Il faut alors traiter l'étanchéité de la traversée, l'accès pour la maintenance et la protection contre la corrosion, l'exposition en toiture étant plus sévère qu'en façade."),
]

P["traitement-surface.html"]["sections"] += [
  ("Choisir la protection selon l'ambiance réelle",
   ["Il n'existe pas de traitement universel : le bon choix découle de l'ambiance dans laquelle la machine va vivre. Un ventilateur en <b>intérieur sec</b> se contente d'une peinture industrielle ; en <b>extérieur ou en atmosphère humide</b>, la galvanisation s'impose ; en <b>agroalimentaire ou en milieu corrosif</b>, l'inox devient la base.",
    "Trois questions suffisent le plus souvent à trancher : la machine est-elle exposée aux intempéries ? Le fluide véhiculé est-il corrosif, acide ou chargé de vapeurs ? Le nettoyage se fait-il avec des produits agressifs, et à quelle fréquence ?",
    "Surprotéger coûte cher sans bénéfice ; sous-protéger se paie en remplacement anticipé. L'écart entre les deux se joue au moment de l'étude, pas après."]),
]
P["traitement-surface.html"]["faq"] = [
  ("Galvanisation ou métallisation : laquelle choisir ?",
   "La galvanisation à chaud protège l'intérieur comme l'extérieur des pièces et convient aux dimensions compatibles avec le bain de zinc. La métallisation ne chauffe pas la pièce : elle s'impose pour les grands ensembles soudés ou les géométries complexes qui risqueraient de se déformer."),
  ("Quelle est la couleur standard des ventilateurs Euroventilatori ?",
   "Les machines de série sont peintes en RAL 7038, un gris agate qui a remplacé le gris standard historique. Toute autre teinte du nuancier RAL est réalisable sur demande, notamment pour s'aligner sur la charte visuelle d'un site industriel."),
  ("Quand faut-il un ventilateur en inox ?",
   "L'acier inoxydable s'impose lorsque le fluide est corrosif ou chargé en vapeurs acides, et lorsque l'hygiène l'exige : agroalimentaire, pharmacie, chimie. Dans ces cas, la roue elle-même est réalisée en inox, pas seulement l'enveloppe."),
  ("Le traitement de surface influence-t-il les performances aérauliques ?",
   "Marginalement sur le débit, mais nettement sur la durée : une roue corrodée ou encrassée se déséquilibre, perd du rendement et use ses roulements. La protection de surface est donc un investissement de performance autant que de longévité."),
]

_FAQ_LOCALE = [
  ("Livrez-vous dans toute la région ?",
   "Oui. Euroventilatori France fabrique dans son atelier de Nivolas-Vermelle, en Isère, et livre partout en France sans surcoût lié à la distance. L'engagement de devis détaillé sous 24 heures s'applique de la même manière sur tout le territoire."),
  ("Quelles informations fournir pour obtenir un devis ?",
   "Trois données suffisent pour démarrer : le débit d'air recherché en m³/h, la pression statique du réseau en Pa, et la nature du fluide véhiculé — air propre, chargé en poussières, humide, chaud ou corrosif. Les contraintes d'encombrement et le niveau sonore admissible affinent ensuite la sélection."),
  ("Intervenez-vous sur une installation existante ?",
   "Oui. Le remplacement d'un ventilateur en place commence par un relevé du point de fonctionnement réel, souvent différent de la plaque signalétique. Ce diagnostic évite de reproduire un sous-dimensionnement ancien et permet de vérifier l'encombrement disponible avant fabrication."),
  ("Proposez-vous des machines conformes ATEX ?",
   "Oui. Une machine destinée à une atmosphère explosible est conçue pour cela dès l'origine, avec des matériaux anti-étincelants, des jeux maîtrisés et un moteur certifié correspondant à la zone concernée."),
]

for _p, _extra in [
  ("ile-de-france-rhone-alpes.html",
   ("Ce que change un fabricant implanté dans la région",
    ["Une visite technique se programme dans la journée plutôt que dans la semaine. Un relevé sur site ne mobilise pas une journée de déplacement. Une pièce urgente peut être retirée directement à l'atelier.",
     "Cette proximité change surtout la <b>qualité du dimensionnement</b> : il devient facile de venir mesurer plutôt que d'estimer, et l'écart entre données déclarées et réalité explique la plupart des installations décevantes.",
     "Elle change aussi la relation en cas d'imprévu. Un arrêt de production ne se règle pas par courriel : il se règle sur place."])),
  ("paris.html",
   ("Réglementation, ICPE et voisinage",
    ["Beaucoup de sites franciliens relèvent d'un régime <b>ICPE</b> et doivent justifier de leurs rejets et de leur niveau sonore. Le ventilateur n'est pas seul en cause, mais il est souvent le plus visible — et le plus facilement mis en cause par un riverain.",
     "Nous documentons donc le niveau sonore attendu et les caractéristiques du rejet dès l'étude, de manière à ce que ces éléments puissent être versés à un dossier.",
     "Lorsque le rejet doit être traité, la <a href=\"/purificateur-air\">filtration</a> se dimensionne conjointement au ventilateur : ajouter un filtre après coup, c'est ajouter une perte de charge que la machine n'était pas prévue pour vaincre."])),
  ("lille.html",
   ("Reprendre une installation ancienne",
    ["Le tissu industriel régional compte de nombreuses installations aérauliques anciennes, souvent modifiées au fil des années sans que le ventilateur ait été revu. Registres partiellement fermés, gaines ajoutées, filtres plus fins : la machine travaille alors hors de son point optimal.",
     "Un relevé de débit et de pression révèle en général un potentiel d'économie immédiat, soit par changement de machine, soit par simple pose d'un variateur de fréquence.",
     "C'est aussi l'occasion de traiter la conformité et le bruit, deux sujets qui remontent souvent en même temps que la question de la consommation."])),
  ("bretagne.html",
   ("Nettoyage, lavage et conception hygiénique",
    ["En agroalimentaire, la machine est lavée régulièrement, parfois plusieurs fois par jour, avec des produits alcalins ou chlorés. La conception doit anticiper ce régime : <b>surfaces lisses</b>, absence de zones de rétention, accessibilité au démontage.",
     "Un ventilateur difficile à nettoyer devient un point de contamination, et un ventilateur mal protégé se corrode par l'intérieur — là où le contrôle visuel ne va pas.",
     "Nous privilégions donc l'inox et une géométrie pensée pour le nettoyage plutôt qu'un traitement de surface appliqué sur une conception qui ne s'y prêtait pas."])),
]:
    P[_p]["sections"] += [_extra]
    P[_p]["faq"] = list(_FAQ_LOCALE)


# --- Panorama de l'offre, angle par region ---------------------------------

P["ile-de-france-rhone-alpes.html"]["sections"] += [
  ("Toute la gamme, disponible en Rhône-Alpes",
   ["Les <a href=\"/ventilateurs-centrifuges\">ventilateurs centrifuges</a> couvrent ici l'essentiel des besoins : extraction de vapeurs de solvants en plasturgie, dépoussiérage en décolletage, captation de brouillards d'huile en usinage, tirage sur four en métallurgie. Basse, moyenne ou haute pression selon les pertes de charge du réseau.",
    "Les <a href=\"/ventilateurs-helicoides\">hélicoïdes</a> prennent le relais pour renouveler l'air des ateliers et des entrepôts, où il faut déplacer de grands volumes sans vaincre de réseau.",
    "En zone classée, la conformité <b>ATEX</b> se conçoit dès l'origine : matériaux anti-étincelants, jeux maîtrisés, moteur certifié pour la zone. C'est une machine spécifique, jamais un modèle standard adapté après coup.",
    "Autour du ventilateur, l'offre se complète de <a href=\"/caissons-insonorises\">caissons acoustiques</a>, de <a href=\"/purificateur-air\">caissons de filtration</a> et des <a href=\"/nos-autres-accessoires\">accessoires</a> de raccordement — manchettes, registres, supports antivibratiles.",
    "Le <a href=\"/traitement-surface\">traitement de surface</a> se choisit selon l'ambiance : peinture RAL 7038 en intérieur sec, galvanisation en extérieur, inox pour les vapeurs corrosives de la chimie."]),
]

P["paris.html"]["sections"] += [
  ("Une offre pensée pour les contraintes franciliennes",
   ["En zone dense, la question acoustique précède souvent la question aéraulique. Nos <a href=\"/caissons-insonorises\">caissons d'insonorisation</a> et nos silencieux se dimensionnent avec la machine, pas après elle : c'est ce qui permet de tenir une émergence sonore faible sans surdimensionner le moteur.",
    "La <a href=\"/purificateur-air\">filtration</a> vient ensuite, imposée par la nature du rejet : vapeurs grasses de cuisine centrale, solvants d'imprimerie, poussières d'atelier. Le filtre ajoutant de la perte de charge, il doit figurer dans le calcul dès le départ.",
    "Côté machines, les <a href=\"/ventilateurs-centrifuges\">centrifuges</a> équipent les réseaux gainés des bâtiments tertiaires et industriels ; les <a href=\"/ventilateurs-helicoides\">hélicoïdes</a> assurent le renouvellement d'air des grands volumes et l'extraction en toiture.",
    "Quand l'implantation sort de l'ordinaire — local technique exigu, toiture chargée, passage étroit — la machine est étudiée <a href=\"/ventilateur-sur-mesure\">sur mesure</a>, y compris en éléments assemblables sur place.",
    "Chaque projet passe par notre <a href=\"/bureau-etudes\">bureau d'études</a>, qui valide encombrement, accès de maintenance et niveau sonore sur vos plans avant lancement en fabrication."]),
]

P["lille.html"]["sections"] += [
  ("L'offre adaptée aux industries des Hauts-de-France",
   ["Les fluides chargés dominent ici : poussières de meulage, fumées de soudure, fibres textiles, poussières de carton, particules abrasives. Ils appellent des <a href=\"/ventilateurs-centrifuges\">centrifuges à aubes radiales</a>, qui ne se colmatent pas, et des revêtements anti-abrasion.",
    "En agroalimentaire, la logique s'inverse : ce sont l'hygiène et l'humidité qui commandent. La machine se construit en <b>inox</b>, avec des surfaces lavables et une géométrie sans rétention.",
    "Le transport pneumatique de chutes, de copeaux ou de granulés relève de la <b>haute pression</b> : roues épaisses, jeux maîtrisés, maintenance pensée dès la conception.",
    "Les <a href=\"/ventilateurs-helicoides\">hélicoïdes</a> couvrent le renouvellement d'air des grands volumes logistiques, très présents dans la région.",
    "S'y ajoutent la <a href=\"/purificateur-air\">filtration</a> pour maîtriser rejets et odeurs, les <a href=\"/caissons-insonorises\">solutions acoustiques</a> pour les sites proches d'habitations, et le <a href=\"/traitement-surface\">traitement de surface</a> adapté à chaque ambiance."]),
]

P["bretagne.html"]["sections"] += [
  ("L'offre adaptée à l'agroalimentaire breton",
   ["L'<b>inox</b> est ici le point de départ plutôt que l'option : abattoirs, ateliers de découpe, laiteries et conserveries lavent leurs installations avec des produits alcalins ou chlorés qu'un acier peint ne supporte pas dans la durée.",
    "Les <a href=\"/ventilateurs-helicoides\">hélicoïdes</a> assurent les grands débits des bâtiments d'élevage, du séchage et de la ventilation des silos — des applications où le volume prime sur la pression.",
    "Les <a href=\"/ventilateurs-centrifuges\">centrifuges</a> interviennent dès qu'un réseau, un filtre ou un cyclone oppose de la résistance : extraction de vapeurs, dépoussiérage, transport pneumatique de farines et de granulés.",
    "La <a href=\"/purificateur-air\">filtration</a> traite la question des odeurs, souvent sensible lorsque le site jouxte des habitations, et les <a href=\"/caissons-insonorises\">caissons acoustiques</a> celle du bruit.",
    "Enfin, le <a href=\"/traitement-surface\">traitement de surface</a> tient compte de l'air marin : galvanisation à chaud ou inox selon l'exposition, jusqu'au choix de la visserie."]),
]


# ===========================================================================
# PAGES LEGALES — donnees d'identification reelles, redaction neuve.
# ⚠️ A relire par la direction avant mise en ligne, et a confirmer le jour de
# la bascule pour la section hebergeur.
# ===========================================================================

P["mentions-legales.html"] = dict(
  title="Mentions légales | Euroventilatori France",
  desc="Mentions légales du site euroventilatori.fr : identification de la société Euroventilatori France, directeur de publication, hébergement et propriété intellectuelle.",
  h1="Mentions légales",
  kicker="Informations légales",
  ghost="Légal",
  intro="""<p>Informations relatives à l'éditeur et à l'hébergeur du site
<b>euroventilatori.fr</b>, publiées en application de la loi pour la confiance
dans l'économie numérique.</p>""",
  cta='<a class="btn ghost-b" href="/contact">Nous contacter</a>',
  sections=[
    ("Éditeur du site",
     ["<b>Raison sociale :</b> Euroventilatori France<br>"
      "<b>Forme juridique :</b> société à responsabilité limitée (SARL)<br>"
      "<b>Capital social :</b> 50 000 €<br>"
      "<b>RCS :</b> Vienne B 383 242 500<br>"
      "<b>SIRET :</b> 383 242 500 00056<br>"
      "<b>N° de TVA intracommunautaire :</b> FR92383242500",
      "<b>Siège social :</b> 150 rue du Vernay, 38300 Nivolas-Vermelle, France<br>"
      "<b>Téléphone :</b> <a href=\"tel:0474436838\">04 74 43 68 38</a><br>"
      "<b>Adresse électronique :</b> <a href=\"mailto:contact@euroventilatori-france.com\">contact@euroventilatori-france.com</a>",
      "<b>Directeur de la publication :</b> M. Mathieu Hollard.",
      "L'établissement n'est pas concerné par le dispositif de médiation de la consommation, son activité s'adressant exclusivement à une clientèle professionnelle."]),
    ("Hébergement du site",
     ["<b>Hébergeur :</b> Cloudflare, Inc.<br>"
      "<b>Adresse :</b> 101 Townsend Street, San Francisco, CA 94107, États-Unis<br>"
      "<b>Site :</b> <a href=\"https://www.cloudflare.com\" rel=\"noopener\">www.cloudflare.com</a>",
      "Le site est distribué depuis le réseau de serveurs de l'hébergeur, dont les points de présence européens assurent la diffusion des pages en France.",
      "<i>Section à confirmer le jour de la mise en ligne : les informations d'hébergement doivent correspondre au prestataire effectivement retenu.</i>"]),
    ("Propriété intellectuelle",
     ["L'ensemble des éléments composant ce site — textes, mise en page, éléments graphiques, illustrations et développements — est protégé par le droit de la propriété intellectuelle et demeure la propriété d'Euroventilatori France, sauf mention contraire.",
      "Toute reproduction, représentation, adaptation ou exploitation, totale ou partielle, par quelque procédé que ce soit et sur quelque support que ce soit, est interdite sans autorisation écrite préalable.",
      "Les marques, dénominations sociales et logotypes cités appartiennent à leurs titulaires respectifs."]),
    ("Responsabilité et liens",
     ["Les informations techniques publiées sur ce site sont fournies à titre indicatif. Les caractéristiques des matériels, les valeurs de débit, de pression et de rendement sont susceptibles d'évoluer : seule une étude établie par notre bureau d'études engage la société.",
      "Le site peut renvoyer vers des sites tiers dont Euroventilatori France ne maîtrise ni le contenu ni les pratiques, et dont elle ne saurait être tenue responsable.",
      "Toute question relative au présent site peut être adressée à <a href=\"mailto:contact@euroventilatori-france.com\">contact@euroventilatori-france.com</a>."]),
  ])

P["vie-privee.html"] = dict(
  title="Vie privée et protection des données | Euroventilatori France",
  desc="Politique de protection des données personnelles d'Euroventilatori France : responsable du traitement, finalités, destinataires, durées de conservation et droits RGPD.",
  h1="Vie privée et protection des données personnelles",
  kicker="Protection des données — RGPD",
  ghost="Données",
  intro="""<p>Euroventilatori France traite des données personnelles dans le cadre
de sa relation commerciale et des demandes reçues par ce site. Cette page décrit
<b>ce qui est collecté, pourquoi, pour combien de temps</b>, et les droits dont
vous disposez.</p>""",
  cta='<a class="btn ghost-b" href="/contact">Exercer vos droits</a>',
  sections=[
    ("Responsable du traitement",
     ["Le responsable du traitement est la société <b>Euroventilatori France</b>, SARL au capital de 50 000 €, dont le siège est situé 150 rue du Vernay, 38300 Nivolas-Vermelle.",
      "Toute demande relative à vos données peut être adressée par courriel à <a href=\"mailto:contact@euroventilatori-france.com\">contact@euroventilatori-france.com</a> ou par courrier à l'adresse du siège."]),
    ("Quelles données, et pour quelles finalités ?",
     ["Les données collectées sont celles que vous nous transmettez volontairement : <b>nom, société, adresse électronique, numéro de téléphone</b> et les éléments techniques nécessaires à l'étude de votre besoin — débit, pression, nature du fluide, contraintes du site.",
      "Elles servent exclusivement à <b>répondre à votre demande</b>, établir un devis, assurer le suivi de la relation commerciale et, le cas échéant, la gestion de la fourniture et du service après-vente.",
      "Aucune donnée n'est collectée à des fins publicitaires, et le site ne procède à aucun profilage ni à aucune décision automatisée."]),
    ("Qui accède à ces données ?",
     ["Vos données sont accessibles aux seuls collaborateurs d'Euroventilatori France concernés par le traitement de votre demande : équipe technico-commerciale, bureau d'études, administration des ventes.",
      "Elles peuvent être communiquées à des <b>sous-traitants techniques</b> agissant sur instruction — hébergement du site, service d'acheminement des courriels — tenus par contrat à la confidentialité et à la sécurité.",
      "Elles ne sont ni vendues, ni louées, ni cédées à des tiers à des fins commerciales."]),
    ("Combien de temps sont-elles conservées ?",
     ["Les demandes n'ayant pas donné lieu à une relation commerciale sont conservées <b>trois ans</b> à compter du dernier contact.",
      "Les données liées à une relation commerciale sont conservées pendant la durée de cette relation, puis archivées conformément aux obligations légales de conservation des documents comptables et contractuels.",
      "Au-delà de ces durées, les données sont supprimées ou anonymisées."]),
    ("Vos droits",
     ["Conformément au règlement général sur la protection des données, vous disposez d'un droit d'<b>accès</b>, de <b>rectification</b>, d'<b>effacement</b>, de <b>limitation</b> et d'<b>opposition</b> au traitement, ainsi que d'un droit à la <b>portabilité</b> des données que vous nous avez fournies.",
      "Ces droits s'exercent sur simple demande à <a href=\"mailto:contact@euroventilatori-france.com\">contact@euroventilatori-france.com</a>, accompagnée de tout élément permettant de vérifier votre identité. Une réponse vous est apportée dans un délai d'un mois.",
      "En cas de désaccord persistant, vous pouvez introduire une réclamation auprès de la <b>Commission nationale de l'informatique et des libertés</b> (CNIL), 3 place de Fontenoy, 75007 Paris — <a href=\"https://www.cnil.fr\" rel=\"noopener\">www.cnil.fr</a>."]),
    ("Cookies et mesure d'audience",
     ["Ce site fonctionne sans cookie publicitaire et sans traceur tiers à des fins de ciblage.",
      "Seuls peuvent être déposés les cookies strictement nécessaires au fonctionnement du site, qui ne requièrent pas votre consentement préalable, ainsi que, le cas échéant, une mesure d'audience configurée pour être exemptée de consentement.",
      "<i>Section à ajuster à la mise en ligne selon les outils de mesure effectivement installés : toute solution non exemptée impose un bandeau de consentement préalable.</i>"]),
  ])


# --- Questions frequentes des pages initiales ------------------------------

P["ventilateurs.html"]["faq"] = [
  ("Quelle différence entre un ventilateur de gamme et un ventilateur sur mesure ?",
   "Un ventilateur de gamme est un modèle préfabriqué du catalogue, disponible rapidement et éprouvé sur les applications courantes. Un ventilateur sur mesure est conçu pour un cahier des charges précis : fluide chargé, haute température, matériau spécial, encombrement imposé ou conformité ATEX."),
  ("Comment savoir quel ventilateur convient à mon installation ?",
   "Trois données suffisent pour orienter la sélection : le débit d'air recherché en m³/h, la pression statique du réseau en Pa, et la nature du fluide véhiculé. Les contraintes d'encombrement et le niveau sonore admissible affinent ensuite le choix."),
  ("Quel est le délai pour obtenir un devis ?",
   "Euroventilatori France s'engage sur un devis détaillé sous 24 heures, aussi bien pour un ventilateur de gamme que pour une machine sur mesure, dès lors que le point de fonctionnement est connu."),
  ("Fournissez-vous aussi les accessoires et le traitement acoustique ?",
   "Oui. L'offre couvre l'installation complète : caissons insonorisés, caissons de filtration, manchettes souples, registres et supports antivibratiles. Un ventilateur mal raccordé perd une partie de ses performances et transmet ses vibrations au bâtiment."),
]

P["ventilateur-gamme.html"]["faq"] = [
  ("Combien de modèles compte le catalogue Euroventilatori ?",
   "Le catalogue réunit 53 séries de machines, déclinées en 25 tailles, 16 orientations et 6 types d'arrangements, avec plusieurs matériaux possibles. Cette combinatoire couvre la grande majorité des besoins aérauliques industriels."),
  ("Qu'est-ce que l'orientation et l'arrangement d'un ventilateur ?",
   "L'orientation désigne la position de la sortie de la volute par rapport à l'aspiration, à choisir selon le sens du réseau. L'arrangement décrit le mode d'entraînement : accouplement direct, transmission par courroies ou moteur déporté lorsque la température l'impose."),
  ("Un ventilateur de gamme est-il moins performant qu'une machine sur mesure ?",
   "Non. Sur une application courante, un modèle de gamme correctement sélectionné atteint le même rendement qu'une machine dédiée, pour un coût et un délai inférieurs. Le sur-mesure ne se justifie que lorsque la gamme ne couvre pas la contrainte."),
  ("Comment comparer deux modèles entre eux ?",
   "La plateforme LiveCurve trace les courbes aérauliques de toute la gamme : en saisissant débit et pression, elle affiche les modèles capables de tenir ce point et le rendement de chacun. C'est le rendement au point d'usage, et non la puissance nominale, qui détermine la consommation."),
]

P["ventilateur-sur-mesure.html"]["faq"] = [
  ("Dans quels cas faut-il un ventilateur sur mesure ?",
   "Le sur-mesure s'impose quand la gamme ne couvre pas la contrainte : fluide chargé ou abrasif, température élevée, atmosphère explosible, matériau particulier, encombrement imposé, ou point de fonctionnement situé hors des plages standard."),
  ("Combien de temps prend la conception d'une machine spéciale ?",
   "Le devis détaillé est établi sous 24 heures. Le délai de conception et de fabrication dépend ensuite de la complexité de la machine et des matériaux retenus ; il est communiqué avec l'étude."),
  ("Que faut-il fournir pour lancer une étude ?",
   "Le point de fonctionnement visé (débit et pression), la nature et la température du fluide, les contraintes d'implantation et d'encombrement, le niveau sonore admissible, et le cas échéant la zone ATEX concernée."),
  ("Une machine sur mesure est-elle réparable et maintenable ?",
   "Oui. Les machines spéciales sont conçues à partir des composants et des principes de la gamme, ce qui garantit la disponibilité des pièces et la simplicité de la maintenance dans la durée."),
]

P["solutions-ventilateur-industriel.html"]["faq"] = [
  ("Pourquoi ajouter un caisson de filtration à un ventilateur ?",
   "Le caisson de filtration purifie l'air aspiré ou soufflé : il protège le process et les opérateurs, et évite l'encrassement rapide de la roue. Il ajoute toutefois une perte de charge qui doit être intégrée au dimensionnement du ventilateur dès l'origine."),
  ("Peut-on insonoriser un ventilateur déjà installé ?",
   "Oui, par caisson d'insonorisation ou par silencieux placés à l'aspiration et au refoulement. Traiter le bruit dès la sélection reste préférable : une grande roue tournant lentement est structurellement plus silencieuse qu'une petite roue rapide."),
  ("Les accessoires sont-ils indispensables ?",
   "Ils conditionnent la performance réelle. Une manchette souple isole la machine des contraintes du réseau, des supports antivibratiles évitent de transmettre les vibrations au bâtiment, un registre permet de régler le débit sans intervenir sur la machine."),
  ("Fournissez-vous l'ensemble en un seul lot ?",
   "Oui. Ventilateur, traitement acoustique, filtration et accessoires de raccordement peuvent être étudiés et fournis ensemble, ce qui garantit leur compatibilité et évite les pertes de charge non anticipées."),
]

P["caissons-insonorises.html"]["faq"] = [
  ("Comment réduire le bruit d'un ventilateur industriel ?",
   "Trois leviers se combinent : dimensionner la machine pour qu'elle tourne moins vite à débit égal, l'enfermer dans un caisson d'insonorisation, et poser des silencieux à l'aspiration et au refoulement. Les supports antivibratiles empêchent en outre la transmission des vibrations à la structure."),
  ("De combien de décibels peut-on espérer réduire le niveau sonore ?",
   "Le gain dépend de la machine, du spectre du bruit et de la solution retenue ; il ne se prédit pas de façon générale. C'est pourquoi l'atténuation attendue est calculée cas par cas, à partir du niveau mesuré ou estimé à la source."),
  ("Un caisson d'insonorisation dégrade-t-il les performances ?",
   "Il ajoute une perte de charge, qui doit être prise en compte au moment de la sélection du ventilateur. Intégrée dès l'étude, elle est sans conséquence ; ajoutée après coup à une machine déjà dimensionnée, elle réduit le débit obtenu."),
  ("Quelle isolation est utilisée dans vos caissons ?",
   "Les caissons sont isolés en laine de roche haute densité, un matériau incombustible qui conserve ses propriétés acoustiques dans le temps et supporte les ambiances industrielles."),
]

P["purificateur-air.html"]["faq"] = [
  ("À quoi sert un caisson de filtration statique ?",
   "Il retient les particules présentes dans l'air aspiré ou soufflé par le ventilateur. Il protège ainsi le process, les produits et les opérateurs, et limite l'encrassement de la roue qui déséquilibrerait la machine à terme."),
  ("Comment choisir le niveau de filtration ?",
   "Le choix dépend de la taille des particules à retenir et de l'exigence du process : une simple préfiltration pour protéger une machine, une filtration fine pour un atelier propre, une filtration haute efficacité en laboratoire ou en salle propre."),
  ("À quelle fréquence changer les filtres ?",
   "La fréquence dépend de l'empoussièrement réel. Le repère fiable est la perte de charge : un filtre colmaté fait chuter le débit et augmenter la consommation. Un manomètre différentiel permet de déclencher le remplacement au bon moment plutôt qu'à date fixe."),
  ("La filtration permet-elle de traiter les odeurs ?",
   "La filtration particulaire seule ne traite pas les odeurs. Leur maîtrise relève d'une approche combinant le type de média, le dimensionnement du rejet et parfois un traitement spécifique, à étudier selon la nature des composés en cause."),
]

P["nos-autres-accessoires.html"]["faq"] = [
  ("Quels accessoires sont indispensables à une installation ?",
   "Trois éléments reviennent presque toujours : la manchette souple, qui isole la machine des contraintes du réseau ; les supports antivibratiles, qui évitent de transmettre les vibrations au bâtiment ; et la grille de protection, qui sécurise l'aspiration."),
  ("À quoi sert une manchette souple ?",
   "Elle assure la liaison entre le ventilateur et la gaine tout en absorbant les mouvements et les vibrations. Sans elle, les efforts du réseau se reportent sur la machine et les vibrations se propagent dans toute l'installation."),
  ("Peut-on régler le débit après installation ?",
   "Oui, par registre ou par variateur de fréquence. Le registre est simple mais dissipe de l'énergie ; le variateur adapte la vitesse au besoin réel et réduit fortement la consommation, une baisse de 20 % de la vitesse divisant la puissance absorbée par deux environ."),
  ("Fournissez-vous les pièces de rechange des machines anciennes ?",
   "Les machines de la gamme partagent des composants communs, ce qui facilite l'approvisionnement en pièces dans la durée. Pour une machine ancienne ou spéciale, une identification préalable permet de déterminer les pièces disponibles ou reproductibles."),
]

P["bureau-etudes.html"]["faq"] = [
  ("Que fait concrètement le bureau d'études ?",
   "Il analyse le besoin réel — débit, pression, fluide, contraintes du site —, dimensionne la machine, réalise les plans d'implantation en CAO 2D et 3D, et vérifie la compatibilité avec l'installation existante avant lancement en fabrication."),
  ("Quel logiciel utilisez-vous pour la conception ?",
   "La conception est réalisée sous SolidWorks, en 2D et en 3D, ce qui permet de fournir des plans d'implantation exploitables et de valider les encombrements avant fabrication."),
  ("Peut-on faire modifier un plan en cours de projet ?",
   "Oui. L'adaptation des plans d'implantation en cours de projet fait partie du travail courant du bureau d'études, avec le nouveau dimensionnement correspondant lorsque la modification touche l'aéraulique."),
  ("L'étude est-elle facturée ?",
   "L'établissement du devis, y compris le dimensionnement associé, est réalisé sous 24 heures dans le cadre de la démarche commerciale. Les études approfondies liées à des projets spécifiques font l'objet d'un accord préalable."),
]

P["competences.html"]["faq"] = [
  ("Quelles étapes maîtrisez-vous en interne ?",
   "La chaîne est maîtrisée de bout en bout : conception et dimensionnement, fabrication, contrôles qualité avant expédition, puis livraison. Cette continuité est ce qui permet de tenir des délais et un niveau de qualité constants."),
  ("Comment garantissez-vous la qualité des machines ?",
   "De nombreux contrôles sont réalisés avant expédition du matériel, afin d'assurer une qualité constante. Le centre d'essais permet en outre de valider techniquement les performances annoncées."),
  ("Quelle est la capacité de production du groupe ?",
   "Le groupe produit jusqu'à 30 000 ventilateurs industriels par an, sur un site de 28 000 m², et distribue dans le monde entier."),
  ("Depuis quand le groupe existe-t-il ?",
   "Euroventilatori a été fondée en Italie en 1981 et cumule plus de quarante ans d'expérience dans la conception et la fabrication de ventilateurs axiaux, centrifuges et spéciaux. Euroventilatori France s'appuie sur ce savoir-faire depuis 35 ans."),
]

P["qui-sommes-nous.html"]["faq"] = [
  ("Où se situe Euroventilatori France ?",
   "Euroventilatori France est implantée au 150 rue du Vernay, à Nivolas-Vermelle, en Isère, à proximité de Lyon. La société intervient dans toute la France."),
  ("Euroventilatori France fait-elle partie d'un groupe ?",
   "Oui. La maison mère italienne, fondée en 1981, conçoit et fabrique des ventilateurs axiaux, centrifuges et spéciaux depuis plus de quarante ans. Euroventilatori France s'appuie sur cette capacité industrielle avec une équipe et un bureau d'études français."),
  ("Quelle est la capacité de production ?",
   "Le site de production couvre 28 000 m² et fabrique jusqu'à 30 000 ventilateurs industriels par an, distribués dans le monde entier."),
  ("Quels secteurs industriels servez-vous ?",
   "Les principaux domaines servis sont l'énergie et la pétrochimie, l'industrie agroalimentaire, la métallurgie et l'industrie textile, auxquels s'ajoutent la chimie, le papier-carton, le bois et l'agriculture."),
]

P["secteurs-activite.html"]["faq"] = [
  ("Quels secteurs industriels équipez-vous ?",
   "Les principaux sont l'énergie et la pétrochimie, l'agroalimentaire, la métallurgie et le textile. S'y ajoutent la chimie, la plasturgie, le papier-carton, le bois, la cimenterie et l'agriculture."),
  ("Pourquoi le secteur d'activité change-t-il le choix du ventilateur ?",
   "Parce qu'il détermine la nature du fluide et l'ambiance : poussières abrasives en métallurgie, vapeurs grasses et exigence d'hygiène en agroalimentaire, atmosphère explosible en pétrochimie, fibres en textile. Chacun impose un type de roue, un matériau et un traitement de surface différents."),
  ("Proposez-vous des machines conformes ATEX ?",
   "Oui. Une machine destinée à une atmosphère explosible est conçue pour cela dès l'origine, avec des matériaux anti-étincelants, des jeux maîtrisés et un moteur certifié correspondant à la zone."),
  ("Intervenez-vous sur des installations existantes ?",
   "Oui. Le remplacement d'une machine en place commence par le relevé du point de fonctionnement réel, souvent différent de la plaque signalétique, afin de ne pas reproduire un sous-dimensionnement ancien."),
]

P["telechargement.html"]["faq"] = [
  ("Qu'est-ce que LiveCurve ?",
   "LiveCurve est la plateforme de simulation développée par Euroventilatori. Elle trace les courbes aérauliques de la gamme : en modifiant les données d'entrée, elle affiche les modèles capables de tenir le point de fonctionnement et le rendement de chacun."),
  ("Faut-il un compte pour utiliser LiveCurve ?",
   "Les modalités d'accès sont indiquées sur la plateforme. Nos technico-commerciaux peuvent également réaliser la simulation avec vous et vous transmettre la sélection commentée."),
  ("Une simulation remplace-t-elle une étude ?",
   "Non. La simulation oriente vers les modèles pertinents ; la sélection définitive intègre la densité de l'air, la température, la vitesse et le niveau sonore, et fait l'objet d'une validation par nos équipes."),
  ("Où trouver les fiches techniques des produits ?",
   "Les documentations et fiches techniques sont mises à disposition dans l'espace de téléchargement. Pour un document précis ou une machine ancienne, la demande peut être adressée à notre équipe."),
]

P["contact.html"]["faq"] = [
  ("Quelles informations transmettre pour obtenir un devis rapidement ?",
   "Le débit recherché en m³/h, la pression statique en Pa et la nature du fluide véhiculé suffisent à démarrer. En précisant l'encombrement disponible et le niveau sonore admissible, la proposition est directement exploitable."),
  ("Sous quel délai obtient-on une réponse ?",
   "Euroventilatori France s'engage sur un devis détaillé sous 24 heures, pour un ventilateur de gamme comme pour une machine sur mesure."),
  ("Je ne connais pas mon débit ni ma pression : que faire ?",
   "Décrivez l'application, le volume du local ou le process concerné, ainsi que la machine en place le cas échéant. Nos technico-commerciaux reconstituent le besoin, et un relevé sur site peut être organisé lorsque l'installation existe déjà."),
  ("Intervenez-vous partout en France ?",
   "Oui. La fabrication est réalisée dans notre atelier de Nivolas-Vermelle, en Isère, et la livraison couvre l'ensemble du territoire, sans différence d'engagement selon la région."),
]

# ---------------------------------------------------------------------------
# Métadonnées de navigation, par page :
#   nav      → entrée de menu à surligner
#   trail    → fil d'Ariane (le dernier élément, sans URL, est la page courante)
#   proof    → afficher le bandeau de preuves (non pertinent sur contact/actus)
#   related  → 3 pages liées : circulation du lecteur + maillage interne
# ---------------------------------------------------------------------------
PRODUITS = ("Nos produits", "/ventilateurs")

R = {
  "gamme":    ("/ventilateur-gamme", "Ventilateurs de gamme",
               "53 séries, 25 tailles, 16 orientations : le catalogue standard."),
  "mesure":   ("/ventilateur-sur-mesure", "Ventilateurs sur mesure",
               "Aciers spéciaux, hautes températures, ATEX : la machine dédiée."),
  "produits": ("/ventilateurs", "Tous nos ventilateurs",
               "Centrifuges et hélicoïdaux, standards ou spécifiques."),
  "acou":     ("/caissons-insonorises", "Caissons insonorisés",
               "Traiter le bruit à la source, sans dégrader l'aéraulique."),
  "filtr":    ("/purificateur-air", "Filtration de l'air",
               "Caissons de filtration pour purifier l'air aspiré ou soufflé."),
  "acc":      ("/nos-autres-accessoires", "Accessoires",
               "Manchettes, registres, supports : raccorder proprement."),
  "solutions":("/solutions-ventilateur-industriel", "Solutions complètes",
               "Filtration, insonorisation et accessoires réunis."),
  "be":       ("/bureau-etudes", "Bureau d'études",
               "Dimensionnement et conception CAO 2D/3D SolidWorks."),
  "comp":     ("/competences", "Nos compétences",
               "Conception, dimensionnement, essais et suivi."),
  "secteurs": ("/secteurs-activite", "Secteurs d'activité",
               "Énergie, agroalimentaire, métallurgie, textile…"),
  "qui":      ("/qui-sommes-nous", "Qui sommes-nous ?",
               "40 ans de savoir-faire, 28 000 m² de production."),
  "dl":       ("/telechargement", "LiveCurve & documentation",
               "Simuler les courbes aérauliques et télécharger les fiches."),
  "contact":  ("/contact", "Contact & devis",
               "Devis détaillé sous 24 h pour votre point de fonctionnement."),
  "centri":   ("/ventilateurs-centrifuges", "Ventilateurs centrifuges",
               "Vaincre les fortes pertes de charge : dépoussiérage, fumées, transport."),
  "helico":   ("/ventilateurs-helicoides", "Ventilateurs hélicoïdes",
               "Grands débits sous faible pression : ateliers, entrepôts, élevages."),
  "surface":  ("/traitement-surface", "Traitement de surface",
               "Galvanisation, métallisation, RAL 7038 ou inox selon l'ambiance."),
  "rhone":    ("/ile-de-france-rhone-alpes", "Rhône-Alpes",
               "Notre atelier est en Isère : intervention à moins d'une heure."),
  "paris":    ("/paris", "Paris et Île-de-France",
               "Zone dense : acoustique renforcée et accès contraints."),
  "lille":    ("/lille", "Lille et Hauts-de-France",
               "Agroalimentaire, métallurgie, papier-carton, textile."),
  "bretagne": ("/bretagne", "Bretagne",
               "Agroalimentaire, élevage, séchage céréalier, air marin."),
}

META = {
 "ventilateurs.html":                  dict(nav="/ventilateurs", trail=[("Nos produits", None)],
                                            related=["gamme","mesure","solutions"]),
 "ventilateur-gamme.html":             dict(nav="/ventilateurs", trail=[PRODUITS, ("Ventilateurs de gamme", None)],
                                            related=["mesure","dl","secteurs"]),
 "ventilateur-sur-mesure.html":        dict(nav="/ventilateurs", trail=[PRODUITS, ("Ventilateurs sur mesure", None)],
                                            related=["be","gamme","secteurs"]),
 "solutions-ventilateur-industriel.html": dict(nav="/solutions-ventilateur-industriel", trail=[("Solutions", None)],
                                            related=["acou","filtr","acc"]),
 "caissons-insonorises.html":          dict(nav="/solutions-ventilateur-industriel", trail=[("Solutions", "/solutions-ventilateur-industriel"), ("Acoustique", None)],
                                            related=["filtr","acc","produits"]),
 "purificateur-air.html":              dict(nav="/solutions-ventilateur-industriel", trail=[("Solutions", "/solutions-ventilateur-industriel"), ("Filtration", None)],
                                            related=["acou","acc","produits"]),
 "nos-autres-accessoires.html":        dict(nav="/solutions-ventilateur-industriel", trail=[("Solutions", "/solutions-ventilateur-industriel"), ("Accessoires", None)],
                                            related=["acou","filtr","produits"]),
 "bureau-etudes.html":                 dict(nav="/bureau-etudes", trail=[("Bureau d'études", None)],
                                            related=["comp","mesure","dl"]),
 "competences.html":                   dict(nav="/bureau-etudes", trail=[("Bureau d'études", "/bureau-etudes"), ("Compétences", None)],
                                            related=["be","qui","produits"]),
 "qui-sommes-nous.html":               dict(nav="/bureau-etudes", trail=[("Qui sommes-nous ?", None)],
                                            related=["comp","secteurs","be"]),
 "secteurs-activite.html":             dict(nav="/secteurs-activite", trail=[("Secteurs d'activité", None)],
                                            related=["produits","mesure","qui"]),
 "telechargement.html":                dict(nav="/telechargement", trail=[("Téléchargement", None)],
                                            related=["gamme","be","contact"]),
 "contact.html":                       dict(nav="/contact", trail=[("Contact", None)], proof=False,
                                            related=["dl","be","produits"]),
 "actualites.html":                    dict(nav="/telechargement", trail=[("Actualités", None)], proof=False,
                                            related=["qui","secteurs","produits"]),

 # Pages produits : rattachees a la rubrique « Nos produits »
 "ventilateurs-centrifuges.html":      dict(nav="/ventilateurs", trail=[PRODUITS, ("Ventilateurs centrifuges", None)],
                                            related=["helico","gamme","surface"]),
 "ventilateurs-helicoides.html":       dict(nav="/ventilateurs", trail=[PRODUITS, ("Ventilateurs hélicoïdes", None)],
                                            related=["centri","acou","surface"]),
 "traitement-surface.html":            dict(nav="/ventilateurs", trail=[PRODUITS, ("Traitement de surface", None)],
                                            related=["mesure","centri","be"]),

 # Pages locales : rattachees aux secteurs, reliees entre elles et au metier
 "ile-de-france-rhone-alpes.html":     dict(nav="/secteurs-activite", trail=[("Rhône-Alpes", None)],
                                            related=["be","centri","contact"]),
 "paris.html":                         dict(nav="/secteurs-activite", trail=[("Paris et Île-de-France", None)],
                                            related=["acou","filtr","contact"]),
 "lille.html":                         dict(nav="/secteurs-activite", trail=[("Lille et Hauts-de-France", None)],
                                            related=["centri","surface","secteurs"]),
 "bretagne.html":                      dict(nav="/secteurs-activite", trail=[("Bretagne", None)],
                                            related=["helico","surface","secteurs"]),

 # Pages légales : ni bandeau de preuves, ni argumentaire commercial
 "mentions-legales.html":              dict(nav="", trail=[("Mentions légales", None)], proof=False,
                                            related=["contact","qui"]),
 "vie-privee.html":                    dict(nav="", trail=[("Vie privée", None)], proof=False,
                                            related=["contact","qui"]),
}


def liste_articles_html():
    """Index des publications, de la plus recente a la plus ancienne."""
    items = "".join(
        '<a href="/%s"><span class="go">%s</span><strong>%s</strong>'
        '<span>%s</span></a>' % (a["slug"], a["date_fr"], a["titre"], a["chapo"])
        for a in ARTICLES)
    return ('<section class="related">\n  <div class="wrap">\n'
            '    <h2>Toutes nos publications</h2>\n'
            '    <div class="related-grid actus">%s</div>\n  </div>\n</section>' % items)


def generer_articles():
    """Une page par publication, batie sur le meme gabarit que les autres."""
    for a in ARTICLES:
        corps = "\n".join("      <p>%s</p>" % p for p in a["corps"])
        section = ('<section class="page-sec">\n  <div class="wrap sec-grid">\n'
                   '    <h2>%s</h2>\n    <div class="prose">\n%s\n    </div>\n'
                   '  </div>\n</section>' % (a["chapo"], corps))
        html = TPL.format(
            title=a["titre"].replace("&nbsp;", " ") + " | Euroventilatori France",
            desc=a["desc"], h1=a["titre"],
            kicker="Actualités — %s" % a["date_fr"],
            ghost="Actualité",
            intro='<p>%s</p>' % a["chapo"],
            cta='<a class="btn ghost-b" href="/actualites">Toutes les actualités</a>',
            sections=section,
            nav=nav_html("/actualites"),
            breadcrumb=breadcrumb_html([("Actualités", "/actualites"),
                                        (a["titre"].replace("&nbsp;", " "), None)]),
            bcjson=breadcrumb_jsonld([("Actualités", "/actualites"),
                                      (a["titre"].replace("&nbsp;", " "), None)]),
            org=ORG_JSONLD, canonical=SITE + "/" + a["slug"],
            proof="", faq="", faqjson=blogposting_jsonld(a),
            related=autres_articles(a["slug"]), footer=FOOTER)
        with io.open(a["slug"] + ".html", "w", encoding="utf-8") as f:
            f.write(html)
        print("OK", a["slug"] + ".html")

os.chdir(os.path.dirname(os.path.abspath(__file__)))
for fname, d in P.items():
    m = META.get(fname, dict(nav="", trail=[(d["h1"][:40], None)], related=[]))
    slug = "/" + fname.replace(".html", "")
    sections = "\n".join(sec(h2, paras, *rest) for h2, paras, *rest in d["sections"])
    if d.get("liste_articles"):
        sections += "\n" + liste_articles_html()
    html = TPL.format(title=d["title"], desc=d["desc"], h1=d["h1"], kicker=d["kicker"],
                      ghost=d["ghost"], intro=d["intro"], cta=d["cta"],
                      sections=sections,
                      nav=nav_html(m["nav"]),
                      breadcrumb=breadcrumb_html(m["trail"]),
                      bcjson=breadcrumb_jsonld(m["trail"]),
                      org=ORG_JSONLD,
                      canonical=SITE + slug,
                      proof=PROOF if m.get("proof", True) else "",
                      faq=faq_html(d.get("faq")),
                      faqjson=faq_jsonld(d.get("faq")),
                      related=related_html([R[k] for k in m["related"]]),
                      footer=FOOTER)
    with io.open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    print("OK", fname)
generer_articles()
print("Terminé :", len(P) + len(ARTICLES), "pages")
