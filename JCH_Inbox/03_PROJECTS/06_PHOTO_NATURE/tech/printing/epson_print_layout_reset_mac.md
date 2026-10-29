---
tags:
  - type/project
  - status/active
---
# Procédure de purge progressive des réglages mémorisés dans Epson Print Layout sur Mac

## Objectif
Éliminer les réglages conservés en mémoire qui peuvent bloquer certaines modifications dans Epson Print Layout, sans tout réinstaller immédiatement.

---

## 1. Vérifier si un preset Epson Print Layout est chargé

Dans [[Epson Print Layout]] :

- ouvrir le document ou l’image ;
- repérer le champ **Preset** ;
- vérifier si un preset enregistré est actif ;
- si oui, revenir à des réglages courants ou non enregistrés ;
- tester ensuite si les options redeviennent modifiables.

### Pourquoi
Un preset peut réappliquer automatiquement un ensemble de paramètres et donner l’impression que certaines options sont “bloquées”.

---

## 2. Supprimer les presets inutiles dans Epson Print Layout

Si tu identifies un preset suspect :

- ouvrir la gestion des presets ;
- sélectionner le preset concerné ;
- le supprimer avec le bouton `-` si nécessaire.

### Conseil
Ne supprimer que les presets douteux ou anciens si tu veux garder une configuration de travail utile.

---

## 3. Réinitialiser les préférences d’Epson Print Layout

Dans Epson Print Layout :

- aller dans **File > Preferences** ;
- chercher l’option **Reset** ;
- lancer la remise à zéro.

### Effet attendu
Cela remet Epson Print Layout dans un état proche de l’installation initiale.

### Attention
Cette opération peut supprimer les **Custom Settings** enregistrés dans Epson Print Layout.

---

## 4. Fermer complètement Epson Print Layout puis le relancer

Après le reset :

- quitter totalement Epson Print Layout ;
- le relancer ;
- rouvrir une image ;
- vérifier si les paramètres auparavant bloqués sont redevenus actifs.

---

## 5. Vérifier le type de pilote utilisé par macOS

Sur Mac :

- ouvrir **Réglages Système > Imprimantes et scanners** ;
- sélectionner l’imprimante Epson ;
- vérifier si elle utilise bien le **pilote Epson** ;
- si elle apparaît en **AirPrint**, cela peut limiter fortement les options disponibles.

### Si l’imprimante est en AirPrint
- supprimer l’imprimante ;
- la réajouter ;
- lors de l’ajout, choisir explicitement le **pilote Epson** et non AirPrint.

---

## 6. Vérifier les presets d’impression macOS

macOS peut aussi conserver ses propres réglages d’impression.

Quand la fenêtre d’impression apparaît :

- vérifier s’il existe un preset d’impression sélectionné ;
- repasser sur une configuration standard ;
- éviter de réutiliser un preset ancien tant que le problème n’est pas résolu.

---

## 7. Tester avec une configuration minimale

Pour éviter les interactions entre réglages :

- choisir un format papier standard ;
- choisir un papier Epson courant ;
- désactiver temporairement les options spéciales ;
- éviter le borderless au début ;
- tester avec une impression simple.

### But
Vérifier si le blocage vient réellement d’une mémoire de réglages ou simplement d’une combinaison de paramètres incompatibles.

---

## 8. Si le problème persiste : supprimer puis réinstaller le pilote Epson

Si Epson Print Layout continue à se comporter comme si des réglages étaient “figés” :

- désinstaller le pilote Epson ;
- redémarrer le Mac ;
- réinstaller le pilote Epson officiel ;
- réajouter l’imprimante ;
- vérifier de nouveau dans Epson Print Layout.

---

# Diagnostic probable

Les causes les plus probables sont :

1. un **preset Epson Print Layout** qui se recharge ;
2. des **Custom Settings** conservés par Epson Print Layout ;
3. un **preset d’impression macOS** ;
4. une imprimante configurée en **AirPrint** au lieu du vrai pilote Epson ;
5. une combinaison de réglages qui rend certaines options indisponibles.

---

# Ordre recommandé

## Méthode la plus propre
1. vérifier les presets EPL ;
2. faire le **Reset** dans Epson Print Layout ;
3. relancer le logiciel ;
4. vérifier le pilote dans macOS ;
5. remplacer AirPrint par le pilote Epson si nécessaire ;
6. réinstaller le pilote uniquement en dernier recours.

---

# Conclusion

Oui, il est très plausible que des réglages soient conservés en mémoire.
Le plus probable n’est pas une panne matérielle, mais une persistance de presets ou de préférences à plusieurs niveaux : Epson Print Layout, macOS, ou pilote Epson.
