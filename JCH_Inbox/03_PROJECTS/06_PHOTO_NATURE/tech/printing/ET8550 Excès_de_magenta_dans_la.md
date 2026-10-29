---
date: 2026-04-07
source: chat-ai
domain: photo/printing
project:
tags:
  - ET8550
  - magenta
  - ICC
  - profil
  - impression
  - type/project
  - status/active
status: raw
---
# Excès de magenta dans la chaîne d'impression

**Created:** 2026-04-07  
**Updated:** 2026-04-09  
**Messages:** 22

[[ET8550_Workflow]][[ET8550_color_fix]]

[[Tirage_Photo]]

[[ET8550_Workflow_Impression_]]
## Human
*2026-04-07 09:18*

Tu es mon expert en tirage photo. tu sais analyser les photos et accompagner le photographe dans l’édition des photos pour qu’il n’y ai pas de discordances en l’écran et l’impression. Nous avons un soucis avec notre système. Les écrans sont calibrer avec spyder et les fichier ICC créés sont utilisés lors de l’impression avec Epson Layout pointer sur Epson ET8550. On a beau essayer des solutions d’autres ICC mais les images imprimées sont systématiquement en excès de magenta. Peux tu lister des pistes correctives dans la chaine graphique?

---

## Assistant
*2026-04-07 09:19*

# Excès de magenta systématique — pistes correctives

Un excès de magenta constant et reproductible pointe vers un problème structurel dans la chaîne, pas vers un fichier isolé. Voici les axes à investiguer, dans un ordre logique de diagnostic.

## 1. Profil ICC de l'imprimante

Le profil ICC généré par Spyder (SpyderPrint, je suppose) dépend fortement des conditions de mesure. Plusieurs points à vérifier :

- Le **type de papier utilisé lors du profilage** est-il exactement le même que celui utilisé à l'impression ? Même grammage, même lot, même côté imprimé. Un papier différent peut suffire à décaler la balance couleur.
- Le **nombre de patchs** utilisés lors de la création du profil : un profilage avec trop peu de patchs (par ex. 225 au lieu de 729+) donne un profil ICC imprécis, surtout dans les tons moyens et les gris neutres — exactement là où un excès de magenta se voit le plus.
- La **charte** a-t-elle été imprimée **sans gestion de couleur** (« No Color Management » dans le driver) ? Si Epson Layout ou le driver applique un profil par-dessus la charte de profilage, le profil résultant est faux dès le départ.

## 2. Double gestion de couleur

C'est la cause la plus fréquente d'un shift chromatique systématique. Il faut vérifier qu'il n'y a pas **deux conversions ICC empilées** :

- Dans Epson Print Layout : le rendering intent et le profil ICC doivent être gérés **soit** par l'application (Lightroom, Photoshop…), **soit** par Epson Print Layout — jamais les deux en même temps.
- Si Lightroom envoie déjà une image convertie vers le profil imprimante, et qu'Epson Print Layout applique à nouveau le profil, on obtient une double conversion qui décale systématiquement les couleurs.
- Vérifier dans le driver Epson que le mode couleur est bien sur **« Pas de gestion des couleurs »** ou **« ICM désactivé »** quand c'est l'application source qui gère le profil.

## 3. Réglages du driver Epson

L'ET-8550 a ses propres réglages internes :

- Le paramètre **« Amélioration des couleurs »** ou **« PhotoEnhance »** doit être **désactivé**. Ce mode applique des corrections automatiques qui interfèrent avec le profil ICC.
- Vérifier le réglage **« Type de support »** dans le driver : s'il ne correspond pas au papier réel, le firmware ajuste les quantités d'encre, ce qui peut provoquer un shift magenta.
- Le mode **« Vitesse rapide »** (impression bidirectionnelle) peut aussi créer des variations de couleur, bien que ce soit rarement un shift magenta pur.

## 4. Calibration de l'écran

Même si les écrans sont calibrés avec Spyder :

- Quel **point blanc** est utilisé ? Un D50 sur l'écran avec un éclairage ambiant froid (LED 6500K+) peut donner l'impression que le tirage est trop magenta, alors que c'est l'environnement visuel qui fausse la comparaison.
- La **luminance cible** de l'écran est-elle adaptée au tirage ? Un écran à 120 cd/m² face à un tirage vu sous un éclairage de bureau standard va créer un décalage de perception important.
- Quel **âge** a la sonde Spyder ? Les filtres colorimétriques des Spyder (surtout les versions < Spyder5) dérivent avec le temps et peuvent induire un biais dans la calibration écran.

## 5. Éclairage de visualisation des tirages

Un point souvent négligé :

- Sous quel éclairage évaluez-vous les tirages ? Un éclairage LED avec un CRI bas ou un pic spectral bleu va faire apparaître un excès de magenta qui n'est pas réellement dans le tirage.
- L'idéal est un éclairage D50 (5000K, CRI > 95). À défaut, un éclairage à 5000K même imparfait reste plus fiable qu'un plafonnier de bureau.

## 6. Encres et têtes d'impression

- Les **encres** sont-elles d'origine Epson ? Des encres tierces peuvent avoir des courbes spectrales différentes qui rendent le profil ICC inutilisable.
- Une **tête d'impression encrassée** ou avec des buses obstruées (particulièrement sur le canal cyan) peut provoquer un shift magenta par déficit de cyan. Un test de buses s'impose.
- Le **niveau d'encre** dans les réservoirs : un réservoir presque vide peut donner un débit irrégulier.

## Démarche de diagnostic recommandée

Pour isoler la cause : imprimez une mire de gris neutre (patches de R=G=B de 0 à 255) **sans aucune gestion de couleur** (ni dans l'application, ni dans le driver, ni dans Epson Print Layout). Si les gris sont neutres, le problème est dans la chaîne ICC. S'ils tirent déjà vers le magenta, le problème est matériel (encres, buses, ou réglage driver).

Ça permettra de savoir de quel côté creuser en priorité. Tu veux qu'on détaille l'un de ces axes ?

---

## Human
*2026-04-07 13:39*

petite nuance magenta visible dans les bandes les plus sombres

---

## Assistant
*2026-04-07 13:40*

Ça précise bien le diagnostic. Un shift magenta **limité aux bandes sombres** avec des gris neutres corrects dans les moyens et hauts élimine pas mal de pistes (double gestion de couleur, éclairage, profil écran). On est probablement sur un problème plus ciblé.

## Pistes prioritaires pour un excès magenta dans les ombres uniquement

### 1. Linéarisation de l'imprimante dans les noirs

L'ET-8550 utilise une encre noire photo et une noire mate. Dans les tons très sombres, le driver mélange noir + CMY pour obtenir un noir « riche ». Si le ratio CMY n'est pas parfaitement équilibré dans les basses lumières, le magenta domine — c'est un comportement connu sur les imprimantes à réservoirs Epson.

Le réglage **« Type de support »** dans le driver influence directement ce ratio. Un type de support mal renseigné peut pousser trop de magenta dans les ombres profondes.

### 2. Profil ICC imprécis dans les basses lumières

Les sondes colorimétriques (SpyderPrint inclus) perdent en précision dans les patchs très sombres. Le rapport signal/bruit de la mesure se dégrade, et c'est exactement là que le profil ICC devient approximatif.

Deux choses à tenter :

- **Reprofilage avec davantage de patchs dans les ombres** si le logiciel le permet (certains outils permettent de densifier la zone sombre de la charte).
- Si tu as accès à un spectrophotomètre (i1Pro, par exemple) plutôt qu'un colorimètre, les mesures dans les sombres seront nettement plus fiables.

### 3. Rendu du noir dans le profil ICC

Le **black point compensation** (BPC) joue un rôle direct ici. Si le BPC est activé dans l'application source mais que le profil ICC a été construit sans en tenir compte (ou inversement), les ombres profondes subissent un remapping qui peut décaler la teinte.

Vérifier que le réglage BPC est cohérent entre Lightroom/Photoshop et Epson Print Layout.

### 4. Séchage et métamérisme

Un point spécifique aux ombres : les encres dans les zones sombres sont déposées en couche épaisse. Le **métamérisme** (changement de couleur perçue selon l'illuminant) est plus prononcé dans les hautes densités d'encre. Si tu évalues le tirage peu après l'impression ou sous un éclairage non-D50, l'excès de magenta visible dans les ombres peut être en partie un artefact métamérique.

Test simple : attendre 24h de séchage complet, puis réévaluer sous un éclairage D50. Si le magenta s'atténue, c'est du métamérisme.

### 5. Test de vérification

Pour confirmer que c'est bien un problème de profil/driver et pas un défaut matériel : imprime la même mire de gris **avec le profil ICC appliqué** cette fois. Si le magenta dans les ombres s'accentue par rapport au tirage sans gestion de couleur, le profil ICC est le coupable et il faut le reconstruire en améliorant la mesure des patchs sombres.

Si le magenta est identique avec et sans profil, c'est le comportement par défaut du driver dans sa gestion du noir riche — et la correction passera par un ajustement du type de support ou un profil ICC qui compense activement ce biais.

Quelle est ta sonde de profilage exacte et combien de patchs as-tu utilisés ?

---

## Human
*2026-04-07 16:20*

Uhm petite derive mais plutot jaune dans les bandes plus sombres

---

## Assistant
*2026-04-07 16:21*

Correction notée — dérive jaune, pas magenta, dans les bandes sombres.

Ça change la lecture. Si les gris moyens et clairs sont neutres et que seules les ombres profondes tirent vers le jaune, on est sur un scénario différent.

## Pistes pour une dérive jaune dans les ombres

### 1. Déficit de bleu dans les noirs riches

Le jaune est l'opposé du bleu. Une dérive jaune dans les ombres signifie soit un excès de jaune déposé, soit un déficit de la composante bleue (donc un déséquilibre entre les canaux cyan et magenta qui ensemble produisent le bleu). Sur l'ET-8550, le mélange CMY dans les noirs riches est piloté par le driver — un **type de support incorrect** reste une cause probable.

### 2. Encre noire photo vs noire mate

L'ET-8550 sélectionne automatiquement l'encre noire selon le type de support déclaré. Si le driver utilise la noire mate sur un papier qui attend la noire photo (ou inversement), la densité des noirs change et le ratio CMY d'accompagnement se retrouve déséquilibré. Résultat typique : une teinte parasite dans les ombres profondes uniquement.

Quel papier utilises-tu et quel type de support est sélectionné dans le driver ?

### 3. Sonde et mesure des patchs sombres

Le point reste valide : les colorimètres de type Spyder sont peu fiables sous les densités élevées. Une dérive jaune mesurée à tort comme neutre par la sonde donnera un profil ICC qui ne corrige pas le biais — voire l'amplifie.

### 4. Séchage

Le jaune dans les ombres est un symptôme classique d'encre pas encore stabilisée. Les pigments jaunes sèchent plus lentement dans les zones à forte densité d'encre. Si tu évalues le tirage dans l'heure qui suit l'impression, refais le test après 24h — ça peut suffire à régler la question.

### Point important

Tu as dit au départ que le problème global était un **excès de magenta systématique**. Maintenant le test de la mire de gris sans gestion de couleur montre une dérive **jaune dans les ombres seulement**. Ce sont deux problèmes distincts. Le magenta que tu voyais sur les tirages habituels vient probablement de la chaîne ICC (profil, double conversion, BPC), tandis que la dérive jaune dans les sombres est un comportement du driver ou du matériel.

Il faudrait traiter les deux séparément. On attaque lequel en premier ?

---

## Human
*2026-04-07 16:22*

Jaune

---

## Assistant
*2026-04-07 16:22*

D'accord. Concentrons-nous sur la dérive jaune dans les ombres.

Pour affiner le diagnostic, j'ai besoin de quelques infos :

1. **Quel papier** utilises-tu exactement (marque, référence) ?
2. **Quel type de support** est sélectionné dans le driver Epson pour ce papier ?
3. **Combien de temps** après impression as-tu évalué la mire — immédiatement, ou après séchage ?
4. **Sous quel éclairage** tu regardes le tirage ?

Si le jaune persiste après 24h de séchage sous un éclairage correct, la prochaine étape serait de vérifier la correspondance type de support / papier réel, et éventuellement de faire un nozzle check pour voir si le canal cyan dépose correctement.

---

## Human
*2026-04-07 16:23*

Ok j’imprime avec epson print layout. Tu peux controler mon setup sur papier espon premium glossy ?

---

## Assistant
*2026-04-07 16:23*

Je ne peux pas voir ton écran ni accéder à ton installation d'Epson Print Layout. Je n'ai pas de capacité de prise de contrôle à distance.

Par contre, si tu fais des captures d'écran des éléments suivants, je peux les analyser :

1. **Epson Print Layout** — l'écran principal avec les réglages de gestion des couleurs (profil ICC sélectionné, rendering intent, BPC activé ou non)
2. **Epson Print Layout** — le réglage du type de support sélectionné
3. **Le driver Epson** — l'onglet où apparaissent les paramètres de qualité, type de support, et gestion des couleurs côté driver

Envoie-moi ça et je te dis si quelque chose cloche dans la configuration.

---

## Human
*2026-04-07 16:26*

Passe en sonnet

---

## Assistant
*2026-04-07 16:26*

Compris, je continue en Sonnet.

Je ne peux pas changer de modèle moi-même — c'est un réglage que tu contrôles côté interface. Sur l'app [[Claude]] ou [[Claude]].ai, tu peux sélectionner le modèle (Opus, Sonnet, Haiku) dans le sélecteur en haut de la conversation.

En attendant, envoie les captures d'écran quand tu les as, quel que soit le modèle actif — l'analyse sera la même.

---

## Human
*2026-04-07 17:59*

*(empty message)*

---

## Assistant
*2026-04-07 18:00*

Let me read the uploaded file to understand its contents.
```
This block is not supported on your current device yet.
```

Le fichier est une sauvegarde HTML d'une conversation [[ChatGPT]]. Le contenu utile est tronqué — je n'ai que le code HTML/CSS/JS de l'interface [[ChatGPT]], pas le texte de la conversation elle-même.

Laisse-moi essayer d'extraire le texte utile.
```
This block is not supported on your current device yet.
```

J'ai pu extraire le contenu. C'est une conversation [[ChatGPT]] sur l'automatisation d'un rendu mosaïque/collage pour photos — pas directement liée au problème de dérive jaune dans les ombres à l'impression.

C'est ce fichier que tu voulais me soumettre, ou tu comptais m'envoyer des captures d'écran de ton setup Epson Print Layout sur papier Premium Glossy ?

Si c'est les réglages d'impression qu'on doit analyser, il me faut plutôt :

- une capture d'Epson Print Layout montrant le **profil ICC sélectionné**, le **rendering intent**, et le **type de support**
- une capture du **driver Epson** (onglet qualité/couleur)

---

## Human
*2026-04-07 18:00*

*(empty message)*

---

## Assistant
*2026-04-07 18:00*

Bien. Voici ce que je lis sur ta capture d'Epson Print Layout :

- **Paper Source** : Cassette 2 - Standard
- **Quality** : Best Quality
- **Color Settings Type** : Use ICC Profile
- **ICC Profile** : EPSON ET-8500 L8160 Series Premium Glossy
- **Rendering Intent** : Relative Colorimetric
- **Black Point Compensation** : activé

Plusieurs points à relever :

### 1. Le profil ICC utilisé

Tu utilises le profil **générique Epson** fourni avec le driver (« EPSON ET-8500 L8160 Series Premium Glossy »), pas un profil personnalisé créé avec Spyder. C'est ce profil-là que tu as profilé toi-même, ou c'est le profil usine ? Si tu as créé un profil custom avec SpyderPrint, il devrait porter un nom différent et il faudrait le sélectionner ici à la place.

Les profils génériques Epson sont notoirement approximatifs dans les ombres — c'est cohérent avec une dérive jaune dans les bandes sombres.

### 2. Paper Source : « Cassette 2 - Standard »

C'est suspect. « Standard » fait référence à du papier ordinaire. Pour du Premium Glossy, le driver devrait indiquer un type de support adapté (Premium Glossy Photo Paper ou équivalent). Si le driver pense imprimer sur du papier standard, il va ajuster le dépôt d'encre en conséquence — moins d'encre, mauvais ratio CMY dans les noirs riches. C'est une cause directe possible de ta dérive jaune dans les ombres.

### 3. Black Point Compensation activé + Relative Colorimetric

Ce combo est correct en principe, mais avec un profil générique imprécis dans les ombres, le BPC peut amplifier une dérive existante.

### Actions immédiates

1. **Vérifie le type de support** dans le driver Epson (pas dans EPL, dans le driver lui-même). Il doit être réglé sur « Epson Premium Glossy » ou équivalent — pas « Standard ».
2. **Clarifie quel profil ICC tu utilises** : profil usine Epson ou profil custom Spyder ? Si c'est le profil usine, c'est probablement la source principale du problème.

Tu peux me montrer l'écran du driver Epson (les propriétés de l'imprimante côté macOS) ?

---

## Human
*2026-04-09 05:26*

C’est ok magenta disparu. PEux tu me faire un workflow pour que cela soit evité à l’avenir

---

## Assistant
*2026-04-09 05:28*

Bien — problème résolu. Voici le workflow.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Le document couvre la chaîne complète : calibration écran, profilage imprimante, configuration EPL, workflow Lightroom → impression, checklist pré-impression à cocher avant chaque session, table de diagnostic en cas de dérive, et calendrier de maintenance. Le point spécifique qui t'a posé problème (profil usine vs custom + type de support incorrect) est signalé en encadré d'avertissement.

---

## Human
*2026-04-09 05:55*

Rule : avant de creer un fichier contenant du texte, tu propose dorenavant de le faire en .md ou Docx

---

## Assistant
*2026-04-09 05:55*

Compris. J'enregistre cette préférence.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

C'est noté. À partir de maintenant, je te demanderai systématiquement si tu préfères un .md ou un .docx avant de générer un document texte.

---

## Human
*2026-04-09 05:56*

emet le workflow en .md

---

## Assistant
*2026-04-09 05:57*

```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Contenu identique au .docx, en markdown. Tu as maintenant les deux formats.

---
