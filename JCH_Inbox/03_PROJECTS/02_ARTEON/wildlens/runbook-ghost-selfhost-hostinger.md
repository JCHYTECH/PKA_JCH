---
date: 2026-11-15
source: dobby
domain: arteon/wildlens
type: runbook
status: active
owner: "[[Dobby]]"
lang: fr
---

# Runbook — Ghost self-host sur VPS Hostinger (WildLens)

> **Décision 15/11** : WildLens migre de Ghost(Pro) (18 $/mois) vers self-host Ghost sur
> VPS Hostinger **KVM 1** (1 vCPU, 4 Go RAM, 50 Go NVMe), Ubuntu 24.04 LTS, datacenter UE.
> Domaine : `wildlens.arteon.be`. Newsletter hebdo ~500 abonnés (croissance ~2000), thème custom ARTEON, multilingue EN/FR/IT.
> Source de vérité : `thread-arteon.md`, `operations-creation-site-ghost.md`, `decisions-actives.md`.

---

## État d'avancement (maj 17/11)

- [x] **Étape 0** — VPS acheté : IP `2.25.8.208`, 86,97 €/an TTC
- [x] **Étape 1** — SSH durci (utilisateur `deploy` + clé, fail2ban, ufw)
- [x] **Étape 2** — DNS A `wildlens` → `2.25.8.208` — ✅ vérifié 17/11 (résout + HTTP 200)
- [x] **Étape 3** — Ghost 6.77.0 + nginx + SSL Let's Encrypt — ✅ 17/11 (`https://wildlens.arteon.be` → 200)
- [x] **Étape 4** — Mailgun (compte + DNS SPF/DKIM/MX/CNAME/DMARC + SMTP Ghost + test) — ✅ 18/11
- [ ] **Étape 5** — Migration contenu (4 éditions) → VPS
- [ ] **Étapes 6-7** — Backups + monitoring

---

## Rôles

- **JC** : achat VPS (carte perso), DNS chez le registrar d'arteon.be, création compte Mailgun + vérification domaine.
- **Forge / Dobby** : tout ce qui se passe en SSH sur le VPS (installation, sécurité, config, migration).

---

## Étape 0 — Achat VPS (JC, navigateur)

1. `hostinger.com/vps/ghost-hosting` → plan **KVM 1** (cycle 24 mois = meilleur prix ; renouvellement plus cher).
2. Datacenter **Europe** (RGPD).
3. OS : **Ubuntu 24.04 LTS**.
4. Noter l'**IP du VPS**. Configurer une **clé SSH** dans hPanel (VPS → SSH access) plutôt qu'un mot de passe root.

---

## Étape 1 — Accès SSH + sécurité (Forge/Dobby)

Depuis le M5 :

```
[M5] ssh root@<IP_VPS>
```

Sur le VPS (root), dans l'ordre :

```bash
# utilisateur dédié (pas root)
adduser deploy
usermod -aG sudo deploy

# clé SSH pour deploy
mkdir -p /home/deploy/.ssh && chmod 700 /home/deploy/.ssh
# coller la clé publique M5 dans /home/deploy/.ssh/authorized_keys
chmod 600 /home/deploy/.ssh/authorized_keys
chown -R deploy:deploy /home/deploy/.ssh

# pare-feu : SSH + HTTP + HTTPS uniquement
ufw allow OpenSSH
ufw allow 80
ufw allow 443
ufw --force enable

# fail2ban (anti brute-force SSH)
apt install -y fail2ban
systemctl enable --now fail2ban

# désactiver le login root par mot de passe
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
systemctl restart ssh
```

Ensuite travailler en `deploy` :

```
[M5] ssh deploy@<IP_VPS>
```

---

## Étape 2 — DNS (JC, registrar d'arteon.be)

1. Record **A** : `wildlens` → `<IP_VPS>` (TTL 3600).
2. (Optionnel) record **AAAA** si IPv6 fourni par Hostinger.
3. Attendre la propagation (~5-30 min) **avant** `ghost install` (SSL Let's Encrypt exige que le domaine résolve déjà).

Vérifier : `[M5] dig +short wildlens.arteon.be` doit renvoyer l'IP du VPS.

---

## Étape 3 — Installation Ghost (Forge/Dobby)

Sur le VPS en `deploy` :

```bash
sudo apt update && sudo apt upgrade -y

# Node.js 20 LTS (requis par Ghost)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# nginx + MySQL
sudo apt install -y nginx mysql-server

# ghost-cli
sudo npm install -g ghost-cli@latest

# dossier d'installation
sudo mkdir -p /var/www/ghost
sudo chown deploy:deploy /var/www/ghost
sudo chmod 775 /var/www/ghost
cd /var/www/ghost

# installation interactive
ghost install
```

Réponses à `ghost install` :

- **Blog URL** : `https://wildlens.arteon.be`
- **MySQL hostname** : `localhost`
- **MySQL username** : `ghost`
- **MySQL password** : générer un mot de passe fort (→ `JCH_PRIVATE/credentials-central.md`)
- **Database name** : `ghost_prod`
- **Setup nginx** : `Yes`
- **Setup SSL** : `Yes` (Let's Encrypt)
- **Setup systemd** : `Yes` (démarrage auto + redémarrage)

Vérifier : `[M5] curl -I https://wildlens.arteon.be` → HTTP 200.

---

## Étape 4 — Email newsletter (JC + Forge/Dobby)

1. **JC** crée un compte **Mailgun** (free tier : ~100 emails/jour — suffisant pour ~500 lecteurs hebdo).
2. **JC** ajoute le domaine d'envoi `mg.wildlens.arteon.be` dans Mailgun, puis crée les enregistrements DNS demandés (TXT SPF, TXT DKIM, MX, CNAME) chez le registrar. Valider la vérification dans Mailgun.
3. **JC** récupère le **SMTP username** (`postmaster@mg.wildlens.arteon.be`) et le **SMTP password / API key**.

Sur le VPS (Forge/Dobby) :

```bash
cd /var/www/ghost
ghost config set mail transport SMTP
ghost config set mail options.service Mailgun
ghost config set mail options.host smtp.mailgun.org
ghost config set mail options.port 587
ghost config set mail options.secure false
ghost config set mail options.auth.user postmaster@mg.wildlens.arteon.be
ghost config set mail options.auth.pass '<SMTP_PASSWORD>'
ghost restart
```

Tester : envoyer une newsletter de test depuis l'admin Ghost.

> ⚠️ **Piège `ghost config set` (constaté 18/11)** : `ghost config set mail options.host x` (3 arguments) est **faux** — ghost-cli n'accepte que `<key> <value>` (2 arguments) et écrit `mail = "options.host"` (la config mail a été écrasée). Méthode sûre : écrire le bloc `"mail"` (transport/options/from) directement dans `config.production.json` puis `ghost restart`.

> ⚠️ **Seuil (vérifié 17/11, source Mailgun pricing)** : le plan Free = **100 emails/jour** (permanent). Un envoi hebdo unique à N abonnés = N emails le même jour → **le Free ne couvre que jusqu'à ~100 abonnés par envoi**. À ~500 abonnés (1 blast hebdo = 500 emails en 1 jour), il faut **Basic 15 $/mois (10 000 emails/mois)**. Règle : Free pour démarrer/tester (liste ~0 aujourd'hui), basculer Basic dès que la liste dépasse ~100 abonnés actifs.

---

## Étape 5 — Migration du contenu (JC export + Forge import)

1. **JC** : Ghost(Pro) admin → **Settings → Labs → Export all content** → fichier JSON.
2. **Forge/Dobby** : nouvel admin (sur le VPS) → **Settings → Labs → Import** → sélectionner le JSON.
3. Vérifier : articles, tags, membres, thème (réimporter le thème ARTEON séparément si besoin), images.

> Le thème ARTEON custom se réimporte via **Settings → Design → Change theme → Upload**.

---

## Étape 6 — Backups (Forge/Dobby)

```bash
# backup Ghost (JSON + images + thème)
cd /var/www/ghost
ghost backup

# cron quotidien à 3h
crontab -e
# ajouter :
0 3 * * * cd /var/www/ghost && ghost backup --no-prune
```

- **Snapshots VPS Hostinger** : activer les backups hebdo auto dans hPanel (inclus dans le plan).
- Copier périodiquement les backups hors du VPS (vers M5 / iCloud) — ne pas garder la seule copie sur le serveur.

---

## Étape 7 — Monitoring (Forge/Dobby)

- **Uptime** : UptimeRobot (free) sur `https://wildlens.arteon.be`, ou intégrer à `bin/pka-watch-host`.
- **Certificat SSL** : renouvellement auto géré par Ghost (`ghost run` relance `acme.sh`). Vérifier `sudo certbot certificates` ou le log ghost.
- **Disque / RAM** : `df -h` et `free -h` en cron, ou étendre la watch host PKA.

---

## Étape 8 — Sécurité des secrets (⚠️ repo PKA PUBLIC)

- **Jamais** de secret dans un fichier suivi par git (le dépôt PKA_JCH est **public**).
- Tous les secrets vont dans `JCH_PRIVATE/credentials-central.md` (hors git) :
  - IP + clé SSH VPS
  - mot de passe MySQL `ghost`
  - SMTP username + SMTP password Mailgun
  - token d'admin Ghost
- Le hook `pre-commit` PKA (installé 28/10) bloque déjà l'ajout de motifs de secret.

---

## Ordre critique

**0 → 2 → 3** (achat → DNS → install, car SSL exige le domaine résolu), puis **4 → 5** (email avant newsletter, migration après install), puis **6-7** (backups + monitoring dès que le site tourne).

## Points de blocage connus

1. **SSL échoue** si le DNS ne résout pas encore → refaire `ghost setup ssl` après propagation.
2. **Newsletter bloquée** si le domaine Mailgun n'est pas vérifié → les DNS TXT/MX doivent être validés côté Mailgun.
3. **Port 25** est fermé chez Hostinger (relai SMTP interdit) → utiliser le **SMTP Mailgun sur 587** (déjà prévu), jamais un serveur mail local.

---

*Runbook généré par Dobby 🦉 le 2026-11-15. À exécuter quand JC a acheté le VPS + pointé le DNS.*