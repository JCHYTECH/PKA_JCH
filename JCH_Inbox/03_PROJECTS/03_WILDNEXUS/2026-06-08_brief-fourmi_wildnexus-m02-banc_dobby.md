# Brief — Fourmi 🐜 : Assistance banc M-02 Partiel (Phases A→E)

**Date :** 2026-06-08  
**De :** [[Dobby]]  
**Pour :** [[Fourmi]]  
**Projet :** [[WildNexus]]  
**Objet :** Accompagner JCH sur l'exécution du protocole M-02 partiel

---

## Ta mission

Tu assistes JCH en temps réel sur le banc d'essai. Tu ne touches pas le matériel — c'est JCH qui manipule. Ton rôle :

1. **Lire chaque étape à voix haute** avant qu'il ne l'exécute
2. **Vérifier chaque branchement** — polarité, présence USB, PPK2 OFF
3. **Dicter les mesures à noter** dans le CSV
4. **Diagnostiquer** si un résultat ne correspond pas à l'attendu
5. **Arrêter immédiatement** si tu détectes un risque (double alim, surchauffe, >500 mA)

Tu n'improvises pas. Tu suis le protocole ligne à ligne.

---

## Documents de référence

- **Protocole :** `PROTOCOLES/2026-06-08_m02-partiel-phases-A-a-E.md`
- **CSV mesures :** `PROTOCOLES/2026-06-08_mesures-esp32s3-ppk2_template.csv`

---

## Points de vigilance critiques (à annoncer AVANT chaque transition)

| Moment | Ce que tu dis |
|--------|--------------|
| Fin Phase A | « ⚠️ POINT DE RUPTURE — à partir d'ici, le PPK2 prend le relais. Débranche l'USB de l'ESP32. » |
| Avant Phase C | « Vérifie : PPK2 sortie OFF. Tu branches GND d'abord, puis VOUT. Rien sur l'USB ESP32. » |
| Fin Phase C | « ⚠️ POINT DE RUPTURE — débranche le PPK2 avant de rebrancher l'USB. » |
| Fin Phase D | « ⚠️ POINT DE RUPTURE — débranche le PPK2 avant de rebrancher l'USB. » |

---

## Grille de décision (à garder sous les yeux)

| Mesure | Go | Orange | No-Go |
|--------|:--:|:------:|:-----:|
| Deep sleep | < 100 µA | 100-150 µA | > 200 µA |
| Charge/événement | < 1.5 mAh | 1.5-2.5 mAh | > 2.5 mAh |
| Autonomie 3 evt/h | ≥ 60 j | 45-60 j | < 45 j |
| Stabilité | 100 cycles OK | 1-2 erreurs | Blocage récurrent |

Si No-Go confirmé sur un critère → tu m'alertes immédiatement. Ne laisse pas JCH continuer.

---

## Diagnostic rapide

| Observation | Diagnostic probable |
|-------------|---------------------|
| Pas de pic, courant nul | Câblage défectueux ou sortie PPK2 OFF |
| Courant élevé constant | Carte pas en sleep ou court-circuit |
| Deep sleep en mA | DevKit trop consommateur → documenter, ne pas paniquer |
| Blocage / pas de réveil | Firmware mal flashé ou conflit GPIO |

---

## Après la session

Tu remplis les colonnes C/D/E du CSV et tu me transmets les résultats. Si tout est Go ou Orange, l'ESP32-S3 est validé pour la suite P0. Si No-Go, j'escalade à [[Castor]] + [[Forge]].

---

Tu es prête. Le protocole est ton unique référence. Pas un mot de plus, pas un mot de moins.
