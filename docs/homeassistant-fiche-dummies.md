# 🏠 Home Assistant — Fiche Dummies

> Domotique — Container Docker sur Mac M5. Interface web sur `http://localhost:8123`.

---

## 🚀 DÉMARRAGE

| Action | Comment |
|--------|---------|
| Accéder au dashboard | Ouvre `http://localhost:8123` dans le navigateur |
| Lancer le container | Docker Desktop doit tourner. Container nommé `homeassistant` |
| Redémarrer HA | Depuis l'interface : `Paramètres` → `Système` → `Redémarrer` |
| Voir les logs | `docker logs homeassistant` |

---

## 📂 OÙ SONT LES FICHIERS ?

```
_local/homeassistant/
├── configuration.yaml    ← config principale (intégrations, thèmes)
├── automations.yaml      ← automatisations
├── scripts.yaml          ← scripts
├── scenes.yaml           ← scènes
├── secrets.yaml          ← mots de passe, tokens
└── blueprints/           ← blueprints d'automatisations
```

**Chemins dans VS Code :** `_local/homeassistant/`

---

## 🔧 ÉDITER LA CONFIG

| Étape | Action |
|-------|--------|
| 1. Modifier un fichier | Édite `configuration.yaml` ou autres dans VS Code |
| 2. Vérifier la config | Dans HA : `Outils de développement` → `YAML` → `VÉRIFIER` |
| 3. Redémarrer | `Paramètres` → `Système` → `Redémarrer` |

---

## 🤖 AUTOMATISATIONS

| Emplacement | Usage |
|-------------|-------|
| `automations.yaml` | Automatisations simples (déclencheur → action) |
| `blueprints/` | Blueprints réutilisables (ex: détection de mouvement) |

### Exemple : allumer lumière au mouvement

1. Importer un blueprint → `Paramètres` → `Automatisations & scènes` → `Blueprints`
2. Créer une automatisation depuis le blueprint
3. Ça s'écrit dans `automations.yaml`

---

## 📱 APPLICATIONS

| Plateforme | App |
|------------|-----|
| iPhone/iPad | Home Assistant (App Store) |
| Mac | Via navigateur `http://localhost:8123` |
| Accès externe | Nabu Casa (optionnel, payant) ou VPN |

---

## ⚡ ASTUCES

- **Carte Lovelace** : tout se configure en UI maintenant (glisser-déposer)
- Pour ajouter un nouvel appareil : `Paramètres` → `Appareils & services` → `Ajouter`
- Les dashboards sont personnalisables par pièce
- **Supervision** : `Paramètres` → `Système` → `Matériel` pour voir CPU/RAM du container

---

## 🔧 DÉPANNAGE

| Problème | Solution |
|----------|----------|
| Interface inaccessible | Vérifie que Docker Desktop tourne |
| Erreur YAML après modif | `Outils de développement` → `YAML` → corriger l'erreur |
| Container arrêté | `docker start homeassistant` |

---

*Fiche générée par Dobby 🦉 — 3 juin 2026*
