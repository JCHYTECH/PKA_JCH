---
tags:
  - type/project
  - status/active
---
# WORKFLOW D'IMPRESSION — Epson ET-8550 + Epson Print Layout

**Objectif : éliminer les dérives chromatiques entre écran et tirage.**

---

## 1. Préparation de l'espace de travail

### 1.1 Calibration écran

- **Sonde :** SpyderX ou équivalent, recalibrer tous les 30 jours.
- **Point blanc :** D50 (5000K) pour correspondre à l'éclairage de visualisation des tirages.
- **Luminance cible :** 80–120 cd/m² selon l'éclairage ambiant.
- **Gamma :** 2.2

> ⚠️ Si l'éclairage de visualisation des tirages n'est pas D50, calibrer l'écran à la température de votre illuminant réel. Un écart entre point blanc écran et illuminant du tirage crée un biais chromatique systématique.

### 1.2 Éclairage de visualisation

- **Idéal :** lampe D50 (5000K), CRI > 95.
- **Minimum acceptable :** LED 5000K, CRI > 90.

Évaluer les tirages uniquement sous cet éclairage, jamais sous plafonnier de bureau.

---

## 2. Profilage de l'imprimante

### 2.1 Génération de la charte

Imprimer la charte de profilage (minimum 729 patchs) depuis le logiciel de profilage.

> ⚠️ **CRITIQUE :** la charte DOIT être imprimée SANS gestion de couleur. Dans le driver Epson : désactiver toute gestion couleur (ICM désactivé / No Color Management). Vérifier aussi qu'Epson Print Layout n'applique aucun profil ICC.

- **Type de support dans le driver :** doit correspondre EXACTEMENT au papier utilisé (ex : Epson Premium Glossy pour du Premium Glossy).
- **Qualité :** Best Quality (identique au réglage qui sera utilisé pour les tirages finaux).

Laisser sécher la charte 24 heures avant mesure.

### 2.2 Mesure et création du profil ICC

- Mesurer la charte sèche avec la sonde dans un environnement à lumière contrôlée.
- Nommer le profil de manière explicite : `ET8550_PremiumGlossy_BestQ_2026-04.icc`
- Installer le profil dans le système macOS : `/Library/ColorSync/Profiles/`

> ⚠️ Un profil par combinaison papier + qualité. Changer de papier = nouveau profilage.

---

## 3. Configuration Epson Print Layout

### 3.1 Réglages obligatoires

| Paramètre | Valeur correcte |
|---|---|
| **Paper Source** | Correspondant au bac utilisé (pas "Standard") |
| **Quality** | Best Quality (identique au profilage) |
| **Color Settings → Type** | Use ICC Profile |
| **ICC Profile** | Votre profil CUSTOM (pas le profil usine Epson) |
| **Rendering Intent** | Relative Colorimetric (photos) ou Perceptual (gamut large) |
| **Black Point Compensation** | Activé |

> ⚠️ **NE JAMAIS utiliser le profil générique Epson** (ex : "EPSON ET-8500 L8160 Series Premium Glossy"). Ce profil usine est approximatif dans les ombres et provoque des dérives chromatiques, notamment jaune dans les basses lumières.

### 3.2 Vérifications dans le driver Epson (macOS)

Ouvrir Préférences Système → Imprimantes → ET-8550 → Options & Fournitures.

- **PhotoEnhance :** DÉSACTIVÉ
- **Amélioration des couleurs :** DÉSACTIVÉ
- **Type de support :** doit correspondre au papier réel

Si Epson Print Layout gère le profil ICC, le driver ne doit appliquer aucune correction couleur (pas de double conversion).

---

## 4. Workflow Lightroom → Epson Print Layout

### 4.1 Export depuis Lightroom

- **Espace colorimétrique d'export :** sRGB ou Adobe RGB selon votre flux.
- **Format :** TIFF 16 bits (préféré) ou JPEG qualité maximale.
- **Résolution :** 300 dpi.

Ne pas appliquer de netteté d'export pour impression (Epson Print Layout ou le driver s'en chargent si nécessaire).

> ⚠️ Vérifier que Lightroom n'applique PAS de profil d'impression à l'export. La conversion ICC est gérée par Epson Print Layout, pas par Lightroom.

### 4.2 Impression

1. Ouvrir l'image dans Epson Print Layout.
2. Vérifier les 6 paramètres du tableau ci-dessus AVANT chaque session d'impression.
3. Lancer l'impression.
4. **Séchage :** attendre minimum 2 heures (idéal 24h) avant évaluation finale des couleurs.

---

## 5. Checklist pré-impression

Cocher chaque élément avant de lancer un tirage :

| ✔ | Action | Vérification |
|---|---|---|
| ☐ | **Écran** — Calibration à jour (< 30 jours) | Vérifier date dernière calibration |
| ☐ | **Papier** — Type de support correct dans EPL et driver | Pas "Standard" pour du glossy |
| ☐ | **Profil** — Profil ICC CUSTOM sélectionné dans EPL | Pas le profil usine Epson |
| ☐ | **Driver** — PhotoEnhance et corrections couleur désactivés | Pas de double gestion |
| ☐ | **Qualité** — Best Quality (identique au profilage) | Changer = reprofilage |
| ☐ | **BPC** — Black Point Compensation activé | Coché dans EPL |
| ☐ | **Intent** — Relative Colorimetric ou Perceptual | Selon le type d'image |
| ☐ | **Export** — TIFF 16 bits, 300 dpi, pas de profil imprimante | LR n'applique pas de conversion |
| ☐ | **Buses** — Test de buses OK (pas de manque) | Imprimer nozzle check |
| ☐ | **Séchage** — Attendre 2h+ avant évaluation | 24h pour évaluation finale |

---

## 6. Diagnostic en cas de dérive chromatique

### 6.1 Test rapide

Imprimer une mire de gris neutres (R=G=B de 0 à 255, par paliers de 10) SANS gestion de couleur (à la fois dans EPL et dans le driver).

| Résultat du test | Diagnostic |
|---|---|
| Gris neutres partout | Imprimante OK — problème dans la chaîne ICC |
| Dérive dans les ombres uniquement | Profil ICC imprécis dans les basses lumières OU type de support incorrect |
| Dérive globale | Double gestion de couleur OU problème matériel (buses, encres) |
| Dérive jaune dans les ombres | Type de support incorrect (noir mat/photo) OU profil usine utilisé à la place du custom |
| Dérive magenta globale | Double conversion ICC OU profil écran biaisé |

### 6.2 Arbre de décision

1. Imprimer mire de gris sans gestion de couleur.
2. Si gris neutres → le problème est dans le profil ICC ou la configuration EPL. Reprendre la section 3.
3. Si dérive visible → vérifier type de support, faire nozzle check, vérifier encres.
4. Si dérive persistée après correction matérielle → reprofilage complet.

---

## 7. Maintenance régulière

| Fréquence | Action | Notes |
|---|---|---|
| Avant chaque session | Nozzle check | Si manque → nettoyage tête |
| Mensuel | Recalibration écran | Sonde SpyderX |
| Tous les 6 mois | Reprofilage imprimante | Par type de papier utilisé |
| Changement de papier | Nouveau profilage ICC | Obligatoire |
| Changement de lot d'encre | Vérifier neutralité des gris | Reprofilage si dérive |

---

> **Règle d'or :** une seule conversion ICC dans la chaîne, jamais deux. Soit l'application gère le profil, soit le driver — jamais les deux en même temps.

---

*JC — Chaîne graphique v1.0*
