# M1 LLM Access

## Objet

Fiche d'accès technique pour le MacBook M1 dédié aux modèles locaux [[Ollama]] dans le projet [[AI_IT_TOOLS]].

## État vérifié

- Date de vérification : 2026-06-02
- Machine [[Tailscale]] : `m1-llm`
- IP [[Tailscale]] : `100.73.212.110`
- Utilisateur SSH : `m1`
- Nom d'hôte macOS observé : `FE:CC:48:61:DF:7F`
- Architecture : `arm64`
- macOS : `26.5.1`
- SSH : opérationnel avec clé publique locale du Mac M5
- Screen Sharing / VNC : opérationnel via [[Tailscale]]
- [[Ollama]] : actif via l'application macOS `com.ollama.ollama`
- CLI [[Ollama]] : disponible dans le `PATH` du compte `m1` via `~/.zshenv`
- API locale [[Ollama]] : `http://127.0.0.1:11434`
- API [[Ollama]] sur IP [[Tailscale]] : non exposée directement (`100.73.212.110:11434` refusé)

## Commandes utiles depuis le Mac M5

Tester SSH :

```bash
ssh m1@100.73.212.110
```

Ouvrir le partage d'écran depuis le Mac M5 :

```bash
open vnc://100.73.212.110
```

Lister les modèles via l'API locale du M1 :

```bash
ssh m1@100.73.212.110 'ollama list'
```

Alternative via l'API locale du M1 :

```bash
ssh m1@100.73.212.110 'curl -sS http://127.0.0.1:11434/api/tags'
```

Tester une inférence courte :

```bash
ssh m1@100.73.212.110 'curl -sS http://127.0.0.1:11434/api/generate -d '\''{"model":"llama3.2:3b","prompt":"Reponds en un mot: OK","stream":false}'\'''
```

Créer un tunnel local si une application du Mac M5 doit appeler l'API [[Ollama]] du M1 :

```bash
ssh -N -L 11435:127.0.0.1:11434 m1@100.73.212.110
```

Puis appeler depuis le Mac M5 :

```bash
curl http://127.0.0.1:11435/api/tags
```

## Modèles présents

| Modèle | Taille | Quantization | Context |
|---|---:|---|---:|
| `qwen2.5:32b` | 19.85 GB | Q4_K_M | 32768 |
| `codestral:22b` | 12.57 GB | Q4_0 | 32768 |
| `deepseek-r1:14b` | 8.99 GB | Q4_K_M | 131072 |
| `llama3.2:3b` | 2.02 GB | Q4_K_M | 131072 |

## Sécurité

Ne pas exposer le port `11434` directement sur [[Tailscale]] sauf besoin explicite. Le tunnel SSH local est préférable pour les usages ponctuels ou les intégrations depuis le Mac M5.

## Voir aussi

- [[MEMORY]]
- [[Runtime_Service_Register]]
- [[AI_Runtime_Audit]]
