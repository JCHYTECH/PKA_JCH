# Décommissionnement M1 — décision et plan de migration

> **Décision initiale : 2026-10-27, JC.** M1 (`m1-llm`, MacBook Pro 14" M1,
> `100.73.212.110`) déclaré **hors service**.
>
> **Rebondissement le même jour — statut : récupérable.** Deux faits ont changé la
> donne : capot fermé, l'écran externe redevient fonctionnel (mode clamshell, la
> dalle interne morte n'est plus sollicitée) ; et une **clé de récupération
> FileVault** a été retrouvée dans l'app Mots de passe. Réinitialisation du mot de
> passe en cours. **Migration suspendue** en attendant l'issue.
> Dobby 🦉.

---

## 1. État constaté

| Élément | Constat |
|---|---|
| Tailscale | `m1-llm` → `offline, last seen 21d` (dernier contact ~2026-10-07) |
| Réseau | absent du LAN `192.168.128.0/23`, aucun bail DHCP, Bonjour muet |
| Écran interne | hors service — quelques lignes allumées seulement |
| Sortie HDMI | aucune image sur écran externe |
| Amorçage | carillon de démarrage audible → firmware sain, la machine boote |
| Verrou | arrêt à l'écran FileVault ; mot de passe non validé à l'aveugle |
| Alimentation | LED MagSafe verte, carte alimentée |

**Diagnostic retenu :** panne matérielle de la chaîne d'affichage, combinée à
l'impossibilité de franchir FileVault sans retour visuel. La machine n'est pas
morte — elle est **inutilisable sans écran**.

## 2. Ce qui ne sert plus à rien

- `bin/m1-wake` — le WoL est inapplicable (aucune NIC filaire sur un 14")
- `bin/m1-rearm` — inutile tant que la machine n'a pas de session
- `M1_HOST` / `100.73.212.110` comme cible d'exécution

Les deux scripts sont conservés : ils redeviendraient utiles si la dalle était
réparée, ou sur une machine de remplacement.

## 3. Dépendances à recâbler

Tous ces fichiers pointent sur `http://100.73.212.110:11434` et échouent
silencieusement depuis 21 jours.

| Fichier | Usage | Modèle attendu | Recommandation |
|---|---|---|---|
| `scripts/pka_retrieve.py` | recherche sémantique mémoire | `nomic-embed-text` (0,27 Go) | **Ollama local M5** — coût nul, modèle minuscule |
| `scripts/mcp_ollama_server.py` | serveur MCP Ollama | tous | **Ollama local M5** (`OLLAMA_HOST=127.0.0.1:11434`) |
| `scripts/pka_memory_capture.py` | extraction auto de faits | `gemma3:12b-it-qat` (8 Go) | **DeepSeek API** — le fallback existe déjà |
| `scripts/graphify_llm_bridge.py` | enrichissement du graphe | `qwen2.5-coder:14b` (9 Go) | **DeepSeek API** (Flash) ou `qwen2.5-coder:7b` local |
| `scripts/photo_keyworder.py --m1` | vision, mots-clés photo | `llama3.2-vision:11b` (8 Go) | **Gemini API**, ou `qwen2.5vl:7b` local |
| `scripts/backup_vault_to_m1.sh` | sauvegarde du vault | rsync SSH | **nouvelle cible à définir** |
| `bin/m1-datasets-mount.sh` | montage datasets | SSHFS | obsolète |
| `scripts/ask-gemma-*.sh` | audits ponctuels | gemma sur M1 | obsolète |

## 4. Contrainte matérielle à retenir pour la substitution

**M5 : MacBook Pro 16" (`Mac17,2`), 16 Go de RAM, 205 Go libres.**

Conséquence directe : les modèles de 8 à 9 Go (gemma3:12b, qwen2.5-coder:14b,
llama3.2-vision:11b) tiennent en mémoire mais **étouffent macOS** et tournent
lentement. Sur 16 Go, la règle pratique est de rester sous 7 Go de modèle.

- Ce qui doit rester local : **embeddings** (`nomic-embed-text`, 0,27 Go) — usage
  fréquent, gain de latence net, aucun coût API.
- Ce qui doit passer au cloud : **extraction, raisonnement, vision** — la qualité
  y est supérieure et le coût par appel négligeable.

## 5. Décisions à prendre

1. **Cible de sauvegarde du vault** — remplace `backup_vault_to_m1.sh` :
   disque externe, cloud, ou dépôt distant ?
2. **Vision photo** — Gemini API (qualité) ou modèle local 7B (souveraineté) ?
3. **Sort du matériel** — réparation de la dalle (700 à 800 € chez Apple),
   réemploi en pièces, ou rangement ? Les données restent sur le SSD : ne rien
   effacer tant que la décision n'est pas prise.

## 6. Leçon à retenir

Une machine headless **avec FileVault** est un piège : le pré-démarrage exige un
mot de passe, sans réseau et sans écran de secours. Toute machine qui doit
tourner sans surveillance doit avoir, avant sa mise en service :

- FileVault désactivé, ou clé de récupération accessible hors de la machine ;
- ouverture de session automatique ;
- partage d'écran (VNC) et accès distant activés et testés ;
- `pmset -a sleep 0 disablesleep 1` sur secteur ;
- un moyen de redémarrage à froid à distance (prise connectée).

---

## 7. Rebondissement — la clé de récupération (2026-10-27)

**Deux découvertes ont rouvert le dossier.**

1. **Capot fermé = écran externe fonctionnel.** macOS bascule en mode clamshell et
   ne sollicite plus la dalle interne morte. L'écran HDMI affiche enfin l'écran de
   verrouillage. Le clavier intégré, lui, est désactivé capot fermé.
2. **Clé de récupération FileVault retrouvée** dans l'app Mots de passe. Elle ne
   donne pas le mot de passe : elle permet de le **réinitialiser**.

### Procédure de réinitialisation

À l'écran de verrouillage, le lien de réinitialisation n'apparaît qu'après
plusieurs échecs.

```
1. subir le verrouillage temporaire du compte
2. saisir trois fois un mot de passe volontairement faux
3. le lien « réinitialiser avec la clé de récupération » apparaît
4. Tab puis Espace pour l'activer (pas de souris disponible)
5. saisir la clé — insensible à la casse, tirets souvent automatiques
6. ATTENTION clavier belge : les chiffres exigent Maj
7. définir un nouveau mot de passe et le consigner dans l'app Mots de passe
```

Un point de vigilance : sur le pré-démarrage FileVault, **un clavier USB branché
derrière un dock n'est pas énuméré**. Il faut soit le clavier intégré (capot
ouvert), soit un clavier USB en direct, soit un clavier Bluetooth déjà appairé.

### Après le déverrouillage

```
[M5] ssh m1@100.73.212.110
[M5] bin/m1-rearm          # pmset + disablesleep + WoL + VNC + SSH + état FileVault
sudo fdesetup disable     # supprime le piège du pré-démarrage (décision JC)
```

`bin/m1-rearm` active désormais aussi l'accès distant et le partage d'écran, et
affiche l'état FileVault. La machine redevient pilotable depuis M5, sans écran.

### Ce qui reste suspendu

La migration des six dépendances (section 3) reste en attente. Si M1 revient, rien
n'est à migrer ; si la réinitialisation échoue, la section 3 s'applique telle
quelle.
