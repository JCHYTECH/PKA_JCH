# 🌳 Arbor — InsectNet Classification V0.1

> 2026-06-19 — Dobby 🦉

## Arbre

```
ROOT (merged, baseline 0.20)
│
├─ H1 (PRUNED) — BirdNET logits + descripteurs spectraux
│   Verdict : BirdNET ne voit que la fréquence porteuse, pas la structure fine
│   ΔF1 = 0 → aucun gain sur logits seuls
│
└─ H2 (MERGED) ★ — CNN from scratch sur mel-spectrogrammes
    Verdict : F1 = 0.98 sur 5 espèces, 98% accuracy
    Modèle : tmp/insectnet_cnn.pt
```

## Résultat

| Espèce | Precision | Recall | F1 |
|--------|:---------:|:------:|:--:|
| Gryllus campestris | 0.98 | 1.00 | 0.99 |
| Leptophyes punctatissima | 0.98 | 1.00 | 0.99 |
| Pholidoptera griseoaptera | 0.97 | 0.97 | 0.97 |
| Roeseliana roeselii | 0.97 | 0.97 | 0.97 |
| Tettigonia viridissima | 1.00 | 0.95 | 0.97 |
| **Macro avg** | | | **0.98** |

## Dataset

- 5 espèces, 187 enregistrements Xeno-Canto (qualité A+B, worldwide)
- 5 442 segments de 3 secondes
- Train: 800, Test: 200 (équilibré)

## Décision

**MERGE H2** — Le CNN sur mel-spectrogrammes est la baseline V0.1 validée.
H1 est élagué définitivement — BirdNET n'est pas adapté aux insectes.

Prochaine étape : exporter en ONNX/TFLite, tester sur les enregistrements iPhone de JC.
