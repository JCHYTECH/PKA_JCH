# Transcript — « Utilise DeepSeek Agent MIEUX que 99 % des Gens (Guide Complet) »

- **Source** : Julien Massey
- **URL** : https://www.youtube.com/watch?v=nHqCp7AQkE0
- **Durée** : 19:57
- **Date** : 2026-11-17
- **Moteur** : sous-titres YouTube
- **Segments** : 1254

---

[00:02] Le géant de l'IA DeepSeek a récemment
[00:02] Le géant de l'IA DeepSeek a récemment sorti son propre Claude Code et je suis
[00:04] sorti son propre Claude Code et je suis
[00:04] sorti son propre Claude Code et je suis intimement convaincu que ça va remettre
[00:06] intimement convaincu que ça va remettre
[00:06] intimement convaincu que ça va remettre en question beaucoup de choses pour
[00:07] en question beaucoup de choses pour
[00:07] en question beaucoup de choses pour Entropic. Il y en a peu qui le
[00:09] Entropic. Il y en a peu qui le
[00:09] Entropic. Il y en a peu qui le connaissent et encore moins qui savent
[00:11] connaissent et encore moins qui savent
[00:11] connaissent et encore moins qui savent réellement bien l'utiliser. C'est
[00:12] réellement bien l'utiliser. C'est
[00:12] réellement bien l'utiliser. C'est exactement pour ça que dans cette vidéo,
[00:14] exactement pour ça que dans cette vidéo,
[00:14] exactement pour ça que dans cette vidéo, je vais te faire un guide complet sur
[00:16] je vais te faire un guide complet sur
[00:16] je vais te faire un guide complet sur l'agent IA de DeepSeek, DeepSeek Harness
[00:19] l'agent IA de DeepSeek, DeepSeek Harness
[00:19] l'agent IA de DeepSeek, DeepSeek Harness avec son super agent. Tu vas donc voir
[00:20] avec son super agent. Tu vas donc voir
[00:20] avec son super agent. Tu vas donc voir comment le configurer efficacement, mais
[00:22] comment le configurer efficacement, mais
[00:22] comment le configurer efficacement, mais également comment importer tes propres
[00:24] également comment importer tes propres
[00:24] également comment importer tes propres skills et je te passerai les miens
[00:25] skills et je te passerai les miens
[00:25] skills et je te passerai les miens également, créer une équipe de
[00:27] également, créer une équipe de
[00:27] également, créer une équipe de sous-agents et surtout déléguer des
[00:29] sous-agents et surtout déléguer des
[00:29] sous-agents et surtout déléguer des tâches à Claude Code avec DeepSeek
[00:31] tâches à Claude Code avec DeepSeek
[00:31] tâches à Claude Code avec DeepSeek Agent. Et à la fin, tu verras même le
[00:33] Agent. Et à la fin, tu verras même le
[00:33] Agent. Et à la fin, tu verras même le super agent de DeepSeek travailler sur
[00:35] super agent de DeepSeek travailler sur
[00:35] super agent de DeepSeek travailler sur un projet GitHub qui construit en toute
[00:38] un projet GitHub qui construit en toute
[00:38] un projet GitHub qui construit en toute autonomie absolument tout ce qu'il faut.
[00:40] autonomie absolument tout ce qu'il faut.
[00:40] autonomie absolument tout ce qu'il faut. Et si je dis DeepSeek Agent, c'est pour
[00:41] Et si je dis DeepSeek Agent, c'est pour
[00:41] Et si je dis DeepSeek Agent, c'est pour simplifier parce qu'en réalité, on est
[00:43] simplifier parce qu'en réalité, on est
[00:43] simplifier parce qu'en réalité, on est plutôt sur DeepSeek Harness. Et Harness,
[00:45] plutôt sur DeepSeek Harness. Et Harness,
[00:45] plutôt sur DeepSeek Harness. Et Harness, voici ce que c'est exactement. C'est un
[00:47] voici ce que c'est exactement. C'est un
[00:47] voici ce que c'est exactement. C'est un modèle plus un Harness qui forme un
[00:49] modèle plus un Harness qui forme un
[00:49] modèle plus un Harness qui forme un agent IA. Les deux combinés, en fait,
[00:51] agent IA. Les deux combinés, en fait,
[00:51] agent IA. Les deux combinés, en fait, vont faire un agent IA grâce au cerveau,
[00:53] vont faire un agent IA grâce au cerveau,
[00:53] vont faire un agent IA grâce au cerveau, donc le modèle de langage et les outils
[00:55] donc le modèle de langage et les outils
[00:55] donc le modèle de langage et les outils exactement comme Claude Code. Sauf que
[00:57] exactement comme Claude Code. Sauf que
[00:57] exactement comme Claude Code. Sauf que le problème, c'est que Claude Code est
[00:59] le problème, c'est que Claude Code est
[00:59] le problème, c'est que Claude Code est fermé. C'est Entropic qui le possède et
[01:01] fermé. C'est Entropic qui le possède et
[01:02] fermé. C'est Entropic qui le possède et à l'inverse, DeepSeek Harness, il est
[01:03] à l'inverse, DeepSeek Harness, il est
[01:03] à l'inverse, DeepSeek Harness, il est complètement ouvert, c'est-à-dire que
[01:04] complètement ouvert, c'est-à-dire que
[01:04] complètement ouvert, c'est-à-dire que c'est un socle qu'on pourra
[01:05] c'est un socle qu'on pourra
[01:05] c'est un socle qu'on pourra personnaliser exactement comme un Lego.
[01:07] personnaliser exactement comme un Lego.
[01:07] personnaliser exactement comme un Lego. Et si on veut, on pourra changer le
[01:08] Et si on veut, on pourra changer le
[01:08] Et si on veut, on pourra changer le modèle de langage comme je vais te
[01:09] modèle de langage comme je vais te
[01:09] modèle de langage comme je vais te montrer dans cette vidéo. Et il faut pas
[01:11] montrer dans cette vidéo. Et il faut pas
[01:11] montrer dans cette vidéo. Et il faut pas confondre Harness et Super Agent.
[01:13] confondre Harness et Super Agent.
[01:13] confondre Harness et Super Agent. L'Harness, c'est tout simplement
[01:15] L'Harness, c'est tout simplement
[01:15] L'Harness, c'est tout simplement l'outil. C'est ce qui va lui permettre
[01:17] l'outil. C'est ce qui va lui permettre
[01:17] l'outil. C'est ce qui va lui permettre de faire des actions. Et le Super Agent,
[01:19] de faire des actions. Et le Super Agent,
[01:19] de faire des actions. Et le Super Agent, c'est un prototype encore en bêta, mais
[01:21] c'est un prototype encore en bêta, mais
[01:21] c'est un prototype encore en bêta, mais qui fonctionne extrêmement bien pour
[01:23] qui fonctionne extrêmement bien pour
[01:23] qui fonctionne extrêmement bien pour faire travailler l'agent IA de DeepSeek
[01:24] faire travailler l'agent IA de DeepSeek
[01:25] faire travailler l'agent IA de DeepSeek directement sur GitHub en toute
[01:27] directement sur GitHub en toute
[01:27] directement sur GitHub en toute autonomie. Maintenant, on va installer
[01:28] autonomie. Maintenant, on va installer
[01:28] autonomie. Maintenant, on va installer DeepSeek Harness. Et pour ça, je vais te
[01:30] DeepSeek Harness. Et pour ça, je vais te
[01:30] DeepSeek Harness. Et pour ça, je vais te filer un prompt que tu vas balancer dans
[01:32] filer un prompt que tu vas balancer dans
[01:33] filer un prompt que tu vas balancer dans Claude Code et tu vas avoir une
[01:34] Claude Code et tu vas avoir une
[01:34] Claude Code et tu vas avoir une installation 100 % sécurisée et rapide.
[01:36] installation 100 % sécurisée et rapide.
[01:37] installation 100 % sécurisée et rapide. Et à la fin, on a une interface qui va
[01:38] Et à la fin, on a une interface qui va
[01:38] Et à la fin, on a une interface qui va s'ouvrir. Pourquoi je fais ça? Pour te
[01:40] s'ouvrir. Pourquoi je fais ça? Pour te
[01:40] s'ouvrir. Pourquoi je fais ça? Pour te simplifier l'installation premièrement
[01:41] simplifier l'installation premièrement
[01:41] simplifier l'installation premièrement et deuxièmement pour que tu puisses te
[01:43] et deuxièmement pour que tu puisses te
[01:43] et deuxièmement pour que tu puisses te baser sur mon process d'installation 100
[01:45] baser sur mon process d'installation 100
[01:45] baser sur mon process d'installation 100 % sécurisé que j'ai fait plusieurs fois
[01:47] % sécurisé que j'ai fait plusieurs fois
[01:47] % sécurisé que j'ai fait plusieurs fois parce qu'attention, on est sur une IA
[01:49] parce qu'attention, on est sur une IA
[01:49] parce qu'attention, on est sur une IA comme Claude Code qui peut agir sur tous
[01:50] comme Claude Code qui peut agir sur tous
[01:51] comme Claude Code qui peut agir sur tous les fichiers. Il faut bien la contrôler
[01:52] les fichiers. Il faut bien la contrôler
[01:52] les fichiers. Il faut bien la contrôler et surtout bien l'installer. Donc faire
[01:54] et surtout bien l'installer. Donc faire
[01:54] et surtout bien l'installer. Donc faire attention. Tout le prompt d'installation
[01:56] attention. Tout le prompt d'installation
[01:56] attention. Tout le prompt d'installation se trouvera en description dans mon
[01:57] se trouvera en description dans mon
[01:57] se trouvera en description dans mon school gratuit, ma communauté gratuite.
[01:59] school gratuit, ma communauté gratuite.
[01:59] school gratuit, ma communauté gratuite. Tu auras juste connecter, puis aller
[02:00] Tu auras juste connecter, puis aller
[02:00] Tu auras juste connecter, puis aller dans Classroom et ensuite dans
[02:02] dans Classroom et ensuite dans
[02:02] dans Classroom et ensuite dans ressources YouTube. Tu trouveras une
[02:03] ressources YouTube. Tu trouveras une
[02:03] ressources YouTube. Tu trouveras une vidéo qui s'intitulera installer
[02:06] vidéo qui s'intitulera installer
[02:06] vidéo qui s'intitulera installer DeepSeek Harness. Pour commencer, tu va
[02:08] DeepSeek Harness. Pour commencer, tu va
[02:08] DeepSeek Harness. Pour commencer, tu va ouvrir Claude. Ensuite, tu vas cliquer
[02:10] ouvrir Claude. Ensuite, tu vas cliquer
[02:10] ouvrir Claude. Ensuite, tu vas cliquer sur Claude Code et là, tu vas créer un
[02:12] sur Claude Code et là, tu vas créer un
[02:12] sur Claude Code et là, tu vas créer un nouveau fichier. Donc on va créer un
[02:14] nouveau fichier. Donc on va créer un
[02:14] nouveau fichier. Donc on va créer un nouveau dossier. Ensuite, tu auras
[02:15] nouveau dossier. Ensuite, tu auras
[02:15] nouveau dossier. Ensuite, tu auras simplement à coller ce grand prompt que
[02:17] simplement à coller ce grand prompt que
[02:17] simplement à coller ce grand prompt que tu trouveras justement dans mon groupe
[02:19] tu trouveras justement dans mon groupe
[02:19] tu trouveras justement dans mon groupe gratuit. Et l'idée en fait, c'est que
[02:21] gratuit. Et l'idée en fait, c'est que
[02:21] gratuit. Et l'idée en fait, c'est que ici Claude Code l'installe à ta place,
[02:23] ici Claude Code l'installe à ta place,
[02:23] ici Claude Code l'installe à ta place, il fasse les commandes qui sont un petit
[02:24] il fasse les commandes qui sont un petit
[02:24] il fasse les commandes qui sont un petit peu chiantes à faire à ta place. Et
[02:26] peu chiantes à faire à ta place. Et
[02:26] peu chiantes à faire à ta place. Et surtout, ça va permettre de l'installer
[02:28] surtout, ça va permettre de l'installer
[02:28] surtout, ça va permettre de l'installer en toute sécurité en faisant attention à
[02:30] en toute sécurité en faisant attention à
[02:30] en toute sécurité en faisant attention à toutes tes données et surtout, eh bien
[02:32] toutes tes données et surtout, eh bien
[02:32] toutes tes données et surtout, eh bien si tu as un problème avec, Claude Code
[02:33] si tu as un problème avec, Claude Code
[02:33] si tu as un problème avec, Claude Code pourra avoir la main dessus et régler
[02:36] pourra avoir la main dessus et régler
[02:36] pourra avoir la main dessus et régler par exemple un potentiel problème si tu
[02:37] par exemple un potentiel problème si tu
[02:37] par exemple un potentiel problème si tu arrives pas à trouver une certaine
[02:38] arrives pas à trouver une certaine
[02:38] arrives pas à trouver une certaine fonctionnalité ou à régler un certain
[02:39] fonctionnalité ou à régler un certain
[02:39] fonctionnalité ou à régler un certain paramètre. Il a été ouvert sur ce port
[02:41] paramètre. Il a été ouvert sur ce port
[02:41] paramètre. Il a été ouvert sur ce port précisément et du coup, j'ai accès à
[02:43] précisément et du coup, j'ai accès à
[02:43] précisément et du coup, j'ai accès à DeepSeek Harness, cet agent IA DeepSeek.
[02:46] DeepSeek Harness, cet agent IA DeepSeek.
[02:46] DeepSeek Harness, cet agent IA DeepSeek. Et exactement comme Claude Code, tu peux
[02:48] Et exactement comme Claude Code, tu peux
[02:48] Et exactement comme Claude Code, tu peux voir qu'il y a des fonctionnalités qui
[02:50] voir qu'il y a des fonctionnalités qui
[02:50] voir qu'il y a des fonctionnalités qui sont très similaires et c'est normal
[02:51] sont très similaires et c'est normal
[02:51] sont très similaires et c'est normal parce qu'on est sur un Harness. Mais
[02:52] parce qu'on est sur un Harness. Mais
[02:52] parce qu'on est sur un Harness. Mais concrètement, là tu as la barre de chat
[02:54] concrètement, là tu as la barre de chat
[02:54] concrètement, là tu as la barre de chat et puis tu peux directement lui parler.
[02:56] et puis tu peux directement lui parler.
[02:56] et puis tu peux directement lui parler. Sauf qu'il faut ajouter une clé API et
[02:58] Sauf qu'il faut ajouter une clé API et
[02:58] Sauf qu'il faut ajouter une clé API et je vais te montrer comment la faire. Tu
[03:00] je vais te montrer comment la faire. Tu
[03:00] je vais te montrer comment la faire. Tu retrouveras sur la gauche bah tous tes
[03:01] retrouveras sur la gauche bah tous tes
[03:01] retrouveras sur la gauche bah tous tes espaces de travail, mais aussi des
[03:03] espaces de travail, mais aussi des
[03:03] espaces de travail, mais aussi des automatisations, des tâches
[03:04] automatisations, des tâches
[03:04] automatisations, des tâches automatisées, le super agent, des
[03:06] automatisées, le super agent, des
[03:06] automatisées, le super agent, des plugins. Et c'est exactement pour ça que
[03:08] plugins. Et c'est exactement pour ça que
[03:08] plugins. Et c'est exactement pour ça que je dis que DeepSeek Agent, c'est un
[03:09] je dis que DeepSeek Agent, c'est un
[03:09] je dis que DeepSeek Agent, c'est un petit peu comme en Lego. On peut ajouter
[03:11] petit peu comme en Lego. On peut ajouter
[03:11] petit peu comme en Lego. On peut ajouter par exemple à des plugins pour aller sur
[03:14] par exemple à des plugins pour aller sur
[03:14] par exemple à des plugins pour aller sur le web ou encore pour faire des loops
[03:16] le web ou encore pour faire des loops
[03:16] le web ou encore pour faire des loops avec l'agent IA, donc des boucles. Et
[03:17] avec l'agent IA, donc des boucles. Et
[03:17] avec l'agent IA, donc des boucles. Et même bien plus si on va voir d'autres
[03:19] même bien plus si on va voir d'autres
[03:19] même bien plus si on va voir d'autres plugins ou créer son propre plugin. La
[03:22] plugins ou créer son propre plugin. La
[03:22] plugins ou créer son propre plugin. La toute première étape, c'est d'aller sur
[03:23] toute première étape, c'est d'aller sur
[03:23] toute première étape, c'est d'aller sur More en bas à gauche, settings et
[03:26] More en bas à gauche, settings et
[03:26] More en bas à gauche, settings et cliquer sur Model. Ici, tu vas
[03:27] cliquer sur Model. Ici, tu vas
[03:27] cliquer sur Model. Ici, tu vas configurer DeepSeek. Il va donc te
[03:29] configurer DeepSeek. Il va donc te
[03:29] configurer DeepSeek. Il va donc te falloir une clé API. Tu vas donc sur
[03:31] falloir une clé API. Tu vas donc sur
[03:31] falloir une clé API. Tu vas donc sur platform.deepseek.com
[03:33] platform.deepseek.com
[03:33] platform.deepseek.com et tu vas cliquer sur clé API, créer ta
[03:35] et tu vas cliquer sur clé API, créer ta
[03:35] et tu vas cliquer sur clé API, créer ta nouvelle clé API, aller dans billing et
[03:37] nouvelle clé API, aller dans billing et
[03:37] nouvelle clé API, aller dans billing et ajouter un moyen de paiement.
[03:38] ajouter un moyen de paiement.
[03:38] ajouter un moyen de paiement. Personnellement, j'ai mis à 5 dollars
[03:40] Personnellement, j'ai mis à 5 dollars
[03:40] Personnellement, j'ai mis à 5 dollars pour faire plusieurs tests et surtout
[03:42] pour faire plusieurs tests et surtout
[03:42] pour faire plusieurs tests et surtout beaucoup de tokens et ça m'a coûté que
[03:45] beaucoup de tokens et ça m'a coûté que
[03:45] beaucoup de tokens et ça m'a coûté que 56 cents, c'est rien du tout. Donc
[03:49] 56 cents, c'est rien du tout. Donc
[03:49] 56 cents, c'est rien du tout. Donc attention, tu vas pas dépenser des
[03:50] attention, tu vas pas dépenser des
[03:50] attention, tu vas pas dépenser des fortunes pour pouvoir utiliser cet agent
[03:52] fortunes pour pouvoir utiliser cet agent
[03:52] fortunes pour pouvoir utiliser cet agent IA. Ensuite, cette clé tu la colles ici
[03:55] IA. Ensuite, cette clé tu la colles ici
[03:55] IA. Ensuite, cette clé tu la colles ici et tu fais apply. Et là, tu vas pouvoir
[03:57] et tu fais apply. Et là, tu vas pouvoir
[03:57] et tu fais apply. Et là, tu vas pouvoir utiliser notamment les modèles de
[03:59] utiliser notamment les modèles de
[03:59] utiliser notamment les modèles de DeepSeek, le DeepSeek V4.1 Flash et V4
[04:03] DeepSeek, le DeepSeek V4.1 Flash et V4
[04:03] DeepSeek, le DeepSeek V4.1 Flash et V4 Pro. Mais bien parce que dans quelques
[04:04] Pro. Mais bien parce que dans quelques
[04:04] Pro. Mais bien parce que dans quelques secondes, je vais te montrer comment
[04:05] secondes, je vais te montrer comment
[04:05] secondes, je vais te montrer comment utiliser un modèle de Claude ou encore
[04:07] utiliser un modèle de Claude ou encore
[04:07] utiliser un modèle de Claude ou encore de Gemini ou même d'OpenAI directement
[04:10] de Gemini ou même d'OpenAI directement
[04:10] de Gemini ou même d'OpenAI directement sur DeepSeek. Et là directement, tu
[04:12] sur DeepSeek. Et là directement, tu
[04:12] sur DeepSeek. Et là directement, tu pourra faire ton premier test de prompt.
[04:14] pourra faire ton premier test de prompt.
[04:14] pourra faire ton premier test de prompt. Là, on va lui demander de créer un
[04:15] Là, on va lui demander de créer un
[04:15] Là, on va lui demander de créer un fichier .txt et de voir en fait s'il est
[04:18] fichier .txt et de voir en fait s'il est
[04:18] fichier .txt et de voir en fait s'il est capable de créer justement un fichier
[04:19] capable de créer justement un fichier
[04:19] capable de créer justement un fichier tout comme Claude Code. Il a bien créé
[04:21] tout comme Claude Code. Il a bien créé
[04:21] tout comme Claude Code. Il a bien créé un fichier hello.txt avec la phrase que
[04:24] un fichier hello.txt avec la phrase que
[04:24] un fichier hello.txt avec la phrase que je lui ai demandé. Bon maintenant, pour
[04:25] je lui ai demandé. Bon maintenant, pour
[04:25] je lui ai demandé. Bon maintenant, pour commencer, on va créer un nouveau
[04:27] commencer, on va créer un nouveau
[04:27] commencer, on va créer un nouveau workspace. On va cliquer ici et faire un
[04:29] workspace. On va cliquer ici et faire un
[04:29] workspace. On va cliquer ici et faire un new folder et par exemple marquer test
[04:31] new folder et par exemple marquer test
[04:31] new folder et par exemple marquer test guide DeepSeek et tu vas créer un
[04:35] guide DeepSeek et tu vas créer un
[04:35] guide DeepSeek et tu vas créer un fichier exactement comme sur Claude Code
[04:36] fichier exactement comme sur Claude Code
[04:36] fichier exactement comme sur Claude Code pour avoir un projet. Maintenant
[04:38] pour avoir un projet. Maintenant
[04:38] pour avoir un projet. Maintenant attention, écoute bien parce qu'il y a
[04:40] attention, écoute bien parce qu'il y a
[04:40] attention, écoute bien parce qu'il y a différents types de permissions parce
[04:41] différents types de permissions parce
[04:41] différents types de permissions parce qu'en fait DeepSeek fonctionne avec
[04:43] qu'en fait DeepSeek fonctionne avec
[04:43] qu'en fait DeepSeek fonctionne avec trois niveaux de permission exactement
[04:45] trois niveaux de permission exactement
[04:45] trois niveaux de permission exactement comme Claude. On a le moins risqué au
[04:47] comme Claude. On a le moins risqué au
[04:47] comme Claude. On a le moins risqué au plus risqué avec le
[04:49] plus risqué avec le
[04:49] plus risqué avec le On va uniquement lire les fichiers ou
[04:51] On va uniquement lire les fichiers ou
[04:51] On va uniquement lire les fichiers ou les prompts qu'on lui envoie. Ensuite,
[04:52] les prompts qu'on lui envoie. Ensuite,
[04:52] les prompts qu'on lui envoie. Ensuite, on a uniquement la possibilité d'écrire
[04:54] on a uniquement la possibilité d'écrire
[04:54] on a uniquement la possibilité d'écrire dans l'espace de travail et avoir un
[04:56] dans l'espace de travail et avoir un
[04:56] dans l'espace de travail et avoir un access complet. C'est évidemment le plus
[04:59] access complet. C'est évidemment le plus
[04:59] access complet. C'est évidemment le plus sensible et pour débuter, je te
[05:00] sensible et pour débuter, je te
[05:00] sensible et pour débuter, je te recommande uniquement dans le workspace
[05:02] recommande uniquement dans le workspace
[05:02] recommande uniquement dans le workspace de lui dire d'écrire. On va donc
[05:04] de lui dire d'écrire. On va donc
[05:04] de lui dire d'écrire. On va donc sélectionner ça ici. Maintenant, pour
[05:06] sélectionner ça ici. Maintenant, pour
[05:06] sélectionner ça ici. Maintenant, pour bien configurer notre projet, on va
[05:08] bien configurer notre projet, on va
[05:08] bien configurer notre projet, on va faire exactement comme sur Claude Code.
[05:10] faire exactement comme sur Claude Code.
[05:10] faire exactement comme sur Claude Code. Où est-ce que sur Claude on a un fichier
[05:12] Où est-ce que sur Claude on a un fichier
[05:12] Où est-ce que sur Claude on a un fichier cloud.md qui vont réduire toutes les
[05:15] cloud.md qui vont réduire toutes les
[05:15] cloud.md qui vont réduire toutes les règles de notre projet. Là, on va
[05:17] règles de notre projet. Là, on va
[05:17] règles de notre projet. Là, on va utiliser un agent.md. C'est exactement
[05:20] utiliser un agent.md. C'est exactement
[05:20] utiliser un agent.md. C'est exactement la même chose. Le agent.md va donc
[05:23] la même chose. Le agent.md va donc
[05:23] la même chose. Le agent.md va donc consister pour DeepSeek à être à une
[05:25] consister pour DeepSeek à être à une
[05:25] consister pour DeepSeek à être à une sorte de mémo, une sorte d'instruction,
[05:27] sorte de mémo, une sorte d'instruction,
[05:27] sorte de mémo, une sorte d'instruction, de règle, de contexte qu'il va lire à
[05:28] de règle, de contexte qu'il va lire à
[05:28] de règle, de contexte qu'il va lire à chaque fois et à chaque nouvelle
[05:30] chaque fois et à chaque nouvelle
[05:30] chaque fois et à chaque nouvelle section, il va pouvoir charger
[05:32] section, il va pouvoir charger
[05:32] section, il va pouvoir charger automatiquement ce fichier exactement
[05:34] automatiquement ce fichier exactement
[05:34] automatiquement ce fichier exactement comme un cloud.md. Pour ça, tu as
[05:36] comme un cloud.md. Pour ça, tu as
[05:36] comme un cloud.md. Pour ça, tu as simplement à lui dire créer un fichier
[05:37] simplement à lui dire créer un fichier
[05:37] simplement à lui dire créer un fichier agent.md avec les règles du projet. Là,
[05:40] agent.md avec les règles du projet. Là,
[05:40] agent.md avec les règles du projet. Là, je l'ai bien contextualisé avec beaucoup
[05:42] je l'ai bien contextualisé avec beaucoup
[05:42] je l'ai bien contextualisé avec beaucoup de texte et il va commencer par créer ce
[05:44] de texte et il va commencer par créer ce
[05:44] de texte et il va commencer par créer ce petit fichier qui va être lu à chaque
[05:46] petit fichier qui va être lu à chaque
[05:46] petit fichier qui va être lu à chaque nouvelle session. On peut le voir
[05:48] nouvelle session. On peut le voir
[05:48] nouvelle session. On peut le voir d'abord réfléchir et ensuite utiliser
[05:51] d'abord réfléchir et ensuite utiliser
[05:51] d'abord réfléchir et ensuite utiliser ses outils, donc son harness pour
[05:53] ses outils, donc son harness pour
[05:53] ses outils, donc son harness pour pouvoir faire toute cette action. Et ça,
[05:55] pouvoir faire toute cette action. Et ça,
[05:55] pouvoir faire toute cette action. Et ça, c'est magnifique. Il m'a donc construit
[05:56] c'est magnifique. Il m'a donc construit
[05:56] c'est magnifique. Il m'a donc construit ce fichier agent.md qu'il va pouvoir
[05:59] ce fichier agent.md qu'il va pouvoir
[05:59] ce fichier agent.md qu'il va pouvoir relire à chaque nouvelle interaction.
[06:01] relire à chaque nouvelle interaction.
[06:01] relire à chaque nouvelle interaction. Bon désormais, passons à l'action. On va
[06:03] Bon désormais, passons à l'action. On va
[06:03] Bon désormais, passons à l'action. On va créer un petit projet avec comme fil
[06:05] créer un petit projet avec comme fil
[06:05] créer un petit projet avec comme fil rouge le fait que je veux créer un SaaS
[06:07] rouge le fait que je veux créer un SaaS
[06:07] rouge le fait que je veux créer un SaaS qui permet de créer des agents IA sur
[06:09] qui permet de créer des agents IA sur
[06:09] qui permet de créer des agents IA sur WhatsApp. L'idée, c'est de pouvoir faire
[06:12] WhatsApp. L'idée, c'est de pouvoir faire
[06:12] WhatsApp. L'idée, c'est de pouvoir faire une V1 fictive et un simulateur complet.
[06:15] une V1 fictive et un simulateur complet.
[06:15] une V1 fictive et un simulateur complet. Tout ça avec les fonctionnalités de la
[06:16] Tout ça avec les fonctionnalités de la
[06:16] Tout ça avec les fonctionnalités de la V1 qui seront le choix du modèle
[06:18] V1 qui seront le choix du modèle
[06:18] V1 qui seront le choix du modèle possible, les instructions de l'agent,
[06:19] possible, les instructions de l'agent,
[06:19] possible, les instructions de l'agent, les skills, la base de données et les
[06:21] les skills, la base de données et les
[06:21] les skills, la base de données et les aperçus de conversation fictives. On va
[06:23] aperçus de conversation fictives. On va
[06:23] aperçus de conversation fictives. On va donc lui coller ce prompt et lui
[06:24] donc lui coller ce prompt et lui
[06:24] donc lui coller ce prompt et lui envoyer. Et là, attention, avec ce que
[06:26] envoyer. Et là, attention, avec ce que
[06:26] envoyer. Et là, attention, avec ce que je lui ai envoyé, il va avoir un petit
[06:28] je lui ai envoyé, il va avoir un petit
[06:28] je lui ai envoyé, il va avoir un petit peu de boulot. Avant de faire quoi que
[06:29] peu de boulot. Avant de faire quoi que
[06:29] peu de boulot. Avant de faire quoi que ce soit, il va faire une analyse poussée
[06:31] ce soit, il va faire une analyse poussée
[06:31] ce soit, il va faire une analyse poussée et surtout une réflexion. Il va
[06:32] et surtout une réflexion. Il va
[06:32] et surtout une réflexion. Il va réfléchir à haute voix avant de poser
[06:34] réfléchir à haute voix avant de poser
[06:34] réfléchir à haute voix avant de poser n'importe quelle brique sur mon projet.
[06:36] n'importe quelle brique sur mon projet.
[06:36] n'importe quelle brique sur mon projet. Ça nous permet d'être complètement
[06:37] Ça nous permet d'être complètement
[06:37] Ça nous permet d'être complètement cohérent avec le prompt que j'ai envoyé.
[06:39] cohérent avec le prompt que j'ai envoyé.
[06:39] cohérent avec le prompt que j'ai envoyé. Et ensuite, il est parti pour faire tout
[06:41] Et ensuite, il est parti pour faire tout
[06:41] Et ensuite, il est parti pour faire tout un tas de commandes pour vérifier
[06:42] un tas de commandes pour vérifier
[06:42] un tas de commandes pour vérifier d'abord si j'ai Node. DeepSeek va sans
[06:44] d'abord si j'ai Node. DeepSeek va sans
[06:44] d'abord si j'ai Node. DeepSeek va sans doute te demander si tu valides ou pas
[06:47] doute te demander si tu valides ou pas
[06:47] doute te demander si tu valides ou pas l'action qu'il te propose. Là, il est en
[06:48] l'action qu'il te propose. Là, il est en
[06:48] l'action qu'il te propose. Là, il est en train concrètement de me faire un plan.
[06:50] train concrètement de me faire un plan.
[06:50] train concrètement de me faire un plan. Donc je lis ce qu'il me propose, le plan
[06:52] Donc je lis ce qu'il me propose, le plan
[06:52] Donc je lis ce qu'il me propose, le plan en cinq étapes, et ensuite, et bien je
[06:55] en cinq étapes, et ensuite, et bien je
[06:55] en cinq étapes, et ensuite, et bien je peux soit cocher une case qu'il me
[06:57] peux soit cocher une case qu'il me
[06:57] peux soit cocher une case qu'il me prédéfinit ou soit lui dire bah
[06:58] prédéfinit ou soit lui dire bah
[06:58] prédéfinit ou soit lui dire bah concrètement non, fais plutôt cette
[07:00] concrètement non, fais plutôt cette
[07:00] concrètement non, fais plutôt cette troisième option qui consiste à et là on
[07:02] troisième option qui consiste à et là on
[07:02] troisième option qui consiste à et là on écrit. Donc je vais lui dire que je
[07:03] écrit. Donc je vais lui dire que je
[07:03] écrit. Donc je vais lui dire que je valide complètement ce qu'il me met. Et
[07:05] valide complètement ce qu'il me met. Et
[07:05] valide complètement ce qu'il me met. Et là, on a bien utilisé le modèle DeepSeek
[07:08] là, on a bien utilisé le modèle DeepSeek
[07:08] là, on a bien utilisé le modèle DeepSeek V4.1 Flash en effort high. On a aussi le
[07:11] V4.1 Flash en effort high. On a aussi le
[07:11] V4.1 Flash en effort high. On a aussi le niveau max. On peut aussi aller sur
[07:14] niveau max. On peut aussi aller sur
[07:14] niveau max. On peut aussi aller sur DeepSeek V4 Pro qui lui sera plus poussé
[07:17] DeepSeek V4 Pro qui lui sera plus poussé
[07:17] DeepSeek V4 Pro qui lui sera plus poussé pour faire du code et tu pourras suivre
[07:19] pour faire du code et tu pourras suivre
[07:19] pour faire du code et tu pourras suivre le contexte en temps réel grâce à ce
[07:22] le contexte en temps réel grâce à ce
[07:22] le contexte en temps réel grâce à ce petit icône juste ici. Pour l'instant,
[07:23] petit icône juste ici. Pour l'instant,
[07:23] petit icône juste ici. Pour l'instant, on est à 2 %. On a l'utilisation de
[07:26] on est à 2 %. On a l'utilisation de
[07:26] on est à 2 %. On a l'utilisation de tokens complets juste ici, la vitesse de
[07:28] tokens complets juste ici, la vitesse de
[07:28] tokens complets juste ici, la vitesse de tokens par seconde, donc c'est assez
[07:30] tokens par seconde, donc c'est assez
[07:30] tokens par seconde, donc c'est assez précis quand même. Sur la droite, tu
[07:31] précis quand même. Sur la droite, tu
[07:31] précis quand même. Sur la droite, tu auras aussi accès à certains outils. Par
[07:33] auras aussi accès à certains outils. Par
[07:33] auras aussi accès à certains outils. Par exemple, si tu veux lui faire ouvrir des
[07:35] exemple, si tu veux lui faire ouvrir des
[07:35] exemple, si tu veux lui faire ouvrir des pages internet, et bien tu as la
[07:37] pages internet, et bien tu as la
[07:37] pages internet, et bien tu as la possibilité d'avoir les tools juste ici.
[07:39] possibilité d'avoir les tools juste ici.
[07:39] possibilité d'avoir les tools juste ici. Et c'est exactement ça qu'on appelle en
[07:41] Et c'est exactement ça qu'on appelle en
[07:41] Et c'est exactement ça qu'on appelle en fait le harness. Tout comme dans Claude
[07:43] fait le harness. Tout comme dans Claude
[07:43] fait le harness. Tout comme dans Claude Code ou encore dans Codex, il va se
[07:45] Code ou encore dans Codex, il va se
[07:45] Code ou encore dans Codex, il va se créer sa to-do list. Donc on a toutes
[07:47] créer sa to-do list. Donc on a toutes
[07:47] créer sa to-do list. Donc on a toutes les fonctionnalités des plus grandes IA
[07:49] les fonctionnalités des plus grandes IA
[07:49] les fonctionnalités des plus grandes IA du marché aujourd'hui. Voici donc
[07:51] du marché aujourd'hui. Voici donc
[07:51] du marché aujourd'hui. Voici donc l'application qu'a pu me créer
[07:53] l'application qu'a pu me créer
[07:53] l'application qu'a pu me créer directement DeepSeek que j'avais en tête
[07:55] directement DeepSeek que j'avais en tête
[07:55] directement DeepSeek que j'avais en tête pour créer des agents IA sur WhatsApp.
[07:57] pour créer des agents IA sur WhatsApp.
[07:57] pour créer des agents IA sur WhatsApp. Donc là, on peut imaginer lancer un
[07:58] Donc là, on peut imaginer lancer un
[07:58] Donc là, on peut imaginer lancer un nouvel agent IA, modifier le message
[08:01] nouvel agent IA, modifier le message
[08:01] nouvel agent IA, modifier le message d'accueil, modifier également les
[08:03] d'accueil, modifier également les
[08:03] d'accueil, modifier également les instructions de cet agent IA et
[08:05] instructions de cet agent IA et
[08:05] instructions de cet agent IA et également les différents modèles. Pour
[08:07] également les différents modèles. Pour
[08:07] également les différents modèles. Pour l'instant, on en a que de DeepSeek, mais
[08:09] l'instant, on en a que de DeepSeek, mais
[08:09] l'instant, on en a que de DeepSeek, mais attention, hein, on est quand même sur
[08:10] attention, hein, on est quand même sur
[08:10] attention, hein, on est quand même sur quelque chose d'assez sympa en termes de
[08:12] quelque chose d'assez sympa en termes de
[08:12] quelque chose d'assez sympa en termes de design. C'est exactement ce que j'avais
[08:13] design. C'est exactement ce que j'avais
[08:13] design. C'est exactement ce que j'avais en tête et surtout d'aperçu. Donc là, je
[08:16] en tête et surtout d'aperçu. Donc là, je
[08:16] en tête et surtout d'aperçu. Donc là, je peux lui dire hello et il va me
[08:17] peux lui dire hello et il va me
[08:17] peux lui dire hello et il va me répondre. Donc ça, c'est assez génial.
[08:19] répondre. Donc ça, c'est assez génial.
[08:19] répondre. Donc ça, c'est assez génial. Si je lui dis tu peux parler français,
[08:21] Si je lui dis tu peux parler français,
[08:21] Si je lui dis tu peux parler français, OK, il peut parler français et on peut
[08:23] OK, il peut parler français et on peut
[08:23] OK, il peut parler français et on peut avoir ses connaissances où est-ce qu'on
[08:24] avoir ses connaissances où est-ce qu'on
[08:24] avoir ses connaissances où est-ce qu'on va upload des fichiers dedans. Une belle
[08:26] va upload des fichiers dedans. Une belle
[08:26] va upload des fichiers dedans. Une belle petite interface qui est fonctionnelle
[08:28] petite interface qui est fonctionnelle
[08:28] petite interface qui est fonctionnelle et qui a coûté, attention, à tout casser
[08:30] et qui a coûté, attention, à tout casser
[08:30] et qui a coûté, attention, à tout casser 40 centimes seulement. Et reste bien
[08:32] 40 centimes seulement. Et reste bien
[08:32] 40 centimes seulement. Et reste bien jusqu'à la fin parce que après je vais
[08:33] jusqu'à la fin parce que après je vais
[08:33] jusqu'à la fin parce que après je vais te montrer comment le super agent il y a
[08:35] te montrer comment le super agent il y a
[08:35] te montrer comment le super agent il y a DeepSeek, une nouvelle fonctionnalité,
[08:37] DeepSeek, une nouvelle fonctionnalité,
[08:37] DeepSeek, une nouvelle fonctionnalité, peut améliorer ton application en temps
[08:39] peut améliorer ton application en temps
[08:39] peut améliorer ton application en temps réel et en toute autonomie. Bon,
[08:41] réel et en toute autonomie. Bon,
[08:41] réel et en toute autonomie. Bon, désormais, maintenant qu'on a fait le
[08:42] désormais, maintenant qu'on a fait le
[08:42] désormais, maintenant qu'on a fait le premier projet, si jamais tu fais slash
[08:44] premier projet, si jamais tu fais slash
[08:44] premier projet, si jamais tu fais slash sur la barrière d'espace de DeepSeek
[08:46] sur la barrière d'espace de DeepSeek
[08:46] sur la barrière d'espace de DeepSeek Harness, tu peux voir qu'on a
[08:47] Harness, tu peux voir qu'on a
[08:47] Harness, tu peux voir qu'on a différentes choses. On peut lui joindre
[08:48] différentes choses. On peut lui joindre
[08:48] différentes choses. On peut lui joindre des fichiers, lui définir un goal, donc
[08:51] des fichiers, lui définir un goal, donc
[08:51] des fichiers, lui définir un goal, donc un objectif, lui faire un plan, un
[08:53] un objectif, lui faire un plan, un
[08:53] un objectif, lui faire un plan, un feedback, compacter une session et
[08:56] feedback, compacter une session et
[08:56] feedback, compacter une session et changer la permission, le modèle ou
[08:57] changer la permission, le modèle ou
[08:57] changer la permission, le modèle ou exporter tout ça. Donc si je fais slash
[08:59] exporter tout ça. Donc si je fais slash
[08:59] exporter tout ça. Donc si je fais slash goal et là je peux lui décrire
[09:00] goal et là je peux lui décrire
[09:00] goal et là je peux lui décrire concrètement l'objectif de cette
[09:02] concrètement l'objectif de cette
[09:02] concrètement l'objectif de cette session, faire un site web 3D par
[09:04] session, faire un site web 3D par
[09:04] session, faire un site web 3D par exemple, ce qu'on va faire dans quelques
[09:05] exemple, ce qu'on va faire dans quelques
[09:05] exemple, ce qu'on va faire dans quelques secondes, fonctionnel. Mais tu as aussi
[09:07] secondes, fonctionnel. Mais tu as aussi
[09:07] secondes, fonctionnel. Mais tu as aussi si tu fais slash et que tu regardes bien
[09:08] si tu fais slash et que tu regardes bien
[09:08] si tu fais slash et que tu regardes bien et que tu descends un petit peu, la
[09:10] et que tu descends un petit peu, la
[09:10] et que tu descends un petit peu, la possibilité d'avoir des skills. Et là,
[09:11] possibilité d'avoir des skills. Et là,
[09:11] possibilité d'avoir des skills. Et là, ce sont tous mes skills que j'ai pris de
[09:13] ce sont tous mes skills que j'ai pris de
[09:13] ce sont tous mes skills que j'ai pris de Cloud pour les mettre directement dans
[09:15] Cloud pour les mettre directement dans
[09:15] Cloud pour les mettre directement dans DeepSeek. Le gros avantage, c'est que
[09:17] DeepSeek. Le gros avantage, c'est que
[09:17] DeepSeek. Le gros avantage, c'est que toutes les IA du marché se sont adaptées
[09:19] toutes les IA du marché se sont adaptées
[09:19] toutes les IA du marché se sont adaptées au skill de Cloud. Et donc si tu as des
[09:21] au skill de Cloud. Et donc si tu as des
[09:21] au skill de Cloud. Et donc si tu as des skills sur Cloud, tu peux juste les
[09:23] skills sur Cloud, tu peux juste les
[09:23] skills sur Cloud, tu peux juste les prendre et les glisser dans Harness
[09:25] prendre et les glisser dans Harness
[09:25] prendre et les glisser dans Harness ultra simplement pour avoir la même
[09:27] ultra simplement pour avoir la même
[09:27] ultra simplement pour avoir la même chose et tu n'as pas besoin de les
[09:29] chose et tu n'as pas besoin de les
[09:29] chose et tu n'as pas besoin de les réécrire. Et en bonus, tu auras accès à
[09:31] réécrire. Et en bonus, tu auras accès à
[09:31] réécrire. Et en bonus, tu auras accès à mes 10 meilleurs skills que j'utilise
[09:33] mes 10 meilleurs skills que j'utilise
[09:33] mes 10 meilleurs skills que j'utilise tous les jours pour pouvoir travailler.
[09:35] tous les jours pour pouvoir travailler.
[09:35] tous les jours pour pouvoir travailler. Donc des skills qui vont de la création
[09:36] Donc des skills qui vont de la création
[09:36] Donc des skills qui vont de la création de site web 3D jusqu'à l'analyse poussée
[09:39] de site web 3D jusqu'à l'analyse poussée
[09:39] de site web 3D jusqu'à l'analyse poussée de script pour YouTube, tout se trouvera
[09:41] de script pour YouTube, tout se trouvera
[09:41] de script pour YouTube, tout se trouvera directement dans mon groupe school
[09:42] directement dans mon groupe school
[09:42] directement dans mon groupe school gratuit en description. La manière la
[09:44] gratuit en description. La manière la
[09:44] gratuit en description. La manière la plus simple d'installer des skills comme
[09:45] plus simple d'installer des skills comme
[09:45] plus simple d'installer des skills comme par exemple les 10 skills que je t'offre
[09:47] par exemple les 10 skills que je t'offre
[09:47] par exemple les 10 skills que je t'offre dans cette vidéo, c'est de télécharger
[09:49] dans cette vidéo, c'est de télécharger
[09:49] dans cette vidéo, c'est de télécharger le dossier et juste de l'envoyer à
[09:51] le dossier et juste de l'envoyer à
[09:51] le dossier et juste de l'envoyer à DeepSeek en lui disant install tous ces
[09:54] DeepSeek en lui disant install tous ces
[09:54] DeepSeek en lui disant install tous ces skills et il va faire tout le boulot à
[09:56] skills et il va faire tout le boulot à
[09:56] skills et il va faire tout le boulot à ta place. Le gros avantage de DeepSeek
[09:58] ta place. Le gros avantage de DeepSeek
[09:58] ta place. Le gros avantage de DeepSeek Harness, c'est qu'il est libre, que le
[10:00] Harness, c'est qu'il est libre, que le
[10:00] Harness, c'est qu'il est libre, que le socle on peut le modifier exactement
[10:01] socle on peut le modifier exactement
[10:01] socle on peut le modifier exactement comme on veut. Donc toutes les personnes
[10:03] comme on veut. Donc toutes les personnes
[10:03] comme on veut. Donc toutes les personnes qui sont pas à l'aise avec le fait
[10:04] qui sont pas à l'aise avec le fait
[10:04] qui sont pas à l'aise avec le fait d'utiliser des IA chinoises pourront
[10:05] d'utiliser des IA chinoises pourront
[10:05] d'utiliser des IA chinoises pourront utiliser n'importe quelle IA du marché,
[10:08] utiliser n'importe quelle IA du marché,
[10:08] utiliser n'importe quelle IA du marché, que ce soit des modèles d'Anthropic,
[10:10] que ce soit des modèles d'Anthropic,
[10:10] que ce soit des modèles d'Anthropic, d'OpenAI ou de Gemini, et tout ça grâce
[10:12] d'OpenAI ou de Gemini, et tout ça grâce
[10:12] d'OpenAI ou de Gemini, et tout ça grâce à une seule chose, un hub qui fait la
[10:15] à une seule chose, un hub qui fait la
[10:15] à une seule chose, un hub qui fait la passerelle entre tout. Imagine Harness
[10:17] passerelle entre tout. Imagine Harness
[10:17] passerelle entre tout. Imagine Harness avec ce hub de LLM qui s'appelle
[10:19] avec ce hub de LLM qui s'appelle
[10:19] avec ce hub de LLM qui s'appelle OpenRouter que je vais te montrer
[10:20] OpenRouter que je vais te montrer
[10:20] OpenRouter que je vais te montrer comment utiliser dans quelques secondes.
[10:22] comment utiliser dans quelques secondes.
[10:22] comment utiliser dans quelques secondes. C'est ce qu'on utilise nous avec notre
[10:23] C'est ce qu'on utilise nous avec notre
[10:23] C'est ce qu'on utilise nous avec notre agence IA qui nous permet de switcher
[10:25] agence IA qui nous permet de switcher
[10:25] agence IA qui nous permet de switcher rapidement de modèle sur nimporte quelle
[10:27] rapidement de modèle sur nimporte quelle
[10:27] rapidement de modèle sur nimporte quelle infrastructure quand on en construit une
[10:29] infrastructure quand on en construit une
[10:29] infrastructure quand on en construit une pour un client. D'ailleurs, si tu as
[10:30] pour un client. D'ailleurs, si tu as
[10:30] pour un client. D'ailleurs, si tu as besoin d'IA dans ton entreprise, réserve
[10:32] besoin d'IA dans ton entreprise, réserve
[10:32] besoin d'IA dans ton entreprise, réserve un appel avec moi-même en personne, on
[10:34] un appel avec moi-même en personne, on
[10:34] un appel avec moi-même en personne, on pourra voir ce qu'on peut mettre en
[10:35] pourra voir ce qu'on peut mettre en
[10:35] pourra voir ce qu'on peut mettre en place pour toi et comment t'accompagner
[10:37] place pour toi et comment t'accompagner
[10:37] place pour toi et comment t'accompagner pendant 3 à 6 mois pour changer ta boîte
[10:39] pendant 3 à 6 mois pour changer ta boîte
[10:39] pendant 3 à 6 mois pour changer ta boîte avec l'IA. On fait une connexion entre
[10:40] avec l'IA. On fait une connexion entre
[10:40] avec l'IA. On fait une connexion entre le Harness et OpenRouter et OpenRouter a
[10:43] le Harness et OpenRouter et OpenRouter a
[10:43] le Harness et OpenRouter et OpenRouter a accès à énormément de modèles de
[10:46] accès à énormément de modèles de
[10:46] accès à énormément de modèles de langage, que ce soit du Anthropic, du
[10:47] langage, que ce soit du Anthropic, du
[10:47] langage, que ce soit du Anthropic, du OpenAI ou encore du Gemini, on va
[10:49] OpenAI ou encore du Gemini, on va
[10:49] OpenAI ou encore du Gemini, on va pouvoir tout changer en un seul clic.
[10:51] pouvoir tout changer en un seul clic.
[10:51] pouvoir tout changer en un seul clic. Pour ça, tu te rends sur openrouter.ai
[10:53] Pour ça, tu te rends sur openrouter.ai
[10:53] Pour ça, tu te rends sur openrouter.ai et ensuite tu vas directement aller dans
[10:56] et ensuite tu vas directement aller dans
[10:56] et ensuite tu vas directement aller dans ton dashboard, cliquer sur Key et
[10:59] ton dashboard, cliquer sur Key et
[10:59] ton dashboard, cliquer sur Key et pouvoir ajouter une nouvelle clé. Tu
[11:01] pouvoir ajouter une nouvelle clé. Tu
[11:01] pouvoir ajouter une nouvelle clé. Tu peux sélectionner une date d'expiration
[11:02] peux sélectionner une date d'expiration
[11:02] peux sélectionner une date d'expiration pour ne pas avoir de problème, par
[11:03] pour ne pas avoir de problème, par
[11:03] pour ne pas avoir de problème, par exemple 30 jours, et mettre une limite
[11:05] exemple 30 jours, et mettre une limite
[11:05] exemple 30 jours, et mettre une limite d'utilisation de crédit. Cette clé, tu
[11:07] d'utilisation de crédit. Cette clé, tu
[11:07] d'utilisation de crédit. Cette clé, tu la copies et tu vas aller sur DeepSeek
[11:09] la copies et tu vas aller sur DeepSeek
[11:09] la copies et tu vas aller sur DeepSeek dans Settings, Model et là tu ajoutes un
[11:12] dans Settings, Model et là tu ajoutes un
[11:12] dans Settings, Model et là tu ajoutes un nouveau provider et tu sélectionnes bien
[11:14] nouveau provider et tu sélectionnes bien
[11:14] nouveau provider et tu sélectionnes bien OpenRouter et tu colles ta clé API. Et
[11:17] OpenRouter et tu colles ta clé API. Et
[11:17] OpenRouter et tu colles ta clé API. Et désormais, quand tu vas dans les
[11:18] désormais, quand tu vas dans les
[11:18] désormais, quand tu vas dans les modèles, tu as accès à tous les modèles
[11:20] modèles, tu as accès à tous les modèles
[11:20] modèles, tu as accès à tous les modèles de langage que tu veux et tu en a même
[11:22] de langage que tu veux et tu en a même
[11:22] de langage que tu veux et tu en a même des gratuits. Si tu marques Free, tu
[11:24] des gratuits. Si tu marques Free, tu
[11:24] des gratuits. Si tu marques Free, tu auras ceux qui sont gratuits en ce
[11:26] auras ceux qui sont gratuits en ce
[11:26] auras ceux qui sont gratuits en ce moment. Par exemple, Gemma 4 avec
[11:28] moment. Par exemple, Gemma 4 avec
[11:28] moment. Par exemple, Gemma 4 avec certaines limites, mais gratuits. Donc
[11:30] certaines limites, mais gratuits. Donc
[11:30] certaines limites, mais gratuits. Donc tu peux utiliser le Harness qui est
[11:31] tu peux utiliser le Harness qui est
[11:31] tu peux utiliser le Harness qui est gratuit et les modèles de OpenRouter
[11:34] gratuit et les modèles de OpenRouter
[11:34] gratuit et les modèles de OpenRouter avec une certaine limite, mais qui sont
[11:35] avec une certaine limite, mais qui sont
[11:35] avec une certaine limite, mais qui sont gratuits. Pour ce prochain test, on va
[11:37] gratuits. Pour ce prochain test, on va
[11:37] gratuits. Pour ce prochain test, on va partir de cette vidéo que j'ai
[11:38] partir de cette vidéo que j'ai
[11:38] partir de cette vidéo que j'ai complètement générée avec l'intelligence
[11:40] complètement générée avec l'intelligence
[11:40] complètement générée avec l'intelligence artificielle. L'idée, ça va être de
[11:41] artificielle. L'idée, ça va être de
[11:41] artificielle. L'idée, ça va être de demander à DeepSeek et plus précisément
[11:43] demander à DeepSeek et plus précisément
[11:43] demander à DeepSeek et plus précisément un modèle autre que DeepSeek pour faire
[11:46] un modèle autre que DeepSeek pour faire
[11:46] un modèle autre que DeepSeek pour faire un site en entier avec le Harness de
[11:48] un site en entier avec le Harness de
[11:48] un site en entier avec le Harness de DeepSeek. Donc grâce à OpenRouter, cette
[11:50] DeepSeek. Donc grâce à OpenRouter, cette
[11:50] DeepSeek. Donc grâce à OpenRouter, cette vidéo et un Skills et un autre modèle
[11:52] vidéo et un Skills et un autre modèle
[11:52] vidéo et un Skills et un autre modèle langage, on va créer un site web
[11:54] langage, on va créer un site web
[11:54] langage, on va créer un site web immersif pour une agence immobilière à
[11:56] immersif pour une agence immobilière à
[11:56] immersif pour une agence immobilière à Dubaï. Pour ça, je vais d'abord choisir
[11:58] Dubaï. Pour ça, je vais d'abord choisir
[11:58] Dubaï. Pour ça, je vais d'abord choisir le modèle de langage et grâce à
[11:59] le modèle de langage et grâce à
[11:59] le modèle de langage et grâce à OpenRouter, je peux par exemple choisir
[12:01] OpenRouter, je peux par exemple choisir
[12:01] OpenRouter, je peux par exemple choisir un modèle avec OpenAI et GPT-6 Astra,
[12:05] un modèle avec OpenAI et GPT-6 Astra,
[12:05] un modèle avec OpenAI et GPT-6 Astra, par exemple. Je lui envoie le prompt
[12:06] par exemple. Je lui envoie le prompt
[12:06] par exemple. Je lui envoie le prompt ainsi que la vidéo et il est déjà parti
[12:08] ainsi que la vidéo et il est déjà parti
[12:08] ainsi que la vidéo et il est déjà parti pour voir ses différents Skills. On est
[12:10] pour voir ses différents Skills. On est
[12:10] pour voir ses différents Skills. On est et sur GPT-6 Astra qui va utiliser le
[12:14] et sur GPT-6 Astra qui va utiliser le
[12:14] et sur GPT-6 Astra qui va utiliser le harness de DeepSeek pour fonctionner. Il
[12:16] harness de DeepSeek pour fonctionner. Il
[12:16] harness de DeepSeek pour fonctionner. Il va se créer des goals et fonctionner
[12:17] va se créer des goals et fonctionner
[12:17] va se créer des goals et fonctionner exactement de la même façon que
[12:19] exactement de la même façon que
[12:19] exactement de la même façon que DeepSeek. Et regardons désormais le
[12:22] DeepSeek. Et regardons désormais le
[12:22] DeepSeek. Et regardons désormais le résultat de GPT-6 Astra. Regardez ce
[12:26] résultat de GPT-6 Astra. Regardez ce
[12:26] résultat de GPT-6 Astra. Regardez ce scroll animé. Donc ce que j'aime
[12:27] scroll animé. Donc ce que j'aime
[12:27] scroll animé. Donc ce que j'aime par-dessus tout, alors oui, niveau SEO,
[12:30] par-dessus tout, alors oui, niveau SEO,
[12:30] par-dessus tout, alors oui, niveau SEO, c'est pas optimisé, mais c'est beau à
[12:32] c'est pas optimisé, mais c'est beau à
[12:32] c'est pas optimisé, mais c'est beau à voir. Donc c'est une démo qui est
[12:33] voir. Donc c'est une démo qui est
[12:33] voir. Donc c'est une démo qui est palpable. Regardez ce scroll animé.
[12:35] palpable. Regardez ce scroll animé.
[12:35] palpable. Regardez ce scroll animé. Selon comment je scroll, on a tout
[12:37] Selon comment je scroll, on a tout
[12:37] Selon comment je scroll, on a tout simplement le défilé de la vidéo qui se
[12:40] simplement le défilé de la vidéo qui se
[12:40] simplement le défilé de la vidéo qui se fait notamment grâce à un skill, mais
[12:42] fait notamment grâce à un skill, mais
[12:42] fait notamment grâce à un skill, mais ensuite il faut tout coder. On a le nom
[12:44] ensuite il faut tout coder. On a le nom
[12:44] ensuite il faut tout coder. On a le nom du projet qui est ici, Sera Residence à
[12:47] du projet qui est ici, Sera Residence à
[12:47] du projet qui est ici, Sera Residence à Dubaï. Et ensuite on a demandé une
[12:49] Dubaï. Et ensuite on a demandé une
[12:49] Dubaï. Et ensuite on a demandé une brochure. Et surtout ce que j'aime
[12:50] brochure. Et surtout ce que j'aime
[12:50] brochure. Et surtout ce que j'aime par-dessus tout, c'est la barre de
[12:52] par-dessus tout, c'est la barre de
[12:52] par-dessus tout, c'est la barre de progression en bas et également les
[12:54] progression en bas et également les
[12:54] progression en bas et également les images qui ont été découpées avec les
[12:57] images qui ont été découpées avec les
[12:57] images qui ont été découpées avec les duplex, les appartements, le penthouse.
[12:59] duplex, les appartements, le penthouse.
[12:59] duplex, les appartements, le penthouse. Bref, c'est vraiment génial. Et à partir
[13:01] Bref, c'est vraiment génial. Et à partir
[13:01] Bref, c'est vraiment génial. Et à partir de la vidéo, il a fait les cuts qu'il
[13:03] de la vidéo, il a fait les cuts qu'il
[13:03] de la vidéo, il a fait les cuts qu'il faut. Il a tout fait super bien. C'est
[13:05] faut. Il a tout fait super bien. C'est
[13:05] faut. Il a tout fait super bien. C'est magnifique. On a même une petite carte
[13:07] magnifique. On a même une petite carte
[13:07] magnifique. On a même une petite carte avec les arguments avec les différents
[13:10] avec les arguments avec les différents
[13:10] avec les arguments avec les différents quartiers qui sont apportés demain. Bon,
[13:13] quartiers qui sont apportés demain. Bon,
[13:13] quartiers qui sont apportés demain. Bon, c'est vraiment génial. C'est
[13:14] c'est vraiment génial. C'est
[13:14] c'est vraiment génial. C'est complètement fictif, mais c'est dans le
[13:15] complètement fictif, mais c'est dans le
[13:15] complètement fictif, mais c'est dans le style que j'attendais, quelque chose de
[13:17] style que j'attendais, quelque chose de
[13:17] style que j'attendais, quelque chose de luxueux. Donc c'est un 10 sur 10. Et
[13:19] luxueux. Donc c'est un 10 sur 10. Et
[13:19] luxueux. Donc c'est un 10 sur 10. Et tout ça, on l'a fait avec un harness qui
[13:20] tout ça, on l'a fait avec un harness qui
[13:20] tout ça, on l'a fait avec un harness qui est gratuit. Les modèles sont payants,
[13:22] est gratuit. Les modèles sont payants,
[13:22] est gratuit. Les modèles sont payants, mais le harness est gratuit. Et si on
[13:24] mais le harness est gratuit. Et si on
[13:24] mais le harness est gratuit. Et si on veut, on pouvait switcher sur des
[13:25] veut, on pouvait switcher sur des
[13:25] veut, on pouvait switcher sur des modèles qui sont gratuits. Jusqu'à
[13:26] modèles qui sont gratuits. Jusqu'à
[13:26] modèles qui sont gratuits. Jusqu'à maintenant, on avait un seul agent IA,
[13:28] maintenant, on avait un seul agent IA,
[13:28] maintenant, on avait un seul agent IA, mais dès maintenant, on va créer une
[13:30] mais dès maintenant, on va créer une
[13:30] mais dès maintenant, on va créer une équipe de sous-agents. Harness va être
[13:32] équipe de sous-agents. Harness va être
[13:32] équipe de sous-agents. Harness va être le chef d'orchestre et il va pouvoir
[13:34] le chef d'orchestre et il va pouvoir
[13:34] le chef d'orchestre et il va pouvoir déléguer des tâches à trois agents IA
[13:37] déléguer des tâches à trois agents IA
[13:37] déléguer des tâches à trois agents IA différents pour par exemple le design,
[13:39] différents pour par exemple le design,
[13:39] différents pour par exemple le design, le backend et les tests qui vont se
[13:41] le backend et les tests qui vont se
[13:41] le backend et les tests qui vont se faire simultanément pour gagner du
[13:43] faire simultanément pour gagner du
[13:43] faire simultanément pour gagner du temps, gagner en précision et en qualité
[13:45] temps, gagner en précision et en qualité
[13:45] temps, gagner en précision et en qualité de résultat. Si je envoie ce prompt, il
[13:46] de résultat. Si je envoie ce prompt, il
[13:46] de résultat. Si je envoie ce prompt, il y a trois sous-agents qui vont
[13:47] y a trois sous-agents qui vont
[13:47] y a trois sous-agents qui vont travailler sur un seul et même quiz en
[13:49] travailler sur un seul et même quiz en
[13:49] travailler sur un seul et même quiz en même temps. Un qui va faire le design,
[13:51] même temps. Un qui va faire le design,
[13:51] même temps. Un qui va faire le design, l'autre qui va faire les questions et
[13:52] l'autre qui va faire les questions et
[13:52] l'autre qui va faire les questions et l'autre qui va le tester. Et en
[13:54] l'autre qui va le tester. Et en
[13:54] l'autre qui va le tester. Et en simplement lui disant de lancer trois
[13:56] simplement lui disant de lancer trois
[13:56] simplement lui disant de lancer trois sous-agents, il va comprendre et il va
[13:58] sous-agents, il va comprendre et il va
[13:58] sous-agents, il va comprendre et il va le faire. Il a déjà ça de façon native.
[14:00] le faire. Il a déjà ça de façon native.
[14:00] le faire. Il a déjà ça de façon native. Il va du coup créer le dossier et on
[14:02] Il va du coup créer le dossier et on
[14:02] Il va du coup créer le dossier et on peut voir les trois sous-agents qui sont
[14:04] peut voir les trois sous-agents qui sont
[14:04] peut voir les trois sous-agents qui sont en train de fonctionner et en train de
[14:06] en train de fonctionner et en train de
[14:06] en train de fonctionner et en train de travailler en même temps. On a donc
[14:08] travailler en même temps. On a donc
[14:08] travailler en même temps. On a donc DeepSeek Harness qui est le cerveau, qui
[14:10] DeepSeek Harness qui est le cerveau, qui
[14:10] DeepSeek Harness qui est le cerveau, qui pilote, qui est le chef d'orchestre et
[14:12] pilote, qui est le chef d'orchestre et
[14:12] pilote, qui est le chef d'orchestre et les trois sous-agents qui vont eux
[14:13] les trois sous-agents qui vont eux
[14:13] les trois sous-agents qui vont eux travailler pour faire remonter
[14:15] travailler pour faire remonter
[14:15] travailler pour faire remonter l'information à DeepSeek Harness. Et
[14:17] l'information à DeepSeek Harness. Et
[14:17] l'information à DeepSeek Harness. Et attention, chaque agent IA a une tâche
[14:20] attention, chaque agent IA a une tâche
[14:20] attention, chaque agent IA a une tâche indépendante et de ce fait, on aura un
[14:22] indépendante et de ce fait, on aura un
[14:22] indépendante et de ce fait, on aura un périmètre par sous-agent pour éviter
[14:24] périmètre par sous-agent pour éviter
[14:24] périmètre par sous-agent pour éviter tout simplement un conflit. Chaque
[14:26] tout simplement un conflit. Chaque
[14:26] tout simplement un conflit. Chaque sous-agent a donc son propre
[14:28] sous-agent a donc son propre
[14:28] sous-agent a donc son propre environnement de travail avec son propre
[14:30] environnement de travail avec son propre
[14:30] environnement de travail avec son propre périmètre. Ils sont donc tous en train
[14:32] périmètre. Ils sont donc tous en train
[14:32] périmètre. Ils sont donc tous en train de travailler toutes les trois et tu
[14:33] de travailler toutes les trois et tu
[14:33] de travailler toutes les trois et tu peux faire ça pour plusieurs de tes
[14:35] peux faire ça pour plusieurs de tes
[14:35] peux faire ça pour plusieurs de tes projets afin d'aller encore plus vite
[14:37] projets afin d'aller encore plus vite
[14:37] projets afin d'aller encore plus vite sur tout ça. Et voilà, le quiz est
[14:39] sur tout ça. Et voilà, le quiz est
[14:39] sur tout ça. Et voilà, le quiz est opérationnel en une vitesse record. On a
[14:41] opérationnel en une vitesse record. On a
[14:42] opérationnel en une vitesse record. On a donc quelque chose qui est construit et
[14:44] donc quelque chose qui est construit et
[14:44] donc quelque chose qui est construit et on peut voir tout ça dès maintenant. Et
[14:46] on peut voir tout ça dès maintenant. Et
[14:46] on peut voir tout ça dès maintenant. Et voilà, mon score 5/5 sur ce test sur
[14:48] voilà, mon score 5/5 sur ce test sur
[14:48] voilà, mon score 5/5 sur ce test sur est-ce que tu sais ce que c'est un agent
[14:50] est-ce que tu sais ce que c'est un agent
[14:50] est-ce que tu sais ce que c'est un agent IA évidemment et heureusement
[14:51] IA évidemment et heureusement
[14:51] IA évidemment et heureusement d'ailleurs. On a donc trois agents IA
[14:53] d'ailleurs. On a donc trois agents IA
[14:53] d'ailleurs. On a donc trois agents IA qui ont fait le design, les questions et
[14:54] qui ont fait le design, les questions et
[14:55] qui ont fait le design, les questions et les tests sur un seul et même projet
[14:56] les tests sur un seul et même projet
[14:56] les tests sur un seul et même projet qu'on a fait en temps record. Tout ça
[14:58] qu'on a fait en temps record. Tout ça
[14:58] qu'on a fait en temps record. Tout ça c'est bien beau mais au début, je t'ai
[14:59] c'est bien beau mais au début, je t'ai
[14:59] c'est bien beau mais au début, je t'ai parlé quand même du fait que DeepSeek,
[15:01] parlé quand même du fait que DeepSeek,
[15:01] parlé quand même du fait que DeepSeek, ce Harness, il permet d'avoir une
[15:03] ce Harness, il permet d'avoir une
[15:03] ce Harness, il permet d'avoir une certaine flexibilité et surtout que
[15:05] certaine flexibilité et surtout que
[15:05] certaine flexibilité et surtout que c'est un vrai Lego et on va pouvoir
[15:07] c'est un vrai Lego et on va pouvoir
[15:07] c'est un vrai Lego et on va pouvoir faire ce genre de chose. On va pouvoir
[15:08] faire ce genre de chose. On va pouvoir
[15:08] faire ce genre de chose. On va pouvoir déléguer des tâches à Claude Code. Donc
[15:10] déléguer des tâches à Claude Code. Donc
[15:10] déléguer des tâches à Claude Code. Donc Harness va décider d'utiliser Claude
[15:12] Harness va décider d'utiliser Claude
[15:12] Harness va décider d'utiliser Claude Code ou bien Codex quand il le veut pour
[15:14] Code ou bien Codex quand il le veut pour
[15:14] Code ou bien Codex quand il le veut pour faire certains types de tâches, pour
[15:15] faire certains types de tâches, pour
[15:15] faire certains types de tâches, pour répartir ton utilisation de token sur
[15:17] répartir ton utilisation de token sur
[15:17] répartir ton utilisation de token sur différents abonnements ou surtout pour
[15:18] différents abonnements ou surtout pour
[15:18] différents abonnements ou surtout pour utiliser différents outils en même
[15:20] utiliser différents outils en même
[15:20] utiliser différents outils en même temps. Et donc on peut avoir un brief
[15:22] temps. Et donc on peut avoir un brief
[15:22] temps. Et donc on peut avoir un brief qui va être envoyé à Claude Code pour
[15:24] qui va être envoyé à Claude Code pour
[15:24] qui va être envoyé à Claude Code pour pouvoir être exécuté et le résultat va
[15:26] pouvoir être exécuté et le résultat va
[15:26] pouvoir être exécuté et le résultat va être retourné directement au Harness de
[15:28] être retourné directement au Harness de
[15:28] être retourné directement au Harness de DeepSeek. Donc si tu as un abonnement
[15:30] DeepSeek. Donc si tu as un abonnement
[15:30] DeepSeek. Donc si tu as un abonnement Claude, tu pourra utiliser à souhait ton
[15:33] Claude, tu pourra utiliser à souhait ton
[15:33] Claude, tu pourra utiliser à souhait ton abonnement pour économiser des tokens
[15:34] abonnement pour économiser des tokens
[15:34] abonnement pour économiser des tokens que tu payes par utilisation. Pour ça,
[15:36] que tu payes par utilisation. Pour ça,
[15:36] que tu payes par utilisation. Pour ça, tu te rends dans la catégorie plugin
[15:38] tu te rends dans la catégorie plugin
[15:38] tu te rends dans la catégorie plugin juste ici. Et là, c'est réellement des
[15:41] juste ici. Et là, c'est réellement des
[15:41] juste ici. Et là, c'est réellement des vrais Lego qu'on va pouvoir ajouter à ce
[15:43] vrais Lego qu'on va pouvoir ajouter à ce
[15:43] vrais Lego qu'on va pouvoir ajouter à ce Harness notamment avec le Claude Code de
[15:45] Harness notamment avec le Claude Code de
[15:45] Harness notamment avec le Claude Code de Sub Agent qui est par défaut
[15:47] Sub Agent qui est par défaut
[15:47] Sub Agent qui est par défaut directement, tu as juste à l'activer et
[15:49] directement, tu as juste à l'activer et
[15:50] directement, tu as juste à l'activer et il va te demander de te connecter à ton
[15:51] il va te demander de te connecter à ton
[15:51] il va te demander de te connecter à ton compte Claude, Claude Code. Tu peux
[15:53] compte Claude, Claude Code. Tu peux
[15:53] compte Claude, Claude Code. Tu peux aussi activer d'ailleurs Voice Input
[15:55] aussi activer d'ailleurs Voice Input
[15:55] aussi activer d'ailleurs Voice Input pour pouvoir faire des vocaux. Et comme
[15:57] pour pouvoir faire des vocaux. Et comme
[15:57] pour pouvoir faire des vocaux. Et comme plugin par défaut, tu as par exemple la
[15:58] plugin par défaut, tu as par exemple la
[15:59] plugin par défaut, tu as par exemple la recherche web. Et là par exemple, si je
[16:00] recherche web. Et là par exemple, si je
[16:00] recherche web. Et là par exemple, si je lui envoie ce prompt qui va demander
[16:02] lui envoie ce prompt qui va demander
[16:02] lui envoie ce prompt qui va demander déjà de faire une recherche web grâce à
[16:04] déjà de faire une recherche web grâce à
[16:04] déjà de faire une recherche web grâce à ce plugin qu'on a ajouté directement sur
[16:06] ce plugin qu'on a ajouté directement sur
[16:06] ce plugin qu'on a ajouté directement sur DeepSeek pour ensuite envoyer un brief
[16:09] DeepSeek pour ensuite envoyer un brief
[16:09] DeepSeek pour ensuite envoyer un brief très clair à Claude Code qui permettra
[16:11] très clair à Claude Code qui permettra
[16:11] très clair à Claude Code qui permettra de faire une page coming soon élégante
[16:13] de faire une page coming soon élégante
[16:13] de faire une page coming soon élégante pour un projet immobilier. Regarde ce
[16:15] pour un projet immobilier. Regarde ce
[16:15] pour un projet immobilier. Regarde ce qui va se passer. On va d'abord utiliser
[16:16] qui va se passer. On va d'abord utiliser
[16:16] qui va se passer. On va d'abord utiliser le plugin par défaut de Websearch
[16:19] le plugin par défaut de Websearch
[16:19] le plugin par défaut de Websearch directement de DeepSeek et ensuite on va
[16:21] directement de DeepSeek et ensuite on va
[16:21] directement de DeepSeek et ensuite on va créer un brief qui va être envoyé à
[16:23] créer un brief qui va être envoyé à
[16:23] créer un brief qui va être envoyé à Claude Code qui va passer par
[16:25] Claude Code qui va passer par
[16:25] Claude Code qui va passer par l'utilisation de ton abonnement Claude.
[16:27] l'utilisation de ton abonnement Claude.
[16:27] l'utilisation de ton abonnement Claude. Et imagine si à la fois tu as une équipe
[16:29] Et imagine si à la fois tu as une équipe
[16:29] Et imagine si à la fois tu as une équipe de sous-agents et également la
[16:31] de sous-agents et également la
[16:31] de sous-agents et également la possibilité de déléguer des tâches à
[16:32] possibilité de déléguer des tâches à
[16:33] possibilité de déléguer des tâches à Claude qui lui-même a des sous-agents,
[16:34] Claude qui lui-même a des sous-agents,
[16:34] Claude qui lui-même a des sous-agents, tu comprends qu'ici tu as une vraie
[16:36] tu comprends qu'ici tu as une vraie
[16:36] tu comprends qu'ici tu as une vraie petite entreprise. Et voilà par exemple
[16:37] petite entreprise. Et voilà par exemple
[16:38] petite entreprise. Et voilà par exemple là on a Claude Code qui est en train de
[16:40] là on a Claude Code qui est en train de
[16:40] là on a Claude Code qui est en train de travailler en backend parce que on a une
[16:42] travailler en backend parce que on a une
[16:42] travailler en backend parce que on a une fiche qui lui a été envoyée après une
[16:44] fiche qui lui a été envoyée après une
[16:44] fiche qui lui a été envoyée après une grande recherche web grâce au plugin de
[16:46] grande recherche web grâce au plugin de
[16:46] grande recherche web grâce au plugin de DeepSeek. Donc le Websearch est surtout
[16:48] DeepSeek. Donc le Websearch est surtout
[16:48] DeepSeek. Donc le Websearch est surtout le fait de pouvoir déléguer à Claude
[16:49] le fait de pouvoir déléguer à Claude
[16:49] le fait de pouvoir déléguer à Claude Code et j'ai hâte de montrer ce que
[16:51] Code et j'ai hâte de montrer ce que
[16:51] Code et j'ai hâte de montrer ce que Claude Code a produit. Il vient de nous
[16:52] Claude Code a produit. Il vient de nous
[16:53] Claude Code a produit. Il vient de nous remonter ce qu'a fait Claude Code. On a
[16:55] remonter ce qu'a fait Claude Code. On a
[16:55] remonter ce qu'a fait Claude Code. On a un document HTML. Donc là clairement ce
[16:57] un document HTML. Donc là clairement ce
[16:57] un document HTML. Donc là clairement ce sont les tokens de mon abonnement Claude
[16:58] sont les tokens de mon abonnement Claude
[16:58] sont les tokens de mon abonnement Claude Code qui ont été utilisés en backend au
[17:01] Code qui ont été utilisés en backend au
[17:01] Code qui ont été utilisés en backend au lieu que ce soit une API payante par
[17:03] lieu que ce soit une API payante par
[17:03] lieu que ce soit une API payante par utilisation. Et surtout ça permet de
[17:05] utilisation. Et surtout ça permet de
[17:05] utilisation. Et surtout ça permet de déléguer des tâches et de pouvoir faire
[17:07] déléguer des tâches et de pouvoir faire
[17:07] déléguer des tâches et de pouvoir faire d'autres tâches avec ce harness. Alors
[17:09] d'autres tâches avec ce harness. Alors
[17:09] d'autres tâches avec ce harness. Alors attention à pas tomber dans ce piège,
[17:10] attention à pas tomber dans ce piège,
[17:10] attention à pas tomber dans ce piège, c'est pas parce qu'il y a plusieurs
[17:12] c'est pas parce qu'il y a plusieurs
[17:12] c'est pas parce qu'il y a plusieurs agents que le travail va être mieux
[17:13] agents que le travail va être mieux
[17:13] agents que le travail va être mieux fait. C'est surtout une question de
[17:14] fait. C'est surtout une question de
[17:15] fait. C'est surtout une question de contexte et de token et de modèle de
[17:17] contexte et de token et de modèle de
[17:17] contexte et de token et de modèle de langage qui va vraiment compter.
[17:18] langage qui va vraiment compter.
[17:18] langage qui va vraiment compter. Crois-moi, un bon prompt va vraiment
[17:21] Crois-moi, un bon prompt va vraiment
[17:21] Crois-moi, un bon prompt va vraiment rivaliser 10 agents qui sont mal
[17:22] rivaliser 10 agents qui sont mal
[17:22] rivaliser 10 agents qui sont mal promptés et mal contextualisés. Bon,
[17:24] promptés et mal contextualisés. Bon,
[17:24] promptés et mal contextualisés. Bon, tout ça c'est bien beau mais il y a un
[17:25] tout ça c'est bien beau mais il y a un
[17:25] tout ça c'est bien beau mais il y a un truc dont je t'ai pas encore réellement
[17:27] truc dont je t'ai pas encore réellement
[17:27] truc dont je t'ai pas encore réellement parlé, c'est le super agent IA de
[17:29] parlé, c'est le super agent IA de
[17:29] parlé, c'est le super agent IA de DeepSeek. Le super agent de DeepSeek,
[17:31] DeepSeek. Le super agent de DeepSeek,
[17:32] DeepSeek. Le super agent de DeepSeek, c'est une nouvelle fonctionnalité qui
[17:33] c'est une nouvelle fonctionnalité qui
[17:33] c'est une nouvelle fonctionnalité qui permet à un agent autonome d'être
[17:35] permet à un agent autonome d'être
[17:35] permet à un agent autonome d'être connecté à ton compte GitHub pour
[17:37] connecté à ton compte GitHub pour
[17:37] connecté à ton compte GitHub pour travailler sur tous les projets que tu
[17:39] travailler sur tous les projets que tu
[17:39] travailler sur tous les projets que tu vas avoir publié. Le parcours est simple
[17:41] vas avoir publié. Le parcours est simple
[17:41] vas avoir publié. Le parcours est simple en fait, à chaque fois qu'il y a une
[17:42] en fait, à chaque fois qu'il y a une
[17:42] en fait, à chaque fois qu'il y a une issue sur GitHub, on va voir un portier
[17:45] issue sur GitHub, on va voir un portier
[17:45] issue sur GitHub, on va voir un portier et ce qu'il est autorisé à soumettre
[17:47] et ce qu'il est autorisé à soumettre
[17:47] et ce qu'il est autorisé à soumettre cette demande pour que ensuite DeepSeek
[17:48] cette demande pour que ensuite DeepSeek
[17:49] cette demande pour que ensuite DeepSeek y travaille dessus. On va voir une fiche
[17:50] y travaille dessus. On va voir une fiche
[17:50] y travaille dessus. On va voir une fiche de mission qui va être créée et puis on
[17:52] de mission qui va être créée et puis on
[17:52] de mission qui va être créée et puis on va voir des workers. Des workers qui
[17:54] va voir des workers. Des workers qui
[17:54] va voir des workers. Des workers qui vont tout simplement envoyer des pull
[17:56] vont tout simplement envoyer des pull
[17:56] vont tout simplement envoyer des pull requests, donc des échantillons, des
[17:58] requests, donc des échantillons, des
[17:58] requests, donc des échantillons, des propositions du travail qui a été
[18:00] propositions du travail qui a été
[18:00] propositions du travail qui a été réalisé pour avoir ensuite un
[18:02] réalisé pour avoir ensuite un
[18:02] réalisé pour avoir ensuite un commentaire. Et c'est uniquement par
[18:03] commentaire. Et c'est uniquement par
[18:03] commentaire. Et c'est uniquement par issue ou commentaire que ce super agent
[18:05] issue ou commentaire que ce super agent
[18:06] issue ou commentaire que ce super agent va s'activer pour travailler. Ce mode
[18:07] va s'activer pour travailler. Ce mode
[18:07] va s'activer pour travailler. Ce mode est vraiment autonome. Alors fais
[18:08] est vraiment autonome. Alors fais
[18:08] est vraiment autonome. Alors fais attention, soit tu utilises une machine
[18:10] attention, soit tu utilises une machine
[18:10] attention, soit tu utilises une machine dédiée ou un environnement jetable, un
[18:11] dédiée ou un environnement jetable, un
[18:11] dédiée ou un environnement jetable, un compte GitHub complètement dédié, le
[18:14] compte GitHub complètement dédié, le
[18:14] compte GitHub complètement dédié, le mode observe et surtout un merge manuel.
[18:17] mode observe et surtout un merge manuel.
[18:17] mode observe et surtout un merge manuel. Si on va dans super agent, qu'on va dans
[18:18] Si on va dans super agent, qu'on va dans
[18:18] Si on va dans super agent, qu'on va dans settings, on peut voir que est activé
[18:21] settings, on peut voir que est activé
[18:21] settings, on peut voir que est activé avec bien le repo que je viens de créer.
[18:24] avec bien le repo que je viens de créer.
[18:24] avec bien le repo que je viens de créer. Et si je vais dans issue et que je fais
[18:26] Et si je vais dans issue et que je fais
[18:26] Et si je vais dans issue et que je fais une nouvelle issue où est-ce que je dis
[18:27] une nouvelle issue où est-ce que je dis
[18:28] une nouvelle issue où est-ce que je dis justement que je veux ajouter par
[18:29] justement que je veux ajouter par
[18:29] justement que je veux ajouter par exemple un compteur de caractères pour
[18:31] exemple un compteur de caractères pour
[18:31] exemple un compteur de caractères pour les instructions de l'agent, bien sache
[18:32] les instructions de l'agent, bien sache
[18:33] les instructions de l'agent, bien sache qu'à chaque fois que tu fais une
[18:33] qu'à chaque fois que tu fais une
[18:34] qu'à chaque fois que tu fais une nouvelle issue, le super agent va
[18:35] nouvelle issue, le super agent va
[18:35] nouvelle issue, le super agent va s'activer. Plusieurs minutes après, il a
[18:37] s'activer. Plusieurs minutes après, il a
[18:37] s'activer. Plusieurs minutes après, il a fini sa tâche et on peut voir que sur
[18:39] fini sa tâche et on peut voir que sur
[18:39] fini sa tâche et on peut voir que sur mon application, il a donc modifié ce
[18:40] mon application, il a donc modifié ce
[18:41] mon application, il a donc modifié ce que je voulais. Il a clairement mis un
[18:42] que je voulais. Il a clairement mis un
[18:42] que je voulais. Il a clairement mis un compteur de caractère directement là où
[18:45] compteur de caractère directement là où
[18:45] compteur de caractère directement là où je voulais. Donc la fonctionnalité a
[18:46] je voulais. Donc la fonctionnalité a
[18:47] je voulais. Donc la fonctionnalité a bien été développée. Concrètement, dès à
[18:49] bien été développée. Concrètement, dès à
[18:49] bien été développée. Concrètement, dès à présent, on a fait l'installation, la
[18:51] présent, on a fait l'installation, la
[18:51] présent, on a fait l'installation, la configuration, un nouveau projet, ajouté
[18:53] configuration, un nouveau projet, ajouté
[18:53] configuration, un nouveau projet, ajouté des skills, ajouté open router des
[18:54] des skills, ajouté open router des
[18:55] des skills, ajouté open router des sous-agents, on a délégué à Claude Code
[18:56] sous-agents, on a délégué à Claude Code
[18:56] sous-agents, on a délégué à Claude Code et surtout on a utilisé le super agent
[18:58] et surtout on a utilisé le super agent
[18:58] et surtout on a utilisé le super agent et au final, qu'est-ce qu'on en retient
[19:00] et au final, qu'est-ce qu'on en retient
[19:00] et au final, qu'est-ce qu'on en retient de cet outil? Bah selon moi, DeepSeek va
[19:02] de cet outil? Bah selon moi, DeepSeek va
[19:02] de cet outil? Bah selon moi, DeepSeek va gagner en flexibilité et en prix et
[19:04] gagner en flexibilité et en prix et
[19:04] gagner en flexibilité et en prix et surtout en liberté. Là où Claude Code OK
[19:07] surtout en liberté. Là où Claude Code OK
[19:07] surtout en liberté. Là où Claude Code OK peut gagner en finition si on ajoute les
[19:09] peut gagner en finition si on ajoute les
[19:09] peut gagner en finition si on ajoute les bons modèles de langage. Mais ce qu'on
[19:10] bons modèles de langage. Mais ce qu'on
[19:10] bons modèles de langage. Mais ce qu'on en retient de ces outils chinois même si
[19:12] en retient de ces outils chinois même si
[19:12] en retient de ces outils chinois même si on a peur des données, bah côté
[19:15] on a peur des données, bah côté
[19:15] on a peur des données, bah côté Amérique, on sait pas où vont les
[19:16] Amérique, on sait pas où vont les
[19:16] Amérique, on sait pas où vont les données non plus. Et DeepSeek, elle
[19:17] données non plus. Et DeepSeek, elle
[19:18] données non plus. Et DeepSeek, elle mérite de nous donner un outil qui est
[19:20] mérite de nous donner un outil qui est
[19:20] mérite de nous donner un outil qui est flexible où est-ce qu'on peut connecter
[19:21] flexible où est-ce qu'on peut connecter
[19:22] flexible où est-ce qu'on peut connecter n'importe quel modèle de langage et
[19:23] n'importe quel modèle de langage et
[19:23] n'importe quel modèle de langage et posséder ce harness. Évidemment
[19:25] posséder ce harness. Évidemment
[19:25] posséder ce harness. Évidemment attention parce que c'est un outil qui
[19:27] attention parce que c'est un outil qui
[19:27] attention parce que c'est un outil qui peut jouer avec toutes vos données si
[19:28] peut jouer avec toutes vos données si
[19:28] peut jouer avec toutes vos données si vous le configurez mal. Alors regardez
[19:30] vous le configurez mal. Alors regardez
[19:30] vous le configurez mal. Alors regardez bien le guide qui se trouvera juste en
[19:32] bien le guide qui se trouvera juste en
[19:32] bien le guide qui se trouvera juste en description dans mon school complètement
[19:34] description dans mon school complètement
[19:34] description dans mon school complètement gratuit. Un groupe communautaire avec
[19:35] gratuit. Un groupe communautaire avec
[19:35] gratuit. Un groupe communautaire avec déjà plus de 3400 personnes où est-ce
[19:37] déjà plus de 3400 personnes où est-ce
[19:37] déjà plus de 3400 personnes où est-ce qu'on a simplement à s'inscrire
[19:38] qu'on a simplement à s'inscrire
[19:39] qu'on a simplement à s'inscrire gratuitement et accéder à plus de 3 ans
[19:41] gratuitement et accéder à plus de 3 ans
[19:41] gratuitement et accéder à plus de 3 ans de ressources dans l'IA et la ressource
[19:43] de ressources dans l'IA et la ressource
[19:43] de ressources dans l'IA et la ressource pour installer ce DeepSeek se trouvera
[19:45] pour installer ce DeepSeek se trouvera
[19:45] pour installer ce DeepSeek se trouvera dans ressources YouTube. On aura ici une
[19:47] dans ressources YouTube. On aura ici une
[19:47] dans ressources YouTube. On aura ici une vidéo comment installer DeepSeek
[19:48] vidéo comment installer DeepSeek
[19:48] vidéo comment installer DeepSeek harness. Je mettrai mon prompt entier en
[19:50] harness. Je mettrai mon prompt entier en
[19:50] harness. Je mettrai mon prompt entier en description. Donc va récupérer ça,
[19:52] description. Donc va récupérer ça,
[19:52] description. Donc va récupérer ça, dis-moi ce que tu en penses en
[19:53] dis-moi ce que tu en penses en
[19:53] dis-moi ce que tu en penses en commentaire très sincèrement. En tout
[19:55] commentaire très sincèrement. En tout
[19:55] commentaire très sincèrement. En tout cas, on se trouve à la prochaine pour
[19:56] cas, on se trouve à la prochaine pour
[19:56] cas, on se trouve à la prochaine pour une nouvelle vidéo. C'était Julien.
