# Procédure — Accès Instagram (Meta Graph API) pour WildLens

> **Objectif :** publier sur `wildlens_arteon` (image + légende + hashtags) et lire les statistiques avec l’API officielle Meta.
> **État au 2026-11-04 :** authentification et lectures réelles validées. Première publication réelle encore à effectuer avec l’accord explicite de JC.
> **Règle :** aucune publication sans `publish --confirm`, après validation de JC.

---

## 1. Configuration active

| Élément | Valeur validée |
|---|---|
| Compte Instagram | `wildlens_arteon` |
| IG User ID | `17841457681553313` |
| App Meta | `Wildlens` — App ID `1742977503435858` |
| Page Facebook | `Intro wildlens` — ID `1400080959860179` |
| Business Portfolio | `Wildlens` — ID `1484716640422165` |
| Graph API | `v26.0` |
| Configuration OAuth active | **Utilisateur** — Config ID `4639447586297242` |
| Ancienne configuration à ne plus utiliser | Système — Config ID `978600488130939` |
| Redirect URI | `https://localhost:8443/callback` |
| Token | Keychain `IG_GRAPH_TOKEN` / compte `wildlens` |
| Durée du token reçu | `5183959` secondes, soit environ 60 jours à partir du 2026-11-04 |

Le token obtenu est déjà un token longue durée : aucun second échange n’a été nécessaire. Son renouvellement n’est pas encore automatisé ni testé ; il faudra renouveler ou refaire l’OAuth avant son expiration.

### Permissions réellement accordées

Vérifiées avec `GET /me/permissions` :

- `instagram_basic` — profil et médias Instagram ;
- `instagram_content_publish` — création de publications ;
- `instagram_manage_insights` — statistiques Instagram ;
- `pages_read_engagement` — lecture de la Page ;
- `pages_show_list` — liste des Pages gérées ;
- `public_profile` — ajouté automatiquement par Meta.

Pendant le consentement, choisir **les éléments actuels uniquement**, puis sélectionner seulement `wildlens_arteon` et `Intro wildlens`. Ne pas donner accès automatiquement aux futurs comptes ou Pages.

---

## 2. Causes des blocages et résolution

1. **Aucune permission n’était rattachée au cas d’utilisation `INSTAGRAM_BUSINESS`.** Les cinq permissions ont été ajoutées dans **Cas d’utilisation → Gérer les messages et les contenus sur Instagram → Personnaliser → Autorisations et fonctionnalités**. Elles sont toutes « Prête pour le test ».
2. **Instagram Login direct est indisponible pour cette app récente.** Meta impose **API setup with Unified login / Facebook Login for Business**, avec un `config_id`.
3. **La configuration avec token système est une impasse pour ce projet.** Elle demandait le contrôle total de la Page par le portefeuille et ajoutait un Dataset inutile. Elle a été conservée dans Meta mais n’est plus utilisée.
4. **La configuration utilisateur résout ces deux problèmes.** Variante `General`, token `user`, aucun actif professionnel dans la configuration elle-même, et les cinq permissions ci-dessus. Les actifs sont choisis pendant le consentement.
5. **Le champ `account_type` est refusé sur ce compte avec cette connexion.** Il a été retiré de la commande `account` ; les champs `id,username,media_count` fonctionnent.

Le projet n’est donc plus arrêté par la configuration Meta.

---

## 3. Rejouer l’autorisation OAuth

Cette section sert au renouvellement ou à une réinstallation. Elle n’est pas nécessaire pour l’usage courant tant que le token est valide.

1. Dans **Facebook Login for Business → Paramètres**, conserver Client OAuth, Web OAuth, HTTPS et le mode strict activés. L’URI `https://localhost:8443/callback` est enregistrée.
2. Dans **Facebook Login for Business → Configurations**, utiliser `WildLens Instagram utilisateur`, Config ID `4639447586297242`.
3. Générer un état OAuth aléatoire et démarrer un récepteur HTTPS local qui vérifie cet état. Le récepteur doit échanger le code avec `IG_APP_SECRET`, puis écrire le token directement dans le Keychain, sans journaliser le code ni le token.
4. Ouvrir dans la session Facebook authentifiée :

```text
https://www.facebook.com/v26.0/dialog/oauth?client_id=1742977503435858&redirect_uri=https%3A%2F%2Flocalhost%3A8443%2Fcallback&config_id=4639447586297242&state=<ETAT_ALEATOIRE>&response_type=code&override_default_response_type=true
```

5. Sélectionner uniquement la Page et le compte Instagram actuels, vérifier le récapitulatif, puis laisser JC cliquer sur **Enregistrer**.
6. Récupérer l’IG User ID via la Page avec les champs `id,name,instagram_business_account{id,username}` et le token transmis en en-tête `Authorization: Bearer`.
7. Stocker l’identifiant dans le Keychain `IG_USER_ID` / compte `wildlens`.

Les certificats locaux utilisés pour l’OAuth du 2026-11-04 ont été supprimés après usage. Ne pas conserver de code OAuth ou de token dans les logs, la documentation ou l’historique shell.

---

## 4. Utilisation du script

Script : `scripts/instagram_post.py`. Les secrets sont lus depuis le Keychain ; ils ne sont pas affichés.

```bash
[M5] PYTHONDONTWRITEBYTECODE=1 python3 scripts/instagram_post.py account
[M5] PYTHONDONTWRITEBYTECODE=1 python3 scripts/instagram_post.py media --limit 5
[M5] PYTHONDONTWRITEBYTECODE=1 python3 scripts/instagram_post.py insights --media-id <MEDIA_ID>
[M5] PYTHONDONTWRITEBYTECODE=1 python3 scripts/instagram_post.py media --limit 5 --with-insights
```

### Résultats réellement vérifiés

`account` renvoie :

```json
{
  "id": "17841457681553313",
  "media_count": 0,
  "username": "wildlens_arteon"
}
```

`media --limit 5` répond correctement avec une liste vide : le compte ne contient encore aucune publication.

Les métriques insights configurées sont `reach,likes,comments,shares,saved`. Leur compatibilité réelle reste à vérifier sur un média existant.

---

## 5. Publication : simulation et accord explicite

Le flux implémenté est : création du conteneur → attente de `FINISHED` → publication. Il a été validé avec des réponses Meta simulées, sans réseau. La publication réelle n’a pas encore été testée.

Simulation locale, sans aucun appel réseau :

```bash
[M5] PYTHONDONTWRITEBYTECODE=1 python3 scripts/instagram_post.py publish --image-url https://example.com/robin.jpg --caption "WildLens — simulation #wildlens"
```

Après validation explicite du JPEG, de la légende et de l’URL publique par JC :

```bash
[M5] PYTHONDONTWRITEBYTECODE=1 python3 scripts/instagram_post.py publish --image-url <URL_HTTPS_PUBLIQUE_DU_JPEG> --caption-file <FICHIER_LEGENDE> --confirm
```

Contraintes : JPEG accessible en HTTPS public, légende de 2200 caractères maximum. Le lien cliquable se place dans la bio, pas dans la légende.

---

## 6. Reste à faire pour le post d’ouverture

Le kit éditorial est `JCH_Inbox/03_PROJECTS/02_ARTEON/wildlens/instagram-launch-kit.md`.

1. **JPEG corrigé validé visuellement par JC le 2026-11-04.** Le fichier `/Users/jchavauxm5/Desktop/LrC To /Dobby select/LrC to-27.jpg` représente une statue : ce n’est pas le rouge-gorge du kit. Ne pas l’utiliser ni appliquer au nouveau candidat le recadrage autorisé pour cette statue. La bonne source est `/Users/jchavauxm5/Desktop/LrC To /LrC to-27.jpg` (3723 × 2633). Son dérivé `tmp/wildlens-instagram-opening/robin.jpg` a été vérifié : rouge-gorge dans la neige, image entière sans recadrage, JPEG sRGB 1440 × 1018, 292415 octets, avec seulement les métadonnées `Artist: JC Havaux / ARTEON` et `Copyright: © JC Havaux / ARTEON`. Il respecte les contraintes Meta : JPEG, sRGB, largeur de 320 à 1440 px, ratio entre 4:5 et 1,91:1, maximum 8 Mo.
2. **JPEG hébergé dans un dépôt GitHub public séparé.** `https://github.com/JCHYTECH/wildlens-assets` contient uniquement `robin.jpg` sur `main`. URL vérifiée : `https://raw.githubusercontent.com/JCHYTECH/wildlens-assets/main/robin.jpg` renvoie HTTP 200 et `image/jpeg`. Son empreinte SHA-256 `e536ba6987867ba284f886d6cbabf67f46920d2bfa0efe9969b6d8eaf1e5c780` est identique à celle du JPEG local. Aucun contenu de `PKA_JCH` ne doit être ajouté à ce dépôt.
3. **Ne pas annoncer de lien Ghost dans le premier post.** `https://wildlens.ghost.io/` renvoie actuellement HTTP 404 ; l’appel « Full story → link in bio » a été retiré de la légende. Le chantier Ghost reste distinct et n’est pas ouvert par cette publication.
4. **Simulation validée sans réseau.** La commande `publish` avec cette URL et la légende `tmp/wildlens-instagram-opening/caption.txt` a renvoyé `network_requests: 0` et `caption_characters: 527`. Cette simulation ne sollicite ni Meta ni Instagram.
5. **Publication non effectuée par choix de JC.** Lors de la demande explicite du 2026-11-04, JC a choisi « Ne pas publier » pour cette image, cette légende et cette URL. La préparation est terminée, mais `publish --confirm` ne doit être exécuté que sur une nouvelle demande explicite de JC. L’autorisation d’héberger l’image ne vaut pas autorisation de publier.
6. Vérifier le média publié avec `media`, puis tester `insights` sur son identifiant. En cas d’échec, vérifier d’abord les médias récents pour éviter tout doublon ; ne jamais republier pour tester les statistiques.

Aucune publication Instagram n’a été créée pendant la configuration et les contrôles en lecture.
