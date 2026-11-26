# Procédure — Migration vers 1Password (compte existant récupéré)

> Dobby 🦉 · 2026-11-18 · suite au conseil protection-comptes (politique figée, règle 1).
> Objectif : **1Password** (compte déjà existant, accès récupéré) = coffre unique et source de vérité.
> Apple « Mots de passe » + Google en secondaire, mis à jour au fil de l'usage.

---

## Étape 0 — Verrouiller l'accès (priorité absolue, avant tout)

On vient de vivre la panique de l'oubli : on verrouille d'abord, on migre ensuite.

1. **Écris ta phrase maîtresse sur papier** et range-la dans l'enveloppe scellée (règle 4).
2. **Télécharge l'Emergency Kit** : app 1Password → Réglages → ton compte → « Télécharger le kit d'urgence » / « Get Emergency Kit ». **Imprime-le** et range-le **hors du coffre** (papier, lieu sûr). C'est le filet si tu oublies encore.

→ Tant que ces 2 choses ne sont pas faites, on ne migre rien.

## Étape 1 — Migrer les 211 lignes de `credentials-central.md`

**Règle de classement simple :**
- **Identifiant + mot de passe d'un site/app** → type **« Connexion »** (Login) : HA M5, HA Lupo, Instagram/Meta, Ghost (admin), Hostinger, Mailgun, comptes macOS, « Accès divers », Tailscale.
- **Clé API / jeton / secret** (clés API, jetons HA, MQTT, Zigbee2MQTT) → type **« API Credential »** ou **« Note sécurisée »**.
- **Clé SSH** (M5, Lupo) → type **« Clé SSH »** ou **« Note sécurisée »** (copier la clé privée).

**Méthode** : un item par ligne/section. Nommer clairement : `HA M5 (Docker)`, `SSH M5`, `Ghost wildlens.arteon.be`, etc. Recopier la valeur depuis `credentials-central.md` (fichier encore en clair, local).

## Étape 2 — Vider le fichier en clair

Une fois chaque entrée copiée dans 1Password, réécrire `credentials-central.md` pour ne garder **que des renvois** :
```
## Home Assistant
→ 1Password : entrée « HA M5 (Docker) »
```
Plus aucun mot de passe ni clé en clair. (Dobby peut générer ce fichier-renvois une fois la migration faite.)

## Étape 3 — Apple / Google en secondaire

- **Apple « Mots de passe »** : se remplit tout seul quand on se connecte depuis Safari.
- **Google** : idem depuis Chrome.
- Objectif : 1Password = référence ; Apple/Google = copies de confort. La cohérence se fait à l'usage, pas en triple saisie.

## Étape 4 — Tester la reprise (avant de conclure)

1. Se **déconnecter** de 1Password.
2. Se reconnecter avec **la phrase maîtresse** (vérifier qu'on la retrouve).
3. Vérifier qu'on sait **où** sont le papier et l'Emergency Kit.

---

## Check-list de sortie

- [ ] Phrase maîtresse écrite sur papier, rangée
- [ ] Emergency Kit téléchargé + imprimé, rangé hors coffre
- [ ] 211 lignes migrées (comptes + API + SSH + jetons)
- [ ] `credentials-central.md` réduit à des renvois (plus rien en clair)
- [ ] Apple/Google synchronisés à l'usage
- [ ] Reprise testée (déconnexion + reconnexion)
