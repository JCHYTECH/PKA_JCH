---
tags:
  - type/project
  - status/active
---
# Raccourcis Lightroom et automatisation

**Created:** 2026-03-13 09:58  
**Updated:** 2026-03-13 10:08  
**Messages:** 11

---

## Human
*2026-03-13 09:58*

J’utilise lightroom LrC, j’ai des plugins pour transferer des images à des logiciels tels que photoshop ou autre. Problemes pour acceder à la fonction de transfert, il ya plusieurs etapes avant d’accéder à la commande . Y a t’il un moyen pour resoudre ce soucis par exemple avec des shorcuts ou autre automatisme

---

## Assistant
*2026-03-13 09:58*

Je vérifie les options les plus fiables pour LrC sur Mac, surtout les raccourcis, les presets d’éditeur externe et les automatismes qui évitent les menus à répétition.

---

## Assistant
*2026-03-13 09:59*

J’ai déjà un point utile : dans LrC, l’accès direct existe pour certains cas, notamment Commande+E pour Photoshop et Commande+Option+E pour “autre éditeur”. Le vrai gain vient ensuite de bien configurer les éditeurs externes et, si nécessaire, d’ajouter un raccourci macOS pour une commande de menu précise.

---

## Assistant
*2026-03-13 09:59*

Oui. Dans Lightroom Classic, il y a trois niveaux de solution, du plus simple au plus efficace.

À 10:59 à Bruxelles, la réponse la plus directe est la suivante : pour éviter les menus à répétition, commencez par exploiter les raccourcis intégrés de LrC. Adobe indique notamment `Commande + E` pour envoyer vers Photoshop et `Commande + Option + E` pour ouvrir dans “autre éditeur”. Adobe documente aussi la création de préréglages d’éditeur externe dans les préférences, ce qui permet d’appeler plus vite une application tierce depuis `Photo > Edit In` sans reparamétrer à chaque fois. citeturn411946search0turn621233search5turn411946search3turn621233search2turn621233search14

La meilleure méthode, dans votre cas, est généralement celle-ci : dans `Lightroom Classic > Préférences > External Editing`, configurez chaque logiciel externe comme “Additional External Editor”, puis enregistrez un preset par usage, par exemple “Topaz TIFF 16 bits”, “PS calque”, “Helicon 8 bits”, etc. Adobe précise qu’on peut créer plusieurs presets d’éditeurs externes et ensuite les appeler via `Photo > Edit In > Edit In [Nom du preset]`. Cela réduit déjà fortement le nombre d’étapes. citeturn411946search2turn411946search3turn621233search14turn621233search16

Ensuite, sur Mac, vous pouvez souvent créer un vrai raccourci clavier personnalisé pour cette commande de menu. Apple explique que, dans `Réglages Système > Clavier > Raccourcis clavier > Raccourcis de l’app`, on peut ajouter un raccourci pour une commande de menu d’une application, à condition de saisir le titre du menu exactement comme il apparaît, y compris la hiérarchie avec `->`, la ponctuation et les points de suspension éventuels. Concrètement, pour Lightroom Classic, cela peut fonctionner avec une entrée du type `Photo->Edit In->Edit In Photoshop` ou `Photo->Edit In->Edit In Topaz TIFF 16 bits`, mais le texte doit correspondre exactement à la langue de votre interface Lightroom. citeturn621233search0turn621233search7turn621233search15

Si votre “transfert” passe par un plugin ou une commande plus enfouie qui n’est pas facilement assignable par le système, la solution la plus robuste sur Mac est un automatisme de type Keyboard Maestro. Sa documentation montre qu’il sait sélectionner directement un menu d’application via l’action “Select or Show a Menu Item”, et même rechercher des menus par nom. C’est très utile quand Lightroom ne propose pas de raccourci natif ou quand la commande est dans un sous-menu. citeturn342041search1turn342041search3turn342041search5

En pratique, je vous conseille ce plan très concret :
1. Vérifier si votre commande actuelle est bien dans `Photo > Edit In`. Si oui, utilisez d’abord les raccourcis Adobe existants. citeturn411946search0turn621233search5  
2. Créer un preset d’éditeur externe par logiciel ou par type de fichier. citeturn411946search3turn621233search2  
3. Assigner un raccourci macOS au menu exact du preset. citeturn621233search0turn621233search7  
4. Si cela échoue parce que la commande n’est pas un vrai menu exploitable, passer à Keyboard Maestro pour automatiser la séquence. citeturn342041search1turn342041search5

Mon avis pratique :  
- Pour Photoshop uniquement, rien de plus rapide que `Commande + E`. citeturn411946search0turn621233search5  
- Pour un autre logiciel fixe, le meilleur compromis est “preset externe + raccourci macOS”. citeturn411946search3turn621233search0  
- Pour des workflows plus complexes, variables, ou plugin-dépendants, Keyboard Maestro est nettement plus puissant qu’un simple raccourci système. citeturn342041search1turn342041search5

Si vous me donnez le nom exact du plugin ou de la commande que vous utilisez dans Lightroom, je peux vous indiquer la combinaison la plus adaptée et même vous écrire la procédure pas à pas pour macOS, en français, avec le libellé exact à saisir.

---

## Human
*2026-03-13 10:01*

Photoshop, luminar neo, Topaz, helicon focus

---

## Assistant
*2026-03-13 10:01*

Je vérifie les chemins les plus directs pour vos quatre outils, afin de distinguer ce qui relève des raccourcis natifs de LrC et ce qui exige un automatisme externe sur Mac.

---

## Assistant
*2026-03-13 10:02*

Le point important se confirme : vos quatre logiciels n’entrent pas tous dans Lightroom par le même “tuyau”, donc un seul raccourci ne couvrira pas proprement tous les cas. Topaz et Luminar ont des chemins différents selon le type de fichier et le type d’intégration, et c’est ce qui crée souvent l’impression de workflow trop long.

---

## Assistant
*2026-03-13 10:03*

À 11:03 à Bruxelles, oui, vous pouvez nettement simplifier ce workflow, mais pas avec une seule méthode pour tout. Dans Lightroom Classic, Adobe ne fournit en natif qu’un raccourci direct pour Photoshop (`⌘E`) et un raccourci générique pour “autre éditeur” (`⌘⌥E`). Pour aller plus loin, il faut combiner les préréglages d’éditeur externe de Lightroom avec des raccourcis macOS, et parfois un outil de macro sur Mac. citeturn975882time0turn572292view4turn572292view2turn572292view3

Pour Photoshop, c’est le cas le plus simple : `⌘E` envoie directement l’image vers Photoshop. Adobe documente aussi `⌘⌥X` pour ouvrir comme Smart Object dans Photoshop. Pour ce logiciel, il n’y a donc pas réellement de problème de profondeur de menu : le raccourci natif est déjà la meilleure solution. citeturn572292view4

Pour Topaz Photo AI, il faut distinguer deux usages. Pour un RAW, Topaz recommande de passer par `File > Plug-in Extras > Process with Topaz Photo AI`, car c’est cette voie qui conserve l’accès à RAW Denoise et renvoie un DNG dans les cas compatibles. Pour des JPEG, TIFF ou PNG, la voie prévue est `Photo > Edit In > Topaz Photo AI`. Topaz précise aussi que, pour le traitement par lot, il vaut mieux sélectionner plusieurs images dans la grille Library ou le filmstrip et utiliser ce chemin adapté, et ne pas lancer `Photo > Edit In > Topaz Photo AI` depuis Develop si vous voulez envoyer plusieurs images, car cela ne traite que l’image affichée. citeturn572292view1turn508851view3turn508851view4

Pour Luminar Neo, le flux documenté par Skylum n’est pas le même : ils indiquent un envoi via clic droit `Export > Luminar Neo`, avec le choix entre ouvrir les fichiers source ou envoyer une copie avec les ajustements Lightroom. Skylum précise aussi qu’en mode plugin Lightroom envoie souvent un TIFF, et que si vous voulez réellement travailler le RAW dans Luminar, il faut soit utiliser le mode autonome, soit passer par `Export > Luminar Neo > Open Source Files`. Ils indiquent également que les outils de Focus Stacking, HDR Merge et Upscale AI sont disponibles dans le plugin Lightroom. citeturn572292view0turn508851view0turn508851view1

Pour Helicon Focus, Lightroom n’a pas de raccourci natif dédié comparable à Photoshop. La logique à appliquer est donc celle d’un “éditeur externe” ou d’une macro pilotant le menu réel qui apparaît sur votre machine. Adobe permet de définir un éditeur externe supplémentaire dans `Préférences > External Editing`, puis de créer plusieurs presets d’éditeurs externes avec des réglages distincts. C’est la bonne base si Helicon apparaît chez vous comme destination d’édition externe. citeturn572292view2turn572292view4

La meilleure organisation, pour vos quatre logiciels, serait la suivante. Photoshop reste sur `⌘E`. Topaz RAW reçoit un raccourci séparé sur la commande `File->Plug-in Extras->Process with Topaz Photo AI`. Topaz non-RAW reçoit un autre raccourci sur `Photo->Edit In->Topaz Photo AI`. Luminar Neo reçoit soit un raccourci de menu si la commande existe dans la barre de menus de Lightroom sur votre Mac, soit une macro. Helicon Focus suit la même logique que Luminar. Cette séparation est importante, car Topaz n’utilise pas le même chemin pour RAW et non-RAW, et Luminar ne suit pas le schéma standard “Edit In” dans sa documentation principale. citeturn572292view1turn508851view3turn572292view0turn508851view0

Sur macOS, vous pouvez créer des raccourcis clavier d’application dans `Réglages Système > Clavier > Raccourcis clavier > Raccourcis de l’app`. Apple précise qu’il faut saisir le titre du menu exactement comme il apparaît, et donne même l’exemple du format hiérarchique avec `->`, par exemple `File->Export as PDF…`. Ils précisent aussi que certaines apps ne permettent pas ces raccourcis. Pour Lightroom Classic, cela donne des intitulés du type `File->Plug-in Extras->Process with Topaz Photo AI` ou `Photo->Edit In->Topaz Photo AI`, à condition que ces commandes soient bien présentes dans la barre de menus et que le texte corresponde exactement à votre interface. citeturn572292view3

Là où macOS atteint ses limites, c’est quand la commande utile est surtout accessible par clic droit, ou quand l’intitulé varie selon le contexte. Dans ce cas, Keyboard Maestro est le meilleur outil sur Mac pour ce problème précis : sa fonction “Select or Show a Menu Item” sait piloter un élément de menu, tolère la différence entre `...` et `…`, et peut même utiliser une expression régulière si le nom varie un peu. C’est, à mon avis, la solution la plus propre pour Luminar Neo et possiblement pour Helicon si leur entrée Lightroom n’est pas facilement raccourcissable par le système seul. citeturn508851view2turn197418search0

En pratique, je vous conseillerais ceci. Gardez Photoshop en natif. Faites de Topaz RAW un raccourci clavier dédié séparé. Faites de Topaz TIFF/JPEG un second raccourci. Ensuite, utilisez soit `⌘⌥E` pour l’éditeur externe que vous utilisez le plus souvent hors Photoshop, soit Keyboard Maestro pour Luminar Neo et Helicon Focus. C’est le montage le plus rapide et le plus robuste pour un utilisateur Mac qui passe souvent de Lightroom à plusieurs logiciels externes. citeturn572292view4turn572292view2turn572292view1turn572292view0turn508851view2

Si vous voulez, je peux maintenant vous préparer la configuration exacte, touche par touche, pour votre Mac, par exemple un schéma du type : Photoshop = `⌘E`, Topaz RAW = `⌃⌥T`, Topaz TIFF = `⌃⇧T`, Luminar = `⌃⌥L`, Helicon = `⌃⌥H`, avec les intitulés exacts à saisir dans macOS ou dans Keyboard Maestro.

---

## Human
*2026-03-13 10:05*

Ok

---

## Assistant
*2026-03-13 10:05*

Je prépare un schéma concret pour votre Mac, avec une logique de touches simple et les chemins de menus à tester dans Lightroom Classic pour chaque logiciel.

---

## Assistant
*2026-03-13 10:07*

À 11:07 à Bruxelles, voici la configuration que je vous recommande sur Mac pour Lightroom Classic. Le principe est simple : garder le natif pour Photoshop, créer deux raccourcis distincts pour Topaz, et traiter Luminar Neo et Helicon comme des commandes de menu/plugin à automatiser. Lightroom Classic fournit déjà `⌘E` pour Photoshop et `⌘⌥E` pour “autre éditeur”, et Adobe permet aussi de créer plusieurs préréglages d’éditeur externe dans `Préférences > External Editing`. citeturn970035time0turn943369search0turn943369search1

Je vous propose ce mapping :
`⌘E` = Photoshop  
`⌃⌥T` = Topaz Photo AI sur RAW  
`⌃⇧T` = Topaz Photo AI sur TIFF/JPEG/PNG  
`⌃⌥L` = Luminar Neo “Open Source Files”  
`⌃⇧L` = Luminar Neo “Edit a Copy with Lightroom Adjustments”  
`⌃⌥H` = Helicon Focus  
J’ai choisi des combinaisons qui évitent les raccourcis Adobe les plus classiques et qui restent faciles à mémoriser par logiciel.

Pour Photoshop, ne changez rien : `⌘E` est déjà le meilleur choix. Pour Topaz, il faut vraiment séparer les deux cas, car la documentation Topaz prévoit deux chemins différents : pour les RAW, `File > Plug-in Extras > Process with Topaz Photo AI`; pour les fichiers non-RAW, `Photo > Edit In > Topaz Photo AI`. Topaz précise aussi que, pour du multi-image, il vaut mieux lancer cela depuis la grille Library ou le filmstrip, et non depuis Develop avec `Photo > Edit In`, sinon seule l’image affichée part dans Topaz. citeturn943369search3

Pour Luminar Neo, Skylum documente surtout un flux d’export : clic droit `Export > Luminar Neo`, puis soit `Open Source Files`, soit `Edit a Copy with Lightroom Adjustments`. Ils précisent aussi que si vous envoyez une copie avec ajustements Lightroom, vous travaillez généralement sur un TIFF, tandis que pour garder le RAW il faut passer par `Open Source Files` ou travailler en autonome. Autrement dit, Luminar mérite deux raccourcis distincts si vous l’utilisez souvent de ces deux façons. citeturn652909search0turn652909search2

Pour Helicon Focus, je le traiterais comme une commande de plugin/export dédiée, pas comme un simple “autre éditeur”. Adobe ne fournit pas de raccourci natif dédié à Helicon dans la liste standard de Lightroom Classic, donc la bonne logique est : soit un raccourci macOS sur le menu exact si Helicon apparaît bien dans la barre de menus de Lightroom, soit une macro Keyboard Maestro si la commande n’est accessible que par un sous-menu/plugin plus capricieux. Adobe confirme seulement le raccourci Photoshop et “other editor”; pour les commandes de menu spécifiques, macOS exige le titre exact du menu. citeturn943369search0turn943369search2

Pour créer les raccourcis macOS, allez dans `Réglages Système > Clavier > Raccourcis clavier > Raccourcis de l’app > +`. Choisissez l’application `Lightroom Classic`, puis dans “Titre du menu”, tapez la commande exactement comme elle apparaît, en respectant la hiérarchie avec `->`, la ponctuation et les points de suspension si présents. Apple indique explicitement qu’il faut saisir le titre à l’identique. Donc, si votre interface Lightroom est en français, il faut saisir le titre en français; si elle est en anglais, en anglais. citeturn943369search2

Les premiers intitulés que je testerais chez vous sont ceux-ci :
`File->Plug-in Extras->Process with Topaz Photo AI`  
`Photo->Edit In->Topaz Photo AI`  
Pour Luminar, testez l’équivalent exact visible dans votre menu Lightroom, par exemple un chemin de type `File->Export->Luminar Neo->Open Source Files` ou `...->Edit a Copy with Lightroom Adjustments`, seulement si ces entrées apparaissent bien dans votre barre de menus. Apple impose l’intitulé exact, et Skylum confirme ces deux variantes de flux. citeturn943369search2turn652909search0

Si un raccourci macOS refuse de marcher, passez directement à Keyboard Maestro. Son action `Select or Show a Menu Item` est faite pour ça, et sa documentation indique qu’elle tolère même les variations entre `...` et `…`, avec possibilité d’utiliser une correspondance plus souple. C’est, à mon avis, la solution la plus robuste pour Luminar Neo et Helicon Focus si leurs commandes Lightroom ne sont pas exposées proprement au système. citeturn157594search0turn157594search8

Mon conseil final serait donc : Photoshop en natif, Topaz avec deux vrais raccourcis, Luminar avec deux raccourcis si vous alternez RAW/TIFF, et Helicon sur une touche dédiée via menu exact ou Keyboard Maestro. C’est le montage le plus propre pour réduire réellement les clics sans casser votre flux.

Envoyez-moi une capture de la barre de menus Lightroom ouverte sur `Photo`, `File`, `Plug-in Extras` et `Export`, et je vous donnerai les intitulés exacts à saisir, ligne par ligne, pour votre Mac.

---
