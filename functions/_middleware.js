/* Verrou d'indexation — seule la production peut être indexée.
 *
 * Le `noindex` ne peut pas vivre dans le HTML : préproduction et production
 * servent les mêmes fichiers, et le jour de la bascule la production
 * hériterait de l'interdiction.
 *
 * Il est donc posé ici en fonction du NOM D'HÔTE, avec deux verrous :
 *   1. un robots.txt qui interdit tout — les robots respectueux ne demandent
 *      même pas les pages ;
 *   2. un en-tête X-Robots-Tag sur chaque réponse — il s'applique même si le
 *      robots.txt a été ignoré ou gardé en cache, et couvre les fichiers
 *      non-HTML.
 *
 * Restent hors moteurs en permanence :
 *   - euroventilatori-preprod.pages.dev  (adresse technique du projet,
 *     publique et indexable par défaut — piège courant)
 *   - preprod.euroventilatori.fr et toute adresse de déploiement de branche
 *
 * L'indexation s'ouvre UNIQUEMENT quand le domaine de production est rattaché
 * au projet et que le DNS l'y amène. Aucun fichier à modifier le jour J : donc
 * aucun risque d'oublier de retirer — ni de remettre — la protection.
 */

const HOTES_PRODUCTION = ["www.euroventilatori.fr", "euroventilatori.fr"];

const ROBOTS_INTERDIT = `# Préproduction — ne pas indexer.
User-agent: *
Disallow: /
`;

export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (HOTES_PRODUCTION.includes(url.hostname)) {
    return context.next();          // production : rien à ajouter
  }

  // Verrou 1 — robots.txt restrictif, servi à la place du vrai.
  if (url.pathname === "/robots.txt") {
    return new Response(ROBOTS_INTERDIT, {
      headers: {
        "content-type": "text/plain; charset=utf-8",
        "cache-control": "no-store",
        "X-Robots-Tag": "noindex, nofollow",
      },
    });
  }

  // Verrou 2 — l'en-tête, sur toutes les réponses.
  const reponse = await context.next();
  const entetes = new Headers(reponse.headers);
  entetes.set("X-Robots-Tag", "noindex, nofollow, noarchive, nosnippet");
  return new Response(reponse.body, {
    status: reponse.status,
    statusText: reponse.statusText,
    headers: entetes,
  });
}
