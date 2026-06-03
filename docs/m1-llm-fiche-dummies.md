# 🖥️ Mac M1 LLM — Fiche Dummies

> Utiliser les modèles locaux du Mac M1 depuis le Mac M5 (VS Code ou terminal).

---

## 🗺️ VUE D'ENSEMBLE

```
┌─────────────────────┐     SSH / VNC / Remote-SSH     ┌─────────────────────┐
│     Mac M5 (JC)     │ ◄──────────────────────────────►│   Mac M1 32 Go      │
│   192.168.129.14    │         via Tailscale           │  192.168.129.19     │
│   Tailscale: m5-jc  │                                 │  Tailscale: m1-llm  │
│                     │                                 │  IP: 100.73.212.110 │
│   Tu es ici →       │                                 │  Ollama :11434      │
└─────────────────────┘                                 └─────────────────────┘
```

---

## 🚀 ACCÈS RAPIDE

| Besoin | Commande (depuis le M5) |
|--------|------------------------|
| Prendre la main sur le M1 (écran) | `open vnc://100.73.212.110` |
| Terminal SSH M1 | `ssh m1@100.73.212.110` |
| Lister les modèles | `ssh m1@100.73.212.110 'ollama list'` |
| VS Code sur le M1 | `Cmd+Shift+P` → `Remote-SSH: Connect` → `m1@100.73.212.110` |

---

## 🧠 LES 4 MODÈLES DISPONIBLES

| Modèle | Taille | Usage | Vitesse |
|--------|--------|-------|---------|
| `llama3.2:3b` | 3B | Test rapide, petit prompt | ⚡⚡⚡ |
| `deepseek-r1:14b` | 14B | Raisonnement complexe, logique | ⚡⚡ |
| `codestral:22b` | 22B | Code, scripts, analyse technique | ⚡⚡ |
| `qwen2.5:32b` | 32B | Généraliste lourd, qualité max | ⚡ |

---

## 💻 MÉTHODE 1 — VS Code Remote-SSH (recommandé)

Ouvre VS Code **sur ton M5** mais connecté au M1 :

1. **Installer l'extension** : `Remote - SSH` (Microsoft)
2. **Cmd+Shift+P** → `Remote-SSH: Connect to Host...`
3. Entre : `m1@100.73.212.110`
4. La fenêtre VS Code devient un terminal du M1

Dans le terminal intégré de cette fenêtre :
```bash
ollama run codestral:22b    # Code
ollama run deepseek-r1:14b  # Raisonnement
ollama run qwen2.5:32b      # Généraliste
ollama run llama3.2:3b      # Test rapide
```

---

## 🔌 MÉTHODE 2 — Tunnel SSH + Continue (M5 → M1)

Pour utiliser un modèle M1 **directement dans Continue sur le M5** :

### Étape 1 — Ouvrir le tunnel (terminal 1)

```bash
ssh -N -L 11435:127.0.0.1:11434 m1@100.73.212.110
```

Laisse ce terminal ouvert. Le port `11435` du M5 pointe maintenant vers Ollama du M1.

### Étape 2 — Ajouter le modèle dans Continue

Dans `~/.continue/config.ts`, ajoute ce bloc :

```typescript
{
  title: '🖥️ M1 — Codestral 22B',
  provider: 'ollama',
  model: 'codestral:22b',
  apiBase: 'http://127.0.0.1:11435',
}
```

Puis `Cmd+Shift+P` → `Continue: Reload`.

---

## 🧪 TESTS ET DIAGNOSTIC

| Tester quoi | Commande |
|-------------|----------|
| Le M1 répond ? | `ssh m1@100.73.212.110 'hostname'` |
| Ollama est vivant ? | `ssh m1@100.73.212.110 'ollama list'` |
| Modèle chargé ? | `ssh m1@100.73.212.110 'ollama ps'` |
| Inférence rapide | `ssh m1@100.73.212.110 'ollama run llama3.2:3b "OK ?"'` |
| Taille des modèles | `ssh m1@100.73.212.110 'du -sh ~/.ollama/models'` (40 Go) |

---

## 🧹 NETTOYER LA RAM M1

```bash
# Arrêter un modèle qui tourne
ssh m1@100.73.212.110 'ollama stop qwen2.5:32b'

# Vider la RAM macOS
ssh m1@100.73.212.110 'sudo purge'
```

---

## ⚡ ASTUCES

- **Gros modèle lent ?** Passe sur `codestral:22b` ou `deepseek-r1:14b`
- **Tunnel SSH coupé ?** Relance la commande `ssh -N -L ...`
- **VS Code Remote-SSH lent ?** C'est normal au premier lancement (installation serveur)
- **M1 non joignable ?** Vérifie que Tailscale tourne → `/Applications/Tailscale.app/Contents/MacOS/Tailscale status`
- **Modèles :** 40 Go sur le disque M1 — ne pas les déplacer manuellement

---

## 📊 RÉSUMÉ — QUEL MODÈLE POUR QUOI ?

| Ton besoin | Modèle | Méthode |
|------------|--------|---------|
| Coder un script Python | `codestral:22b` | VS Code Remote-SSH ou ollama run |
| Raisonnement, logique, maths | `deepseek-r1:14b` | ollama run |
| Analyse de doc, rédaction | `qwen2.5:32b` | ollama run |
| Test rapide | `llama3.2:3b` | ollama run |
| Rester dans VS Code M5 | Continue + tunnel SSH | Méthode 2 |

---

*Fiche générée par Dobby 🦉 — 3 juin 2026*
