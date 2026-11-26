# Transcript — « Ta carte de 8 Go peut faire tourner une grosse IA : la technique secrète du MoE »

- **Source** : Kiara · IA locale
- **URL** : https://www.youtube.com/watch?v=eYNdQTp2dPs&t=13s
- **Durée** : 10:45
- **Date** : 2026-11-18
- **Moteur** : sous-titres YouTube
- **Segments** : 789

---

[00:00] Vous avez une carte graphique de 8&nbsp;Go ?
[00:02] Comme un joueur sur 4.
[00:02] Vous avez une carte graphique de 8 Go,
[00:02] Vous avez une carte graphique de 8 Go, comme un joueur sur quatre. Je vais y
[00:04] Je vais y faire tourner un modèle de 35 milliards de paramètres…
[00:04] comme un joueur sur quatre. Je vais y
[00:04] comme un joueur sur quatre. Je vais y faire tourner un modèle de 35 milliards
[00:06] faire tourner un modèle de 35 milliards
[00:06] faire tourner un modèle de 35 milliards de paramètres, plus vite que vous ne
[00:07] plus vite que vous ne lisez.
[00:08] de paramètres, plus vite que vous ne
[00:08] de paramètres, plus vite que vous ne lisez. Et restez jusqu'à la fin, on va
[00:09] Et restez jusqu'à la fin : on va composer une petite chanson, avec 2 IA sur une
[00:10] lisez. Et restez jusqu'à la fin, on va
[00:10] lisez. Et restez jusqu'à la fin, on va composer une petite chanson avec deux IA
[00:12] composer une petite chanson avec deux IA
[00:13] composer une petite chanson avec deux IA sur une seule carte.
[00:13] seule carte.
[00:15] sur une seule carte.
[00:15] sur une seule carte. [musique]
[00:17] Ah !
[00:18] 100 degrés !
[00:18] Ah,
[00:18] Ah, 100 degrés, je vais finir par fondre.
[00:19] Je vais finir par fondre !
[00:21] C'est le moment de sortir prendre l'air !
[00:22] 100 degrés, je vais finir par fondre.
[00:22] 100 degrés, je vais finir par fondre. C'est le moment de sortir prendre l'air.
[00:28] Hello !
[00:29] Moi, c'est Kiara, votre experte de l'IA !
[00:31] Hello, moi c'est Kiara, votre experte de
[00:31] Hello, moi c'est Kiara, votre experte de l'IA.
[00:42] Pfff, ça réveille !
[00:44] Bon.
[00:44] Ça réveille.
[00:45] Ça réveille. Bon, le problème, vous le connaissez. Un
[00:45] Le problème, vous le connaissez.
[00:47] Un vrai modèle, par exemple Qwen 3.6 : 35 milliards de paramètres.
[00:48] Bon, le problème, vous le connaissez. Un
[00:48] Bon, le problème, vous le connaissez. Un vrai modèle, par exemple 3.6, 35
[00:51] vrai modèle, par exemple 3.6, 35
[00:51] vrai modèle, par exemple 3.6, 35 milliards de paramètres. Même compressé
[00:52] Même compressé en Q4, il lui faut 20&nbsp;Go.
[00:53] milliards de paramètres. Même compressé
[00:53] milliards de paramètres. Même compressé en Q4, il lui faut 20 Go. Votre carte en
[00:55] Votre carte en a 8.
[00:56] en Q4, il lui faut 20 Go. Votre carte en
[00:56] en Q4, il lui faut 20 Go. Votre carte en a huit, ça ne rentre pas.
[00:56] Ça ne rentre pas.
[00:58] Alors aujourd'hui, je vous montre comment le faire rentrer quand même dans votre
[00:58] a huit, ça ne rentre pas.
[00:58] a huit, ça ne rentre pas. Alors aujourd'hui, je vous montre
[01:00] Alors aujourd'hui, je vous montre
[01:00] Alors aujourd'hui, je vous montre comment le faire rentrer quand même dans
[01:02] comment le faire rentrer quand même dans
[01:02] comment le faire rentrer quand même dans votre carte de 8 Go, la technique
[01:02] carte de 8&nbsp;Go : la technique secrète du MoE, pour « Mixture of Experts ».
[01:04] votre carte de 8 Go, la technique
[01:04] votre carte de 8 Go, la technique secrète du MOE pour Mixture of Experts.
[01:08] Une IA, c'est une usine à mots.
[01:08] secrète du MOE pour Mixture of Experts.
[01:08] secrète du MOE pour Mixture of Experts. Une IA, c'est une usine à mots. Votre
[01:11] Votre phrase entre…
[01:11] Une IA, c'est une usine à mots. Votre
[01:11] Une IA, c'est une usine à mots. Votre phrase entre et elle est découpée en
[01:12] et elle est découpée en morceaux : des tokens.
[01:13] phrase entre et elle est découpée en
[01:14] phrase entre et elle est découpée en morceaux, des tokens.
[01:16] Prenons « Kiara, votre experte en…
[01:16] morceaux, des tokens.
[01:16] morceaux, des tokens. Prenons Kiara, votre experte en
[01:18] ».
[01:18] Mon prénom ?
[01:18] Prenons Kiara, votre experte en
[01:19] Prenons Kiara, votre experte en mon prénom coupé en deux, qui ara et
[01:19] Coupé en 2 : « Ki », « ara ».
[01:22] Et « experte » : « expert », plus un petit « e » tout seul.
[01:22] mon prénom coupé en deux, qui ara et
[01:22] mon prénom coupé en deux, qui ara et experte, expert plus un petit e tout
[01:25] experte, expert plus un petit e tout
[01:25] experte, expert plus un petit e tout seul.
[01:25] Charmant.
[01:26] seul.
[01:26] seul. Charmant.
[01:27] Chaque token devient une liste de 2 048 nombres.
[01:27] Charmant.
[01:27] Charmant. Chaque token devient une liste de 2048
[01:30] Chaque token devient une liste de 2048
[01:30] Chaque token devient une liste de 2048 nombres. Puis, couche après couche,
[01:31] Puis, couche après couche, l'usine travaille : 40 fois pour chaque token.
[01:32] nombres. Puis, couche après couche,
[01:33] nombres. Puis, couche après couche, l'usine travaille 40 fois pour chaque
[01:35] l'usine travaille 40 fois pour chaque
[01:35] l'usine travaille 40 fois pour chaque token.
[01:35] À la sortie, elle devine le token suivant…
[01:36] token.
[01:36] token. À la sortie, elle devine le token
[01:38] À la sortie, elle devine le token
[01:38] À la sortie, elle devine le token suivant.
[01:38] « IA ».
[01:38] suivant.
[01:39] suivant. IA, elle a tout compris.
[01:39] Elle a tout compris.
[01:41] Toutes les pièces de l'usine, les paramètres, sont rangées dans la mémoire de votre
[01:41] IA, elle a tout compris.
[01:41] IA, elle a tout compris. Toutes les pièces de l'usine, les
[01:42] Toutes les pièces de l'usine, les
[01:42] Toutes les pièces de l'usine, les paramètres, sont rangés dans la mémoire
[01:44] paramètres, sont rangés dans la mémoire
[01:44] paramètres, sont rangés dans la mémoire de votre carte, la VRAM.
[01:44] carte : la VRAM.
[01:46] Tant que tout tient dedans, tout va vite.
[01:46] de votre carte, la VRAM.
[01:47] de votre carte, la VRAM. Tant que tout tient dedans, tout va
[01:48] Tant que tout tient dedans, tout va
[01:48] Tant que tout tient dedans, tout va vite. Mais 35 milliards de paramètres,
[01:49] Mais 35 milliards de paramètres, ça déborde.
[01:51] vite. Mais 35 milliards de paramètres,
[01:51] vite. Mais 35 milliards de paramètres, ça déborde.
[01:52] Alors on range le gros du modèle dans un deuxième entrepôt : la RAM de votre PC.
[01:52] ça déborde.
[01:53] ça déborde. Alors on range le gros du modèle dans un
[01:54] Alors on range le gros du modèle dans un
[01:55] Alors on range le gros du modèle dans un deuxième entrepôt, la RAM de votre PC.
[01:57] Sur place, votre processeur fait travailler les experts.
[01:57] deuxième entrepôt, la RAM de votre PC.
[01:57] deuxième entrepôt, la RAM de votre PC. Sur place, votre processeur fait
[01:59] Sur place, votre processeur fait
[01:59] Sur place, votre processeur fait travailler les experts. Mais on garde
[02:00] Mais on garde sur la carte tout ce qui sert à chaque token : l'attention, le
[02:01] travailler les experts. Mais on garde
[02:01] travailler les experts. Mais on garde sur la carte tout ce qui sert à chaque
[02:03] sur la carte tout ce qui sert à chaque
[02:03] sur la carte tout ce qui sert à chaque token, la tension, le routeur et le
[02:04] routeur…
[02:05] et le contexte de la conversation.
[02:05] token, la tension, le routeur et le
[02:05] token, la tension, le routeur et le contexte de la conversation.
[02:07] À chaque token, le routeur choisit 8 experts : la commande part par le petit
[02:08] contexte de la conversation.
[02:08] contexte de la conversation. À chaque token, le routeur choisit huit
[02:09] À chaque token, le routeur choisit huit
[02:09] À chaque token, le routeur choisit huit experts. La commande part par le petit
[02:11] chemin…
[02:12] experts. La commande part par le petit
[02:12] experts. La commande part par le petit chemin et seuls ces huit-là se mettent
[02:12] et seuls ces huit-là se mettent au travail.
[02:14] chemin et seuls ces huit-là se mettent
[02:14] chemin et seuls ces huit-là se mettent au travail.
[02:15] au travail.
[02:15] Et seul le résultat revient à la carte.
[02:15] au travail. Et seul le résultat revient à la carte.
[02:17] Et ainsi de suite, 40 fois par token.
[02:17] Et seul le résultat revient à la carte.
[02:17] Et seul le résultat revient à la carte. Et ainsi de suite, 40 fois par token.
[02:20] Le hic : ce petit chemin est lent.
[02:20] Et ainsi de suite, 40 fois par token.
[02:20] Et ainsi de suite, 40 fois par token. Le hic, ce petit chemin est lent.
[02:22] Le temps d'un aller-retour vers la RAM, la VRAM en fait plus de 5.
[02:22] Le hic, ce petit chemin est lent.
[02:22] Le hic, ce petit chemin est lent. Le temps d'un aller-retour vers la RAM,
[02:25] Le temps d'un aller-retour vers la RAM,
[02:25] Le temps d'un aller-retour vers la RAM, la VRAM en fait plus de cinq.
[02:27] la VRAM en fait plus de cinq.
[02:27] Heureusement, on n'y va chercher que 8 experts, pas tout le modèle.
[02:27] la VRAM en fait plus de cinq. Heureusement, on y va chercher que huit
[02:28] Heureusement, on y va chercher que huit
[02:28] Heureusement, on y va chercher que huit experts, pas tout le modèle.
[02:31] Mais…
[02:31] experts, pas tout le modèle.
[02:31] experts, pas tout le modèle. Mais qu'est-ce qu'un expert, Jami?
[02:31] qu'est-ce qu'un expert, Jamy ?
[02:34] Laissez-moi vous montrer mon jeu préféré, pour que vous compreniez bien.
[02:34] Mais qu'est-ce qu'un expert, Jami?
[02:34] Mais qu'est-ce qu'un expert, Jami? Laissez-moi vous montrer mon jeu préféré
[02:36] Laissez-moi vous montrer mon jeu préféré
[02:36] Laissez-moi vous montrer mon jeu préféré pour que vous compreniez bien.
[02:40] Voici AI Fighters !
[02:43] Le but du jeu : vaincre tous les ennemis.
[02:43] Voici [musique] AI Fighters. Le but du
[02:43] Voici [musique] AI Fighters. Le but du jeu, vaincre tous les ennemis. Vous avez
[02:45] Vous avez 16 combattants, chacun expert dans son art.
[02:46] jeu, vaincre tous les ennemis. Vous avez
[02:46] jeu, vaincre tous les ennemis. Vous avez 16 combattants, chacun expert dans son
[02:48] 16 combattants, chacun expert dans son
[02:48] 16 combattants, chacun expert dans son art. Premier ennemi, un boxeur. Pas
[02:48] Premier ennemi : un boxeur ?
[02:50] Pas besoin des judokas ni des karatékas : le grand maître envoie les spécialistes
[02:51] art. Premier ennemi, un boxeur. Pas
[02:51] art. Premier ennemi, un boxeur. Pas besoin des judokas ni des karatékas,
[02:52] besoin des judokas ni des karatékas,
[02:52] besoin des judokas ni des karatékas, [musique]
[02:52] [musique]
[02:52] [musique] le grand maître envoie les spécialistes
[02:54] de la boxe.
[02:54] le grand maître envoie les spécialistes
[02:54] le grand maître envoie les spécialistes de la boxe. L'ennemi suivant se bat au
[02:55] L'ennemi suivant se bat au sol ?
[02:56] de la boxe. L'ennemi suivant se bat au
[02:56] de la boxe. L'ennemi suivant se bat au sol. D'autres combattants. Les autres
[02:57] D'autres combattants.
[02:58] Les autres restent sur le banc de touche.
[02:59] sol. D'autres combattants. Les autres
[02:59] sol. D'autres combattants. Les autres restent sur le banc de touche.
[03:01] Le modèle, c'est pareil : chaque token est un nouvel ennemi, avec ses points forts
[03:01] restent sur le banc de touche.
[03:01] restent sur le banc de touche. Le modèle, c'est pareil. [musique]
[03:02] Le modèle, c'est pareil. [musique]
[03:02] Le modèle, c'est pareil. [musique] Chaque token est un nouvel ennemi avec
[03:05] Chaque token est un nouvel ennemi avec
[03:05] Chaque token est un nouvel ennemi avec ses points forts et ses points faibles.
[03:05] et ses points faibles, et un routeur, le grand maître, choisit 8 experts sur
[03:06] ses points forts et ses points faibles.
[03:06] ses points forts et ses points faibles. Et un routeur, le [musique] grand
[03:08] Et un routeur, le [musique] grand
[03:08] Et un routeur, le [musique] grand maître, choisit huit experts sur 16.
[03:09] 16.
[03:10] 16, c'est pour illustrer : en réalité, Qwen, lui, en a 256.
[03:11] maître, choisit huit experts sur 16.
[03:11] maître, choisit huit experts sur 16. 16, c'est pour illustrer. En réalité,
[03:13] 16, c'est pour illustrer. En réalité,
[03:13] 16, c'est pour illustrer. En réalité, Quen lui en a 256. [musique] Et ceux qui
[03:15] Et ceux qui restent sur le banc de touche, on peut les installer plus loin, dans
[03:15] Quen lui en a 256. [musique] Et ceux qui
[03:15] Quen lui en a 256. [musique] Et ceux qui restent sur le banc de touche, on peut
[03:17] restent sur le banc de touche, on peut
[03:17] restent sur le banc de touche, on peut les installer plus loin dans les
[03:18] les vestiaires : la RAM.
[03:18] les installer plus loin dans les
[03:18] les installer plus loin dans les vestiaires, la RAM. Ils sont très
[03:20] Ils sont très patients.
[03:21] vestiaires, la RAM. Ils sont très
[03:21] vestiaires, la RAM. Ils sont très patients.
[03:22] Et un modèle classique, dit « dense » ?
[03:22] patients.
[03:22] patients. Et un modèle classique dit [musique]
[03:23] Et un modèle classique dit [musique]
[03:23] Et un modèle classique dit [musique] dense, lui n'a ni grand maître ni
[03:24] Lui n'a ni grand maître ni spécialistes : à chaque token, tous les combattants
[03:25] dense, lui n'a ni grand maître ni
[03:25] dense, lui n'a ni grand maître ni spécialiste. À chaque token, tous les
[03:28] spécialiste. À chaque token, tous les
[03:28] spécialiste. À chaque token, tous les combattants montent sur [musique] le
[03:28] montent sur le ring.
[03:29] combattants montent sur [musique] le
[03:29] combattants montent sur [musique] le ring. Impossible d'en laisser une partie
[03:29] Impossible d'en laisser une partie sur le banc de touche, dans les vestiaires : il
[03:31] ring. Impossible d'en laisser une partie
[03:31] ring. Impossible d'en laisser une partie sur le banc de touche dans les
[03:31] sur le banc de touche dans les
[03:31] sur le banc de touche dans les vestiaires. Il faudrait tout faire
[03:32] faudrait tout faire revenir, à chaque token.
[03:33] vestiaires. Il faudrait tout faire
[03:33] vestiaires. Il faudrait tout faire [musique] revenir à chaque token.
[03:35] Mais attention : les experts sont dans votre RAM…
[03:35] [musique] revenir à chaque token.
[03:35] [musique] revenir à chaque token. Mais attention, les experts sont dans
[03:37] Mais attention, les experts sont dans
[03:37] Mais attention, les experts sont dans votre RAM, donc c'est elles qui font la
[03:38] donc c'est elle qui fait la vitesse.
[03:39] votre RAM, donc c'est elles qui font la
[03:39] votre RAM, donc c'est elles qui font la vitesse. Et là, une erreur courante, une
[03:40] Et là, une erreur courante : une seule barrette.
[03:42] vitesse. Et là, une erreur courante, une
[03:42] vitesse. Et là, une erreur courante, une seule barrette. Avec deux barrettes bien
[03:43] Avec 2 barrettes bien placées, 2 voies en même temps : en théorie, presque
[03:44] seule barrette. Avec deux barrettes bien
[03:44] seule barrette. Avec deux barrettes bien placées, deux voies en même temps. En
[03:46] placées, deux voies en même temps. En
[03:46] placées, deux voies en même temps. En théorie, presque deux fois plus de
[03:47] 2 fois plus de débit.
[03:47] théorie, presque deux fois plus de
[03:47] théorie, presque deux fois plus de débit. C'est le dual channel.
[03:47] C'est le dual channel.
[03:50] Mais attention : pour en profiter, vos barrettes doivent être dans les bons
[03:50] débit. C'est le dual channel.
[03:50] débit. C'est le dual channel. Mais attention, pour en profiter, vos
[03:53] Mais attention, pour en profiter, vos
[03:53] Mais attention, pour en profiter, vos barrettes doivent être dans les bons
[03:54] emplacements.
[03:54] barrettes doivent être dans les bons
[03:54] barrettes doivent être dans les bons emplacements, souvent A2 et B2.
[03:55] Souvent A2 et B2…
[03:57] et en cas de doute, regardez la notice de votre carte mère.
[03:57] emplacements, souvent A2 et B2.
[03:57] emplacements, souvent A2 et B2. Et en cas de doute, regardez la notice
[03:59] Et en cas de doute, regardez la notice
[03:59] Et en cas de doute, regardez la notice de votre carte mère.
[04:00] Et la fréquence compte aussi : de la DDR5 à 6 000 plutôt qu'à 4 800,
[04:01] de votre carte mère.
[04:01] de votre carte mère. Et la fréquence compte aussi. De la DDR5
[04:03] Et la fréquence compte aussi. De la DDR5
[04:03] Et la fréquence compte aussi. De la DDR5 à 6000 plutôt qu'à 4800, c'est 1/4 de
[04:05] c'est un quart de débit en plus.
[04:06] à 6000 plutôt qu'à 4800, c'est 1/4 de
[04:06] à 6000 plutôt qu'à 4800, c'est 1/4 de débit en plus.
[04:07] Pensez à activer le profil EXPO ou XMP dans le BIOS : sans lui, votre RAM tourne
[04:07] débit en plus.
[04:07] débit en plus. Pensez à activer le profil EXPO ou XMP
[04:10] Pensez à activer le profil EXPO ou XMP
[04:10] Pensez à activer le profil EXPO ou XMP dans le BIOS. Sans lui, votre RAM tourne
[04:12] moins vite que prévu.
[04:12] dans le BIOS. Sans lui, votre RAM tourne
[04:12] dans le BIOS. Sans lui, votre RAM tourne moins vite que prévu.
[04:13] C'est gratuit, ce serait dommage de s'en priver.
[04:13] moins vite que prévu.
[04:13] moins vite que prévu. C'est gratuit, ce serait dommage de s'en
[04:14] C'est gratuit, ce serait dommage de s'en
[04:14] C'est gratuit, ce serait dommage de s'en priver.
[04:15] Je résume.
[04:15] priver.
[04:15] priver. Je résume. Le MOE, ça fait deux choses.
[04:16] Le MoE, ça fait 2 choses.
[04:19] Un : le modèle écrit plus vite, parce qu'à chaque token il ne relit que ses experts
[04:19] Je résume. Le MOE, ça fait deux choses.
[04:19] Je résume. Le MOE, ça fait deux choses. Un, le modèle écrit plus vite parce qu'à
[04:22] Un, le modèle écrit plus vite parce qu'à
[04:22] Un, le modèle écrit plus vite parce qu'à chaque token, il ne relie que ses
[04:24] chaque token, il ne relie que ses
[04:24] chaque token, il ne relie que ses experts actifs.
[04:24] actifs.
[04:25] 2 : un gros modèle tient sur une petite carte.
[04:25] experts actifs.
[04:25] experts actifs. Deux, un gros modèle tient sur une
[04:27] Deux, un gros modèle tient sur une
[04:27] Deux, un gros modèle tient sur une petite carte.
[04:29] La capacité d'un gros modèle…
[04:29] petite carte.
[04:29] petite carte. La capacité d'un gros modèle à la
[04:31] à la vitesse d'un petit.
[04:32] La capacité d'un gros modèle à la
[04:32] La capacité d'un gros modèle à la vitesse d'un petit.
[04:33] Maintenant, voyons comment le reconnaître…
[04:34] vitesse d'un petit.
[04:34] vitesse d'un petit. Maintenant, voyons comment le
[04:35] Maintenant, voyons comment le
[04:35] Maintenant, voyons comment le reconnaître et ce que ça donne vraiment
[04:35] et ce que ça donne vraiment sur une carte de 8&nbsp;Go.
[04:37] reconnaître et ce que ça donne vraiment
[04:37] reconnaître et ce que ça donne vraiment sur une carte de 8 Go.
[04:39] Comment reconnaître un MoE ?
[04:39] sur une carte de 8 Go.
[04:39] sur une carte de 8 Go. Comment reconnaître un MOE?
[04:41] Regardez son nom.
[04:41] Comment reconnaître un MOE?
[04:41] Comment reconnaître un MOE? Regardez son nom.
[04:43] Sous ce nom barbare, chaque morceau compte.
[04:43] Regardez son nom.
[04:43] Regardez son nom. Sous ce nom barbare, chaque morceau
[04:45] Sous ce nom barbare, chaque morceau
[04:45] Sous ce nom barbare, chaque morceau compte. Qwen 3.6, la famille et la
[04:45] Qwen 3.6 : la famille et la version.
[04:47] compte. Qwen 3.6, la famille et la
[04:47] compte. Qwen 3.6, la famille et la version.
[04:48] 35 B : 35 milliards de paramètres en tout.
[04:49] version.
[04:49] version. 35B, 35 milliards de paramètres en tout.
[04:51] A3B : 3 milliards actifs.
[04:52] 35B, 35 milliards de paramètres en tout.
[04:52] 35B, 35 milliards de paramètres en tout. A 3B, 3 milliards actifs. C'est la
[04:54] C'est la signature d'un MoE.
[04:55] A 3B, 3 milliards actifs. C'est la
[04:55] A 3B, 3 milliards actifs. C'est la signature d'un MOE.
[04:57] UD : la recette de compression d'Unsloth, qui garde les parties importantes plus
[04:57] signature d'un MOE.
[04:57] signature d'un MOE. UD, la recette de compression Dense
[04:59] UD, la recette de compression Dense
[04:59] UD, la recette de compression Dense Llama qui garde les parties importantes
[05:01] Llama qui garde les parties importantes
[05:01] Llama qui garde les parties importantes plus précises.
[05:01] précises.
[05:02] plus précises.
[05:02] plus précises. Q4 KM, la compression elle-même, environ
[05:03] Q4_K_M : la compression elle-même, environ 4 bits par paramètre.
[05:06] Q4 KM, la compression elle-même, environ
[05:06] Q4 KM, la compression elle-même, environ 4 bits par paramètre. Et .gguf, le
[05:07] Et point GGUF : le format que lisent llama.cpp et Ollama.
[05:09] 4 bits par paramètre. Et .gguf, le
[05:09] 4 bits par paramètre. Et .gguf, le format que lisent Llama.cpp et Ollama.
[05:12] Attention au piège : E4B chez Gemma, ce n'est pas des experts, c'est « effectif ».
[05:12] format que lisent Llama.cpp et Ollama.
[05:12] format que lisent Llama.cpp et Ollama. Attention au piège. E4B chez Gemma, ce
[05:16] Attention au piège. E4B chez Gemma, ce
[05:16] Attention au piège. E4B chez Gemma, ce n'est pas des experts, c'est effectif.
[05:18] Un petit modèle pour téléphone.
[05:18] n'est pas des experts, c'est effectif.
[05:18] n'est pas des experts, c'est effectif. Un petit modèle pour téléphone.
[05:20] Concrètement, sur une carte de 8&nbsp;Go : les parties communes et les experts de
[05:21] Un petit modèle pour téléphone.
[05:21] Un petit modèle pour téléphone. Concrètement, sur une carte de 8 Go, les
[05:24] Concrètement, sur une carte de 8 Go, les
[05:24] Concrètement, sur une carte de 8 Go, les parties communes et les experts de 8
[05:25] 8 couches restent sur la carte.
[05:26] parties communes et les experts de 8
[05:26] parties communes et les experts de 8 couches restent sur la carte, 6 Go.
[05:27] 6&nbsp;Go.
[05:29] Les experts des 32 autres couches vont dans la RAM : 14&nbsp;Go et
[05:29] couches restent sur la carte, 6 Go.
[05:29] couches restent sur la carte, 6 Go. Les experts des 32 autres couches vont
[05:31] Les experts des 32 autres couches vont
[05:31] Les experts des 32 autres couches vont dans la RAM, 14 Go et demi.
[05:33] demi.
[05:33] Et le résultat, mesuré : 66&nbsp;tokens par seconde.
[05:33] dans la RAM, 14 Go et demi.
[05:33] dans la RAM, 14 Go et demi. Et le résultat, mesuré, 66 tokens par
[05:36] Et le résultat, mesuré, 66 tokens par
[05:36] Et le résultat, mesuré, 66 tokens par seconde.
[05:37] Alors, je vous ai préparé une petite démo : un MoE dans 8&nbsp;Go de VRAM, face à
[05:38] seconde.
[05:38] seconde. Alors, je vous ai préparé une petite
[05:40] Alors, je vous ai préparé une petite
[05:40] Alors, je vous ai préparé une petite démo. Un MOE dans 8 Go de VRAM face à un
[05:43] un modèle classique.
[05:43] démo. Un MOE dans 8 Go de VRAM face à un
[05:43] démo. Un MOE dans 8 Go de VRAM face à un modèle classique.
[05:44] N'ayant pas de carte de 8&nbsp;Go, j'ai pris une RTX 4070 Ti Super, 16&nbsp;Go.
[05:45] modèle classique.
[05:45] modèle classique. N'ayant pas de carte de 8 Go, j'ai pris
[05:46] N'ayant pas de carte de 8 Go, j'ai pris
[05:46] N'ayant pas de carte de 8 Go, j'ai pris une RTX 4070 Ti Super, 16 Go. Oui, une
[05:50] Oui, une NVIDIA, pour une fois.
[05:50] une RTX 4070 Ti Super, 16 Go. Oui, une
[05:50] une RTX 4070 Ti Super, 16 Go. Oui, une Nvidia pour une fois.
[05:52] Et je l'ai volontairement bridée à 8, pour vous montrer que ça rentre.
[05:52] Nvidia pour une fois.
[05:52] Nvidia pour une fois. Et je l'ai volontairement bridée à 8
[05:54] Et je l'ai volontairement bridée à 8
[05:54] Et je l'ai volontairement bridée à 8 pour vous montrer que ça rentre.
[05:55] Même carte, même question : « Qu'est-ce qu'un modèle MoE ?
[05:56] pour vous montrer que ça rentre.
[05:56] pour vous montrer que ça rentre. Même carte, même question. Qu'est-ce
[05:58] Même carte, même question. Qu'est-ce
[05:58] Même carte, même question. Qu'est-ce qu'un modèle MOE?
[06:00] ».
[06:01] Oui, je lui fais expliquer son propre métier.
[06:01] qu'un modèle MOE?
[06:01] qu'un modèle MOE? Oui, je lui fais expliquer son propre
[06:02] Oui, je lui fais expliquer son propre
[06:02] Oui, je lui fais expliquer son propre métier.
[06:04] À gauche, un modèle classique de 27 milliards.
[06:04] métier.
[06:04] métier. À gauche, un modèle classique de 27
[06:06] À gauche, un modèle classique de 27
[06:06] À gauche, un modèle classique de 27 milliards. À droite, le MOE, plus gros.
[06:07] À droite, le MoE, plus gros.
[06:09] Première étape : le chargement.
[06:09] milliards. À droite, le MOE, plus gros.
[06:09] milliards. À droite, le MOE, plus gros. Première étape, le chargement.
[06:12] Première étape, le chargement.
[06:12] Première étape, le chargement. [grognement] Il ne se fait qu'une fois,
[06:12] Il ne se fait qu'une fois, au lancement.
[06:13] [grognement] Il ne se fait qu'une fois,
[06:13] [grognement] Il ne se fait qu'une fois, au lancement. Regardez les jauges.
[06:14] Regardez les jauges : chacun remplit ses 8&nbsp;Go de carte…
[06:15] au lancement. Regardez les jauges.
[06:15] au lancement. Regardez les jauges. Chacun remplit ses 8 Go de carte et
[06:17] et range le reste en RAM.
[06:17] Chacun remplit ses 8 Go de carte et
[06:17] Chacun remplit ses 8 Go de carte et range le reste en RAM.
[06:19] Le MoE met plus de temps : il est plus gros, et une plus grande partie part en RAM.
[06:19] range le reste en RAM.
[06:19] range le reste en RAM. Le MOE met plus de temps, il est plus
[06:21] Le MOE met plus de temps, il est plus
[06:21] Le MOE met plus de temps, il est plus gros et une plus grande partie part en
[06:22] gros et une plus grande partie part en
[06:22] gros et une plus grande partie part en RAM.
[06:23] Deuxième étape : même question, même départ…
[06:24] RAM.
[06:24] RAM. Deuxième étape, même question, même
[06:26] Deuxième étape, même question, même
[06:26] Deuxième étape, même question, même départ.
[06:27] Et le MoE a déjà fini !
[06:27] départ.
[06:27] départ. Et le MOE a déjà fini. 2 secondes, près
[06:29] 2 secondes, près de 60&nbsp;tokens par seconde.
[06:30] Et le MOE a déjà fini. 2 secondes, près
[06:30] Et le MOE a déjà fini. 2 secondes, près de 60 tokens par seconde.
[06:33] Le classique, lui…
[06:33] de 60 tokens par seconde.
[06:33] de 60 tokens par seconde. Le classique, lui, prend son temps.
[06:34] prend son temps : 5&nbsp;tokens par seconde.
[06:35] Le classique, lui, prend son temps.
[06:35] Le classique, lui, prend son temps. 5 tokens par seconde.
[06:37] Il tourne quand même : une partie de ses couches est déchargée en RAM.
[06:37] 5 tokens par seconde.
[06:37] 5 tokens par seconde. Il tourne quand même. Une partie de ses
[06:39] Il tourne quand même. Une partie de ses
[06:39] Il tourne quand même. Une partie de ses couches est déchargée en RAM, mais sans
[06:40] Mais sans le mécanisme du MoE, à chaque token, il doit tout relire, y compris ce
[06:41] couches est déchargée en RAM, mais sans
[06:41] couches est déchargée en RAM, mais sans le mécanisme du MOE, à chaque token, il
[06:44] le mécanisme du MOE, à chaque token, il
[06:44] le mécanisme du MOE, à chaque token, il doit tout relire, y compris ce qui est
[06:45] qui est en RAM.
[06:46] doit tout relire, y compris ce qui est
[06:46] doit tout relire, y compris ce qui est en RAM, d'où sa lenteur.
[06:46] D'où sa lenteur.
[06:48] Si cette technique secrète vous a bluffés…
[06:48] en RAM, d'où sa lenteur.
[06:48] en RAM, d'où sa lenteur. Si cette technique secrète vous a
[06:50] Si cette technique secrète vous a
[06:50] Si cette technique secrète vous a bluffé, abonnez-vous. La prochaine est
[06:50] abonnez-vous : la prochaine est déjà en préparation.
[06:52] bluffé, abonnez-vous. La prochaine est
[06:52] bluffé, abonnez-vous. La prochaine est déjà en préparation.
[06:54] déjà en préparation.
[06:54] déjà en préparation. Ah, alors le MOE, c'est magique?
[06:55] Alors, le MoE, c'est magique ?
[06:57] Pas tout à fait : cette technique a un coût.
[06:57] Ah, alors le MOE, c'est magique?
[06:57] Ah, alors le MOE, c'est magique? Pas tout à fait. Cette technique a un
[06:59] Pas tout à fait. Cette technique a un
[06:59] Pas tout à fait. Cette technique a un coût.
[07:00] Comme seuls quelques experts travaillent à chaque token, à taille égale, il
[07:00] coût.
[07:00] coût. Comme seuls quelques experts travaillent
[07:02] Comme seuls quelques experts travaillent
[07:02] Comme seuls quelques experts travaillent à chaque token, à taille égale, il
[07:04] raisonne un peu moins bien que son homologue dense.
[07:04] à chaque token, à taille égale, il
[07:04] à chaque token, à taille égale, il résonne un peu moins bien que son
[07:06] résonne un peu moins bien que son
[07:06] résonne un peu moins bien que son homologue dense.
[07:07] Mais comparé aux petits modèles qui tiendraient entièrement dans votre carte de
[07:07] homologue dense.
[07:07] homologue dense. Mais comparé au petit modèle qui
[07:09] Mais comparé au petit modèle qui
[07:09] Mais comparé au petit modèle qui tiendrait entièrement dans votre carte 8
[07:11] 8&nbsp;Go…
[07:11] tiendrait entièrement dans votre carte 8
[07:11] tiendrait entièrement dans votre carte 8 Go, il est bien plus intelligent.
[07:11] il est bien plus intelligent.
[07:13] Alors, quel modèle choisir pour votre machine ?
[07:13] Go, il est bien plus intelligent.
[07:13] Go, il est bien plus intelligent. Alors, quel modèle choisir pour votre
[07:15] Alors, quel modèle choisir pour votre
[07:15] Alors, quel modèle choisir pour votre machine? Je vous montre.
[07:15] Je vous montre.
[07:17] Sur une carte de 8&nbsp;Go, environ 6 gigas de modèle tiennent sur la carte.
[07:17] machine? Je vous montre.
[07:17] machine? Je vous montre. Sur une carte de 8 Go, environ 6 Go de
[07:20] Sur une carte de 8 Go, environ 6 Go de
[07:20] Sur une carte de 8 Go, environ 6 Go de modèle tiennent sur la carte. Le reste,
[07:21] Le reste, les experts, va dans la RAM.
[07:22] modèle tiennent sur la carte. Le reste,
[07:22] modèle tiennent sur la carte. Le reste, les experts, va dans la RAM. Donc tout
[07:24] Donc tout dépend de votre RAM : avec 16&nbsp;Go, Gemma 4.
[07:25] les experts, va dans la RAM. Donc tout
[07:25] les experts, va dans la RAM. Donc tout dépend de votre RAM. Avec 16 Go, Gemma
[07:27] dépend de votre RAM. Avec 16 Go, Gemma
[07:27] dépend de votre RAM. Avec 16 Go, Gemma 4, avec 32, Qwen 3.6, avec 64, jusqu'à
[07:28] Avec 32, Qwen 3.6.
[07:31] Avec 64, jusqu'à 80 milliards de paramètres.
[07:32] 4, avec 32, Qwen 3.6, avec 64, jusqu'à
[07:32] 4, avec 32, Qwen 3.6, avec 64, jusqu'à 80 milliards de paramètres.
[07:34] Bonne nouvelle : ça marche avec toutes les cartes graphiques de 8&nbsp;Go, chez
[07:35] 80 milliards de paramètres.
[07:35] 80 milliards de paramètres. Bonne nouvelle, ça marche avec toutes
[07:37] Bonne nouvelle, ça marche avec toutes
[07:37] Bonne nouvelle, ça marche avec toutes les cartes graphiques de 8 Go chez
[07:38] NVIDIA, AMD ou Intel.
[07:39] les cartes graphiques de 8 Go chez
[07:39] les cartes graphiques de 8 Go chez Nvidia, AMD ou Intel.
[07:41] En voici quelques exemples.
[07:41] Nvidia, AMD ou Intel.
[07:41] Nvidia, AMD ou Intel. En voici quelques exemples.
[07:43] Vous trouverez les liens en description : utilisez-les pour soutenir la chaîne !
[07:43] En voici quelques exemples.
[07:43] En voici quelques exemples. Vous trouverez les liens en description.
[07:45] Vous trouverez les liens en description.
[07:45] Vous trouverez les liens en description. Utilisez-les pour soutenir la chaîne.
[07:47] Pour le faire chez vous : llama.cpp, gratuit et open source.
[07:47] Utilisez-les pour soutenir la chaîne.
[07:47] Utilisez-les pour soutenir la chaîne. Pour le faire [grognement] chez vous,
[07:48] Pour le faire [grognement] chez vous,
[07:48] Pour le faire [grognement] chez vous, llama.cpp, gratuit et open source. Une
[07:51] Une ligne suffit, et 2 paramètres font tout.
[07:52] llama.cpp, gratuit et open source. Une
[07:52] llama.cpp, gratuit et open source. Une ligne suffit et deux paramètres font
[07:53] ligne suffit et deux paramètres font
[07:53] ligne suffit et deux paramètres font tout. Le premier met tout le modèle sur
[07:54] Le premier met tout le modèle sur la carte…
[07:56] tout. Le premier met tout le modèle sur
[07:56] tout. Le premier met tout le modèle sur la carte. Le second garde les experts en
[07:56] le second garde les experts en RAM.
[07:58] la carte. Le second garde les experts en
[07:58] la carte. Le second garde les experts en RAM. Si ça ne rentre pas, augmentez ce
[07:59] Si ça ne rentre pas, augmentez ce nombre.
[08:00] RAM. Si ça ne rentre pas, augmentez ce
[08:00] RAM. Si ça ne rentre pas, augmentez ce nombre.
[08:01] Bonne nouvelle : maintenant, Ollama et llama.cpp le font tout seuls.
[08:01] nombre.
[08:01] nombre. Bonne nouvelle, maintenant Ollama et
[08:03] Bonne nouvelle, maintenant Ollama et
[08:03] Bonne nouvelle, maintenant Ollama et llama.cpp le font tout seul. Au
[08:05] Au lancement, ils rangent d'eux-mêmes les experts en trop dans la RAM.
[08:05] llama.cpp le font tout seul. Au
[08:05] llama.cpp le font tout seul. Au lancement, ils rangent de même les
[08:07] lancement, ils rangent de même les
[08:07] lancement, ils rangent de même les experts en trop dans la RAM.
[08:09] Mon conseil : pour débuter, prenez Ollama, c'est le plus simple.
[08:09] experts en trop dans la RAM.
[08:09] experts en trop dans la RAM. Mon conseil, pour débuter, prenez haut
[08:11] Mon conseil, pour débuter, prenez haut
[08:11] Mon conseil, pour débuter, prenez haut la main, c'est le plus simple. Sous
[08:12] Sous Windows, LM Studio fait aussi très bien l'affaire, avec une vraie interface.
[08:13] la main, c'est le plus simple. Sous
[08:13] la main, c'est le plus simple. Sous Windows, LM Studio fait aussi très bien
[08:15] Windows, LM Studio fait aussi très bien
[08:15] Windows, LM Studio fait aussi très bien l'affaire avec une vraie interface.
[08:17] Et pour aller plus loin, n'hésitez pas à installer llama.cpp directement : vous
[08:17] l'affaire avec une vraie interface.
[08:17] l'affaire avec une vraie interface. Et pour aller plus loin, n'hésitez pas à
[08:19] Et pour aller plus loin, n'hésitez pas à
[08:19] Et pour aller plus loin, n'hésitez pas à installer llama.cpp directement. Vous
[08:21] aurez la main sur tous les réglages.
[08:21] installer llama.cpp directement. Vous
[08:21] installer llama.cpp directement. Vous aurez la main sur tous les réglages.
[08:23] Et si vous avez déjà une grosse carte ?
[08:23] aurez la main sur tous les réglages.
[08:23] aurez la main sur tous les réglages. Et si vous avez déjà une grosse carte,
[08:25] L'astuce sert aussi à faire cohabiter plusieurs usages.
[08:25] Et si vous avez déjà une grosse carte,
[08:25] Et si vous avez déjà une grosse carte, l'astuce sert aussi à faire cohabiter
[08:27] l'astuce sert aussi à faire cohabiter
[08:27] l'astuce sert aussi à faire cohabiter plusieurs usages.
[08:28] Votre assistant garde ses experts en RAM et n'occupe que 6&nbsp;Go de carte…
[08:28] plusieurs usages.
[08:28] plusieurs usages. Votre assistant garde ses experts en RAM
[08:30] Votre assistant garde ses experts en RAM
[08:30] Votre assistant garde ses experts en RAM et n'occupe que 6 Go de carte.
[08:32] Le reste est libre pour autre chose.
[08:33] et n'occupe que 6 Go de carte.
[08:33] et n'occupe que 6 Go de carte. Le reste est libre pour autre chose, par
[08:35] Par exemple, Qwen 3.6 en agent, un assistant qui enchaîne les tâches tout seul,
[08:35] Le reste est libre pour autre chose, par
[08:35] Le reste est libre pour autre chose, par exemple Quen 3.6 en agent, un assistant
[08:37] exemple Quen 3.6 en agent, un assistant
[08:37] exemple Quen 3.6 en agent, un assistant qui enchaîne les tâches tout seul
[08:39] avec un générateur de musique comme ACE-Step.
[08:39] qui enchaîne les tâches tout seul
[08:39] qui enchaîne les tâches tout seul avec un générateur de musique comme Ace
[08:41] avec un générateur de musique comme Ace
[08:41] avec un générateur de musique comme Ace Step
[08:42] Ou pour faire parler Qwen, avec un modèle de synthèse vocale.
[08:42] Step
[08:42] Step ou pour faire parler Quen avec un modèle
[08:44] ou pour faire parler Quen avec un modèle
[08:44] ou pour faire parler Quen avec un modèle de synthèse vocale.
[08:45] Sans l'astuce, il faudrait décharger l'un et recharger l'autre depuis le SSD, à
[08:45] de synthèse vocale.
[08:45] de synthèse vocale. Sans l'astuce, il faudrait décharger
[08:47] Sans l'astuce, il faudrait décharger
[08:47] Sans l'astuce, il faudrait décharger l'un et recharger l'autre depuis le SSD
[08:49] l'un et recharger l'autre depuis le SSD
[08:49] l'un et recharger l'autre depuis le SSD à chaque étape.
[08:49] chaque étape…
[08:50] et un SSD, c'est plus de 10 fois plus lent que la RAM, et encore bien moins que la
[08:51] à chaque étape.
[08:51] à chaque étape. Et un SSD, c'est plus de 10 fois plus
[08:52] Et un SSD, c'est plus de 10 fois plus
[08:52] Et un SSD, c'est plus de 10 fois plus lent que la RAM et encore bien moins que
[08:54] lent que la RAM et encore bien moins que
[08:54] lent que la RAM et encore bien moins que la carte.
[08:54] carte.
[08:55] Je vous ai concocté une petite démo qui allie plusieurs modèles chargés en VRAM :
[08:55] la carte.
[08:55] la carte. Je vous ai concocté une petite démo qui
[08:57] Je vous ai concocté une petite démo qui
[08:57] Je vous ai concocté une petite démo qui allie plusieurs modèles chargés en VRAM.
[08:59] Qwen va écrire une chanson sur les MoE, puis la jouer avec ACE-Step.
[08:59] allie plusieurs modèles chargés en VRAM.
[08:59] allie plusieurs modèles chargés en VRAM. Quen va écrire une chanson sur les MOE
[09:01] Quen va écrire une chanson sur les MOE
[09:01] Quen va écrire une chanson sur les MOE puis la jouer avec Ace Step.
[09:03] Pour ça, j'utilise OpenCode : un logiciel qu'on appelle un harness, qui permet de
[09:03] puis la jouer avec Ace Step.
[09:03] puis la jouer avec Ace Step. Pour ça, j'utilise Open Code, un
[09:05] Pour ça, j'utilise Open Code, un
[09:05] Pour ça, j'utilise Open Code, un logiciel qu'on appelle un harness qui
[09:08] logiciel qu'on appelle un harness qui
[09:08] logiciel qu'on appelle un harness qui permet de faire de l'agentique, une IA
[09:08] faire de l'agentique, une IA qui enchaîne les actions toute seule.
[09:10] permet de faire de l'agentique, une IA
[09:10] permet de faire de l'agentique, une IA qui enchaîne les actions tout seul.
[09:12] Je vous ferai une vidéo pour que vous sachiez tout sur l'agentique.
[09:12] qui enchaîne les actions tout seul.
[09:12] qui enchaîne les actions tout seul. Je vous ferai une vidéo pour que vous
[09:13] Je vous ferai une vidéo pour que vous
[09:13] Je vous ferai une vidéo pour que vous sachiez tout sur l'agentique.
[09:15] Je l'ai fait pour de vrai : dans OpenCode, je demande à Qwen une chanson sur les
[09:15] sachiez tout sur l'agentique.
[09:15] sachiez tout sur l'agentique. Je l'ai fait pour de vrai. Dans Open
[09:17] Je l'ai fait pour de vrai. Dans Open
[09:17] Je l'ai fait pour de vrai. Dans Open Code, je demande à Quen une chanson sur
[09:19] Code, je demande à Quen une chanson sur
[09:19] Code, je demande à Quen une chanson sur les MOE.
[09:19] MoE.
[09:21] Il n'occupe que 6&nbsp;Go de la carte.
[09:21] les MOE.
[09:21] les MOE. Il n'occupe que 6 Go de la carte. Il lit
[09:23] Il lit d'abord ses consignes…
[09:23] Il n'occupe que 6 Go de la carte. Il lit
[09:23] Il n'occupe que 6 Go de la carte. Il lit d'abord ses consignes. C'est long,
[09:24] c'est long, j'accélère.
[09:25] d'abord ses consignes. C'est long,
[09:25] d'abord ses consignes. C'est long, j'accélère.
[09:26] Là, il réfléchit…
[09:26] j'accélère.
[09:26] j'accélère. Là, il réfléchit
[09:28] puis il écrit les paroles.
[09:29] Là, il réfléchit
[09:29] Là, il réfléchit puis il écrit les paroles.
[09:30] « Moi je suis léger comme l'air, et rapide comme un éléphant.
[09:30] puis il écrit les paroles.
[09:30] puis il écrit les paroles. Moi, je suis léger comme l'air et rapide
[09:33] Moi, je suis léger comme l'air et rapide
[09:33] Moi, je suis léger comme l'air et rapide comme un éléphant. Bon, il a encore des
[09:33] » Bon…
[09:34] il a encore des progrès à faire en tant que parolier.
[09:35] comme un éléphant. Bon, il a encore des
[09:35] comme un éléphant. Bon, il a encore des progrès à faire en tant que parolier.
[09:37] Ensuite, il lance ACE-Step, sans se décharger : regardez la carte monter à 15,5 Go
[09:37] progrès à faire en tant que parolier.
[09:37] progrès à faire en tant que parolier. Ensuite, il lance Ace Step sans se
[09:39] Ensuite, il lance Ace Step sans se
[09:39] Ensuite, il lance Ace Step sans se décharger. Regardez la carte montée à 15
[09:42] sur 16.
[09:42] décharger. Regardez la carte montée à 15
[09:42] décharger. Regardez la carte montée à 15 Go et demi sur 16.
[09:43] Les 2 modèles sont chargés en même temps.
[09:44] Go et demi sur 16.
[09:44] Go et demi sur 16. Les deux modèles sont chargés en même
[09:45] Les deux modèles sont chargés en même
[09:45] Les deux modèles sont chargés en même temps.
[09:46] Et voilà !
[09:46] temps.
[09:46] temps. Et voilà.
[09:47] En tout, l'agent a travaillé une minute…
[09:48] Et voilà.
[09:48] Et voilà. En tout, l'agent a travaillé 1 minute
[09:50] dont 23 secondes pour générer 45 secondes de musique.
[09:50] En tout, l'agent a travaillé 1 minute
[09:50] En tout, l'agent a travaillé 1 minute dont 23 secondes pour générer 45
[09:52] dont 23 secondes pour générer 45
[09:52] dont 23 secondes pour générer 45 secondes de musique.
[09:53] Je vous laisse juger…
[09:53] secondes de musique.
[09:53] secondes de musique. Je vous laisse juger. Musique.
[09:55] Musique !
[09:56] Je vous laisse juger. Musique.
[09:56] Je vous laisse juger. Musique. Boès, Boès, [musique]
[09:58] Boès, Boès, [musique]
[09:58] Boès, Boès, [musique] c'est la vie d'un réseau. Chaque expert
[10:01] c'est la vie d'un réseau. Chaque expert
[10:01] c'est la vie d'un réseau. Chaque expert a son rôle et moi j'en ai plein les
[10:03] a son rôle et moi j'en ai plein les
[10:03] a son rôle et moi j'en ai plein les bras. Quand le switch [musique]
[10:04] bras. Quand le switch [musique]
[10:04] bras. Quand le switch [musique] s'active, hop, ça tournera
[10:07] s'active, hop, ça tournera
[10:07] s'active, hop, ça tournera l'IA la plus drôle, c'est moi, je le dit
[10:10] l'IA la plus drôle, c'est moi, je le dit
[10:10] l'IA la plus drôle, c'est moi, je le dit tout bas. Les autres modèles pleurent,
[10:13] tout bas. Les autres modèles pleurent,
[10:13] tout bas. Les autres modèles pleurent, ils sont trop gros et lent. Moi, je suis
[10:15] ils sont trop gros et lent. Moi, je suis
[10:15] ils sont trop gros et lent. Moi, je suis léger comme l'air et rapide comme un
[10:18] léger comme l'air et rapide comme un
[10:18] léger comme l'air et rapide comme un éléphant.
[10:19] éléphant.
[10:19] éléphant. Dites-moi en commentaire votre carte et
[10:20] Dites-moi en commentaire votre carte et votre RAM : je vous dis quel modèle tenter.
[10:21] Dites-moi en commentaire votre carte et
[10:21] Dites-moi en commentaire votre carte et votre RAM, je vous dis quel modèle
[10:23] votre RAM, je vous dis quel modèle
[10:23] votre RAM, je vous dis quel modèle tenter. Si la vidéo vous a plu,
[10:24] Si la vidéo vous a plu : abonnez-vous, un petit like, la petite cloche…
[10:26] tenter. Si la vidéo vous a plu,
[10:26] tenter. Si la vidéo vous a plu, abonnez-vous, un petit like, la petite
[10:28] abonnez-vous, un petit like, la petite
[10:28] abonnez-vous, un petit like, la petite cloche. D'autres techniques secrètes
[10:28] D'autres techniques secrètes arrivent, si vous êtes sages.
[10:30] cloche. D'autres techniques secrètes
[10:30] cloche. D'autres techniques secrètes arrivent si vous êtes sage. À bientôt.
[10:33] À bientôt…
[10:34] arrivent si vous êtes sage. À bientôt.
[10:34] bisous !
[10:34] arrivent si vous êtes sage. À bientôt. Bisous.
