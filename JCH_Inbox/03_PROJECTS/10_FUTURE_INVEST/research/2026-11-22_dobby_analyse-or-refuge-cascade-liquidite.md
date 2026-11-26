---
project: Future Invest
type: research
author: "[[Dobby]]" (lens financier [[Bruno]])
created: 2026-11-22
status: livré
scope: Pourquoi l'or n'est plus « refuge » cette semaine — et ce que ça dit de la prévisibilité
sources: web (Tavily) — voir références en fin de doc
---

# L'or n'est plus le refuge — ce n'est PAS une anomalie

## Ta lecture (et pourquoi elle est légitime)

Tu lis la baisse simultanée de l'or (−9,2 %) et des actions comme un **signal
d'inquiétude supplémentaire sur la prévisibilité** : si même la valeur refuge
« sûre » se comporte à l'envers, alors les relations de marché sur lesquelles on
s'appuie ne tiennent plus.

C'est une bonne intuition, mais elle pointe vers un **modèle trop simple**, pas
vers un marché devenu imprévisible.

## Ce qui se passe réellement — le pattern « dash for cash »

La baisse de l'or en même temps que les actions est **un pattern documenté**, pas
une nouveauté :

| Épisode | Ce qui s'est passé |
|---------|--------------------|
| **2008 (Lehman)** | Or −30 % de mars à octobre, tout vendu pour couvrir les margin calls. « Vous ne vendez pas ce que vous voulez vendre, vous vendez ce que vous pouvez vendre. » |
| **2020-03 (COVID)** | Or −12 % en phase aiguë, puis forte hausse ensuite. |
| **Oct-nov 2026** | Pire octobre pour l'or depuis 2008 (−13 %) ; −9,2 % la semaine du krach. |

**Le mécanisme est en deux temps :**
- **Phase 1 (aiguë)** : « dash for cash » — on vend tout, or compris, pour lever du cash et couvrir les appels de marge. Le dollar monte, l'or baisse.
- **Phase 2 (post-assouplissement CB)** : l'or rebondit fort et reprend son rôle de refuge (2008 : l'or est l'un des rares actifs positifs en fin d'année).

## Les drivers concrets de CETTE semaine (pas juste « panique »)

1. **Re-pricing des taux** — inflation US plus chaude que prévu → la Fed penche
   hawkish (Waller évoque un +50 bp) → rendements >5 %, dollar à 19 mois de haut.
   L'or ne paie pas d'intérêt : son coût d'opportunité explose.
2. **Margin calls** sur positions tech sur-levier → vente forcée de ce qui est
   liquide et en gain, l'or en premier.
3. **Positionnement** : net-long spéculatif COMEX très élevé avant la correction →
   longs forcés de liquider.

## Le vrai enseignement pour la prévisibilité

**Ce n'est pas « le marché est devenu imprévisible ». C'est « le modèle or = refuge est trop naïf ».**

L'or n'a jamais eu UN seul driver. Il en a plusieurs :
- **Taux réels** (inverse) — le coût d'opportunité.
- **Dollar** (inverse) — or libellé en USD.
- **Liquidité/margin** — en phase aiguë, tout se vend.
- **Attentes d'inflation** et **achats des banques centrales**.

La corrélation or/actions est **négative en stress normal**, mais devient
**positive (les deux baissent) en « vente désordonnée »** — quand le VIX monte à
l'extrême. C'est documenté (World Gold Council, Chart 2 : « l'exception pendant
les périodes de vente désordonnée quand la volatilité atteint des extrêmes »).

**Conséquence : l'or est un classificateur de régime, pas un refuge cassé.**

| Signal | Lecture |
|--------|---------|
| Or **baisse** + actions baissent | **Cascade de liquidité** — événement de flux, aigu mais réversible quand la vente forcée s'épuise. |
| Or **monte** + actions baissent | **Vrai risk-off** fondamental/géopolitique — plus persistant. |

Autrement dit : loin de perdre de la prévisibilité, le comportement de l'or te
**donne un signal supplémentaire** — il te dit en temps réel quel régime est actif.
Le problème n'est pas le marché, c'est l'heuristique « refuge » à une variable.

## Ce que ça change pour Future Invest

1. **Le Risk Supervisor doit traiter l'or comme un signal de régime, pas comme une couverture naïve.** C'est l'objet de la spec `architecture/2026-11-22_dobby_spec-risk-supervisor-regimes.md` (régime « cascade de liquidité »).
2. **En régime cascade, corrélations → 1** : aucune diversification ne tient, on réduit tout. C'est le seul comportement rationnel, et il est **prévisible** une fois le régime identifié.
3. **Bonus de prévisibilité** : la corrélation signée or/actions (R1 dans la spec) est un signal **rapide, gratuit et robuste** pour classifier le régime — exactement le genre de signal non-linéaire que les stratégies « momentum déguisé » ne voient pas.

---

## Références (consultées 2026-11-22)

- goldu.cz/en/news/gold-during-stock-market-crashes (2008 −30 %, 2020 −12 %, « forced selling, pas un échec du refuge »)
- keaneyfinancialservices.com (2008 : « dash for cash » 2 phases, dollar monte / or baisse)
- gold.org/goldhub/research/gold-prices-swing-as-markets-sell-off (WGC : corrélation négative sauf « vente désordonnée » VIX extrême ; net-long COMEX élevé)
- xtb.com (oct 2026 : pire octobre depuis 2008, « pas de refuge sauf le cash »)
- finance.yahoo.com/markets/commodities (oct 2026 : or −13 %, « margin call », Prem Soni)
- cnbc.com/2026/11/19/gold-prices-fall-fed-rates-dollar.html (Waller +50bp, yields, dollar, coût d'opportunité)
- youtube.com StoneX 2026-11-16 (dollar 19 mois de haut, yields >5 %, inflation chaude)
- think.ing.com/articles/golds-correction-prompts-a-forecast-reset (re-pricing des taux, forecasts abaissés)
