# VEILLE — Julie Elie · diamant mandarin · perception sémantique des appels

> Dobby 🦉 — DeepSeek TUI 0.8.39 — 2026-10-30
> Objet : veille ciblée P1 — méthodologie de tri des appels par l'animal lui-même.
> Lien doctrine : `WILDNEXUS_DEVICE/01_FOUNDATION/2026-10-30_dobby_parole-animale-fondements.md` (§3-L2 « le motif n'est pas le sens »)
> Spécialistes concernés : Clio 🐬 (bioacoustique/DSP) · Chouette 🦉 (bioacoustique) · Musaraigne 🦇 (edge AI)

---

## 1. La chercheuse et la publication

- **Julie E. Elie** — research associate, Dept of Neuroscience, UC Berkeley (collaboratrice de longue date de **Frédéric Theunissen**).
- **Publication clé** : *Categorical and semantic perception of the meaning of call types in zebra finch*, **Science** (DOI `10.1126/science.ads8482`, nov. 2025).
- **Prix** : lauréate du **Coller-Dolittle Prize 2026** (100 k$), pour avancée vers la communication interspécifique.
- Co-auteurs : Aude de Witasse-Thézy (Lyon), Logan Thomas, Ben Malit (Berkeley).

---

## 2. L'étude en bref

- **Corpus** : répertoire du diamant mandarin domestiqué (`Taeniopygia guttata`) découpé en **11 types d'appels « Etho »** (éthologiques) ; base de **> 8 000 renditions** issues d'environ 45 mâles.
- **Méthode (clé de la veille)** : conditionnement opérant — les oiseaux **picorent un bouton** pour parcourir une piste audio de plusieurs centaines d'appels mélangés, et reçoivent une graine quand ils *laissent jouer* l'appel-cible (le même « mot » émis par de nombreux oiseaux) au lieu de le zapper.
- L'animal **trie lui-même** les appels, au lieu que ce soit l'humain qui impose sa classification.

> « The human is here observing and saying, “Those are your words.” And the bird is saying, “Yes, these are my words.” » — J. Elie

---

## 3. Le résultat clé : la sémantique prime sur l'acoustique

Les oiseaux confondent plus souvent des appels **proches par le sens** que des appels **proches par le son** :

- **« tet »** (contact rapproché, « Marco Polo » : *tu es là ? je suis là*) et **l'appel de distance** (honk ♀ / « pitchiou » ♂) sont acoustiquement très différents, mais tous deux des *appels de contact* → souvent confondus.
- L'**alarme** (« thuk thuk thuk ») *ressemble* au « tet », mais n'est presque jamais confondue avec lui → sens différent.

**Conclusion** : le diamant mandarin possède une **représentation mentale du sens** (catégories sémantiques, « hypercatégories » comme *tous les appels de contact*). Ce n'est pas une simple discrimination acoustique.

C'est la **contre-preuve vivante** de l'expérience de Tel Aviv (transcript, §3-L2) : l'IA y échoue à regrouper les sons par sens ; l'oiseau, lui, y arrive — parce que *pour l'oiseau, ce qui compte, c'est ce que veut dire le cri*.

---

## 4. Pourquoi c'est important pour WildNexus (P1)

1. **La méthode est réutilisable en P1.** Le tri opérant (l'animal classe ses propres vocalisations) est une voie de **grounding sémantique** indépendante du seul signal : elle ancre le sens dans la *réaction* de l'animal, pas dans l'acoustique. C'est exactement le « son + comportement » que WildNexus capture par design (micros + caméra + PIR).

2. **Un répertoire de référence documenté.** Les 11 types d'appels « Etho » du diamant mandarin constituent un **jeu de référence** pour valider nos pipelines de segmentation/classification acoustique en P1 (à côté de BirdNET/TweetyBERT déjà analysés). 8 000 renditions labellisées = modèle de ce qu'on veut construire pour nos propres datasets.

3. **Une frontière scientifique claire.** La ligne « sensation → perception → sens » (Theunissen) est la grille d'honnêteté de notre roadmap : P0 détecte la *présence* (sensation) ; P1 classifie l'*espèce et l'appel* (perception) ; P2 seulement peut viser le *sens* (sémantique). La veille Elie démontre que le palier sémantique est atteignable — mais seulement via le comportement, pas via le son seul.

4. **Limite à respecter.** Elie/Theunissen enregistrent maintenant le cerveau pour localiser « où est le percept de sens ». C'est de la recherche fondamentale — **hors périmètre WildNexus**, mais sa méthodologie comportementale est transposable à nos données de terrain.

---

## 5. Ancrages concrets

- **P0** : inchangé (binaire). Aucune implication.
- **P1 (classification d'espèce/appel)** : intégrer le répertoire des 11 appels comme cas-test de segmentation ; comparer nos erreurs aux erreurs *sémantiques* de l'oiseau (grille d'évaluation du « sens » vs « son »).
- **P1/P2 (grounding)** : documenter le couplage micros + caméra comme instrument de grounding (déjà noté dans la doctrine).
- **Dataset** : croiser avec le skill `bioacoustics-qc-playbook` pour la curation de segments annotés.

---

## 6. Sources

- Berkeley Research : *Finch Chirps Are More Than Mindless Chatter* (Robert Sanders, 04/11/2025) — https://vcresearch.berkeley.edu/news/finch-chirps-are-more-mindless-chatter
- *Science* : Elie et al., *Categorical and semantic perception of the meaning of call types in zebra finch* — https://www.science.org/doi/10.1126/science.ads8482
- The Guardian : *A little bird told her: scientist wins $100,000 prize* (26/06/2026) — https://www.theguardian.com/science/2026/jun/26/human-animal-communication-step-closer-scientist-wins-prize-for-decoding-birdsong
- Elie & Theunissen 2018 (*Nat Commun* 9:4026) : *Zebra finches identify individuals using vocal signatures unique to each call type*.
- Elie & Theunissen 2016 (*Animal Cognition* 19:285) : *The vocal repertoire of the domesticated zebra finch*.
