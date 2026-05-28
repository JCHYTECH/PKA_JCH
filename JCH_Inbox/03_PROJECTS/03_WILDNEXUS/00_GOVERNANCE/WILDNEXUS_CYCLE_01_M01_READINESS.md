# WildNexus — Cycle 01 / M-01 Readiness

**Version :** v0.1  
**Date :** 2026-05-18  
**Statut :** Cycle 01 lancé — Plane synchronisé  
**Owner :** [[Dobby]]  

## 1. Objectif du cycle

Préparer le gel d'architecture P0 (`M-01 Architecture gelee`) sans fabrication ni commande significative.

Le cycle est terminé quand les choix caméra, MCU, radio, budget, gouvernance d'agents et risques juridiques sont suffisamment cadrés pour autoriser le passage vers `M-02 Prototype banc fonctionnel`.

## 2. Situation initiale

| Domaine | Statut | Commentaire |
|---|---|---|
| Périmètre P0 | Cadré | `../01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md` verrouille les exclusions P0 |
| Mapping agents | Cadré | `WILDNEXUS_AGENT_MAPPING.md` relie agents WildNexus et PKA |
| Budget P0 | Première fourchette | `../03_P0_ENGINEERING/WILDNEXUS_P0_BUDGET_RANGE.md`, précision cible ±30% |
| Plane | Synchronisé | API locale revenue après installation du service `com.jchytech.pka-plane-autostart` |
| [[Docker]] | Relancé automatiquement | service launchd PKA installé pour démarrer [[Docker]] Desktop puis Plane |
| Backlog | Synchronisé | nouveaux items Cycle 01 créés dans Plane le 2026-05-18 |
| Données projet | Initialisé | `data/README.md` créé |

## 3. Fronts ouverts

| Item | Front | Owner PKA | Agent WildNexus | Livrable attendu | Statut |
|---|---|---|---|---|---|
| 
| 
| 
| 
| 
| 
| 
| 
| 
| 

## 4. Définition de `M-01 ready`

`M-01` peut être marqué prêt quand :

- une caméra candidate est choisie et justifiée ;
- un MCU candidat est choisi et justifié ;
- une option radio / LPWAN est choisie et justifiée ;
- l'enveloppe P0 est confirmée ou réduite ;
- le registre composants critiques contient au moins une alternative par poste bloquant ;
- la licence / FTO ne bloque pas le prototypage interne ;
- le périmètre P0 reste strict ;
- les risques RGPD terrain ont un owner et un livrable concret ;
- Plane est synchronisé ou la [[Trace]] offline est complète.

## 5. Risques actifs

| Risque | Niveau | Owner | Mitigation immédiate |
|---|---|---|---|
| Plane local indisponible au redémarrage | Réduit | [[Forge]] | service launchd 
| Scope creep bioacoustique / Faune Autour | Élevé | [[Dobby]] | verrou P0 déjà écrit |
| Budget P0 sous-estimé | Élevé | [[Bruno]] | passer du pré-budget aux références fournisseurs |
| FTO / licence retardée | Élevé | [[Renard]] + [[Hermine]] | cadrer prototypage interne vs publication publique |
| Disponibilité composants | Élevé | [[Bruno]] + [[Forge]] | registre supply avec alternatives |
| RGPD terrain EVT | Moyen | [[Renard]] | modèle signalétique + procédure floutage/suppression |

## 6. Prochaines actions [[Dobby]]

1. Produire ou compléter `../03_P0_ENGINEERING/WILDNEXUS_SUPPLY_REGISTER.md`.
2. Préparer les trois ADR de départ : MCU, caméra, radio.
3. Préparer la note juridique initiale FTO/licence avec [[Renard]] + [[Hermine]].
4. Surveiller le service autostart Plane après le prochain redémarrage macOS.

## 7. Commandes de synchronisation

Dry-run :

```bash
python3 scripts/seed_wildnexus_plane.py
```

Application :

```bash
python3 scripts/seed_wildnexus_plane.py --apply
```

État après correction : synchronisation appliquée le 2026-05-18.

Items créés :

- `T01.6 Budget P0 ordre de grandeur`
- `GOV-01 Mapping agents WildNexus vers specialistes PKA`
- `DOC-01 Annexes operatoires v0.3`
- `SUPPLY-01 Registre composants critiques et fournisseurs alternatifs`
- `T03.6 Tests firmware et simulation etats critiques`
- `T04.5 Pipeline evaluation automatise du classifieur`
