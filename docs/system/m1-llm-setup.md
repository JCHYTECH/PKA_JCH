# M1 — serveur d'inférence local

> **2026-10-28** — Dobby 🦉. Machine dédiée aux LLM locaux, pilotée à distance
> depuis M5. État, mesures, réglages et recommandations.

---

## 1. Ce que la machine a dans le ventre

| Élément | Valeur |
|---|---|
| Modèle | `MacBookPro18,4` — MacBook Pro 14" |
| SoC | **Apple M1 Max**, 10 cœurs (8 performance + 2 efficacité) |
| GPU | intégré, accès à toute la mémoire unifiée (Metal) |
| RAM | **32 Go unifiés** |
| Disque | 926 Go, **673 Go libres** (229 Go utilisés) |
| macOS | 26.5.1 |
| Écran | dalle interne HS → clamshell + VNC |
| Alimentation | secteur permanent, `disablesleep 1`, `womp 1` |
| FileVault | désactivé (accès distant garanti) |

**Ce que ça implique pour le choix des modèles :** macOS a besoin de 6 à 8 Go,
donc **environ 24 Go sont disponibles pour les poids et le cache KV**. Le plafond
réaliste est un modèle **30–32 B en quantification Q4**, ou un MoE de 30 B actifs.
Au-delà (70 B, Q8), ça ne tient pas.

### Chemin réseau — à connaître

| Voie | Interface | Remarque |
|---|---|---|
| Ethernet USB-C | `en8` — **1000baseT full-duplex**, IP `192.168.129.30` | route par défaut ; puce **AX88179B** |
| Wi-Fi | `en0` — `192.168.129.19` | secours automatique |
| Tailscale | `utun0` — `100.73.212.110` | seule voie d'accès à l'API Ollama |

**Piège rencontré le 2026-10-28 :** l'adaptateur AX88179B est énuméré par le bus
USB (`ioreg`) mais aucun pilote ASIX n'existe sur macOS. Il ne fonctionne
qu'après avoir **accepté le dialogue « se connecter à ASIX AX88179B »** qui
apparaît sur l'écran de la machine à la première connexion — sans cette
validation, l'interface n'existe pas et le trafic passe par le Wi-Fi.

**Le débit de téléchargement est limité par la ligne, pas par le LAN** : mesuré
à ~2,3 Mo/s (≈ 8 Go/h) aussi bien en Wi-Fi qu'en Ethernet 1 Gbit/s. Prévoir
plusieurs heures pour un modèle de 17–19 Go.

## 2. Le problème corrigé

Ollama était installé via **Ollama.app**, application graphique. Deux
conséquences invisibles mais bloquantes :

- le serveur ne démarrait **qu'à l'ouverture d'une session** — sans login, pas
  d'inférence ; après un redémarrage, la machine était muette ;
- aucune variable de réglage n'était définie : pas de flash attention, cache KV
  en pleine précision, modèle déchargé après 5 minutes, contexte à 4 k.

## 3. Ce qui a été mis en place

**Démon système** `/Library/LaunchDaemons/com.pka.ollama.plist` — tourne en
utilisateur `m1`, démarre au boot **avant toute session**, relance automatique.
Il remplace l'instance lancée par l'application.

| Variable | Valeur | Effet |
|---|---|---|
| `OLLAMA_HOST` | `100.73.212.110:11434` | **Tailscale uniquement** — le LAN est refusé (vérifié) |
| `OLLAMA_FLASH_ATTENTION` | `1` | vitesse et mémoire |
| `OLLAMA_KV_CACHE_TYPE` | `q8_0` | cache KV quantifié → contexte 2× plus long |
| `OLLAMA_KEEP_ALIVE` | `30m` | modèle résident, premier token immédiat |
| `OLLAMA_MAX_LOADED_MODELS` | `1` | un seul gros modèle en mémoire |
| `OLLAMA_NUM_PARALLEL` | `1` | tout le cache KV pour une requête |
| `OLLAMA_CONTEXT_LENGTH` | `16384` | contexte par défaut |

**Spotlight** : `~/.ollama/.metadata_never_index` posé — l'indexeur ne parcourt
plus 58 Go de poids à chaque balayage.

**Conséquence de `OLLAMA_HOST` sur l'IP Tailscale** : le serveur n'écoute plus
sur `127.0.0.1`. Sur M1, la CLI doit donc être préfixée :

```bash
OLLAMA_HOST=100.73.212.110:11434 ollama list
OLLAMA_HOST=100.73.212.110:11434 ollama pull <modèle>
```

Un client qui viserait `http://192.168.129.19:11434` (IP LAN) sera refusé —
c'est l'effet recherché.

## 4. Mesures réelles

| Modèle | Avant | Après | Remarque |
|---|---|---|---|
| `llama3.2:3b` | 39,8 tok/s | **70,7 tok/s** | +78 % grâce au flash attention |
| `qwen3:30b-a3b` (MoE, Q4_K_M) | — | **49,7 tok/s** | 19,3 Go entièrement en VRAM, chargement 17 s |

Mesures complémentaires du 2026-10-28, cache chaud :

| Modèle | Débit | VRAM | Commentaire |
|---|---|---|---|
| `qwen3:30b-a3b` (MoE 30 B) | **43,5 tok/s** | 19 Go | meilleur rapport capacité/vitesse |
| `llama3.2:3b` | **72,0 tok/s** | 2 Go | tests rapides |
| `qwen2.5-coder:14b` | **18,0 tok/s** | 9 Go | itération sur du code |
| `qwen2.5-coder:32b` (dense) | **7,7–8,1 tok/s** | 21,9 Go | tâches difficiles uniquement |
| `gemma3:27b` (dense) | **9,4 tok/s** | 17 Go | rédaction française haut de gamme |

Aucun swap utilisé, 29 % de mémoire libre avec le 32B chargé : la machine tient,
mais sans marge. C'est la raison de `OLLAMA_MAX_LOADED_MODELS=1`.

Un MoE de 30 B à ~45 tok/s : c'est le meilleur rapport capacité/vitesse
disponible sur cette machine. À l'inverse, un modèle **dense** de 32 B tombe à
8 tok/s — cinq fois plus lent, pour une qualité supérieure seulement sur les
tâches vraiment difficiles. Le MoE est le choix par défaut.

## 5. Ce qui est déjà installé

| Modèle | Taille | Usage |
|---|---|---|
| `qwen3:30b-a3b` | 18 Go | généraliste, raisonnement — **49 tok/s, le choix par défaut** |
| `qwen2.5-coder:32b` | 19 Go | code difficile — 8 tok/s, patience requise |
| `gemma3:27b` | 17 Go | rédaction française — 9,4 tok/s |
| `qwen2.5-coder:14b` | 9 Go | itération sur du code — 18 tok/s |
| `deepseek-r1:14b` | 9 Go | raisonnement explicite |
| `gemma3:12b-it-qat` | 8,9 Go | rédaction courante |
| `llama3.2-vision:11b` | 7,8 Go | vision (photos, captures) |
| `dobby-prompt` | 9 Go | LoRA maison (Qwen2.5-7B) |
| `qwen3.5` | 6,6 Go | généraliste léger |
| `llama3.2:3b` | 2 Go | tests rapides — 72 tok/s |
| `mxbai-embed-large` | 669 Mo | embeddings lourds |
| `nomic-embed-text` | 274 Mo | embeddings légers (recherche sémantique) |

Total : **93 Go** sur 637 Go libres.

## 6. Recommandations — ce qu'il reste à faire

**À ajouter, par ordre d'intérêt**

1. `qwen2.5-coder:32b` (~19 Go) — le meilleur modèle de code qui tienne ici.
   Remplacerait `qwen2.5-coder:14b`. Débit **mesuré : 7,7–8,1 tok/s** — utilisable
   pour les tâches difficiles, trop lent pour l'itération ; garder le 14b à
   18 tok/s pour le travail courant.
2. `gemma3:27b` (~17 Go) — rédaction française sensiblement meilleure que le 12b.
3. `nomic-embed-text` (274 Mo) — embeddings légers, déjà utilisé par
   `scripts/pka_retrieve.py` en local sur M5 ; le rapatrier ici rendrait la
   recherche sémantique indépendante du portable.

**Options de réglage**

- `OLLAMA_KEEP_ALIVE=-1` : modèle chargé en permanence. Latence minimale, mais
  19 Go immobilisés. Pertinent si la machine ne sert qu'à ça — c'est désormais
  le cas.
- `OLLAMA_CONTEXT_LENGTH=32768` : avec le cache `q8_0`, un 30 B + 32 k de
  contexte tient dans 32 Go. À valider par la mesure avant de généraliser.
- `OLLAMA_HOST` : `0.0.0.0` expose l'API à tout le réseau local. Si le Wi-Fi est
  partagé, restreindre à l'interface Tailscale est plus prudent.

**Non recommandé**

- Les modèles > 32 B : ne tiennent pas, et le swap tuerait les performances.
- `OLLAMA_NUM_PARALLEL` > 1 : divise le cache KV disponible par requête, sans
  gain pour un usage mono-utilisateur.
- Time Machine sur ce volume : aucun destination configurée, aucun snapshot —
  laisser ainsi. Les poids sont retéléchargeables.

## 7. Utilisation depuis M5

```bash
# [M5] version et modèles disponibles
curl -s http://100.73.212.110:11434/api/version
ollama list                      # si le client ollama est installé sur M5

# [M5] une requête
curl -s http://100.73.212.110:11434/api/generate \
  -d '{"model":"qwen3:30b-a3b","prompt":"…","stream":false}'

# [M5] endpoint compatible OpenAI (pour tout client qui parle /v1)
curl -s http://100.73.212.110:11434/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen3:30b-a3b","messages":[{"role":"user","content":"…"}]}'

# [M5] modèles actuellement en mémoire
curl -s http://100.73.212.110:11434/api/ps
```

## 8. Entretien

```bash
# [M5] redémarrer le démon après un changement de plist
ssh m1@100.73.212.110 'sudo -n launchctl bootout system/com.pka.ollama; \
  sudo -n launchctl bootstrap system /Library/LaunchDaemons/com.pka.ollama.plist'

# [M5] logs
ssh m1@100.73.212.110 'tail -20 ~/Library/Logs/ollama-daemon.err'
```
