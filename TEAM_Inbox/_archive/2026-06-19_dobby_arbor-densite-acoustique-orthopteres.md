# Arbor Loop — Densité acoustique d'orthoptères
> Challenge : convertir « N individus détectés » en « individus/m² »
> 2026-06-19 — Dobby 🦉

---

## 🌳 Arbre d'hypothèses

```
┌─ H1: Rayon de détection calibré ── Expérience: calibration dBFS→dB SPL ── RESOLU
│   └─ πr² → densité si distance connue
│
├─ H2: Propagation inverse ── Expérience: atténuation atmosphérique ── RESOLU
│   └─ r = f(SPL_source, bruit_fond, α)
│
├─ H3: Distance sampling ── Expérience: estimer distance par amplitude ── À FAIRE
│   └─ Chaque individu a une distance estimée → fonction de détection
│
├─ H4: Triangulation stéréo ── Expérience: 3 enregistrements espacés ── À FAIRE
│   └─ Positionner chaque individu par azimut croisé
│
└─ H5: Spatial Capture-Recapture ── Expérience: sessions répétées ── FUTUR
    └─ Suivre les mêmes individus sur plusieurs nuits
```

---

## Résultats — Estimation pour SP 31 3

| Scénario | Bruit fond | Rayon détection | Surface | Densité (1 grillon) |
|----------|-----------|-----------------|---------|---------------------|
| Nuit très calme | 25 dB | 139 m | 6.0 ha | 0.17 / ha |
| Nuit calme | 30 dB | 81 m | 2.0 ha | 0.49 / ha |
| Vent léger | 40 dB | 27 m | 0.2 ha | 4.5 / ha |
| Bord de route | 50 dB | 9 m | 0.02 ha | 42 / ha |

**Conclusion :** 1 grillon dans SP 31 3 = entre 0.2 et 5 individus/ha selon les conditions.

---

## Pour réduire l'incertitude (facteur 10 → facteur 2)

1. **Calibrer l'iPhone** — enregistrer un son de niveau connu à 1m (clap, diapason, ou app sonomètre)
2. **Mesurer le bruit de fond absolu** — application sonomètre gratuite (NIOSH SLM)
3. **Trianguler** — 3 enregistrements à 10m d'écart → positionner chaque grillon par azimut croisé
4. **Répéter** — même spot, nuits différentes → confirmer la densité

---

## Protocole terrain proposé

```
Position A ──── 10m ──── Position B ──── 10m ──── Position C
    │                        │                        │
    └──── Enregistrer 3 min à chaque position ────────┘
    
Pour chaque grillon détecté :
  → Azimut depuis A, B, C (analyse stéréo)
  → Intersection des 3 azimuts = position (x,y)
  → Distance au point central = rayon effectif
  → Surface = π × r²
  → Densité = N / surface
```

---

## Statut

- [x] H1 modélisée (propagation sphérique)
- [x] H2 modélisée (absorption atmosphérique)
- [ ] H3 : calibration dBFS→dB SPL (nécessite matériel)
- [ ] H4 : protocole triangulation (3 positions)
- [ ] H5 : spatial capture-recapture (sessions répétées)

*Priorité : P1 — nécessite calibration terrain.*
