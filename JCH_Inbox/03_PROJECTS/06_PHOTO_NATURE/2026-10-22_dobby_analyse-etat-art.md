# PHOTO_NATURE — Analyse & confrontation à l'état de l'art

> 2026-10-22 · Dobby 🦉 · analyse du projet 06 + veille technologique
> Demande JC : fluidité, fiabilité, critique *user-friendly*

---

## 1. Ce qui tourne aujourd'hui (vérifié dans le code)

| Maillon | Outil | État réel |
|---|---|---|
| Capture | Canon R10 + 90D, RF 200-800, Tamron 150-600, Laowa | ✅ mature |
| Développement | DxO PhotoLab, Lightroom, Helicon, Topaz | ✅ mature |
| Auto-tagging | `scripts/photo_keyworder.py` (553 l.) → Ollama vision | 🟡 fonctionne, fragile |
| Taxonomie | `keyword_taxonomy.json` — 62 catégories, 80+ espèces faune | ✅ solide |
| Écriture méta | exiftool → IPTC + XMP + HierarchicalSubject | ✅ fonctionne |
| Critique | Argus (projet 05) → presets XMP | ✅ 11 presets |
| Impression | ET8550, workflow documenté | ✅ mature |

**Verdict global : le pipeline est bon.** Ce qui suit ne dit pas « à refaire »,
mais « où ça casse en vrai ».

---

## 2. Les trois fragilités mesurées

### 2.1 Le cache est alimenté uniquement dans un mode secondaire (bug confirmé)

`keyword_cache.json` contient **1 entrée**, alors que le projet référence
**116 fichiers indexés**. En lisant le code (lignes 426 et 516), la cause est
identifiée :

- ligne **426** : `cache[fingerprint] = {...}` — dans la branche `--template`
- ligne **516** : même chose, seconde branche
- **le chemin normal (flatten → keywords IPTC) n'écrit JAMAIS dans le cache**

Autrement dit, le cache ne sert qu'aux utilisateurs du mode `--template`,
jamais à l'usage courant. Chaque passage en mode normal rejoue donc
l'intégralité de l'inférence.

→ **Fluidité** : sur 500 photos à ~18 s, c'est 2h30 qui pourraient être 10 min.
→ **Correctif** : une ligne à ajouter dans la branche normale. Trivial.

### 2.2 Une seule tentative, aucune reprise

```python
except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
    print(f"  ⚠️  Model error: {e}")
    return None          # ← la photo est simplement perdue
```

Pas de retry, pas de file d'attente, pas de reprise après interruption.
Sur un batch de 500 photos, un Ollama qui hoquette = photos silencieusement
non taguées, sans trace.

→ **Fiabilité** : le pire profil — échec silencieux.

### 2.3 Le garde-fou anti-hallucination est partiel

`validate_subject()` protège bien les **espèces** (downgrade en `indéterminé`
si absente de la taxonomie → excellent choix). Mais seuls les sujets sont validés.
Comportement, habitat, ambiance sont acceptés tels quels, sans vérification
contre la liste fermée.

→ **Fiabilité** : un modèle qui invente « Habitat|Toundra » sur une photo
ardennaise passera.

---

## 3. Confrontation à l'état de l'art 2026

### 3.1 Modèle vision — le vrai levier

| Option | Force | Limite |
|---|---|---|
| **llama3.2-vision:11b** (actuel) | simple, tourne sur M1 | lent, précision moyenne sur espèces |
| **Qwen2.5-VL / Qwen3-VL** | résolution dynamique, nettement meilleur en comptage et détails fins | plus lourd (7B/32B) |
| **Florence-2** (Microsoft, MIT, 0.23–0.77B) | **meilleur petit VLM**, unifié : captioning + **détection d'objets** + segmentation | pas un raisonneur ouvert |

**Recommandation** : Florence-2 en *pré-passe* (détection d'objets → « ici il y a
un oiseau, cadré en haut à droite »), puis Qwen-VL pour la classification fine.
Deux modèles spécialisés battent un gros modèle généraliste sur cette tâche.

**Gain attendu** : précision espèce ↑, vitesse ↑ (Florence-2 est 10-50× plus
petit que llama3.2-vision:11b).

### 3.2 L'écosystème Lightroom a bougé

Adobe n'a **jamais** ajouté l'auto-tagging natif à Lightroom Classic — c'est
toujours vrai en 2026. Des plugins tiers ont émergé (MetaMagic et consorts),
avec collections automatiques, export CSV pour agences stock, mode légende
éditoriale.

**Mais** : ils sont cloud. Or la décision PKA de 2026-06-19 est **« keyworder
100 % autonome, zéro API »** — c'est un choix délibéré et il tient.

→ **Ne pas adopter un plugin cloud.** En revanche, deux idées à reprendre :
1. **Collections automatiques** basées sur les keywords (faisable en local
   via le catalogue SQLite de LrC — quelqu'un explore déjà cette voie sur les
   forums Backcountry Gallery)
2. **Mode légende éditoriale** : générer une `Caption`/`Headline` IPTC, pas
   seulement des mots-clés — utile pour WildLens et le stock.

### 3.3 Le catalogue Lightroom est une base SQLite

Découverte utile : le catalogue LrC **est** une base SQLite interrogeable.
Ça ouvre un contrôle qualité objectif : « quelles photos n'ont aucun keyword ? »,
« quels keywords sont orphelins ? », « cohérence de la hiérarchie ? ».

→ **Fiabilité** : un audit de couverture devient possible, chiffré.

---

## 4. La critique *user-friendly* (le vrai sujet)

Voilà ce que JC vit réellement aujourd'hui :

**1. Le flux est en deux temps, avec une manipulation manuelle au milieu.**
Tagger → ouvrir Lightroom → *Metadata → Read Metadata from Files*.
Rien ne se met à jour tout seul. Sur une session de 300 photos, c'est un
aller-retour de plus, et un oubli = keywords invisibles alors qu'ils sont écrits.

**2. Il n'y a aucun retour visuel pendant le traitement.**
18 s par photo, sans compteur, sans ETA, sans barre. Sur 100 photos on ne sait
pas si ça avance ou si c'est bloqué.

**3. Les erreurs sont invisibles.**
Une photo qui échoue affiche `⚠️ Model error` dans le flux et disparaît.
Pas de liste finale « 12 photos non taguées », pas de fichier de reprise.

**4. La confiance est binaire.**
Un tag « indéterminé » et un tag sûr se ressemblent. Pourtant `Auto|Confiance_Haute`
existe déjà — mais ce n'est pas exploité dans une vue de tri.

**5. `--m1` est un drapeau, pas une décision automatique.**
Il faut savoir quel modèle est le meilleur et sur quelle machine. C'est une
charge cognitive inutile.

---

## 5. Recommandations, par ordre de rentabilité

### P0 — Reprise et visibilité (0,5 j, effet immédiat)
- **Retry avec backoff** (3 tentatives) + fichier `failed.json` de reprise
- **Barre de progression** : `[142/500] 00:42:10 restant`
- **Rapport de fin** : X taguées, Y en échec, Z en cache

→ Répond directement aux points 3 et 2 de la critique.

### P1 — Le cache comme accélérateur réel (0,25 j)
Vérifier que le cache est bien écrit après chaque succès (1 entrée aujourd'hui
suggère un bug d'écriture ou un usage uniquement en `--dry-run`).
Le cache devrait faire passer un re-run de 2h30 à quelques minutes.

### P2 — Deux modèles au lieu d'un (1 j)
Florence-2 (détection) → Qwen-VL (classification). Gain de précision + vitesse.
À valider sur 50 photos réelles avec mesure de temps et de qualité.

### P3 — Validation étendue à tous les champs (0,25 j)
Étendre le principe déjà excellent de `validate_subject()` aux comportements,
habitats, ambiances — tout contre la liste fermée de la taxonomie.

### P4 — Ouverture directe du catalogue LrC (1 j)
Après écriture, mettre à jour le catalogue SQLite (ou au minimum déclencher
`Read Metadata` de façon scriptée). Supprime l'étape manuelle — **le point
n°1 de la critique user-friendly**.

### P5 — Légendes éditoriales (0,5 j)
Générer `Caption` + `Headline` IPTC en plus des keywords, réutilisables pour
WildLens et le futur stock.

---

## 6. Ce qu'il ne faut PAS faire

- **Adopter un plugin cloud** (MetaMagic & co) : rupture avec la décision
  « 100 % autonome » et sortie de données.
- **Remplacer par un gros modèle unique** (GPT-6 Astra, Claude vision) :
  coût par image rédhibitoire sur des milliers de photos.
- **Réécrire le keyworder** : il n'est pas cassé. Il manque de robustesse
  et de retour utilisateur, ce n'est pas la même chose.

---

## 7. En une phrase

**Le pipeline est solide et le choix d'architecture (local, taxonomie fermée)
reste le bon.** Les gains ne viendront pas d'un meilleur modèle mais de la
**robustesse** (retry, cache, reprise), de la **visibilité** (progression,
rapport d'échec) et de la **suppression du geste manuel Lightroom** — trois
chantiers peu coûteux qui transforment l'expérience quotidienne.

*Sources : code `photo_keyworder.py` (553 l., lu) · `keyword_taxonomy.json` ·
`README_keyworder.md` · Roboflow/Florence-2 · arXiv Qwen2-VL 2409.12191 ·
Adobe Help « Use keywords in Lightroom Classic » · MetaMagic « AI Keyword
Plugins Compared 2026 » · forums Backcountry Gallery (catalogue SQLite).*
