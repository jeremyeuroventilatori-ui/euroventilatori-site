/* Réception du formulaire de contact.
 *
 * Chaîne : le navigateur envoie ici → on vérifie que ce n'est pas un robot →
 * on transmet la demande par Brevo à l'équipe → on envoie un accusé de
 * réception au demandeur → on répond au navigateur, qui affiche le résultat
 * sans recharger la page.
 *
 * Variables d'environnement à renseigner dans Cloudflare Pages
 * (Réglages → Variables et secrets) :
 *   BREVO_API_KEY        clé API Brevo (secret)
 *   TURNSTILE_SECRET     clé privée Turnstile (secret)
 *   DESTINATAIRE         contact@euroventilatori-france.com
 *   EXPEDITEUR           une adresse du domaine authentifié chez Brevo,
 *                        par exemple site@euroventilatori-france.com
 *
 * Tant que ces variables sont absentes, la fonction répond proprement au lieu
 * de casser : le message est journalisé et l'utilisateur reçoit une erreur
 * explicite plutôt qu'une page blanche.
 */

const LIMITE = 5000;              // taille maximale d'un champ
const MINIMUM_SECONDES = 3;       // un humain met plus de 3 s à remplir

function texte(valeur, max = 200) {
  return String(valeur || "").trim().slice(0, max);
}

function echapper(s) {
  return String(s).replace(/[<>&]/g, (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;" }[c]));
}

async function verifierTurnstile(jeton, secret, ip) {
  if (!secret) return true;                 // pas encore configuré : on laisse passer
  const corps = new FormData();
  corps.append("secret", secret);
  corps.append("response", jeton || "");
  if (ip) corps.append("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify",
    { method: "POST", body: corps });
  const d = await r.json();
  return d.success === true;
}

async function envoyerBrevo(cle, charge) {
  const r = await fetch("https://api.brevo.com/v3/smtp/email", {
    method: "POST",
    headers: { "api-key": cle, "content-type": "application/json", accept: "application/json" },
    body: JSON.stringify(charge),
  });
  if (!r.ok) throw new Error("Brevo " + r.status + " " + (await r.text()).slice(0, 200));
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const repondre = (ok, message, code = 200) =>
    new Response(JSON.stringify({ ok, message }), {
      status: code,
      headers: { "content-type": "application/json; charset=utf-8" },
    });

  try {
    const form = await request.formData();

    /* --- Filtres anti-robots ------------------------------------------- */
    // 1. Pot de miel : un champ invisible que seuls les robots remplissent.
    if (texte(form.get("societe_bis"))) return repondre(true, "Demande envoyée.");

    // 2. Délai de remplissage : un envoi instantané n'est pas humain.
    const depart = parseInt(form.get("t0") || "0", 10);
    if (depart && (Date.now() - depart) / 1000 < MINIMUM_SECONDES) {
      return repondre(true, "Demande envoyée.");
    }

    // 3. Turnstile.
    const okRobot = await verifierTurnstile(
      form.get("cf-turnstile-response"),
      env.TURNSTILE_SECRET,
      request.headers.get("CF-Connecting-IP"));
    if (!okRobot) return repondre(false, "Vérification anti-robot échouée. Rechargez la page et réessayez.", 400);

    /* --- Champs --------------------------------------------------------- */
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

    /* --- Configuration incomplète : on le dit franchement --------------- */
    if (!env.BREVO_API_KEY || !env.DESTINATAIRE || !env.EXPEDITEUR) {
      console.log("Formulaire reçu mais envoi non configuré :", { nom, email, telephone, contexte, message });
      return repondre(false,
        "Le formulaire n'est pas encore raccordé. Écrivez-nous à contact@euroventilatori-france.com ou appelez le 04 74 43 68 38.",
        503);
    }

    /* --- Message à l'équipe --------------------------------------------- */
    const corpsEquipe =
      "<p><b>Nom / société :</b> " + echapper(nom) + "</p>" +
      "<p><b>E-mail :</b> " + echapper(email) + "</p>" +
      (telephone ? "<p><b>Téléphone :</b> " + echapper(telephone) + "</p>" : "") +
      (contexte ? "<p><b>Point de fonctionnement :</b> " + echapper(contexte) + "</p>" : "") +
      "<p><b>Besoin :</b><br>" + echapper(message).replace(/\n/g, "<br>") + "</p>";

    await envoyerBrevo(env.BREVO_API_KEY, {
      sender: { name: "Site Euroventilatori France", email: env.EXPEDITEUR },
      to: [{ email: env.DESTINATAIRE }],
      replyTo: { email, name: nom },
      subject: "Demande depuis le site — " + nom,
      htmlContent: corpsEquipe,
    });

    /* --- Accusé de réception au demandeur -------------------------------- */
    try {
      await envoyerBrevo(env.BREVO_API_KEY, {
        sender: { name: "Euroventilatori France", email: env.EXPEDITEUR },
        to: [{ email, name: nom }],
        subject: "Votre demande est bien arrivée — Euroventilatori France",
        htmlContent:
          "<p>Bonjour,</p><p>Nous avons bien reçu votre demande et un technicien " +
          "vous répond rapidement. Pour un ventilateur de gamme comme pour une " +
          "machine sur mesure, notre engagement est un devis détaillé sous 24 heures.</p>" +
          "<p>Pour toute précision : 04 74 43 68 38.</p>" +
          "<p>— L'équipe Euroventilatori France</p>" +
          "<hr><p style=\"color:#666;font-size:13px\">Rappel de votre message :<br>" +
          echapper(message).replace(/\n/g, "<br>") + "</p>",
      });
    } catch (e) {
      // L'accusé est un confort : son échec ne doit pas masquer une demande reçue.
      console.log("Accusé de réception non envoyé :", e.message);
    }

    return repondre(true, "Votre demande est bien partie. Un technicien vous répond rapidement.");
  } catch (e) {
    console.log("Erreur formulaire :", e && e.message);
    return repondre(false,
      "L'envoi a échoué. Écrivez-nous à contact@euroventilatori-france.com ou appelez le 04 74 43 68 38.",
      500);
  }
}
