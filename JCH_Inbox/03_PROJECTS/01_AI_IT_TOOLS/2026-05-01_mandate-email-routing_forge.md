# Mandat [[Forge]] — Email Routing Intelligence

**From:** [[Dobby]] 🦉 | **To:** [[Forge]] 🦦 | **Date:** 2026-05-01  
**Priorité :** Haute — extension de email_digest.py

## Objectif

Ajouter un module de routing intelligent à `email_digest.py` :
chaque [[email]] entrant est analysé, routé vers le bon spécialiste,
et ses actions déclenchées automatiquement dans team.db.

---

## Module à implémenter : `route_email()`

### Fonction signature
```python
def route_email(subject, body, sender_email, sender_name, email_date) -> list[dict]
```
Retourne une liste d'actions à exécuter (peut être vide).

---

## Règles de routing par spécialiste

### 🦊 [[Renard]] — Legal Counsel
**Déclencheurs (subject ou body) :**
```python
RENARD_KEYWORDS = [
    "contrat", "contract", "pacte", "actionnaire", "nda",
    "confidentialité", "signature", "clause", "avocat", "notaire",
    "juridique", "tribunal", "litige", "mise en demeure",
    "résiliation", "accord", "convention", "statuts", "cession",
    "acquisition", "due diligence", "term sheet", "compliance"
]
```
**Actions :**
- INSERT dans `inbox` : direction=`JCH→TEAM`, from=`JCH`, to=`Renard`, subject=objet [[email]], body=résumé
- Notification push priorité haute : `🦊 Renard — email légal détecté`

---

### 🐺 [[Vasco]] — Veterinary Product Specialist
**Déclencheurs :**
```python
VASCO_KEYWORDS = [
    "vetalyx", "vitalyx", "vétérinaire", "veterinaire", "allergie",
    "diagnostic", "ivd", "clinique vétérinaire", "médicament",
    "prescription", "panel allergène", "test sérologique",
    "dermatite", "atopie", "respiratory", "food allergy",
    "nutraceutique", "supplément", "probiotique"
]
```
**Actions :**
- INSERT dans `inbox` : to=`Vasco`
- Notification : `🐺 Vasco — email Vetalyx/clinique détecté`

---

### 🐻 [[Bruno]] — Finance & Investment
**Déclencheurs :**
```python
BRUNO_KEYWORDS = [
    "investissement", "financement", "valorisation", "levée de fonds",
    "dividende", "bilan", "fiscal", "impôt", "capital", "parts sociales",
    "budget", "trésorerie", "term sheet", "due diligence",
    "portefeuille", "rendement", "actions", "obligations", "etf",
    "placement", "patrimoine", "private equity"
]
```
**Actions :**
- INSERT dans `inbox` : to=`Bruno`
- Notification : `🐻 Bruno — email financier détecté`

---

### 🐬 [[Delphi]] — CRM

**Cas 1 — Contact connu ([[email]] dans `contacts`)**
- INSERT dans `interactions` : contact_id=id trouvé, type=`email`, date=aujourd'hui, summary=objet
- Mettre à jour `contacts.last_contact` = aujourd'hui

**Cas 2 — Contact inconnu mais score > 3**
- INSERT dans `inbox` : to=`Delphi`, subject=`Nouveau contact potentiel : {sender_name}`, body=`{sender_email} — {subject}`

**Cas 3 — Demande de rendez-vous détectée**
```python
MEETING_KEYWORDS = ["rendez-vous", "meeting", "réunion", "call", "disponible", "agenda", "planifier", "slot"]
```
- INSERT dans `follow_ups` : contact_id si connu, due_date=demain, subject=`Répondre : {subject}`

---

## Priorités de notification push

| Route | Priority ntfy |
|-------|--------------|
| [[Renard]] (légal) | 5 — urgent |
| [[Vasco]] (Vetalyx) | 4 — high |
| [[Bruno]] (finance) | 4 — high |
| [[Delphi]] nouveau contact | 3 — default |
| [[Delphi]] interaction loguée | silencieux (pas de push) |

---

## Règles d'implémentation

- Un [[email]] peut déclencher **plusieurs routes** (ex: [[email]] Vetalyx avec clause contractuelle → [[Vasco]] + [[Renard]])
- Routing effectué sur `subject` + premiers 500 chars du body (si body disponible)
- Body disponible uniquement si `score > 2` (éviter les appels API inutiles)
- Toutes les insertions DB dans un try/except — une erreur DB ne bloque jamais la notification push
- Ajouter colonne `routed_to` dans le rapport de notification : `→ Renard, Delphi`

---

## Fichiers concernés

- `scripts/email_digest.py` — ajouter `route_email()` + appel dans `main()`
- `team.db` — écritures dans `inbox`, `interactions`, `follow_ups`, `contacts`

## Livrable

Script mis à jour + test sur un [[email]] réel par route.
