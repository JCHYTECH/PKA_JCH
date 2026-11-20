# État des projets — One-Pager
> Tableau de bord unique de tous les projets actifs PKA_JCH.
> Dernière mise à jour : 2026-11-20 par Dobby 🦉 — pivot WildLens « tout en français » (3 éditions FR, thème FR, locale fr) ; ligne Proximus dégradée (14/11) toujours à traiter (RUT240 atelier + failover 4G à planifier).
> 
> **Lecture :** 🔴 = P0 deadline dure, 🟢 = actif autonome, ⚪ = gelé/reporté

---

## 🔴 P0 — Deadline 15 décembre 2026 (installation IOT Van)

| # | Projet | Statut | Dernière action | Prochaine étape | Blocage | Spécialiste(s) |
|---|--------|--------|-----------------|-----------------|---------|----------------|
| 1 | **IOT / Vanlife** | 🔴 P0 | MCP HA Lupo read-only testé avec Kimi/DeepSeek ; dashboard AirGuard et première copie Time Machine validés. | Vérifier la copie Time Machine automatique et hors RPi ; revalider le lot P1 puis intégrer WiCAN Pro + RUT240 dans Lupo. **RUT240 atelier (IP fixe + failover 4G vs coupures Proximus) — session à planifier. ⚠️ Ligne Proximus mesurée dégradée le 14/11 (2 s latence, 10,5 % perte, 6,15 Mbit/s) → rapport `rapport-box-proximus-2026-11-14.md`.** | Quantités et budget d'achat à consolider | Forge, Araignée, Dobby |

---

## 🟢 P1 — Actifs autonomes ou en continu (charge JC variable)

| # | Projet | Statut | Dernière action | Prochaine étape | Spécialiste(s) |
|---|--------|--------|-----------------|-----------------|----------------|
| 2 | **PHOTO_NATURE** | 🟢 autonome | Keyworder et 11 presets Argus ; correctif `headline` confirmé dans le code (22/10) | Maintenance (aucun nouveau run mesuré dans cette revue) | Lynx, Nova, Héron |
| 3 | **PHOTO_AI_JURY** | 🟢 autonome | Base canonique schéma v1 : 52 analyses et 16 évaluations conservées ; test MCP Lightroom `0 → +0,10 → 0` réussi sur copie virtuelle RAW | Recueillir les choix A/B de JCH avec tutoriel et validation sur image inédite ; aucun style déduit des votes sur les rapports | Argus |
| 4 | **AI_IT_TOOLS** | 🟢 autonome | MCP HA Lupo read-only validé avec Kimi/DeepSeek ; `/save` Kimi déjà opérationnel | Réauthentifier Claude, traiter séparément les modèles Codex refusés et essayer le TUI Grok ; ne pas exposer HA publiquement | Dobby, Forge |
| 7 | **ARTEON + WildLens** | 🟢 réactivé | Compte Ghost **récupéré** (admin accessible, essai 14 j) ; 1 post « Coming soon », 0 membre ; domaine final `wildlens.arteon.be` ; **VPS Hostinger créé + Ghost installé 15/11** (IP 2.25.8.208) ; **pilier tirage → « ARTEON Éditions » (GO conditionnel, conseil 17/11)** | **Pivot FR (19/11)** : 3 éditions FR en production (#1 publiée 18/11, #3 28/11, #2 05/12), thème FR + locale fr ; reste abonnement ; publication Instagram sur demande explicite ; **combler la compétence impression photo (lacune actée) avant toute édition** ; séquence presets → WildLens → édition #1 | Dobby, Forge |
| 8 | **TRAVELS** | 🟢 actif — planification « en roulant » | Pipeline DÉCOUVERTES continu, 647 lieux validés, Planner synchronisé ; boîte vélo en conception | Traiter 50 éléments résiduels et poursuivre les aménagements du van | Cigogne, Dobby |
| 9 | **VENTE_OCCASION** | 🟢 Phase 1 | Structure + skill `vente-occasion` créés (30/10) ; six objets en cours, aucun vendu | Finaliser photos/annonces, publication et suivi des six objets selon leur état réel | Dobby (+ Pie à confirmer) |

---

## 🔶 Réactivé

| # | Projet | Statut | Dernière action | Prochaine étape | Spécialiste(s) |
|---|--------|--------|-----------------|-----------------|----------------|
| 5 | **VETALYX** | 🔶 actif (juridique) | Traduction EN du pacte d'actionnaires produite + revue Renard ; **pacte EN envoyé aux partenaires chinois le 08/11**. | Trancher le point Art. 5.1 (« non opposables ») ; valider la mécanique notariale des 6 000 € et la qualification AFMPS/FAMHP. | Renard, Clio, Jade |
| 6 | **WILDNEXUS DEVICE** | 🔶 réactivé (P0 engineering) | Dégelé le 12/11 (décision JC) ; P0 engineering repris le 11/11, SOP-16/17/18 créées. | Lever les gates de reprise : inventaire matériel, rapprochement factures, micros TDK + PIR, matrice GPIO. Aucun montage ni achat avant. | Forge, Araignée, Dobby |

---

## ⚪ Gelés — reprise à replanifier

| # | Projet | Statut | Raison du gel | Reprise prévue |
|---|--------|--------|---------------|----------------|
| — | **INSECTNET** (classification orthoptères) | ⚪ gelé | Pipeline en pause — migration M1 à exécuter ; dépend des clips WAV produits par le nœud device. | Post-reprise DEVICE |
| — | **NEXUS_ACOUSTIC** (BirdNET/TweetyBERT/LEAFNET) | ⚪ gelé | Dépend de la capture WildNexus P0. | Post-reprise DEVICE |

---

## Projets inactifs / archivés

| Projet | Statut | Note |
|--------|--------|------|
| WILDMESH | ⚪ gelé | Réseau LoRa mesh — en attente de maturité WildNexus |
| FUTURE_INVEST | ⚪ gelé | Archivé le 2026-06-23 |
| Maison off-grid | ⚪ concept | Phase concept uniquement |
| FAUNE_AUTOUR | ⚪ gelé | PWA extraite dans PHOTO_NATURE |

---

## Résumé

| Indicateur | Valeur |
|------------|--------|
| Projets totaux | 9 |
| 🔴 P0 (deadline dure) | 1 — IOT/Vanlife |
| 🔶 Réactivé | 2 — VETALYX (juridique), WILDNEXUS DEVICE (P0 engineering) |
| 🟢 P1 (autonome ou continu) | 6 — PHOTO_NATURE, PHOTO_AI_JURY, AI_IT_TOOLS, ARTEON, TRAVELS, VENTE_OCCASION |
| ⚪ Gelé (sous-projets) | 2 — INSECTNET, NEXUS_ACOUSTIC |
| Prochaine échéance | **15 décembre 2026** — installation IOT Van |

---

## Relations inter-projets photo

```
PHOTO_NATURE (terrain, technique, keyworder)
        │
        │ photos brutes + presets Argus
        ▼
PHOTO_AI_JURY (Argus — 58 historiques / 52 analyses conservées, schéma v1)
        │
        │ rapports PDF + presets XMP + conseil papier
        ▼
ARTEON (shop + marque + L'Instant Lu)
        │
        │ acquisition
        ▼
WildLens (journal hebdomadaire — tête du funnel)
```

*Mise à jour par Dobby 🦉 à chaque changement d'état d'un projet.
Source : MEMORY.md, TEAM_Inbox/, 03_PROJECTS/, kanban, wiki/Daily.*