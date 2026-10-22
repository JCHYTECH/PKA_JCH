# Procédure de réactivation — Projet IOT Van (Lupo)

> **Date :** 2026-10-01 | **Orchestré par :** Dobby 🦉
> **Objectif :** relancer le projet IOT Van, arrêté depuis ~09/09 (boot bloqué du RPi 5), et tenir la deadline du **15 décembre 2026** (prolongée JC 19/10).
> **Règle multi-terminal :** chaque commande est préfixée par sa machine cible — [M5] (Mac), [RPi] (Lupo), [M1] (serveur LLM).

---

## Contexte

Le RPi 5 « Lupo » (cœur domotique du van Westfalia Kelsey) est **bloqué au boot** depuis ~09/09 : boot gelé phase init hardware, SQUASHFS NVMe corrompu, `duplicate_os_install`, SSH perdu. La cause software (bug #4785 / #5005) est **corrigée dans HAOS 18.3**. Plan : reflash propre en **SD seule** (le NVMe reste un data disk optionnel — les pogo pins X1205 restent une contrainte d'alimentation).

---

## Phases

### Phase 0 — Vérité terrain (physique)
- Éteindre le RPi, ouvrir le boîtier X1201-C1.
- Constater : NVMe présent/retiré ? microSD 128 ou 256 ?
- **Sortie :** état matériel réel → mise à jour `hardware-state.md`.

### Phase 1 — Flash HAOS 18.3
- Exécuter `SEQUENCE-FLASH-HAOS-18.3-2026-10-01.md`.
- **Sortie :** microSD flashée 18.3, SHA256 vérifié.

### Phase 2 — Onboarding (premier boot)
1. Booter microSD seule (NVMe retiré).
2. **Désactiver l'auto-update immédiatement** : Settings → System → Updates → OFF.
3. Hostname `lupo`.
4. Vérifier statut « Healthy » (pas de `duplicate_os`).

### Phase 3 — Réinstallation des briques
- Zigbee (Sonoff ZBDongle-E + capteurs).
- Tailscale (accès iPhone).
- Restaurer la config HA (backup) si dispo.
- **Sortie :** HA opérationnel sur banc.

### Phase 4 — Test offline (alarme, frigo)
- Valider les scénarios critiques hors réseau.
- **Sortie :** checklist de test validée.

### Phase 5 — Installation van (deadline 15/12)
- Silentblocs + coating (vibration/humidité).
- Câblage 12V (DC-DC) + PV PI HAT.
- Fixation boîtier, câblage capteurs.

### Phase 6 — Réception
- Test route, vérif stabilité 24h.
- Mise à jour `hardware-state.md` + `thread-iot.md`.

---

## Reste à faire (hors RPi)

| Élément | Statut |
|---------|--------|
| Capteurs Zigbee (portes, frigo) | ⏳ à commander |
| Silentblocs | ⏳ à commander |
| Coating (humidité) | ⏳ à commander |
| PV PI HAT câblage | reçu, à câbler |

---

## Points de vigilance

1. **Ne JAMAIS laisser l'auto-update HAOS** — le bug 18.x revient à chaque montée de version non maîtrisée.
2. **Toujours retirer les autres disques** avant un flash.
3. **SHA256 obligatoire** avant chaque flash.
4. **SD seule pour le van** — le NVMe reste data disk optionnel (pogo pins instables).

---

*Fichier maintenu par Dobby 🦉 — à mettre à jour après chaque phase.*
