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
PROOF = """<section class="proof">
  <div class="wrap">
    <div class="proof-grid">
      <div class="proof-item rv"><span class="n"><span data-count="35">0</span><i>ans</i></span><span class="l">d'expertise en France</span></div>
      <div class="proof-item rv"><span class="n"><span data-count="30000">0</span></span><span class="l">ventilateurs produits par an</span></div>
      <div class="proof-item rv"><span class="n"><span data-count="28000">0</span><i>m²</i></span><span class="l">de surface de production</span></div>
      <div class="proof-item rv"><span class="n">24<i>h</i></span><span class="l">pour un devis détaillé</span></div>
    </div>
  </div>
</section>"""

def related_html(cards):
    """Pages liées : circulation du lecteur et maillage interne."""
    if not cards:
        return ""
    items = "".join(
        f'<a href="{u}"><strong>{t}</strong><span>{d}</span>'
        f'<span class="go">Consulter →</span></a>' for u, t, d in cards)
    return f"""<section class="related">
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
        <a href="/actualites">Actualités</a>
      </div>
      <div>
        <h3>Ressources</h3>
        <a href="/solutions-ventilateur-industriel">Solutions</a>
        <a href="/telechargement">Téléchargement &amp; LiveCurve</a>
        <a href="/contact">Contact &amp; devis</a>
      </div>
    </div>
    <div class="foot-note">
      <span>© 2026 Euroventilatori France — Constructeur de ventilateurs industriels</span>
      <span class="foot-legal">
        <a href="/mentions-legales">Mentions légales</a>
        <a href="/vie-privee">Vie privée</a>
        <a href="/privacy">Cookies</a>
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
  title="Actualités d'Euroventilatori - Fabricant de ventilateurs industriels",
  desc="L'actualité d'Euroventilatori France, concepteur et fabricant de ventilateurs industriels à Nivolas-Vermelle : produits, recrutements, conseils métier.",
  h1="Nos actualités",
  kicker="Le fil d'Euroventilatori France",
  ghost="Actus",
  intro="""<p>Produits, conseils métier, vie de l'entreprise&nbsp;: les dernières
nouvelles du fabricant de ventilateurs industriels de Nivolas-Vermelle.</p>""",
  cta='<a class="btn ghost-b" href="https://linkedin.com/company/euroventilatori-france">Nous suivre sur LinkedIn</a>',
  sections=[
    ("Derniers articles",
     ["<b>On recrute notre futur·e alternant·e HSE (H/F)</b> — 16 juillet 2026. Ce n'est pas un poste «&nbsp;café + classeur&nbsp;».",
      "<b>Votre ventilateur, dans votre couleur. Sans rien sacrifier.</b> — 2 juillet 2026.",
      "<b>Pourquoi se contenter du gris standard ?</b> — 15 juin 2026. Un client nous a demandé un ventilateur rose.",
      "<b>La moisson, ce n'est pas la fin du travail. C'est le début de la conservation.</b> — 1 juin 2026.",
      "<b>On ne le voit pas. On ne l'entend pas.</b> — 13 avril 2026. Isolation en laine de roche haute densité sur nos centrifuges.",
      "<b>Ventilation des silos agricoles : la dernière étape qui conditionne toutes les autres</b> — 30 mars 2026.",
      "<i>(Flux complet à raccorder au blog lors de la mise en production.)</i>"]),
  ])

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
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))
for fname, d in P.items():
    m = META.get(fname, dict(nav="", trail=[(d["h1"][:40], None)], related=[]))
    slug = "/" + fname.replace(".html", "")
    sections = "\n".join(sec(h2, paras, *rest) for h2, paras, *rest in d["sections"])
    html = TPL.format(title=d["title"], desc=d["desc"], h1=d["h1"], kicker=d["kicker"],
                      ghost=d["ghost"], intro=d["intro"], cta=d["cta"],
                      sections=sections,
                      nav=nav_html(m["nav"]),
                      breadcrumb=breadcrumb_html(m["trail"]),
                      bcjson=breadcrumb_jsonld(m["trail"]),
                      org=ORG_JSONLD,
                      canonical=SITE + slug,
                      proof=PROOF if m.get("proof", True) else "",
                      related=related_html([R[k] for k in m["related"]]),
                      footer=FOOTER)
    with io.open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    print("OK", fname)
print("Terminé :", len(P), "pages")
