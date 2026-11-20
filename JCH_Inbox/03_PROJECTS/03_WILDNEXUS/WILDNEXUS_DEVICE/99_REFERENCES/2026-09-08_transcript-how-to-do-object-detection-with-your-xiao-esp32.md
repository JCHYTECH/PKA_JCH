# Transcript — « How to do Object Detection with your Xiao ESP32 S3 Sense and Edge Impulse. »

- **Source** : SBPElectronics
- **URL** : https://youtu.be/ggce4GxzHPE
- **Durée** : 05:55
- **Date** : 2026-09-08
- **Moteur** : Whisper local (small, faster-whisper)
- **Segments** : 179

---

[00:00] Bienvenue à une autre vidéo sur le SDP Electronics.
[00:02] Dans cette vidéo je vais vous montrer comment utiliser l'impulse à l'impulse avec la caméra d'ESP32-S3.
[00:08] Donc, le premier qu'on veut, c'est de boire la caméra dans votre PC.
[00:13] Maintenant, le côté de l'air de l'air de l'air est au point où vous pouvez commencer le softwares.
[00:16] Le premier c'est d'assurer que votre version de ESP32 est sous 2.0.17.
[00:20] Pour vérifier ça, vous devez aller au management des bords en tapant l'ESP32.
[00:24] Et ensuite vous pouvez vérifier la version ici.
[00:26] D'engrer et d'abrailler pour obtenir 2.0.17.
[00:29] La prochaine chose que vous voulez faire, c'est de aller au site de cette web.
[00:32] C'est cdestudio.com. Le link est dans la description.
[00:35] Donc, vous voulez regarder pour des codes.
[00:38] Donc, vous vous devez juste scroller et puis il sera ici.
[00:41] Délégez le file sketch de ici.
[00:43] Cliquez ici et puis il va déléger quelque chose sur votre PC.
[00:45] Il sera un file zip.
[00:46] Donc, vous devez l'univerer.
[00:48] Dans le file zip, il sera un file takephotocommand.io.
[00:52] Cliquez ici et vous devez l'uploadir à l'ESP32.
[00:56] Et ensuite, après que vous l'avez upload,
[00:58] cliquez sur capture pour les images de votre machine.
[01:03] Vous pointez votre caméra à l'objet.
[01:06] Cliquez sur capture et cliquez sur capture pour l'image.
[01:10] Si vous avez une erreur de cartes, ne vous inquiétez pas.
[01:12] C'est juste parce que le carton est either empty
[01:15] ou l'esthécard à l'intérieur est de la bonne façon.
[01:18] Ou faute.
[01:19] Dès que vous avez les images de votre esthécard,
[01:21] vous devez aller à l'impôt de l'épisode et l'uploadir le data.
[01:24] Donc, regardez pour l'uploadir le data,
[01:26] et puis cliquez sur les files, les files de vérité.
[01:30] Dès que vous avez fait ça, cliquez sur upload data.
[01:32] Après que vous cliquez sur upload data,
[01:34] cliquez sur label en queue et puis cliquez sur la box
[01:37] autour de l'item ou la chose que vous allez faire
[01:40] le machine-learning.
[01:41] Donc, je fais des fruits ici.
[01:42] Donc, je fais un gros apple.
[01:44] Et puis, cliquez sur le box et cliquez sur save label.
[01:48] Et vous faites ça pour tous ceux-ci.
[01:54] Dès que vous achetez un autre item,
[01:56] cliquez sur label et puis cliquez sur l'autre item.
[02:00] Donc, je clique sur orange.
[02:02] Et maintenant, je vais faire orange et banana.
[02:05] Ok, donc maintenant qu'il n'y a pas de plus de choses à être label,
[02:08] vous devez aller créer l'impôt.
[02:10] Donc, dans créer l'impôt,
[02:11] vous devez ajouter un procès en bloc.
[02:13] Et vous devez faire l'image.
[02:16] Dès que vous avez ajouté ça,
[02:17] vous devez ajouter un bloc de la technique et l'objectif.
[02:20] Et puis cliquez sur save impôt.
[02:23] Maintenant, vous devez aller à l'image.
[02:25] Dans l'image, vous devez changer de colorité
[02:27] à grise et sur save paramètres.
[02:29] Maintenant, vous devez générer des features.
[02:31] Ça peut prendre un peu de temps.
[02:33] Ok, donc maintenant qu'il est terminé,
[02:35] vous devez voir le bloc.
[02:36] Donc, je pense que c'est ok.
[02:39] Ils ne sont pas tous allés ensemble,
[02:40] ce qui est une bonne chose.
[02:41] Il y a peut-être quelques outliers ici et là-bas.
[02:44] Mais je pense que ça devrait être bien.
[02:46] Maintenant, cliquez sur object detection.
[02:48] Settez votre procès à 0.01
[02:50] si vous voulez être plus vite.
[02:51] Maintenant, cliquez sur save impôt.
[02:53] Encore une fois, ça m'a pris un peu de temps.
[02:55] Ok, donc maintenant, je suis terminé.
[02:56] Donc, mon bloc ne ressemble pas très bien.
[02:59] Le background,
[03:00] le bloc de l'applet est mixé.
[03:02] Mais ça peut détecter 75% de l'applet.
[03:05] Banane est tombée.
[03:08] Je ne sais pas ce qui s'est passé là.
[03:10] 0, 0, 0%.
[03:11] Donc, ça peut détecter le bloc de l'applet.
[03:13] Orange, ok, 50%.
[03:16] Je pense que l'applet est le meilleur.
[03:19] Donc, vous allez voir que j'ai uploadé sur l'ID.
[03:22] Donc, ce n'est pas l'endroit.
[03:23] Maintenant, c'est le bloc de l'applet.
[03:25] Dans le bloc, nous avons dû sélectionner
[03:27] l'ID library.
[03:29] Et puis, on va construire.
[03:31] Ça va créer un library pour vous
[03:32] downloader sur votre PC
[03:34] pour vous uploader sur l'ID.
[03:36] Ok, donc maintenant, c'est parti.
[03:37] Vous pourriez avoir un tic-box sur votre écran
[03:39] qui va downloader
[03:41] un file d'EginPulse.
[03:42] Ne l'unzipez pas.
[03:43] Si vous ne l'avez pas,
[03:44] vous pouvez le downloader sur le bouton.
[03:47] Ok, donc maintenant, dans l'ID,
[03:48] vous devez aller au sketch
[03:50] et inclure l'ID library
[03:52] et puis ajouter l'ID library.
[03:54] Si ce n'est pas ouvert,
[03:55] allez au download
[03:56] et cliquez sur l'ID file.
[03:58] Cliquez l'open.
[03:59] Comme vous pouvez le voir, c'est le processant
[04:01] sur le bouton.
[04:02] Le processant va prendre un temps.
[04:03] Ok, donc maintenant, le processant est terminé.
[04:05] Vous pouvez retourner au site
[04:07] que vous avez utilisé avant.
[04:08] Donc, sur le site,
[04:09] il y aura ce code
[04:10] à la étape 3,
[04:11] près du bouton.
[04:12] Reste cet exemple sketch.
[04:14] Donc, copiez le sketch
[04:16] et puis retournez à votre code.
[04:18] Et puis,
[04:20] contrôlez A
[04:21] et puis contrôlez V,
[04:23] qui sera sélectionnée,
[04:24] et puis paste.
[04:26] Et puis, vous allez au bouton
[04:27] et vous trouverez et inclurez.
[04:28] Donc, les changements inclurent
[04:30] à votre library
[04:31] que vous avez juste installé.
[04:33] Donc, mon code est appelé
[04:35] Edge Impulse
[04:36] pour YouTube Inferencing.
[04:37] Et, si vous avez fait ça,
[04:38] uploadz le code.
[04:39] Uploadz-le.
[04:40] Il peut prendre un temps.
[04:41] Ok, le code est terminé.
[04:42] Uploadz-le.
[04:43] Maintenant, let's go to the serial monitor.
[04:45] Comme vous pouvez le voir,
[04:45] il y a de nouveaux objets.
[04:47] Donc, je vais vous mettre en orange
[04:49] et mettre ma caméra à l'écran.
[04:51] Comme vous pouvez le voir,
[04:53] depuis mon cours d'art,
[04:54] ce n'est pas très bon.
[04:56] Je vais vous mettre en orange
[04:57] et vous dites que ça détecte
[04:58] un apple et un orange.
[05:01] Mais parfois, un orange.
[05:02] Ok, maintenant, let's bring in the apple.
[05:04] Ok, le apple
[05:06] est un petit peu mieux.
[05:09] Il y a certaines angles.
[05:10] Il juste me dit que c'est un apple.
[05:12] Mais à un autre angle,
[05:13] il me dit que c'est un orange.
[05:15] C'est un apple,
[05:17] mais il me dit que c'est un full orange
[05:18] d'une certaine raison,
[05:19] peut-être parce que c'est la couleur
[05:20] du lait et de la réflexion.
[05:23] Il me dit que c'est un orange.
[05:25] Maintenant, il me dit...
[05:26] Oh non.
[05:27] Ok, maintenant, j'ai un banane.
[05:29] Apple orange, orange, orange.
[05:32] Non, le banane.
[05:33] Parce que le banane est 0%.
[05:35] Orange, orange, orange.
[05:36] Et je fais un apple et un banane.
[05:38] C'est très off
[05:39] de ce que je pointe,
[05:40] parce que je n'ai pas fait très bien
[05:42] dans la boxe
[05:44] et la lumière
[05:45] en prendre des pictures.
[05:46] Mais je vous montre que vous pouvez faire mieux.
[05:47] Si vous aimez ce tutoriel
[05:49] ou ce tutoriel, j'espère que vous pouvez
[05:50] laisser un like et un abonneur.
[05:52] Merci d'avoir regardé.
