# VENTE OCCASION — Index projet

> Vente d'objets, livres, matériel sur les sites de seconde main (Belgique).
> Créé le 2026-10-30 — Phase 1 validée par JC.
> **Source de vérité opérationnelle : `thread-vente.md`** (le reste s'aligne dessus).

## ⭐ Point d'entrée

- 🟢 **[thread-vente.md](thread-vente.md)** — living doc : état opérationnel à jour.
- **Skill Dobby : `vente-occasion`** — le pipeline automatisé (estimation → annonce → recommandation → suivi).

## Pipeline (Phase 1)

```
1. JC dépose photos + fiche objet  →  inbox/
2. Dobby (skill vente-occasion)     →  estimation prix Belgique (2dehands/Vinted/eBay)
3. Dobby                            →  rédaction annonce (FR + NL) + recommandation site
4. JC publie (manuel, ou Omnivaleur plus tard)
5. Suivi réponses                   →  suivi/  (flag spam, états)
6. Objet vendu                      →  rentabilite.csv  (marge)
```

## Structure

```
12_VENTE_OCCASION/
├── INDEX.md                    ← ce fichier
├── thread-vente.md             ← living doc (source vérité)
├── inbox/                      ← zone de dépôt : photos + fiche objet à traiter
│   └── _modele-fiche-objet.md
├── annonces/                   ← annonces rédigées (une par objet)
│   └── _modele-annonce.md
├── suivi/                      ← tracker réponses/acheteurs par objet
│   └── _modele-suivi.md
├── archives/                   ← objets vendus / abandonnés
└── rentabilite.csv             ← tableau opérations + rentabilité (séparateur ;)
```

## Marketplaces ciblées (Belgique)

| Site | Idéal pour | API |
|---|---|---|
| **2dehands / 2ememain** | meubles, électroménager, matériel, volumineux, local | Adevinta 1.0 (partenaire) |
| **Vinted** | vêtements, livres, petits objets expédiables | aucune publique |
| **eBay** | électronique, collection, pièces rares, enchères | officielle (Browse + Sell) |
| **Facebook Marketplace** | vente express locale (spam élevé) | aucune officielle |

## Décisions Phase 1

- **Build léger, 0 €/mois** : couche IA (estimation + annonce + recommandation) + tracker local.
- **Phase 2 (différée)** : si volume devient goulot → Omnivaleur (Light 9,99 € / Pro 19,99 €/mois) pour la publication multi-sites + analytics.
- **Pas d'API payante ni de scraping** en Phase 1 (fragile vis-à-vis des CGU 2dehands/Vinted).

## Spécialiste

- **Pie 🐦** — chiffrage, estimation de valeur, rentabilité (à confirmer par JC).

---

*Généré par Dobby 🦉 — 2026-10-30.*
