---
project: Future Invest
type: research
author: "[[Dobby]]" (lens [[Bruno]])
created: 2026-11-22
status: shortlist v1 — à passer au double-check IA + JC
scope: Sociétés equity — jambes 1 (efficacité IA) et 2 (data centers actifs)
---

# Shortlist equity — jambes 1 & 2

## Jambe 1 — Efficacité IA (réduire l'énergie/token)

**Constat structurant :** l'inférence représente désormais **60-70 %** de l'énergie
de l'IA (vs l'entraînement). Les leviers d'efficacité : quantification (jusqu'à
−50 % d'énergie), distillation (DistilBERT : +60 % vitesse, −40 % paramètres),
modèles parcimonieux/MoE (DeepSeek-V3 n'active que les paramètres nécessaires).

| Société | Ticker | Thèse efficacité | Liquidité |
|---------|--------|------------------|-----------|
| **Fujitsu** | TYO:6702 | Quantification 1-bit (−94 % mémoire, ×3 vitesse d'inférence) + distillation spécialisée (Takane LLM, Cohere Command A) | ✅ publique |
| **Vertiv** | NYSE:VRT | Refroidissement liquide + gestion d'énergie des data centers (efficacité par unité de calcul) | ✅ publique |

**⚠️ Honnêteté de Dobby :** le cœur de la jambe 1 (modèles efficaces) est
**majoritairement privé ou chinois** — DeepSeek (privé, Chine), Groq, Cerebras,
SambaNova (privés). L'exposition publique liquide est **mince**. La jambe 1 est
donc en partie une thèse VC/privée, pas une thèse de trading liquide. Deux options :
- accepter la jambe 1 comme thèse de conviction (position longue Fujitsu/Vertiv, petite) ;
- la réserver au volet equity non-liquide, hors du cockpit de trading.

## Jambe 2 — Data centers ACTIFS (incumbents, rareté par gel du CAPEX)

| Société | Ticker | Cap (2026) | Capacité existante | Retour 12m (avr 2026) |
|---------|--------|-----------|--------------------|------------------------|
| **Equinix** | EQIX | ~106 Md$ | 522 000 interconnexions, colocation dense | +41 % |
| **Digital Realty** | DLR | ~69 Md$ | 300+ data centers, 50+ métros, wholesale hyperscalers, 21 ans de croissance de CA | +39 % |
| **Iron Mountain** | IRM | — | conversion stockage→colocation | +45 % |

**Lecture (thèse JC) :** ces trois opérateurs détiennent de la capacité **déjà
construite**. Le krach gèle le buildout neuf (coût du capital + hype retombée) →
leur capacité existante devient rare → revalorisation relative. C'est le
« gel du CAPEX → avantage de l'incumbent », robuste aux deux branches de Jevons.

**⚠️ Point corrélation :** ce sont des actions — corrélées au marché (le krach les
a aussi touchées). La jambe 2 est un pari de **valeur relative** (incumbent vs
buildout neuf), pas un actif découplé. Le socle découplé reste l'agricole (futures).

## Prochaine étape

Passer chaque nom au protocole double-check (IA + JC) avant toute entrée :
adoption mesurable, courbe de coût, position Gartner, goulot d'offre, demande
dérivée, verdict croisé. En particulier trancher la **liquidité de la jambe 1**.

## Références (2026-11-22)

- zylos.ai/research (inférence 60-70 % de l'énergie ; quantification/distillation/MoE)
- finance.yahoo.com (Fujitsu : 1-bit quantization −94 % mémoire, ×3 inférence)
- angelinvestorsnetwork.com (EQIX/DLR/IRM : retours 39-45 %, capacité existante)
- fool.com (DLR 300+ DC 21 ans croissance, EQIX 522k interconnexions)
- investing.com (Deutsche Bank bullish EQIX/DLR sur demande IA)
