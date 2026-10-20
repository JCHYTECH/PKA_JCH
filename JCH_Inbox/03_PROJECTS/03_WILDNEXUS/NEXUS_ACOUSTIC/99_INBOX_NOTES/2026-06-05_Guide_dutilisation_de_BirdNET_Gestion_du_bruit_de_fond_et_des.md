# # Guide d'utilisation de BirdNET : Gestion du bruit de fond et des…

> Exporté depuis Apple Notes — créé le ?, modifié le 2026-06-05 05:54

�$�$�## Guide d'utilisation de BirdNET : Gestion du bruit de fond et des faux positifs

Ce document rassemble les explications et les méthodes pour éviter les erreurs d'identification de l'application BirdNET, ajuster ses paramètres et nettoyer ses enregistrements audio.

---

## 1. Comprendre les erreurs et "hallucinations" de BirdNET

BirdNET n'a pas de conscience humaine. L'application convertit les sons en images (spectrogrammes) et cherche des correspondances visuelles dans sa base de données. Plusieurs facteurs peuvent générer des **faux positifs** (erreurs d'interprétation) :

* **Bruits mécaniques et humains :** Un grincement de balançoire, le sifflement du vent, des sirènes, des bruits de circulation ou des aboiements peuvent être confondus avec des cris de rapaces ou de passereaux.
* **Sensibilité extrême de l'IA :** Conçue pour capter les sons lointains, l'application a tendance à surinterpréter le bruit ambiant si le signal est faible.
* **Seuils de confiance bas :** Un indice de confiance faible (ex. 10 % ou 20 %) indique que l'algorithme "devine" une espèce à partir d'un bruit parasite.

### Bonnes pratiques de vérification
1. **Écoutez l'extrait :** Utilisez la fonction de réécoute pour isoler la séquence analysée.
2. **Fiez-vous au score :** Prenez en compte uniquement les résultats avec un indice élevé (idéalement > 0.70 ou 70 %).
3. **Vérifiez la cohérence :** Éliminez les résultats signalant des oiseaux nocturnes en plein jour ou des espèces exotiques absentes de votre région.

---

## 2. Optimiser les réglages de l'application

Pour limiter les erreurs directement sur le terrain, ajustez les options dans les paramètres de BirdNET :

* **Augmenter le seuil de confiance (*Minimum Confidence*) :** Montez le curseur à **0,50 ou 0,60**. Les suggestions trop incertaines basées sur du bruit de fond seront masquées.
* **Activer la localisation automatique (*Species List by Location*) :** Autorisez le GPS et la date. L'application filtrera les espèces selon la base de données eBird, éliminant les oiseaux migrateurs absents ou les espèces d'autres continents.
* **Ajuster la sensibilité (*Sensitivity*) :** En milieu très bruyant (vent, ville), baissez la sensibilité (ex. entre 0,5 et 0,75) pour forcer l'IA à être plus stricte.
* **Augmenter le chevauchement (*Overlap*) :** Sur les outils d'analyse avancés, régler le chevauchement à **2 secondes** permet à l'IA d'analyser plusieurs fois les mêmes segments décalés pour isoler le chant.

---

## 3. Améliorer la qualité de l'enregistrement sur le terrain

Le micro du smartphone capte l'environnement de manière globale. Appliquez ces techniques physiques :

* **Sélectionner la zone propre :** Utilisez votre doigt sur l'écran pour sélectionner uniquement les 3 secondes où le chant de l'oiseau est le plus net.
* **Bloquer le vent :** Le vent sature le micro avec des basses fréquences. Utilisez votre corps, un mur ou votre main pour faire écran autour du micro.
* **Éviter les bruits de manipulation :** Ne bougez pas vos doigts sur la coque du téléphone pendant l'enregistrement pour éviter les craquements aigus.
* **Utiliser un micro externe :** Un micro cravate ou directionnel équipé d'une bonnette anti-vent (*deadcat*) isole efficacement le chant de l'oiseau.

---

## 4. Exporter et nettoyer un enregistrement sur ordinateur

Si un chant reste difficile à identifier à cause du bruit de fond, vous pouvez extraire le fichier audio pour le traiter.

### Étape A : Exporter depuis BirdNET
1. Ouvrez le menu principal (`☰`) en haut à gauche.
2. Allez dans **"Afficher les observations"**.
3. Appuyez sur l'observation concernée.
4. Touchez l'icône **"Partager"** et envoyez le fichier vers votre Cloud (Google Drive, iCloud) ou par e-mail.
5. *Astuce : Si le fichier n'a pas d'extension sur votre ordinateur, renommez-le en ajoutant `.wav` à la fin.*

### Étape B : Filtrer le bruit avec le logiciel Audacity
1. **Importer :** Glissez-déposez votre fichier `.wav` dans Audacity.
2. **Isoler le bruit :** Sélectionnez à la souris une zone de 1 à 2 secondes contenant uniquement le bruit parasite (vent, moteur), sans chant d'oiseau.
3. **Capturer le profil :** Allez dans *Effets* > *Réduction de bruit* > Cliquez sur **"Prendre le profil du bruit"**.
4. **Appliquer le filtre :** Sélectionnez tout le fichier (`Ctrl + A`), retournez dans *Effets* > *Réduction de bruit*, puis cliquez sur **"Valider"**.

(
�"(
��������"

��NSQ�O���!d[���"*�"JPA�%%�K��X ��s�h�ɉ�
