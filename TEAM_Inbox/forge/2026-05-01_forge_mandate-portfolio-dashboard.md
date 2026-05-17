# Mandat Forge — Dashboard Suivi de Portefeuille JCH

**From:** Dobby  
**To:** Forge 🦦  
**Date:** 2026-05-01  
**Priorité:** 🟢 Opérationnel — peut démarrer dès que Sigma est onboardée

---

## Objectif

Construire un dashboard léger de suivi de portefeuille d'investissement pour JCH, alimenté par Sigma (Financial Data Analyst, en cours de recrutement) et consulté par Bruno pour les décisions de rééquilibrage.

---

## Ce que le dashboard doit afficher

### Vue principale — Portefeuille actuel

| Colonne | Description |
|---------|-------------|
| Instrument | Nom + ticker + place de cotation |
| Quantité | Nombre de titres / parts |
| Prix d'entrée moyen | En EUR (converti si nécessaire) |
| Prix actuel | Alimenté par API (Yahoo Finance ou Alpha Vantage) |
| Valeur actuelle | En EUR |
| Performance % | Depuis entrée |
| Performance € | Gain/perte latent |
| Poids % | Part dans le portefeuille total |

### Vue secondaire — Alertes

- Position > +/- 5 % sur la journée → alerte visible
- Publication de résultats dans les 7 prochains jours → flag
- Dividende détaché → notification

### Vue tertiaire — Historique des transactions

Date · Instrument · Achat/Vente · Quantité · Prix · Montant total · Frais (TOB + courtier)

---

## Contraintes techniques

- **Local first** — pas de cloud, pas de compte externe. Tourne sur le Mac de JCH
- **Stack simple** : Python (FastAPI ou Flask) + SQLite pour les transactions + HTML/CSS/JS vanilla pour le front
- **Données** : Yahoo Finance API (yfinance) pour les cours — gratuit, pas de clé requise
- **Change** : EUR/USD et EUR/AUD via même API
- **Pas d'authentification** — usage local uniquement

---

## Livrable attendu

1. Script Python qui lit les positions depuis SQLite et rafraîchit les cours
2. Interface HTML simple — une page, lisible sur écran Mac et éventuellement mobile
3. Table `portfolio` dans `team.db` (à soumettre à Castor pour validation schéma avant création)

---

## Coordination

- **Castor** valide le schéma avant que Forge crée les tables
- **Sigma** alimentera les données une fois onboardée
- **Bruno** définit les alertes et seuils — Forge implémente

*Mandat à démarrer après validation schéma par Castor.*
