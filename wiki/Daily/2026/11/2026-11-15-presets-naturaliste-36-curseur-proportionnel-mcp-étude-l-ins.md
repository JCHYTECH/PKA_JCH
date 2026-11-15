---
date: 2026-11-15
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-15 — Presets Naturaliste 36 + curseur proportionnel MCP + étude L'Instant Lu

## Session — 23:04 — Presets Naturaliste 36 + curseur proportionnel MCP + étude L'Instant Lu

### Contexte
- Modèle : deepseek
- Projet : ARTEON

### Résumé
Session ARTEON charnière (photo). L'Instant Lu passé au conseil 6 stances : verdict NO-GO « lancer tel quel », recadrage vers presets + WildLens (badge « Vérifié » gelé). Pack presets Naturaliste : 36 XMP (12 looks × 3 forces), mode d'emploi + landing, bug courbe ToneCurve corrigé (RDF Seq au lieu d'attribut — Lightroom la jetait). Innovation slider : curseur de force global proportionnel pilotant Lightroom via MCP (set_develop_settings + courbe paramétrique, car le Amount natif ne scale pas la courbe ni le grading) ; brique 2 = sélecteur 12 looks (looks.mjs + strength_server.mjs) ; fix perf (cache PhotoLookup 1×/session + sérialisation « dernier gagne » + retry). Étude marché presets : recensement XMP + cartographie fonctionnelle → créneau Vincent Munier non servi, premium = masques IA. Mémoire VPS Hostinger corrigée (créé + Ghost installé ; reste DNS/SSL/Mailgun/migration).

### Actions
- Diagnostiqué backend Argus : argus_critique.db = 52 analyses, claude-opus-4-7, coût moyen $0,174, score moyen 76,7/100 (range 57-86, 0 EXCEPTIONNEL).
- Conseil 6 stances parallèles sur L'Instant Lu → plan-reorientation-instant-lu.md.
- Généré 36 presets XMP (gen_presets_v2.py) ; mode d'emploi + landing mis à jour (12 looks, plus 4).
- Corrigé la courbe ToneCurve en RDF Seq (attribut → Seq) + SupportsAmount.
- Étendu l'allowlist Lightroom MCP (ToneCurve + TSL + ColorGrade, ~48 clés) ; compilé + copié HandlerDevelop.lua.
- Constat SDK : applyDevelopSettings n'applique PAS la courbe de points → bascule courbe paramétrique.
- Bâti le slider de force (strength_server.mjs, HTTP 8790) + module looks.mjs (12 looks paramétriques) + sélecteur.
- Fix perf : cache d'index PhotoLookup + sérialisation apply + retry transitoire.
- Avant/après réels sur RAW oies du Nil (Marcourt-0183, EOS R10, 637 mm).
- Recensement marché XMP (recensement-presets-xmp-animaliere.md) + cartographie fonctionnelle (3 dimensions).

### Décisions
- L'Instant Lu : NO-GO « lancer tel quel » → recadrer (retirer badge, prix ≥4-5 €, valider l'espèce, conseil éditorial).
- Curseur proportionnel = différenciateur technique (le Amount natif de Lightroom ne scale pas la courbe ni le grading — nous si).
- Aucune réutilisation de XMP tiers (licences « usage personnel ») — différenciation = regard zoologiste curé.
- Feuille de route presets : brique 3 = masques IA (le vrai premium $55+), brique 4 = endpoint /recommend (EXIF niveau 1 d'abord).
- VPS Hostinger : créé + Ghost installé (IP 2.25.8.208) ; reste DNS A → 2.25.8.208, SSL, Mailgun, migration.

### Prochaines étapes
- Pointer DNS A wildlens → 2.25.8.208 (registrar arteon.be) puis ghost setup ssl + Mailgun + migration contenu.
- Nettoyer le doublon de preset LRC (37 importés au lieu de 36).
- Brique 3 : masques IA (sujet/œil/plumage/arrière-plan).
- Brique 4 : endpoint /recommend (niveau 1 EXIF d'abord, puis vision légère).
- Galerie avant/après définitive (12 paires) ; cadrage juridique presets tiers si intégration (Renard).
- P0 parallèle : IOT Van (dl 15/12), VETALYX.
