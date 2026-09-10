/* Point d'entrée unique du site — fonctionne sur Cloudflare Workers ET sur
 * Cloudflare Pages (mode avancé). Les deux plateformes exposent la même API :
 * `env.ASSETS.fetch(request)` sert les fichiers statiques.
 *
 * Pourquoi un seul fichier plutôt que le dossier `functions/` : celui-ci est
 * propre à Pages et reste inerte sur Workers — c'est ce qui a laissé la
 * préproduction indexable. Ce fichier, lui, s'exécute dans les deux cas.
 *
 * En contrepartie, `_headers` et `_redirects` ne sont pas appliqués
 * automatiquement dans ce mode : les en-têtes et les redirections sont donc
 * posés ici, ce qui a l'avantage d'être déterministe.
 *
 * Il assure quatre choses :
 *   1. le verrou d'indexation, selon le nom d'hôte ;
 *   2. les redirections permanentes des anciennes URL ;
 *   3. les en-têtes de sécurité et de cache ;
 *   4. la réception du formulaire de contact.
 */

/* ------------------------------------------------------------------ */
/* 1. Verrou d'indexation                                              */
/* ------------------------------------------------------------------ */

const HOTES_PRODUCTION = ["www.euroventilatori.fr", "euroventilatori.fr"];

const ROBOTS_INTERDIT = `# Préproduction — ne pas indexer.
User-agent: *
Disallow: /
`;

/* ------------------------------------------------------------------ */
/* 2. Redirections permanentes                                         */
/* ------------------------------------------------------------------ */

const REDIRECTIONS = {
  "/outils": "/telechargement",
  "/calculs": "/telechargement",
  "/privacy": "/vie-privee",
};

/* ------------------------------------------------------------------ */
/* 3. En-têtes                                                         */
/* ------------------------------------------------------------------ */

const SECURITE = {
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "X-Frame-Options": "SAMEORIGIN",
  "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
  "Strict-Transport-Security": "max-age=31536000",
  "Content-Security-Policy":
    "default-src 'self'; " +
    "script-src 'self' 'unsafe-inline' https://challenges.cloudflare.com; " +
    "style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; " +
    "connect-src 'self'; form-action 'self'; " +
    "frame-src https://challenges.cloudflare.com; frame-ancestors 'self'; base-uri 'self'",
};

function cachePour(chemin) {
  // Les assets portent une empreinte de contenu dans leur URL : on peut les
  // garder longtemps. Le HTML, lui, doit être revalidé à chaque visite.
  if (chemin.startsWith("/assets/")) return "public, max-age=31536000, immutable";
  if (chemin.startsWith("/favicon.")) return "public, max-age=604800";
  return "public, max-age=0, must-revalidate";
}

function habiller(reponse, chemin, estProduction) {
  const entetes = new Headers(reponse.headers);
  for (const [cle, valeur] of Object.entries(SECURITE)) entetes.set(cle, valeur);
  entetes.set("Cache-Control", cachePour(chemin));
  if (!estProduction) {
    entetes.set("X-Robots-Tag", "noindex, nofollow, noarchive, nosnippet");
  }
  return new Response(reponse.body, {
    status: reponse.status,
    statusText: reponse.statusText,
    headers: entetes,
  });
}

/* ------------------------------------------------------------------ */
/* 4. Formulaire de contact                                            */
/* ------------------------------------------------------------------ */

const LIMITE = 5000;
const MINIMUM_SECONDES = 3;

const texte = (v, max = 200) => String(v || "").trim().slice(0, max);
const echapper = (s) =>
  String(s).replace(/[<>&]/g, (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;" }[c]));

async function verifierTurnstile(jeton, secret, ip) {
  if (!secret) return true;                 // pas encore configuré
  const corps = new FormData();
  corps.append("secret", secret);
  corps.append("response", jeton || "");
  if (ip) corps.append("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify",
    { method: "POST", body: corps });
  return (await r.json()).success === true;
}

async function envoyerBrevo(cle, charge) {
  const r = await fetch("https://api.brevo.com/v3/smtp/email", {
    method: "POST",
    headers: { "api-key": cle, "content-type": "application/json", accept: "application/json" },
    body: JSON.stringify(charge),
  });
  if (!r.ok) throw new Error("Brevo " + r.status + " " + (await r.text()).slice(0, 200));
}

async function traiterContact(request, env) {
  const repondre = (ok, message, code = 200) =>
    new Response(JSON.stringify({ ok, message }), {
      status: code,
      headers: { "content-type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
    });

  try {
    const form = await request.formData();

    // Pot de miel : un champ invisible que seuls les robots remplissent.
    if (texte(form.get("societe_bis"))) return repondre(true, "Demande envoyée.");

    // Délai de remplissage : un envoi instantané n'est pas humain.
    // On ne conclut que sur un écart plausible. L'horodatage vient du poste du
    // visiteur et se compare à l'heure du serveur : une horloge en avance donne
    // un écart négatif. Traiter ce cas comme un robot ferait disparaître
    // silencieusement la demande d'un client réel — bien pire que de laisser
    // passer un robot, que Turnstile arrêtera de toute façon.
    const depart = parseInt(form.get("t0") || "0", 10);
    const ecoule = depart ? (Date.now() - depart) / 1000 : null;
    if (ecoule !== null && ecoule >= 0 && ecoule < MINIMUM_SECONDES) {
      return repondre(true, "Demande envoyée.");
    }

    const okRobot = await verifierTurnstile(
      form.get("cf-turnstile-response"),
      env.TURNSTILE_SECRET,
      request.headers.get("CF-Connecting-IP"));
    if (!okRobot) {
      return repondre(false, "Vérification anti-robot échouée. Rechargez la page et réessayez.", 400);
    }

    const nom = texte(form.get("nom"));
    const email = texte(form.get("email"), 150);
    const telephone = texte(form.get("telephone"), 40);
    const message = texte(form.get("message"), LIMITE);
    const contexte = texte(form.get("contexte"), 400);   // pré-rempli par le sélecteur

    if (!nom || !email || !message) {
      return repondre(false, "Merci de renseigner votre nom, votre e-mail et votre besoin.", 400);
    }
    if (!/^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(email)) {
      return repondre(false, "L'adresse e-mail ne semble pas valide.", 400);
    }

    if (!env.BREVO_API_KEY || !env.DESTINATAIRE || !env.EXPEDITEUR) {
      console.log("Formulaire reçu mais envoi non configuré :", { nom, email, telephone, contexte });
      return repondre(false,
        "Le formulaire n'est pas encore raccordé. Écrivez-nous à contact@euroventilatori-france.com "
        + "ou appelez le 04 74 43 68 38.", 503);
    }

    await envoyerBrevo(env.BREVO_API_KEY, {
      sender: { name: "Site Euroventilatori France", email: env.EXPEDITEUR },
      to: [{ email: env.DESTINATAIRE }],
      replyTo: { email, name: nom },
      subject: "Demande depuis le site — " + nom,
      htmlContent:
        "<p><b>Nom / société :</b> " + echapper(nom) + "</p>" +
        "<p><b>E-mail :</b> " + echapper(email) + "</p>" +
        (telephone ? "<p><b>Téléphone :</b> " + echapper(telephone) + "</p>" : "") +
        (contexte ? "<p><b>Point de fonctionnement :</b> " + echapper(contexte) + "</p>" : "") +
        "<p><b>Besoin :</b><br>" + echapper(message).replace(/\n/g, "<br>") + "</p>",
    });

    // L'accusé est un confort : son échec ne doit pas masquer une demande reçue.
    try {
      await envoyerBrevo(env.BREVO_API_KEY, {
        sender: { name: "Euroventilatori France", email: env.EXPEDITEUR },
        to: [{ email, name: nom }],
        subject: "Votre demande est bien arrivée — Euroventilatori France",
        htmlContent:
          "<p>Bonjour,</p><p>Nous avons bien reçu votre demande et un technicien vous "
          + "répond rapidement. Pour un ventilateur de gamme comme pour une machine sur "
          + "mesure, notre engagement est un devis détaillé sous 24 heures.</p>"
          + "<p>Pour toute précision : 04 74 43 68 38.</p>"
          + "<p>— L'équipe Euroventilatori France</p>"
          + "<hr><p style=\"color:#666;font-size:13px\">Rappel de votre message :<br>"
          + echapper(message).replace(/\n/g, "<br>") + "</p>",
      });
    } catch (e) {
      console.log("Accusé de réception non envoyé :", e.message);
    }

    return repondre(true, "Votre demande est bien partie. Un technicien vous répond rapidement.");
  } catch (e) {
    console.log("Erreur formulaire :", e && e.message);
    return repondre(false,
      "L'envoi a échoué. Écrivez-nous à contact@euroventilatori-france.com "
      + "ou appelez le 04 74 43 68 38.", 500);
  }
}

/* ------------------------------------------------------------------ */
/* Entrée                                                              */
/* ------------------------------------------------------------------ */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const chemin = url.pathname;
    const estProduction = HOTES_PRODUCTION.includes(url.hostname);

    // Formulaire.
    if (chemin === "/api/contact") {
      if (request.method !== "POST") {
        return new Response("Méthode non autorisée", { status: 405 });
      }
      return traiterContact(request, env);
    }

    // Verrou d'indexation : robots.txt restrictif hors production.
    if (!estProduction && chemin === "/robots.txt") {
      return new Response(ROBOTS_INTERDIT, {
        headers: {
          "content-type": "text/plain; charset=utf-8",
          "cache-control": "no-store",
          "X-Robots-Tag": "noindex, nofollow",
        },
      });
    }

    // Redirections permanentes des anciennes URL.
    const cible = REDIRECTIONS[chemin.replace(/\/+$/, "")];
    if (cible) {
      return Response.redirect(url.origin + cible, 301);
    }

    // Fichiers statiques, habillés de leurs en-têtes.
    const reponse = await env.ASSETS.fetch(request);
    return habiller(reponse, chemin, estProduction);
  },
};
