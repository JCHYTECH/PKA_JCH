# Procédure — Accès Instagram (Meta Graph API) pour WildLens

> **Objectif :** donner à Dobby 🦉 la capacité de publier sur le compte Instagram WildLens (image + légende + hashtags) et de lire les stats.
> **Préparé par :** Dobby 🦉 — 2026-10-24.
> **Voie retenue :** API officielle Meta (Instagram Platform / Graph API) — conforme CGU, pas de risque de ban.
> **Sources :** Meta Developer Docs (Instagram Platform, Content Publishing) · Postproxy (2026) · Outstand (2026).

---

## Vue d'ensemble

- L'API ne fonctionne qu'avec des comptes **Professionnels** (Creator ou Business). Un compte personnel est **exclu**.
- La publication suit un **modèle à conteneur** : créer un conteneur média → vérifier son statut (`FINISHED`) → publier.
- Token : courte durée (~1 h) → échangé contre **longue durée (~60 j, renouvelable)**.
- ⚠️ L'ancienne « Instagram Basic Display API » est **dépréciée** (arrêt sept. 2024) — on utilise la **Graph API**.

---

## Prérequis (à avoir)

1. Le compte Instagram WildLens (à créer, cf. `instagram-launch-kit.md`).
2. Un compte **Facebook** (pour se connecter à Meta for Developers).
3. (Recommandé) une **Page Facebook** liée à Instagram — obligatoire pour un compte Business, pas toujours pour un Creator.

---

## Étape 1 — Convertir le compte en Creator

1. Instagram → Paramètres → **Type de compte et outils** → « Passer en compte professionnel ».
2. Choisir **Créateur** (Creator) — publication directe plus simple, sans Page obligatoire.
3. Catégorie suggérée : « Photographe » ou « Magazine ».

---

## Étape 2 — Créer l'app Meta

1. Aller sur **https://developers.facebook.com** → se connecter (compte Facebook).
2. Créer un compte développeur (accepter les conditions).
3. **Créer une app** → type « Entreprise » (Business).
4. Noter l'**App ID** et l'**App Secret** (Tableau de bord → Paramètres → Général).

---

## Étape 3 — Ajouter le produit Instagram

1. Dans l'app : « Ajouter un produit » → **Instagram** (ou « Instagram Graph API »).
2. Suivre l'assistant pour lier le compte Instagram (login Instagram).

---

## Étape 4 — Lier le compte et générer le token

1. Menu Instagram de l'app → **Comptes de test Instagram** (ou « API Setup with Instagram Login »).
2. Ajouter le compte WildLens comme **testeur**.
3. Générer un **token d'accès** (courte durée) via le login Instagram.

> Pour publier **sur son propre compte**, l'« Accès standard » (mode développement + compte test) suffit — pas besoin d'App Review complète tant qu'on ne publie que pour nous-mêmes.

---

## Étape 5 — Permissions

S'assurer que le token / l'app dispose de :
- `instagram_basic` — lire profil et médias.
- `instagram_content_publish` — publier.
- `instagram_manage_insights` — lire les stats (pour le rapport hebdo).

---

## Étape 6 — Token longue durée (60 j)

Échanger le token courte durée contre un token 60 j :

```bash
curl -X GET "https://graph.facebook.com/{API_VERSION}/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={TOKEN_COURT}"
```

→ Réponse : `access_token` longue durée (~60 j). Renouvelable dès 24 h d'ancienneté, avant expiration.

> `{API_VERSION}` = version courante de la Graph API (affichée dans l'Explorateur Graph API de Meta).

---

## Étape 7 — Stocker le token dans PKA

```bash
[M5] security add-generic-password -s "IG_GRAPH_TOKEN" -a "wildlens" -w "{TOKEN}"
```

Même pattern que la clé OpenRouter (`~/.config/pka-jch/openrouter_key.txt`).

---

## Étape 8 — Récupérer l'IG_USER_ID

```bash
curl -X GET "https://graph.facebook.com/{API_VERSION}/me?fields=id,username&access_token={TOKEN}"
# ou, si via Page :
curl -X GET "https://graph.facebook.com/{API_VERSION}/me/accounts?access_token={TOKEN}"
```

---

## Étape 9 — Ce que Dobby build ensuite

`scripts/instagram_post.py` — publie image + légende (3 appels) :

```bash
# 1. Créer le conteneur média
curl -X POST "https://graph.facebook.com/{API_VERSION}/{IG_USER_ID}/media" \
  -d "image_url={URL_IMAGE}" -d "caption={LEGENDE}" -d "access_token={TOKEN}"

# 2. Vérifier le statut (attendre FINISHED)
curl -X GET "https://graph.facebook.com/{API_VERSION}/{CONTAINER_ID}?fields=status_code&access_token={TOKEN}"

# 3. Publier
curl -X POST "https://graph.facebook.com/{API_VERSION}/{IG_USER_ID}/media_publish" \
  -d "creation_id={CONTAINER_ID}" -d "access_token={TOKEN}"
```

**Contraintes à connaître :**
- Images **JPEG uniquement** (pas de PNG).
- Le **lien** se met en **bio**, pas dans le post (pas de lien cliquable dans la légende).
- Carrousel : jusqu'à 10 médias.

---

## Récap — actions JC (manuelles)

1. Créer le compte Instagram + le passer en **Creator**.
2. Créer l'app Meta (developers.facebook.com) — type Business.
3. Lier Instagram à l'app + générer le token.
4. Échanger vers le token 60 j + le stocker en Keychain.
5. Me fournir : `APP_ID`, `APP_SECRET`, `IG_USER_ID` (et le token en Keychain).

→ Dès que c'est fait, je monte `instagram_post.py` et je le câble dans le flux du dimanche (préparer le post automatiquement).
