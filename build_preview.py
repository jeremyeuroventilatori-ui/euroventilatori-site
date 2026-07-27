# -*- coding: utf-8 -*-
"""Construit l'aperçu navigable publié en Artifact.

Le dépôt reste la source de vérité. Un Artifact étant un fichier unique, ce
script embarque les 15 pages dans un même document et les commute côté
navigateur : le menu conduit bien à des pages distinctes, chacune avec son
fil d'Ariane, son contenu et ses pages liées — comme en production.

Lancer après toute modification :  python build_preview.py
"""
import io, os, re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join("..", "maquette-euroventilatori-tendance.html")

PAGES = [
    ("index", "Accueil"),
    ("ventilateurs", "Nos produits"),
    ("ventilateur-gamme", "Ventilateurs de gamme"),
    ("ventilateur-sur-mesure", "Ventilateurs sur mesure"),
    ("solutions-ventilateur-industriel", "Solutions"),
    ("caissons-insonorises", "Acoustique"),
    ("purificateur-air", "Filtration"),
    ("nos-autres-accessoires", "Accessoires"),
    ("bureau-etudes", "Bureau d'études"),
    ("qui-sommes-nous", "Qui sommes-nous ?"),
    ("competences", "Compétences"),
    ("secteurs-activite", "Secteurs d'activité"),
    ("telechargement", "Téléchargement"),
    ("contact", "Contact"),
    ("actualites", "Actualités"),
]
SLUGS = {s for s, _ in PAGES}


def lire(nom):
    return io.open(nom + ".html", encoding="utf-8").read()


def entre(txt, debut, fin):
    """Bloc délimiteurs compris (ex. <header>…</header>)."""
    i = txt.index(debut)
    j = txt.index(fin, i) + len(fin)
    return txt[i:j]


def dedans(txt, debut, fin):
    """Contenu strictement entre les délimiteurs — sans les délimiteurs.
    Indispensable pour le script : réinclure « <script> » créerait une balise
    imbriquée qui coupe le script en deux sans lever d'erreur."""
    i = txt.index(debut) + len(debut)
    return txt[i:txt.index(fin, i)]


def router_liens(html):
    """Les liens internes pilotent le routeur ; le reste est neutralisé."""
    def sub(m):
        url = m.group(1)
        slug = "index" if url == "/" else url.lstrip("/")
        if slug in SLUGS:
            return 'href="#" data-goto="%s"' % slug
        return 'href="#" data-absent="%s"' % url   # mentions légales, etc.
    return re.sub(r'href="(/[^"#]*)"', sub, html)


index = lire("index")
css = io.open(os.path.join("assets", "styles.css"), encoding="utf-8").read()

header = entre(index, "<header>", "</header>")
footer = entre(index, '<footer class="site">', "</footer>")
script_index = dedans(index, "<script>\n(function(){", "</script>")
accueil = index[index.index("</header>") + len("</header>"):
                index.index('<footer class="site">')]
# L'accueil a son propre <main id="contenu"> ; l'apercu fournit le sien,
# on retire donc l'enveloppe pour ne pas imbriquer deux reperes <main>.
accueil = re.sub(r'</?main[^>]*>', "", accueil)

# --- Composition des pages -------------------------------------------------
blocs = ['<div class="pv-page" data-page="index" data-nav="">%s</div>' % accueil]
for slug, _ in PAGES[1:]:
    src = lire(slug)
    main = dedans(src, '<main id="contenu">', "</main>")
    # La rubrique de menu à surligner est déjà calculée par gen_pages.py :
    # on la relit dans l'en-tête de la page plutôt que de la redéclarer ici.
    m = re.search(r'<a href="/([^"]*)"[^>]*aria-current="page"', dedans(src, "<header>", "</header>"))
    blocs.append('<div class="pv-page" data-page="%s" data-nav="%s" hidden>%s</div>'
                 % (slug, m.group(1) if m else "", main))

pages_html = "\n".join(blocs)

# --- Routeur ---------------------------------------------------------------
ROUTEUR = """
/* ---------- Routeur d'aperçu : commute les pages embarquées ---------- */
(function(){
  var pages = document.querySelectorAll(".pv-page");
  var nav = document.querySelectorAll("nav.main [data-goto]");
  function aller(slug, dedansPage){
    var rubrique = null;
    pages.forEach(function(p){
      var actif = p.getAttribute("data-page") === slug;
      p.hidden = !actif;
      if (actif) rubrique = p.getAttribute("data-nav") || slug;
    });
    if (rubrique === null) return;          /* slug inconnu : on ne bouge pas */
    /* Une sous-page surligne la rubrique dont elle dépend, pas elle-même */
    nav.forEach(function(a){
      a.getAttribute("data-goto") === rubrique
        ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current");
    });
    if (!dedansPage) scrollTo({ top: 0, behavior: "instant" });
    /* réveille les éléments révélés au défilement de la page affichée */
    dispatchEvent(new Event("scroll"));
  }
  document.addEventListener("click", function(e){
    var a = e.target.closest("[data-goto], [data-absent]");
    if (!a) return;
    e.preventDefault();
    var slug = a.getAttribute("data-goto");
    if (slug) aller(slug);
  });
  /* Le logo ramène à l'accueil */
  var logo = document.querySelector("header .logo");
  if (logo) logo.addEventListener("click", function(e){ e.preventDefault(); aller("index"); });
})();
"""

CSS_APERCU = """
/* ---------- Aperçu multi-pages ---------- */
.pv-page[hidden]{ display:none }
[data-absent]{ cursor:default }
"""

# Assemblage par concaténation : le JavaScript est truffé d'accolades, un
# gabarit à substitution les confondrait avec ses propres marqueurs.
doc = (
    "<title>Euroventilatori France — Ventilation industrielle près de Lyon</title>\n"
    '<meta name="description" content="Constructeur de ventilateurs industriels '
    "centrifuges et hélicoïdaux : bureau d'études intégré, devis sous 24 h, "
    'intervention partout en France depuis la région lyonnaise.">\n'
    "<style>\n" + css + CSS_APERCU + "\n</style>\n"
    '<canvas id="airCanvas" aria-hidden="true"></canvas>\n'
    '<a class="skip-link" href="#contenu">Aller au contenu</a>\n'
    + router_liens(header) + '\n<main id="contenu">\n'
    + router_liens(pages_html) + "\n</main>\n"
    + router_liens(footer) + "\n"
    "<script>\n(function(){" + script_index + ROUTEUR + "\n</script>\n"
)

io.open(OUT, "w", encoding="utf-8").write(doc)
print("Aperçu navigable :", len(PAGES), "pages -", len(doc) // 1024, "Ko")
print(os.path.abspath(OUT))
