# Analyse — Exosfer OBD Protect

> Dobby 🦉 — DeepSeek V4 (TUI 0.8.39) — 2026-07-13
> Fichier source : `JCH_Inbox/00_INBOX/exosfer obd.pdf`

---

## Résumé

L'Exosfer OBD Protect est un **antivol électronique passif** pour prise OBD. Il fonctionne par **permutation physique des broches** du connecteur OBD — sans électronique, sans batterie. Un plan de câblage spécifique au véhicule indique quels fils déplacer. Un adaptateur propriétaire est nécessaire pour reconnecter un outil de diagnostic.

---

## Fonctionnement

1. **Repérage** de la prise OBD (pieds conducteur, console centrale ou boîte à gants)
2. **Démontage** des garnitures pour accéder au connecteur
3. **Photographie** du câblage d'origine + **notation des couleurs** de chaque fil sur le plan fourni
4. **Permutation** des fils 1 à 1 selon le plan (ne jamais tout décâbler d'un coup)
5. **Remontage** — le plan et l'adaptateur ne doivent **jamais** rester dans le véhicule
6. **Utilisation** : pour un diagnostic, brancher l'adaptateur sur la prise OBD modifiée, puis l'outil diag sur l'adaptateur

---

## Analyse

### Points forts
- **100% passif** — pas de batterie, pas d'électronique, pas de panne possible
- **Invisible** une fois les garnitures remontées
- **Efficace contre le vol OBD** : sans l'adaptateur, aucun outil standard ne peut communiquer
- **Véhicule-spécifique** : plan de câblage adapté au modèle
- Fabriqué en France (Exosfer, spécialiste antivol)

### Points faibles / risques
- **Irréversible sans le plan** : si le plan est perdu, restauration complexe
- **Incompatible avec un dongle OBD permanent** : le WiCAN Pro doit rester branché en continu. L'Exosfer impose de retirer l'adaptateur après chaque usage.
- **Contrôle technique / garage** : nécessite de fournir l'adaptateur à chaque visite
- **⚠️ Compatibilité WiCAN Pro** : l'adaptateur Exosfer réorganise les broches → il faut vérifier que le WiCAN Pro fonctionne **à travers l'adaptateur**. Les protocoles CAN (broches 6 et 14) et le bus MS-CAN Ford (broches 3 et 11) doivent être préservés.

---

## Impact projets PKA

| Projet | Impact | Note |
|--------|--------|------|
| **IOT/Vanlife** 🔴 | 🟡 Élevé | Conflit potentiel WiCAN Pro. L'Exosfer sécurise la prise, mais bloque l'usage permanent du dongle OBD. |
| **TRAVELS** | 🟢 Modéré | Sécurité Lupo renforcée. Document à archiver dans `securite/`. |

---

## Propositions

### 🔴 P0 — Vérifier compatibilité WiCAN Pro + Exosfer
- **Action** : Contacter Exosfer (exosfer.fr) ou MeatPi (meatpi.com) pour confirmer que l'adaptateur préserve les broches CAN nécessaires
- **Si incompatible** : deux options —
  - Option A : WiCAN Pro branché uniquement en roulant / parking sécurisé, Exosfer actif la nuit
  - Option B : Chercher une solution OBD qui fonctionne en série avec l'Exosfer

### 🟡 P1 — Photographier le câblage OBD d'origine du Ford Transit Custom
- **Action** : Avant installation Exosfer, documenter chaque fil (position + couleur) → archive dans `securite-van-lupo.md`

### ⚪ P2 — Intégrer la procédure garage dans le manuel Lupo
- Ajouter une section « Procédure OBD au garage » avec les étapes adaptateur

---

## Décision en attente

> La validation de compatibilité Exosfer ↔ WiCAN Pro est un **prérequis** avant la commande du WiCAN Pro (~82 €).

---

*Analyse terminée. Source à archiver dans `07_TRAVELS/van technique/securite/`.*
