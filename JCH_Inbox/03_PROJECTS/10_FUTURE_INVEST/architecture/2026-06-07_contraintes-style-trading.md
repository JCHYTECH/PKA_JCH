---
project: Future Invest
type: architecture-constraint
author: "[[Dobby]]"
reviewed_by: "[[Bruno]]"
created: 2026-06-07
status: validé
---

# Contraintes d'Architecture — Style de Trading Implicite

> Ce document formalise les contraintes de conception héritées de l'architecture
> actuelle de l'Event Analyzer. À lire avant tout choix de marché ou calibration
> de paramètres de risque.

---

## 1. Biais implicite : swing trading event-driven

L'Event Analyzer a été architecturé avant que le profil investisseur soit rempli.
Ce faisant, il a encodé un style de trading implicite qui **n'est pas neutre** :

| Choix architectural | Style présupposé | Incompatible avec |
|---|---|---|
| Sources FAO, WASDE, NOAA | Fondamentaux lents (semaines à mois) | Scalping, intraday |
| Chaîne causale en 4 niveaux (24h → 6 mois) | Swing / position trading | Day trading |
| Horizons Opinion Engine : "1-4 semaines" | Swing trading | Intraday, HFT |
| Données en différé 10-15 min (sources gratuites) | Tolérance au délai | Intraday impossible |
| Validation humaine avant exécution | Latence décision assumée | Scalping, réaction rapide |

**Conclusion :** le système est conçu pour du **swing trading event-driven** sur des événements macro/géopolitiques à impact sur les commodités. Ce n'est pas un défaut — c'est une contrainte à documenter et à assumer.

---

## 2. Marchés compatibles avec cette architecture

| Marché | Compatibilité | Raison |
|---|---|---|
| Commodités agricoles (ZW, ZC, ZS, ZR) | ✅ Excellente | Sources FAO/USDA directement applicables |
| Énergie (CL, NG, BRN) | ✅ Bonne | GDELT + macro géopolitique couvre bien |
| Métaux précieux — Or (GC), Argent (SI) | ✅ Correcte | Valeur refuge, corrélée aux chocs macro |
| Indices boursiers (ES, NQ, DAX) | ⚠️ Partielle | Réagissent aux mêmes événements mais avec bruit court terme supplémentaire |
| Crypto Futures (BTC, ETH CME) | ❌ Faible | Déconnectés des fondamentaux macro analysés |
| Taux d'intérêt (ZN, ZB) | ⚠️ Complexe | Nécessite expertise banques centrales — démarrage déconseillé |

---

## 3. Ce que l'architecture ne sait pas faire (limites connues)

- **Timing d'entrée précis** : le système dit "haussier sur ZW dans 1-4 semaines" — pas "entrer à 14h32 sur un pullback à X". Le Decision Layer (à concevoir) devra gérer le timing technique.
- **Gestion de position active** : pas de mécanisme d'ajustement de position en cours (pyramiding, take partial profit). Positions binaires : ouvert / fermé.
- **Événements simultanés contradictoires** : si deux chocs macro se produisent en même temps, le Synthesizer délègue la résolution à JCH — pas de protocole automatique.
- **Données temps réel** : upgrade path non documenté. Si le style évolue vers de l'intraday, coût estimé à évaluer (Bloomberg Terminal ~2 000 $/mois, Refinitiv ~500 $/mois).

---

## 4. Contraintes à respecter lors du choix des marchés (Phase 0)

1. Choisir des marchés dont les fondamentaux sont couverts par au moins 2 agents collecteurs existants.
2. Privilégier les marchés avec des événements macro clairs et espacés (pas de bruit quotidien).
3. Démarrer avec **1 à 2 marchés maximum** pour calibrer le système avant d'élargir.
4. Éviter les marchés à levier extrême pour le paper trading (micro-futures disponibles sur IBKR pour limiter l'exposition).

---

## Voir aussi

- [[2026-06-04_event-analyzer-architecture]] — architecture complète du module
- [[2026-06-04_bruno_profil-investisseur]] — profil investisseur (C3 confirmé : swing event-driven)
- [[2026-06-04_checklist-lancement]] — checklist phases 0 à 4
- [[Bruno]] — validation marchés cibles
