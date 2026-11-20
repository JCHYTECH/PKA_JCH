---
date: 2026-11-18
source: dobby
domain: pka-securite
type: conseil-stance
stance: premiers-principes
sujet: politique de protection des comptes et secrets PKA
status: actif
lang: fr
---

# Stance « Premiers Principes » — Protection des comptes : protège-t-on le bon risque ?

> Question motrice : **la politique fige-t-elle une réponse au risque dominant de JC — ou à un risque
> déjà éteint, doublé d'un risque non nommé ?**
> Ancrage vérifié : `.gitignore:2`, `git check-ignore`, `git ls-files`,
> `git log --all -- JCH_PRIVATE/credentials-central.md`, commits `8c8214e` + `83ce2fc`,
> `ls -l JCH_PRIVATE/credentials-central.md`, `fdesetup status`, `/Applications/1Password.app`,
> `credentials-central.md:178-179`,
> `2026-11-18_dobby_analyse-transcript-protection-comptes.md:189,263,290-291`.

---

## 0. Verdict

La politique répond à **« comment rendre la connexion à mes comptes plus difficile à pirater à
distance ? »**. Ce n'est pas la question que pose l'état réel du système. Le risque « secret dans un
fichier versionné » est **déjà éteint** ; le risque dominant est **local, lisible par les agents, et
absent des cinq articles**. On protège la porte d'entrée pendant que la clé est sous le paillasson.

## 1. L'article 1 cible un risque déjà éteint

« Aucun secret en clair dans un fichier versionné » est **sans objet** : `credentials-central.md` n'a
**jamais** été suivi par git (`git log --all` renvoie vide, `git ls-files` ne remonte aucun secret) et
`.gitignore:2` l'exclut. Le risque a existé et a **déjà été traité** — commit `8c8214e` (scrub clés
mortes + untrack configs vivantes) puis `83ce2fc` (filter-repo) : l'historique a été réécrit.

**Figer cet article, c'est ratifier, pas protéger.** Ce qui subsiste de ce risque n'est pas le
*tracking*, c'est la **révocation** (§5).

## 2. Le risque réel : le secret au repos, lisible par les agents

Le fichier reste en clair en `0600`, comme `~/.config/pka-jch/api_keys`, avec **43 lignes de secrets
réels** (HA M5 et Lupo, SSH, Mosquitto, Zigbee2MQTT, Tailscale, API keys, Ghost, Mailgun, VPS
Hostinger, Instagram/Meta). FileVault est actif (`fdesetup status` → *On*) : le vol d'une machine
**éteinte** est couvert.

Mais la menace dominante n'est pas le voleur, c'est **le processus tournant sous le même UID** :
quatre machines, des agents IA avec accès shell, du contenu ingéré (transcripts, pages web) donc du
prompt-injection. Un seul `cat` exfiltre d'un coup l'infrastructure PKA *et* les accès WildLens.
**Aucune des dix actions issues de la vidéo ne réduit ce risque** : une clé FIDO2 ne dit rien de la
lisibilité d'un fichier. La politique ne sur-protège pas la mauvaise chose — elle la protège
excellemment, hors sujet.

## 3. Le coffre existe déjà : une migration, pas un achat

**1Password est installé et utilisé** (données depuis le 5 juin). Le « socle A » n'est donc pas une
acquisition mais une **migration de 43 entrées vers un outil déjà payé**. Il ne faut **pas** installer
`age`/`sops`/`gpg` (aucun n'est présent) : ce serait un coffre sur un coffre. Le pattern pointeur est
d'ailleurs déjà appliqué en `:178-179`, où la clé de récupération FileVault est délibérément absente.
Vraie question : quel parcours rend la migration irréversible en une session, pour un non-technicien ?

## 4. Sur-protection et sous-protection

| Article | Verdict |
|---|---|
| (1) Aucun secret versionné | ✅ vrai mais **déjà satisfait** ; sous-produit de la vraie règle (« illisible par un processus ») |
| (2) Inventaire des comptes maîtres | ⚠️ bonne intuition, **mauvais graphe** (§5) ; risque de 3ᵉ inventaire parallèle (`ADR-011-provisioning-cycle-de-vie-cles.md`) |
| (3) 2 clés, pas de SMS en secours | ⚠️ **sur-protège** : juste pour 3 à 8 comptes ; en France, « pas de SMS en secours » devient souvent « pas de secours » |
| (4) Hiérarchie fixe des facteurs | 🔴 **sur-spécifie le sommet, sous-spécifie les 80 % du milieu**, où le choix réel est « TOTP ou rien » (`:290`) |
| (5) Rotation + reprise testée | 🔴 **seul article vraiment premier-principe, classé dernier** — l'analyse conclut elle-même « le vrai risque est la perte, pas l'attaque » (`:189`) |

## 5. Le nœud racine n'est pas un compte

Dans la topologie réelle, la racine est **le poste + la session d'agent + le fichier de secrets**. Un
inventaire de comptes qui omet ces trois nœuds répond à « qui peut réinitialiser quoi ? » et laisse
sans réponse « qui peut lire quoi, maintenant, sans mot de passe ? ».

Angle mort symétrique : **untrack ≠ revoke**. `8c8214e` a retiré du suivi des secrets *vivants* après
réécriture d'historique, mais un remote GitHub et quatre machines peuvent garder des objets
inaccessibles ou d'anciens clones. Tout secret ayant transité par git doit être **présumé brûlé et
révoqué une fois** : forensique ponctuelle, *pas* une cadence automatisée. La politique la range au
niveau C — celui qu'on n'atteindra jamais.

## 6. Recommandation : réordonner, pas ajouter

- **A′ (urgent)** : migrer les 43 entrées vers 1Password, ne garder que des pointeurs ; **révoquer**
  tout secret jamais commité ; décider ce que les agents ont le droit de lire.
- **B′** : codes de secours hors-ligne **avant** tout enrôlement + un test de reprise après perte sur
  un compte non critique — le point (5), promu au rang 2.
- **C′** : les 2 clés physiques sur 3 à 8 comptes souverains, là où le service le supporte
  réellement ; TOTP sans honte ailleurs.
- **Abandonner** : la hiérarchie comme *règle* (garder comme *préférence*) et la « rotation
  automatisée » tant que A′ n'est pas tenu.

> **Thèse** : la politique protège la serrure d'une porte dont la clé est déjà dans la rue. Le bon
> objectif n'est pas « plus de facteurs », c'est **« moins de copies lisibles »** — plus petit, plus
> vérifiable, et atteignable cette semaine avec un 1Password déjà payé.
