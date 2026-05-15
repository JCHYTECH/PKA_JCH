---
date: 2026-05-03
tags: [daily]
type: daily
status: active
---

# 2026-05-03 — Session PKA

## Actions — Session 13

- **Mail DIM3** : facture 2026-2-1 analysée (€5.235,67 TTC) — texte explicatif rédigé pour Maître Alsteens (prestations conseil + TVA avance €6.500 + solde €1.050 + matériel en attente de facture + proposition compensation déchets)
- **Déchets médicaux DIM3** : tubulures et poches entérale vides sans contact patient = pas des DASRI → poubelle ordinaire, zéro coût
- **Comptabilité DIM3** : pièces à émettre identifiées — facture d'acompte rétroactive + note de crédit €1.050 → transmis au comptable
- **Pie #24 onboardée** : analyste contenu mails & SAC — FR+EN natif, ZH→Jade, intégrée pipeline digest
- **email_digest.py enrichi** : Pie analyse tous les mails nouveaux (intention/urgence/sentiment/langue/projet/résumé), labels `!PKA/XXX` créés dans Gmail (tête panneau gauche), routing Delphi corrigé (score ≥ 2 uniquement), SPAM_SENDERS ajoutés (Temu, AliExpress…), labels affichés dans digest
- **Réauthentification Gmail** : scope `gmail.modify` ajouté, `get_credentials()` corrigé avec flux OAuth
- **Furet mandaté** : profil analyste mails → Pie défini et onboardé
- **Facebook Marketplace** : recherche automatisation Belgique — verdict : Meta AI native (gratuit) suffit pour volume faible (imprimante, moto, divers) — JCH en direct, pas d'équipe nécessaire
- **Retour équipe** : Dobby a sollicité l'équipe sur ses axes d'amélioration — briefs trop incomplets, boucle non fermée, Corbeau non alimenté, Nova/Vasco/Miel en veille active

## Décisions — Session 13

- **Pie** = analyste mails #24 (pas extension Delphi) — profil distinct justifié par SAC futur ARTEON
- **Nova/Vasco/Miel** mis en veille active — recrutés trop tôt, profils à revoir quand projets ARTEON/Vetalyx/WildLens seront matures
- **Facebook Marketplace** : JCH en direct pour ventes d'occasion ponctuelles — brief équipe coûte plus que la vente elle-même
- **Labels Gmail** : préfixe `!PKA/` pour apparition en tête de liste (ordre alphabétique ASCII)
- **DIM3 déchets** : pas de prestataire spécialisé nécessaire — poubelle ordinaire

## Prochaine étape — Session 14

- JCH : lancer digest et vérifier labels `!PKA/` dans panneau Gmail
- JCH : signer DPA Anthropic (trust.anthropic.com)
- JCH : mandater conseil PI marque ARTEON (~€400)
- JCH : récupérer facture matériel DIM3 auprès d'Alsteens
- JCH : envoyer mail Alsteens (texte livré session 13)
- Forge : brancher Pie sur pipeline (fait) — tester sur vrais mails SAC quand L'Instant Lu live
- Corbeau : alimenter `knowledge` avec livrables sessions précédentes
- Phase 0 ARTEON : sélectionner 50 photos JCH pour pipeline Argus
