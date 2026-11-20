# Transcript — « I Built an AI Object Tracking Camera with ESP32-CAM »

- **Source** : Marina
- **URL** : https://youtu.be/1EH5gkYsk3o
- **Durée** : 14:30
- **Date** : 2026-06-03
- **Moteur** : Whisper local (small, faster-whisper)
- **Segments** : 360

---

[00:09] Bonjour à tous, mon nom est Marina, et aujourd'hui je voudrais vous montrer comment j'ai construit mon projet le plus récent.
[00:15] C'est l'Esp32 Object Tracking Camera.
[00:18] J'aime vraiment construire des projets qui connectent à l'AI et à l'Hardware, donc c'est l'un d'entre eux.
[00:24] J'ai eu deux goals pour ce projet, le premier était de trouver un modèle et entraîner avec mes propres photos,
[00:32] ce que j'ai fait, et j'ai créé mon objecteur pour prendre environ 500 photos et m'assurer que mes caméras ne suivent que cet objecteur.
[00:42] Et le deuxième goal était d'actuellement créer mes propres parts mécaniques, ce que j'ai fait et que je suis très heureuse.
[00:50] Pour la première fois, je pense que c'est très cool.
[00:53] J'ai fait surement que c'est mon virus, mon hardware et les servos et il fonctionne bien.
[01:04] Peut-être pas parfait pour la première fois, mais je suis heureuse.
[01:07] Je vais vous tourner dans ce processus.
[01:09] J'espère vraiment que l'information va être utile pour vous et c'est intéressant de regarder.
[01:14] Et j'espère que vous avez aimé.
[01:16] Merci.
[01:17] Avant de aller aux détails, je voudrais vous montrer comment le whole système fonctionne.
[01:22] Pour ce projet, j'utilise l'esp32 camera, laptop, un autre esp32 et le service driver avec deux services.
[01:30] L'esp32 record le vidéo, laptop fonctionne avec l'aile et l'esp32, un autre contrôle deux services.
[01:38] Et ça, tout le monde, ça devient mon camére d'objecteur.
[01:43] L'esp32 caméra envoie le live vidéo de mon laptop sur Wi-Fi.
[01:49] Dans mon laptop, le model AI que j'ai trainé, le model basically regarde le vidéo et essaie de trouver cet objecteur.
[01:57] Et quand l'objecteur est trouvé, le piéton s'occupe où il est dans le frame.
[02:02] Et cette information est utilisée pour changer le caméra.
[02:04] Puis le piéton envoie un commentaire simple pour l'esp32.
[02:09] Et l'esp32 ne fonctionne pas avec l'aile.
[02:12] Le travail c'est juste de recevoir le commentaire et de contrôler le service.
[02:15] Ici, nous avons bougé à l'arrière du mouvement hardware.
[02:18] Le deuxième esp32 envoie les signes pour le service driver.
[02:21] Et le service driver contrôle les deux services.
[02:24] Un pour le gauche et le right mouvement.
[02:26] Et un pour le haut et le bas mouvement.
[02:28] Ces services physiquement évoquent le caméra pour que l'objecteur peut suivre.
[02:31] Avant de continuer, j'aimerais partager deux choses.
[02:34] La première c'est que vous pouvez simplifier ce set-up.
[02:38] Vous n'avez pas à utiliser l'esp32.
[02:41] Mais mon but c'est de faire le travail.
[02:43] Et j'ai utilisé ce que j'avais à l'époque.
[02:46] Et parce qu'il y a beaucoup de processus d'information,
[02:50] il peut y avoir un petit délai.
[02:52] Donc c'est quelque chose que j'ai envie de raconter.
[02:54] La deuxième chose, c'est que des gens me demandent
[02:57] si je suis en train d'avoir un AI directement sur l'esp32.
[03:01] Et dans cette version je n'ai pas.
[03:04] Ma caméra d'esp32 ne fonctionne pas avec l'esp32.
[03:07] Et tout l'aile s'occupe sur mon laptop.
[03:10] Je pense qu'il y a des petits modèles sur l'esp32.
[03:13] Mais ma caméra d'esp32 n'est pas puissante.
[03:16] C'est suffisant pour m'occuper de mon modèle.
[03:18] Donc elle s'occupe sur mon laptop.
[03:20] Maintenant que le système overview est clair,
[03:22] j'aimerais vous montrer comment j'ai construit le corps de la caméra.
[03:25] Cette partie était en fait l'un des parts les plus intéressantes
[03:28] pour moi parce que j'ai designé la pièce 3D
[03:32] et j'ai dû s'assurer que les services, les modèles de caméra,
[03:35] les crous et toutes les parties de mouvement
[03:39] Avant de toucher la pièce 3D et les parties printées,
[03:44] j'ai centré les services avant.
[03:46] C'est important parce que si la pièce 3D n'est pas centrée,
[03:50] la caméra ne peut pas s'occuper plus tard
[03:52] ou ça peut cacher les limites mécaniques quand elle s'occupe.
[03:55] Donc j'ai élevé la pièce 3D en code sur GitHub
[03:58] et vous pouvez l'utiliser avant l'assemblée.
[04:00] J'ai ajouté ma première pièce 3D
[04:02] pour le mouvement de gauche et de droite.
[04:04] La pièce 3D va à l'intérieur de cette pièce 3D
[04:06] et la pièce 3D connecte à la plateforme de rotation.
[04:09] Donc quand la pièce 3D tourne, la caméra tourne avec ça.
[04:13] Et ce sont les crouquettes que j'ai utilisées pour cette pièce 3D.
[04:16] Ensuite, j'ai ajouté la pièce Tilt Yoga Base.
[04:19] Cette pièce s'occupe de la caméra cradle
[04:21] et la cradle s'occupe de l'esp32 caméra model.
[04:24] Cette partie est importante parce que
[04:26] elle supporte la caméra pendant qu'elle s'occupe et s'occupe.
[04:29] Et ici j'ai ajouté la caméra cradle.
[04:31] J'ai attaché la pièce 3D à la pièce 3D.
[04:36] Cette pièce va s'occuper de l'esp32 caméra model.
[04:39] La seule chose que je pense, c'est que j'ai enduré les crouquettes
[04:43] parce qu'elles ont commencé à interferer avec le mouvement de la cradle.
[04:47] Maintenant j'ai ajouté la deuxième pièce pour le mouvement de gauche et de gauche.
[04:50] Il faut être vraiment stable parce qu'elle s'occupe de la caméra
[04:54] pendant qu'elle s'occupe
[04:55] et même un petit mouvement à l'intérieur de la cradle
[04:57] peut faire le mouvement de la caméra.
[04:59] Donc j'ai ajouté la pièce de support
[05:01] pour que la cradle soit plus secure.
[05:03] Et maintenant finalement j'ai placé la pièce s'occupe de la caméra
[05:06] et le câble à l'intérieur de la cradle.
[05:08] La pièce final, cette pièce de base.
[05:17] Elle ajoute plus de stabilité à ma caméra
[05:19] et je pense que ça fait que le tout le design est plus terminé.
[05:22] Et après mettre tout ensemble,
[05:24] c'est ce que j'ai enduré.
[05:26] Je pense que ça ressemble bien.
[05:28] C'est encore un prototype.
[05:29] Je suis juste heureux que la partie mécanique finirait.
[05:32] Je vais partager le code que j'ai utilisé pour créer le file STL.
[05:35] Donc si vous voulez construire quelque chose similaire
[05:37] vous pouvez ajuster le design pour votre propre hardware.
[05:40] Ici je veux rapidement vous montrer le wiring.
[05:43] Le service connecte à le service driver.
[05:45] J'utilise channel 0 pour pan et channel 1 pour tilt.
[05:49] Le service connecte à la deuxième ESP32 par I2C.
[05:53] GPO21 est SDA, qui est la ligne de date
[05:56] et GPO22 est SCL, qui est la ligne de cloc.
[05:59] J'utilise aussi external 5V pour le service
[06:02] parce qu'ils nécessitent plus de current
[06:04] que l'ESP32.
[06:08] Avant d'utiliser le modèle AI,
[06:10] j'ai besoin d'un stream de vidéo stabilisé
[06:12] de la caméra ESP32.
[06:13] Mais ce projet m'a voulu plus
[06:15] de vitesse et de stabilité
[06:16] que de la qualité de qualité de l'image.
[06:18] Ici j'utilise la résolution QVGA
[06:20] qui est 320 x 240.
[06:22] Ce n'est pas la qualité la plus haute
[06:24] mais c'est plus facile à procéder en temps réel.
[06:26] La caméra envoie cette vidéo live
[06:28] sur le wi-fi de mon laptop
[06:30] et le Python peut lire ce stream
[06:32] pour des détections d'objectifs.
[06:34] Maintenant que la partie mécanique
[06:36] s'est travaillée, la prochaine étape
[06:38] était d'éteindre la caméra de l'objectif.
[06:40] Mais j'ai trainé un modèle yellow
[06:42] en utilisant mes propres photos.
[06:44] J'ai pas voulu utiliser un objectif random.
[06:46] J'ai voulu l'objectif de apprendre
[06:48] quelque chose unique.
[06:49] J'ai designé cet objectif
[06:51] et j'ai printé sur mon 3D printer.
[06:53] J'utilise ma ESP32
[06:55] pour prendre des photos
[06:57] parce que j'ai besoin d'un AI
[06:59] pour apprendre de la même caméra
[07:01] et ne pas l'utiliser plus tard dans mon projet.
[07:03] J'utilise un iPhone
[07:05] et j'utilise des images
[07:07] de la caméra de l'objectif
[07:09] sur ma ESP32.
[07:11] J'utilise un script de Python
[07:13] pour prendre des photos comme mes détections
[07:15] et j'utilise mon github
[07:17] pour obtenir ce code si vous avez besoin.
[07:19] Après que j'ai collecté les images
[07:21] la prochaine étape était de l'élaboration.
[07:23] J'ai utilisé un outil
[07:24] qui m'a appelé MakeSense.
[07:26] Je n'ai jamais utilisé ça avant mais c'était assez facile à utiliser.
[07:28] J'ai ajouté toutes mes photos
[07:30] et j'ai créé seulement un label
[07:32] qui s'appelle TargetObject
[07:34] et puis j'ai commencé à mettre des textes
[07:36] autour de cet objectif.
[07:38] C'est-à-dire que les textes
[07:40] m'ont dit que c'est un objectif
[07:42] et j'ai besoin de vous apprendre
[07:44] cet objectif spécifique.
[07:46] Et cette partie est très importante
[07:48] parce que le model s'étend
[07:50] par les exemples que je donne.
[07:52] Donc, le meilleur que mes photos
[07:54] et les labels sont, le meilleur que le model
[07:56] peut reconnaître mon objectif.
[07:58] Et après que j'ai terminé le label
[08:00] j'ai exporté tout dans YOLO format.
[08:02] C'est-à-dire qu'il me donne
[08:04] un folder avec beaucoup de textes
[08:06] et il y a juste des numéros
[08:08] à l'intérieur du texte
[08:10] qui disent en fait
[08:12] YOLO où l'objectif est dans l'image.
[08:14] Donc l'image montre l'objectif
[08:16] et ce petit texte
[08:18] explique le model où l'objectif est.
[08:20] Et après que j'ai exporté
[08:22] mes labels
[08:24] j'ai encore besoin de préparer
[08:26] tout pour YOLO training.
[08:28] J'ai eu mes images rôles
[08:30] et les files labels
[08:32] et j'ai besoin
[08:34] d'organiser elles dans la bonne structure.
[08:36] Donc, j'ai écrit
[08:38] un script Python pour ça.
[08:40] Ce que ça fait,
[08:42] c'est qu'il y a des images
[08:44] qui ont les labels.
[08:46] Il les met ensemble
[08:48] et ensuite explique tout
[08:50] dans le training et la validation data.
[08:52] J'ai utilisé 80% pour le training
[08:54] et 20% pour la validation.
[08:56] Donc, le set de training
[08:58] c'est ce que le model apprend
[09:00] et le set de validation
[09:02] c'est ce que j'ai utilisé pour vérifier
[09:04] si le model peut reconnaître l'objectif de nouvelles images.
[09:06] Et le script
[09:08] aussi crée le file data
[09:10] qui explique YOLO où l'objectif est
[09:12] et ce qu'est l'un des classes.
[09:14] Après le script
[09:16] mon set de data est prêt
[09:18] et il dit
[09:20] que j'ai trouvé 384 images
[09:22] et 383 d'elles ont eu des labels.
[09:24] Donc, c'est comme si
[09:26] l'image était skippée
[09:28] parce qu'on n'avait pas les labels.
[09:30] Et ensuite
[09:32] le folder de data
[09:34] a tous les needs de YOLO.
[09:36] Il a tous les images, les labels
[09:38] et nous avons ce file de data.
[09:40] Ok, maintenant
[09:42] après que l'on ait notre folder de data
[09:44] on peut commencer à trainer notre model de YOLO.
[09:46] J'ai utilisé un petit model
[09:48] qui s'appelle YOLOv8NANA
[09:50] et j'ai trainé sur mon set de data
[09:52] pour 80 ebooks.
[09:54] C'est à dire que le model passe
[09:56] dans mes images 80 fois.
[09:58] Vous pouvez voir beaucoup de numéros.
[10:00] Ils peuvent vérifier si le model s'improve.
[10:02] Le nombre signifie
[10:04] la preuve, la précision, la récolte.
[10:06] Dans mes vidéos c'est difficile de dire
[10:08] ce qu'ils disent parce que c'est juste le début
[10:10] de la training.
[10:12] Et ça m'a pris un peu de temps, ça m'a pris 30 minutes
[10:14] probablement, mais ça dépend de votre
[10:16] compétition et les settings.
[10:18] Alors après la fin de la training
[10:20] YOLO me donne ce best.pt file
[10:22] C'est un file de Pytorch
[10:24] qui s'occupe du model train
[10:26] et c'est ce que j'utilise plus tard pour la détection.
[10:28] J'ai testé sur mes images de validation
[10:30] pour voir si je pouvais reconnaître mon objectif
[10:32] un nouveau exemple.
[10:34] Et c'est en travaillant. YOLO est en passant
[10:36] dans les images et en détectant mon objectif.
[10:38] Après testant le model
[10:40] YOLO a sauvé les résultats
[10:42] dans la folder large-detect.
[10:44] Et ici vous pouvez voir
[10:46] que j'ai trouvé mon objectif
[10:48] et j'ai trouvé la box.
[10:50] Le 0.75 est le score de confiance
[10:52] donc le model est de 75 %
[10:54] confident.
[10:56] J'ai pensé que pour cette qualité de caméra
[10:58] le score était bien, donc j'ai décidé
[11:00] de le faire.
[11:02] Et maintenant nous sommes prêts
[11:04] pour la main Python code.
[11:06] Je ne veux pas aller à chaque ligne
[11:08] mais ici je vous montre
[11:10] la partie importante.
[11:12] C'est que ce path point à mon model
[11:14] pour détecter mon objectif
[11:16] de l'esp32 caméra live stream.
[11:18] Ici vous pouvez voir
[11:20] que la caméra suivait mon objectif
[11:22] mais il ne répond pas
[11:24] à ma main ou à un objectif.
[11:26] C'est-à-dire que ce n'est pas seulement le mouvement
[11:28] mais c'est de reconnaître le objectif
[11:30] que j'ai traîné.
[11:32] Je vais rapidement tourner
[11:34] la main idée de la code de track.
[11:36] Je ne vais pas expliquer à chaque ligne
[11:38] mais je vais vous montrer
[11:40] comment Python connecte la détection AI
[11:42] de l'esp32 server mouvement.
[11:44] Ici j'ai installé la main Python script
[11:46] donc j'ai connecté 3 choses.
[11:48] Le file model train,
[11:50] la porte serial pour la 2e esp32
[11:52] et la URL de l'esp32 caméra stream.
[11:54] J'ai ajouté l'application IP
[11:56] et la porte serial
[11:58] parce qu'ils seront différents pour chaque setup.
[12:00] Et ici j'ai commencé
[12:02] à créer le stream de la vidéo live
[12:04] de ma caméra esp32.
[12:06] J'ai utilisé le frame reader custom
[12:08] pour que Python fasse le nouveau frame
[12:10] de la caméra et ça m'a aidé
[12:12] à réduire la délègue
[12:14] parce que la code de track
[12:16] fonctionne avec le même frame
[12:18] plutôt que le vieux frame de vidéo.
[12:20] Ici Python envoie chaque frame de caméra
[12:22] dans le model YOLO.
[12:24] Le modèle vérifie l'image
[12:26] et essaie de trouver mon objectif target.
[12:28] A la droite vous pouvez voir le résultat.
[12:30] YOLO a trouvé l'objectif
[12:32] et a trouvé une carte grise.
[12:34] Les notes montrent le centre objectif
[12:36] et le centre de la caméra.
[12:38] Puis il y a un commentaire simple
[12:40] pour la seconde esp32.
[12:42] Dans ma code, le commentaire commence
[12:44] avec D et ensuite envoie deux numéros.
[12:46] Une pour le mouvement de pan,
[12:48] qui est à droite et une pour le mouvement de tilt.
[12:50] Ce qui est à droite et une pour le mouvement de tilt.
[12:52] C'est pour ça que Python est disant
[12:54] l'esp32 comment la caméra devrait bouger.
[12:56] Ici, la seconde esp32
[12:58] read le commentaire de Python.
[13:00] Il y a deux valeurs de mouvement.
[13:02] Une pour à droite et une pour à droite.
[13:04] Une pour à droite et une pour à droite.
[13:06] Une pour à droite et une pour le mouvement de tilt.
[13:08] Alors Nardina ajoute ces valeurs
[13:10] pour les positions de target
[13:12] pour que la caméra s'occupe de l'autre.
[13:14] Ici, je suis en train de tourner le mouvement de tilt.
[13:16] Ces valeurs contrôlent
[13:18] comment le pan et le mouvement de tilt
[13:20] et comment la motion s'entend.
[13:22] La caméra s'entend bien.
[13:24] Mais je l'adresse dans ces numéros
[13:26] parce qu'il y a toujours un trait de l'offre.
[13:28] Si je le fais trop smooth,
[13:30] ça réacte plus vite
[13:32] mais si je le fais trop vite,
[13:34] je suis toujours en train de trouver
[13:36] une balance entre ces deux options.
[13:38] Je crois que je vous ai montré
[13:40] tout ce que je voulais vous montrer
[13:42] en regardant ce projet.
[13:44] J'ai pris beaucoup de temps
[13:46] de construire et de débugner.
[13:48] J'ai été très heureuse
[13:50] de voir cela fonctionner.
[13:52] C'est toujours un prototype
[13:54] et je l'ai toujours appris.
[13:56] Mais j'ai été très heureuse.
[13:58] Je n'ai pas beaucoup de gens
[14:00] pour me partager ce type de projet.
[14:02] C'est pourquoi j'espère que vous
[14:04] trouverez des informations
[14:06] et que ce soit utile.
[14:08] Ou peut-être des parts de cette vidéo
[14:10] où j'ai le plaisir de vous regarder.
[14:12] Je vais poser
[14:14] tous mes files STL
[14:16] et les codes qu'il y a dans le Kit Hub.
[14:18] Vous êtes modèles et bienvenue
[14:20] à l'utiliser.
[14:22] J'espère
[14:24] que vous avez aimé.
[14:26] J'espère vous voir bientôt. Merci beaucoup
[14:28] d'avoir regardé et je vous souhaite
[14:30] de vous abonner.
[14:32] Merci.
