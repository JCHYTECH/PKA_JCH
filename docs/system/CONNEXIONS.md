# Connexions machines

Fiche centrale pour les accès rapides aux machines de JCH.  
Règle : ne jamais écrire de mot de passe, token ou secret en clair dans ce fichier.

## Accès rapides

| Machine | Usage | Accès principal | Commandes utiles | État |
|---|---|---|---|---|
| Mac M1 `m1-llm` | LLM locaux [[Ollama]] | [[Tailscale]] `100.73.212.110` | `ssh m1@100.73.212.110`<br>`open vnc://100.73.212.110` | OK 2026-06-02 |
| RPi `rpi-pkajch` | [[BirdNET]] / [[EventNet]] | [[Tailscale]] `100.66.110.60` | `ssh jchavaux@100.66.110.60`<br>`http://100.66.110.60` | Offline dernier scan 2026-06-02 |
| Ancien RPi `birdnetpi` | Ancienne entrée [[BirdNET]] | [[Tailscale]] `100.84.45.93` | `http://100.84.45.93` | Ancienne IP, probablement obsolète |
| Mac M5 `m5-jc` | Machine principale | [[Tailscale]] `100.108.55.44` | `http://100.108.55.44:8123` pour [[Home Assistant]] | OK 2026-06-02 |

## Mac M1 — LLM local

### Connexion écran

Depuis le Mac M5 :

```bash
open vnc://100.73.212.110
```

### Connexion terminal

```bash
ssh m1@100.73.212.110
```

### [[Ollama]]

[[Ollama]] tourne localement sur le M1, mais le port `11434` n'est pas exposé directement sur [[Tailscale]].

Lister les modèles depuis le Mac M5 :

```bash
ssh m1@100.73.212.110 'curl -sS http://127.0.0.1:11434/api/tags'
```

Créer un tunnel local si une application du Mac M5 doit appeler l'API [[Ollama]] du M1 :

```bash
ssh -N -L 11435:127.0.0.1:11434 m1@100.73.212.110
```

Puis appeler :

```bash
curl http://127.0.0.1:11435/api/tags
```

Fiche détaillée : [[M1_LLM_ACCESS]]

## Raspberry Pi — BirdNET / EventNet

### Accès Tailscale actuel

```bash
ssh jchavaux@100.66.110.60
```

Interface web probable :

```text
http://100.66.110.60
```

Note : le RPi était offline au dernier scan [[Tailscale]] du 2026-06-02. L'accès dépend donc de son état d'alimentation et de sa connexion réseau.

### Ancienne entrée

L'ancien nœud `birdnetpi` apparaît encore dans [[Tailscale]] :

```text
100.84.45.93
```

Cette entrée est à considérer comme obsolète sauf confirmation contraire.

Fiche détaillée : [[BIRDNET_PI_ACCESS]]

## Commandes de diagnostic depuis le Mac M5

Voir les machines [[Tailscale]] :

```bash
/Applications/Tailscale.app/Contents/MacOS/Tailscale status
```

Tester un port :

```bash
nc -vz -G 5 100.73.212.110 22
nc -vz -G 5 100.73.212.110 5900
```

## Ajouter une machine

Dupliquer ce bloc :

```markdown
## Nom machine

- Usage :
- Tailscale :
- SSH :
- Web :
- Écran distant :
- Dernière vérification :
- Fiche détaillée :
```

## Voir aussi

- [[M1_LLM_ACCESS]]
- [[BIRDNET_PI_ACCESS]]
- [[MEMORY]]
