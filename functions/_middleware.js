/* Protection de tout ce qui n'est pas la production.
 *
 * Le `noindex` ne peut pas vivre dans le HTML : préproduction et production
 * servent les mêmes fichiers, et le jour de la bascule la production
 * hériterait de l'interdiction d'indexation.
 *
 * Il est donc posé ici, en fonction du NOM D'HÔTE. Cela couvre trois cas :
 *   - preprod.euroventilatori.fr        (la préproduction)
 *   - <projet>.pages.dev                (l'adresse Cloudflare, publique par
 *                                        défaut et indexable — piège courant)
 *   - toute adresse de déploiement de branche
 *
 * Conséquence : le jour J se résume à un changement DNS. Aucun fichier à
 * modifier, aucun redéploiement, donc aucune fenêtre de risque.
 */

const HOTES_PRODUCTION = ["www.euroventilatori.fr", "euroventilatori.fr"];

export async function onRequest(context) {
  const reponse = await context.next();
  const hote = new URL(context.request.url).hostname;

  if (!HOTES_PRODUCTION.includes(hote)) {
    // En-tête HTTP : compris par Google, Bing et les robots des moteurs IA,
    // y compris sur les fichiers non-HTML (PDF, images).
    const entetes = new Headers(reponse.headers);
    entetes.set("X-Robots-Tag", "noindex, nofollow");
    return new Response(reponse.body, {
      status: reponse.status,
      statusText: reponse.statusText,
      headers: entetes,
    });
  }
  return reponse;
}
