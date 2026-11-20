# Conseil « service de correction photo » — stance **Expansionniste**

> Dobby 🦉 · conseil du 2026-11-16 · Question : recevoir une photo, la corriger (look « Naturaliste »), la renvoyer — GO, et sous quelle forme ?
> Lecture : `strategy/service-correction-photo-conception.md`, `strategy/contrat-look-naturaliste.md`, `05_PHOTO_AI_JURY/argus_critique.db`, `_local/lightroom-mcp/plugin/`.

## Verdict de stance

**GO — mais GO sur la version qui capture ce que le service produit en passant.** La V0 chiffre le coût du service ; elle ne chiffre jamais son sous-produit. 3 des 4 options ci-dessous coûtent ≈ 0 € de plus que le MVP déjà prévu : ce serait une faute de les laisser sur la table.

## Les 4 upsides que la V0 ne voit pas

- **O1 · Ne pas héberger le service : le livrer en plugin (le service s'efface).** L'archi A plafonne à une file d'attente sur une seule M5 (~20-40 photos/jour) et empile G3/G4/G6. Or le moteur est *déjà* un plugin Lightroom Lua (`_local/lightroom-mcp/plugin/LightroomMCP.lrplugin`, handlers `Develop`/`Export`). Chez le photographe : 0 upload, 0 donnée personnelle, latence nulle, coût marginal nul, scalabilité = nombre d'installations. **39 €/an × 150 abonnés = 5 850 €/an à ~100 % de marge, zéro serveur** ; le RGPD passe de chantier à non-sujet, et l'offre trouve sa place naturelle comme *hook* de l'abonnement 5 €/mois déjà prévu.

- **O2 · La correction est une machine à dataset de préférences, pas un livrable.** `argus_critique.db` contient déjà `retouch_proposals` (paires A/B, `decision a|b|rejected`, `decided_by`) et `retouch_sessions` — **tables vides, jamais alimentées** ; la roadmap le dit noir sur blanc : « aucun dataset artistique JCH ». Servir **deux** corrections au lieu d'une (look A vs look B, un seul paramètre d'écart — permis par la matrice 12 looks × 3 forces du contrat) fait de chaque client un labelliseur : 100 photos/sem ≈ **5 200 paires A/B/an pour ≈ 0 € de collecte** (le service *est* le protocole). Usages : (a) calibrer `/recommend`, le vrai différenciateur ; (b) actif licenciable à un acteur de modèles photo ; (c) antériorité publiable sur un « Naturaliste Engine ». Coût réel borné à $0,174/analyse si Argus est appelé, ~0 en EXIF seul.

- **O3 · L'avant/après est un flux éditorial, pas un email privé.** La V0 renvoie la preuve au seul client. En faire la « Clinique » hebdo de WildLens (1 photo reçue avec consentement → diagnostic → correction → geste à retenir) : **52 éditions/an qui ne consomment aucun temps créatif de JC** (validation ~10 min), là où la cadence du journal dépend aujourd'hui entièrement de lui. Chaque épisode est un lead magnet autoporteur (« envoyez votre photo ») et alimente Instagram sans effort supplémentaire.

- **O4 · Le lot B2B : clubs, fédérations, festivals, écoles.** La V0 ne vend qu'à l'unité, à des individuels. Le même pipeline vendu au lot : **390 €/an/club** (chiffre déjà posé au conseil du 16/11) ou **0,50 €/photo** pour un lot d'exposition (200 photos = 100 €/lot) ; 20 clubs ≈ **7 800 €/an**. Argument qu'aucun concurrent ne peut tenir : « votre exposition normalisée au regard d'un zoologiste, avec le pourquoi documenté ». Le coût marginal reste du temps Lightroom ; la valeur passe de 29 € l'unité à 390 € l'organisation.

## Trois clauses à coût quasi nul pour ne pas perdre l'upside

1. **A/B dès le MVP** : deux exports par photo + un bouton de vote (O2). Fait après coup, c'est perdu — les photos ne sont pas rejouables.
2. **Consentement explicite à la réutilisation** (case à cocher) : débloque O2 et O3 et rend G6 *utile* au lieu de subi.
3. **Moteur découplé de la M5** : `/recommend` doit pouvoir tourner dans le plugin (O1), sinon l'archi A devient un plafond définitif.

**Ce qui tuerait l'upside** : un `/recommend` qui ne rend qu'une réponse fermée (1 look + 2 ajustements) — parfait pour la démo, stérile pour l'actif ; et un service hébergé qui casse la boucle dès 200 photos/mois, forçant à choisir entre scaler l'infra et scaler le corpus.
