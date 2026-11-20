# Proposition — Analyses EXIF pour améliorer les images et l'analyse Argus

> Dobby 🦉 — 2026-11-20 · Recherche + proposition (aucune implémentation).
> Contexte : module `scripts/exif_raw.py` livré (exposition, focus, WB, optique). Question : quelles analyses pertinentes peut-on ajouter à partir de ces paramètres EXIF ?

---

## Verdict d'ensemble — la sous-expo de JC est une bonne technique, pas un défaut

La littérature ETTR (Expose To The Right) valide précisément le réflexe de JC
(−0,33 / −0,66 sur sujets blancs) :

- Wikipedia (Exposing to the right) : pour les scènes à haute dynamique, l'ETTR
  « requires a seemingly counterintuitive negative exposure compensation » — on
  sous-expose pour caler l'histogramme contre le bord droit sans clipper.
- Tony Whitehead (Simplifying Exposure) et Steve Perry (Backcountry Gallery) :
  en wildlife, on ne pousse PAS l'histogramme à droite ; on protège les hautes
  lumières du plumage blanc et on garde l'ISO le plus bas possible.

→ Conclusion : l'analyse ne doit pas « corriger » JC mais **mesurer** la marge
(marge ETTR en EV, % clipping) pour confirmer quand sa sous-expo est optimale et
quand elle laisse de la marge inutile sur scène sombre.

---

## Analyses candidates — classées valeur × faisabilité

### Tier 1 — déterministes, quasi gratuites (PIL/numpy, sans appel IA)

1. **Audit exposition ETTR** — `ExposureCompensation` + histogramme
   - Calcule : luminance moyenne, p05/p95, % ombres/highlights clippées, **marge
     ETTR en EV** (`log2(255 / p95)`).
   - Verdict : « EC −0,33, marge +0,16 EV → quasi optimal sur sujet blanc » vs
     « marge +0,6 EV → tu aurais pu exposer plus clair sans perte ».
   - Déjà prototypé sur `LrC to-131.jpg` (marge +0,16 EV) et `fou de bassan.jpg`.

2. **Risque de flou de bougé** — `ExposureTime` + `FocalLength` + `ImageStabilization`
   - Règle réciproque : vitesse min ≈ 1/(focale × crop). À 500 mm (R10 ≈ 800 mm
     équiv.), min ≈ 1/800 sans IS, moins avec IS (5 stops).
   - Oiseau perché vs action : perchés ok à ~1/focale, en vol il faut 1/2000+.
   - Verdict binaire + seuil.

3. **Netteté / qualité de focus** — Variance de Laplacian (ou Tenengrad/Sobel)
   - Référence : OpenCV focus measures — `cv2.Laplacian(img, CV_64F).var()` ;
     Tenengrad et Sobel+Variance sont les meilleurs détecteurs de netteté.
   - Croisé avec la **position du collimateur** (`AFAreaX/Y`), on peut mesurer la
     netteté là où l'AF a verrouillé vs le reste → détecte front/back-focus,
     bougé, ou raté de focus.

4. **Limite de diffraction** — `FNumber` + taille capteur
   - Sur R10 (APS-C 32 MP), le seuil de diffraction est ≈ f/8. À f/11, légère
     pénalité de netteté. Verdict : « f/11 dépasse le seuil, choisi pour la DOF ? ».

5. **Profondeur de champ** — `FNumber` + `FocalLength` + `SubjectDistance`
   - Calcul DOF (formule standard) → est-ce que le sujet (adulte + poussin) tient
     dans la DOF à 25 m / f/11 ? Répond à la question « f/11 était-il nécessaire ? ».

6. **Niveau de bruit / ISO** — `ISO` + histogramme ombres
   - R10 pas strictement ISO-invariant (dual gain). Estime le bruit attendu, et
     alerte quand ISO élevé + ombres relevées en post amplifient le bruit.

### Tier 2 — croisement vision × télémétrie

7. **Injecter la télémétrie dans le prompt Argus** — tous les champs EXIF
   - Donner à Opus le contexte de prise de vue (« f/11 → juge la diffraction »,
     « EC −0,33 → juge l'intention d'expo », « AI Servo, distance 25 m »).
   - Coût ~0, ajout de deux champs au prompt. Fort levier sur la pertinence de la
     critique (actuellement le modèle juge sans savoir COMMENT la photo a été prise).

8. **Position du collimateur vs sujet** — `AFAreaX/Y` + détection du sujet
   - Vérifier que le point AF était bien sur l'oiseau (via segmentation/détection
     vision) → diagnostic de placement AF.

### Tier 3 — corpus / coaching (multi-images)

9. **Détection d'habitudes** — agrégat sur N photos
   - « EC moyen −0,4 EV », « f/11 systématique (diffraction) », « vitesse sous le
     seuil bougé dans X % des cas » → coaching de prise de vue. C'est la réponse
     directe à sa question sur son biais.

10. **Score qualité appris (NIMA / MUSIQ)** — second avis
    - NIMA (Google) prédit la distribution de score esthétique/technique ; MUSIQ
      (transformer) est plus récent. Peut servir de 2e juge objectif croisé avec
      Argus. Coût : modèle à servir (plus lourd).

---

## Recommandation

Construire d'abord **Tier 1 (1, 2, 3, 5) + Tier 2 n°7 (injection prompt)** :
- déterministe, quasi gratuit, sans nouvel appel IA ;
- répond exactement aux deux questions de JC (exposition, focus) ;
- l'injection prompt (n°7) améliore la critique Argus à coût nul.

Différer : n°4/6 (incrémentaux), n°8 (détection sujet), n°9 (nécessite un corpus
déjà indexé), n°10 (infra modèle).

---

## Sources

- Exposing to the right — https://photographylife.com/exposing-to-the-right-explained
- Exposing to the right — https://en.wikipedia.org/wiki/Exposing_to_the_right
- Simplifying Exposure (wildlife, rethink ETTR) — https://www.tonywhitehead.com/wildlight/archives/18869
- Autofocus focus measures (OpenCV) — https://opencv.org/autofocus-using-opencv-a-comparative-study-of-focus-measures-for-sharpness-assessment
- Variance of Laplacian (blur detection) — https://www.geeksforgeeks.org/computer-vision/how-to-check-for-blurry-images-in-your-dataset-using-the-laplacian-method
- Reciprocal rule — https://photographylife.com/what-is-reciprocal-rule-in-photography
- ISO invariance — https://photographylife.com/iso-invariance-explained
- NIMA: Neural Image Assessment — https://research.google/blog/introducing-nima-neural-image-assessment
- IQA paper list (MUSIQ, etc.) — https://github.com/TianheWu/IQA-Paperlist
