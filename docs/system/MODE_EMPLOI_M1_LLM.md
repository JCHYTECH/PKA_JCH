# Mode d'emploi — Accès M1 et travail avec LLM locaux

Ce fichier décrit comment utiliser le Mac M1 `m1-llm` depuis le Mac M5 pour travailler avec les modèles locaux [[Ollama]].

Règle : ne jamais écrire de mot de passe, token ou secret en clair dans ce fichier.

## Résumé rapide

| Besoin | Commande |
|---|---|
| Voir l'écran du M1 | `open vnc://100.73.212.110` |
| Ouvrir un terminal M1 | `ssh m1@100.73.212.110` |
| Lister les modèles | `ssh m1@100.73.212.110 'ollama list'` |
| Lancer un modèle léger | `ssh m1@100.73.212.110 'ollama run llama3.2:3b'` |
| Lancer un modèle de code | `ssh m1@100.73.212.110 'ollama run codestral:22b'` |

## 1. Accès écran au M1

Depuis le Terminal du Mac M5 :

```bash
open vnc://100.73.212.110
```

Cela ouvre le Partage d'écran macOS vers le M1 via [[Tailscale]].

Ne pas taper seulement :

```bash
vnc://100.73.212.110
```

Cette forme fonctionne dans Finder `Cmd + K`, mais pas comme commande terminal.

## 2. Accès terminal au M1

Depuis le Mac M5 :

```bash
ssh m1@100.73.212.110
```

Une fois connecté, les commandes tournent sur le M1.

Tester [[Ollama]] :

```bash
ollama list
```

## 3. Utiliser VS Code Remote-SSH

Objectif : garder VS Code sur le Mac M5, mais ouvrir un terminal et des fichiers du M1.

### Première configuration

1. Ouvrir VS Code sur le Mac M5.
2. Installer l'extension Microsoft `Remote - SSH`.
3. `Cmd + Shift + P`.
4. Choisir `Remote-SSH: Connect to Host...`.
5. Entrer :

```text
m1@100.73.212.110
```

6. Si VS Code demande le système distant, choisir `macOS`.

### Utilisation courante

Dans la fenêtre VS Code connectée au M1 :

```bash
ollama list
ollama run llama3.2:3b
ollama run deepseek-r1:14b
ollama run codestral:22b
ollama run qwen2.5:32b
```

Le terminal intégré de VS Code est alors un terminal du M1.

## 4. Modèles disponibles

| Modèle | Usage recommandé | Remarque |
|---|---|---|
| `llama3.2:3b` | Test rapide, commande légère | Très rapide, faible qualité relative |
| `deepseek-r1:14b` | Raisonnement local | Peut produire du raisonnement long |
| `codestral:22b` | Code, scripts, analyse technique | Bon candidat pour développement local |
| `qwen2.5:32b` | Généraliste plus lourd | Plus lent, plus exigeant en mémoire |

## 5. Commandes [[Ollama]] utiles

Lister les modèles :

```bash
ollama list
```

Lancer un modèle :

```bash
ollama run llama3.2:3b
```

Voir les modèles chargés en mémoire :

```bash
ollama ps
```

Arrêter un modèle chargé :

```bash
ollama stop llama3.2:3b
```

Afficher l'aide :

```bash
ollama --help
```

## 6. Appeler [[Ollama]] depuis le Mac M5

Par sécurité, le port `11434` du M1 n'est pas exposé directement sur [[Tailscale]]. Pour l'utiliser depuis le Mac M5, créer un tunnel SSH :

```bash
ssh -N -L 11435:127.0.0.1:11434 m1@100.73.212.110
```

Dans un autre terminal du Mac M5 :

```bash
curl http://127.0.0.1:11435/api/tags
```

Test d'inférence via tunnel :

```bash
curl http://127.0.0.1:11435/api/generate -d '{"model":"llama3.2:3b","prompt":"Reponds en un mot: OK","stream":false}'
```

## 7. Emplacement des modèles sur le M1

Les modèles sont stockés ici :

```bash
/Users/m1/.ollama/models
```

Taille constatée le 2026-06-02 :

```text
40G
```

Ne pas modifier manuellement les fichiers dans :

```bash
/Users/m1/.ollama/models/blobs
```

Pour gérer les modèles, utiliser les commandes [[Ollama]].

## 8. Diagnostic rapide

Tester si le M1 répond :

```bash
/Applications/Tailscale.app/Contents/MacOS/Tailscale ping 100.73.212.110
```

Tester SSH :

```bash
ssh m1@100.73.212.110 'hostname; whoami; ollama list'
```

Tester VNC :

```bash
nc -vz -G 5 100.73.212.110 5900
```

Tester [[Ollama]] côté M1 :

```bash
ssh m1@100.73.212.110 'curl -sS http://127.0.0.1:11434/api/tags'
```

## 9. Bonnes pratiques

- Utiliser `llama3.2:3b` pour tester rapidement que tout fonctionne.
- Utiliser `codestral:22b` pour le code.
- Utiliser `deepseek-r1:14b` pour les questions de raisonnement.
- Utiliser `qwen2.5:32b` quand la qualité prime sur la vitesse.
- Éviter de déplacer les modèles à la main.
- Préférer le tunnel SSH à l'exposition directe du port `11434`.
- Garder le HDMI disponible comme solution physique, mais utiliser VNC pour l'administration courante.

## Voir aussi

- [[CONNEXIONS]]
- [[M1_LLM_ACCESS]]
- [[AI_Runtime_Audit]]
- [[Runtime_Service_Register]]
