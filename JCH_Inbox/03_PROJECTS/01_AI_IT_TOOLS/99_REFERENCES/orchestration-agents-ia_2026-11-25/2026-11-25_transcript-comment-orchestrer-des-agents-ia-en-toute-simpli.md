# Transcript — « Comment orchestrer des agents IA en toute simplicité »

- **Source** : Erwan | IA
- **URL** : https://www.youtube.com/watch?v=cA1dE7f1ZWI
- **Durée** : 12:42
- **Date** : 2026-11-25
- **Moteur** : sous-titres YouTube
- **Segments** : 940

---

[00:01] Tu as sûrement entendu parler des essins
[00:01] Tu as sûrement entendu parler des essins d'agent. C'est des dizaines, des
[00:02] d'agent. C'est des dizaines, des
[00:03] d'agent. C'est des dizaines, des centaines d'agents IA qui feraient tout
[00:04] centaines d'agents IA qui feraient tout
[00:04] centaines d'agents IA qui feraient tout à ta place, qui travailleraient en
[00:06] à ta place, qui travailleraient en
[00:06] à ta place, qui travailleraient en permanence. Sur le papier, la promesse
[00:08] permanence. Sur le papier, la promesse
[00:08] permanence. Sur le papier, la promesse est très belle, mais en réalité, ça ne
[00:09] est très belle, mais en réalité, ça ne
[00:09] est très belle, mais en réalité, ça ne se passe jamais comme ça. Et dans cette
[00:11] se passe jamais comme ça. Et dans cette
[00:11] se passe jamais comme ça. Et dans cette vidéo, à contrario, je vais t'expliquer
[00:12] vidéo, à contrario, je vais t'expliquer
[00:12] vidéo, à contrario, je vais t'expliquer de manière très simple quel est le
[00:14] de manière très simple quel est le
[00:14] de manière très simple quel est le schéma d'orchestration le plus efficace
[00:16] schéma d'orchestration le plus efficace
[00:16] schéma d'orchestration le plus efficace à ce jour selon moi. Je vais t'expliquer
[00:17] à ce jour selon moi. Je vais t'expliquer
[00:17] à ce jour selon moi. Je vais t'expliquer ce que les derniers modèles frontières
[00:18] ce que les derniers modèles frontières
[00:18] ce que les derniers modèles frontières ont changé. Je vais te montrer quel
[00:20] ont changé. Je vais te montrer quel
[00:20] ont changé. Je vais te montrer quel modèle mettre à chaque poste et je
[00:22] modèle mettre à chaque poste et je
[00:22] modèle mettre à chaque poste et je t'expliquerai comment tu peux construire
[00:23] t'expliquerai comment tu peux construire
[00:23] t'expliquerai comment tu peux construire tout cela toi-même en toute simplicité.
[00:25] tout cela toi-même en toute simplicité.
[00:25] tout cela toi-même en toute simplicité. Si c'est la première fois que tu tombes
[00:26] Si c'est la première fois que tu tombes
[00:26] Si c'est la première fois que tu tombes sur ma chaîne, je te souhaite la
[00:27] sur ma chaîne, je te souhaite la
[00:27] sur ma chaîne, je te souhaite la bienvenue et n'hésite pas à t'abonner
[00:28] bienvenue et n'hésite pas à t'abonner
[00:28] bienvenue et n'hésite pas à t'abonner pour rester au top de l'intelligence
[00:30] pour rester au top de l'intelligence
[00:30] pour rester au top de l'intelligence artificielle. Alors déjà, pourquoi
[00:32] artificielle. Alors déjà, pourquoi
[00:32] artificielle. Alors déjà, pourquoi est-ce que les essins d'agents sont
[00:33] est-ce que les essins d'agents sont
[00:33] est-ce que les essins d'agents sont selon moi une très mauvaise idée ? Pour
[00:34] selon moi une très mauvaise idée ? Pour
[00:34] selon moi une très mauvaise idée ? Pour faire simple, les agents qui sont
[00:36] faire simple, les agents qui sont
[00:36] faire simple, les agents qui sont organisés en essin, ils coûtent
[00:37] organisés en essin, ils coûtent
[00:37] organisés en essin, ils coûtent extrêmement cher et ils collaborent
[00:39] extrêmement cher et ils collaborent
[00:39] extrêmement cher et ils collaborent extrêmement mal ensemble. tu payes 15
[00:41] extrêmement mal ensemble. tu payes 15
[00:41] extrêmement mal ensemble. tu payes 15 fois plus pour des agents qui se
[00:42] fois plus pour des agents qui se
[00:42] fois plus pour des agents qui se marchent dessus parce que plus d'agents,
[00:43] marchent dessus parce que plus d'agents,
[00:43] marchent dessus parce que plus d'agents, c'est mécaniquement plus de token, mais
[00:45] c'est mécaniquement plus de token, mais
[00:45] c'est mécaniquement plus de token, mais c'est aussi plus de malentendu. Selon
[00:47] c'est aussi plus de malentendu. Selon
[00:47] c'est aussi plus de malentendu. Selon Entropique, un essin va consommer
[00:48] Entropique, un essin va consommer
[00:48] Entropique, un essin va consommer environ 15 fois plus de token. Et il y a
[00:51] environ 15 fois plus de token. Et il y a
[00:51] environ 15 fois plus de token. Et il y a 1 an et demi déjà, on voyait des papiers
[00:52] 1 an et demi déjà, on voyait des papiers
[00:52] 1 an et demi déjà, on voyait des papiers sortir expliquant qu'il ne fallait
[00:54] sortir expliquant qu'il ne fallait
[00:54] sortir expliquant qu'il ne fallait surtout pas construire des systèmes
[00:55] surtout pas construire des systèmes
[00:55] surtout pas construire des systèmes multiagentiques parce que ça aboutit à
[00:57] multiagentiques parce que ça aboutit à
[00:57] multiagentiques parce que ça aboutit à des systèmes qui sont fragiles. Alors,
[00:59] des systèmes qui sont fragiles. Alors,
[00:59] des systèmes qui sont fragiles. Alors, qu'est-ce que les derniers modèles ont
[01:00] qu'est-ce que les derniers modèles ont
[01:00] qu'est-ce que les derniers modèles ont changé ? Aujourd'hui, les modèles
[01:01] changé ? Aujourd'hui, les modèles
[01:01] changé ? Aujourd'hui, les modèles frontières de nouvelle génération, ils
[01:02] frontières de nouvelle génération, ils
[01:03] frontières de nouvelle génération, ils font tout seul ce qu'il fallait hier
[01:04] font tout seul ce qu'il fallait hier
[01:04] font tout seul ce qu'il fallait hier confier à une équipe. Et le modèle à la
[01:06] confier à une équipe. Et le modèle à la
[01:06] confier à une équipe. Et le modèle à la tête, le modèle orchestrateur, il compte
[01:08] tête, le modèle orchestrateur, il compte
[01:08] tête, le modèle orchestrateur, il compte beaucoup plus que le nombre d'agents. En
[01:10] beaucoup plus que le nombre d'agents. En
[01:10] beaucoup plus que le nombre d'agents. En juin 2025, sur la génération des modèles
[01:11] juin 2025, sur la génération des modèles
[01:12] juin 2025, sur la génération des modèles précédents, Anthropic avait mis en place
[01:13] précédents, Anthropic avait mis en place
[01:13] précédents, Anthropic avait mis en place une expérience dans laquelle ils avaient
[01:14] une expérience dans laquelle ils avaient
[01:14] une expérience dans laquelle ils avaient confié à Opus 4 le soin d'orchestrer des
[01:17] confié à Opus 4 le soin d'orchestrer des
[01:17] confié à Opus 4 le soin d'orchestrer des sous-agents sur Son 4. Et sur leur test
[01:19] sous-agents sur Son 4. Et sur leur test
[01:19] sous-agents sur Son 4. Et sur leur test interne, cette configuration, elle
[01:20] interne, cette configuration, elle
[01:20] interne, cette configuration, elle aboutissait effectivement à un bien
[01:21] aboutissait effectivement à un bien
[01:21] aboutissait effectivement à un bien meilleur résultat, mais ça c'était la
[01:23] meilleur résultat, mais ça c'était la
[01:23] meilleur résultat, mais ça c'était la génération d'avant. Les modèles font
[01:24] génération d'avant. Les modèles font
[01:24] génération d'avant. Les modèles font seuls ce qu'on leur dictait de faire
[01:25] seuls ce qu'on leur dictait de faire
[01:25] seuls ce qu'on leur dictait de faire auparavant. D'ailleurs récemment,
[01:27] auparavant. D'ailleurs récemment,
[01:27] auparavant. D'ailleurs récemment, l'équipe d'anthropique a supprimé 80 %
[01:29] l'équipe d'anthropique a supprimé 80 %
[01:29] l'équipe d'anthropique a supprimé 80 % des consignes systèmes de Claude Code
[01:31] des consignes systèmes de Claude Code
[01:31] des consignes systèmes de Claude Code parce que c'était tout simplement devenu
[01:32] parce que c'était tout simplement devenu
[01:32] parce que c'était tout simplement devenu superflu. Boris Cherni qui est le
[01:33] superflu. Boris Cherni qui est le
[01:33] superflu. Boris Cherni qui est le créateur de Cloud Code, il parle du
[01:35] créateur de Cloud Code, il parle du
[01:35] créateur de Cloud Code, il parle du Hling. Le obling, ça consiste à donner à
[01:37] Hling. Le obling, ça consiste à donner à
[01:37] Hling. Le obling, ça consiste à donner à des modèles devenus surpuissants des
[01:39] des modèles devenus surpuissants des
[01:39] des modèles devenus surpuissants des consignes qui en réalité les brides, des
[01:41] consignes qui en réalité les brides, des
[01:41] consignes qui en réalité les brides, des consignes qui limitent leurs réelles
[01:43] consignes qui limitent leurs réelles
[01:43] consignes qui limitent leurs réelles possibilités. En conséquence, un chef
[01:45] possibilités. En conséquence, un chef
[01:45] possibilités. En conséquence, un chef très fort, il va tenir la mission de
[01:47] très fort, il va tenir la mission de
[01:47] très fort, il va tenir la mission de bout en bout et les sous-agents vont
[01:49] bout en bout et les sous-agents vont
[01:49] bout en bout et les sous-agents vont devenir des exécutants ponctuels et
[01:51] devenir des exécutants ponctuels et
[01:51] devenir des exécutants ponctuels et certainement pas une équipe permanente à
[01:53] certainement pas une équipe permanente à
[01:53] certainement pas une équipe permanente à maintenir. Donc comme bien souvent, la
[01:55] maintenir. Donc comme bien souvent, la
[01:55] maintenir. Donc comme bien souvent, la simplicité est la sophistication
[01:57] simplicité est la sophistication
[01:57] simplicité est la sophistication suprême. Et c'est exactement
[01:58] suprême. Et c'est exactement
[01:58] suprême. Et c'est exactement l'architecture que je vais vous
[01:59] l'architecture que je vais vous
[01:59] l'architecture que je vais vous expliquer aujourd'hui. Hier, il fallait
[02:00] expliquer aujourd'hui. Hier, il fallait
[02:00] expliquer aujourd'hui. Hier, il fallait une équipe entière, aujourd'hui il faut
[02:02] une équipe entière, aujourd'hui il faut
[02:02] une équipe entière, aujourd'hui il faut un bon chef. Alors, concrètement, à quoi
[02:03] un bon chef. Alors, concrètement, à quoi
[02:03] un bon chef. Alors, concrètement, à quoi ressemble ce schéma optimisé ? Ce qui va
[02:05] ressemble ce schéma optimisé ? Ce qui va
[02:05] ressemble ce schéma optimisé ? Ce qui va fonctionner, c'est trois couches. Un
[02:07] fonctionner, c'est trois couches. Un
[02:07] fonctionner, c'est trois couches. Un chef très intelligent, quelques
[02:08] chef très intelligent, quelques
[02:09] chef très intelligent, quelques exécutants ciblés et des skills et
[02:11] exécutants ciblés et des skills et
[02:11] exécutants ciblés et des skills et autres ressources qu'ils vont pouvoir
[02:12] autres ressources qu'ils vont pouvoir
[02:12] autres ressources qu'ils vont pouvoir mobiliser. En premier lieu, on a donc le
[02:14] mobiliser. En premier lieu, on a donc le
[02:14] mobiliser. En premier lieu, on a donc le chef qui est le modèle orchestrateur qui
[02:16] chef qui est le modèle orchestrateur qui
[02:16] chef qui est le modèle orchestrateur qui va découper la mission et garder la vue
[02:18] va découper la mission et garder la vue
[02:18] va découper la mission et garder la vue d'ensemble. Et ce rôle là, il faut le
[02:20] d'ensemble. Et ce rôle là, il faut le
[02:20] d'ensemble. Et ce rôle là, il faut le confier au modèle le plus intelligent de
[02:22] confier au modèle le plus intelligent de
[02:22] confier au modèle le plus intelligent de ton abonnement. Et à ce poste de chef,
[02:23] ton abonnement. Et à ce poste de chef,
[02:23] ton abonnement. Et à ce poste de chef, nos candidats modèles qui sont
[02:25] nos candidats modèles qui sont
[02:25] nos candidats modèles qui sont présidentes à ce jour le 24 novembre
[02:27] présidentes à ce jour le 24 novembre
[02:27] présidentes à ce jour le 24 novembre 2026, ça va être Fable 5.2 chez
[02:29] 2026, ça va être Fable 5.2 chez
[02:29] 2026, ça va être Fable 5.2 chez Antropique qui est tout simplement le
[02:31] Antropique qui est tout simplement le
[02:31] Antropique qui est tout simplement le meilleur à ce jour. 65 sur l'indice
[02:33] meilleur à ce jour. 65 sur l'indice
[02:33] meilleur à ce jour. 65 sur l'indice d'artificial analysis. Ça peut être
[02:35] d'artificial analysis. Ça peut être
[02:35] d'artificial analysis. Ça peut être également Gini 4 néon dont on parle
[02:37] également Gini 4 néon dont on parle
[02:37] également Gini 4 néon dont on parle beaucoup depuis maintenant une semaine
[02:38] beaucoup depuis maintenant une semaine
[02:38] beaucoup depuis maintenant une semaine et qui moi m'a personnellement bluffé,
[02:40] et qui moi m'a personnellement bluffé,
[02:40] et qui moi m'a personnellement bluffé, qui me semble être excellent justement
[02:42] qui me semble être excellent justement
[02:42] qui me semble être excellent justement dans un rôle d'orchestrator, ça va être
[02:44] dans un rôle d'orchestrator, ça va être
[02:44] dans un rôle d'orchestrator, ça va être l'inénarable Opus 5.5, modèle frontière
[02:47] l'inénarable Opus 5.5, modèle frontière
[02:47] l'inénarable Opus 5.5, modèle frontière du quotidien qui lui aussi m'a
[02:48] du quotidien qui lui aussi m'a
[02:48] du quotidien qui lui aussi m'a énormément surpris sur ces dernières
[02:50] énormément surpris sur ces dernières
[02:50] énormément surpris sur ces dernières semaines. Si vous êtes chez Chat GPT, ça
[02:52] semaines. Si vous êtes chez Chat GPT, ça
[02:52] semaines. Si vous êtes chez Chat GPT, ça peut être 6.2 Astra. Bien que
[02:54] peut être 6.2 Astra. Bien que
[02:54] peut être 6.2 Astra. Bien que honnêtement, je sois pas forcément très
[02:55] honnêtement, je sois pas forcément très
[02:55] honnêtement, je sois pas forcément très convaincu par la génération 6.2 de qui
[02:57] convaincu par la génération 6.2 de qui
[02:57] convaincu par la génération 6.2 de qui ne cessent de me décevoir. Au deuxième
[02:59] ne cessent de me décevoir. Au deuxième
[02:59] ne cessent de me décevoir. Au deuxième rang, on va avoir les modèles
[03:00] rang, on va avoir les modèles
[03:00] rang, on va avoir les modèles exécutants. Ici, ça va être quelques
[03:02] exécutants. Ici, ça va être quelques
[03:02] exécutants. Ici, ça va être quelques sous-agents, un par mission, invoqué au
[03:04] sous-agents, un par mission, invoqué au
[03:04] sous-agents, un par mission, invoqué au moment où il y a une tâche que
[03:05] moment où il y a une tâche que
[03:05] moment où il y a une tâche que l'orchestrateur estime qu'il faut
[03:06] l'orchestrateur estime qu'il faut
[03:06] l'orchestrateur estime qu'il faut réaliser. Et ici, on va choisir un
[03:08] réaliser. Et ici, on va choisir un
[03:08] réaliser. Et ici, on va choisir un modèle plus rapide et moins cher. Pour
[03:10] modèle plus rapide et moins cher. Pour
[03:10] modèle plus rapide et moins cher. Pour moi, le candidat parfait aujourd'hui,
[03:11] moi, le candidat parfait aujourd'hui,
[03:11] moi, le candidat parfait aujourd'hui, c'est Sony 5.5 qui reste un modèle
[03:13] c'est Sony 5.5 qui reste un modèle
[03:13] c'est Sony 5.5 qui reste un modèle redoutablement intelligent mais qui va
[03:14] redoutablement intelligent mais qui va
[03:15] redoutablement intelligent mais qui va être beaucoup plus efficient. Ça peut
[03:16] être beaucoup plus efficient. Ça peut
[03:16] être beaucoup plus efficient. Ça peut être aussi un GPT 6.2 de sol, ça peut
[03:18] être aussi un GPT 6.2 de sol, ça peut
[03:18] être aussi un GPT 6.2 de sol, ça peut être aussi les modèles ouverts chinois,
[03:20] être aussi les modèles ouverts chinois,
[03:20] être aussi les modèles ouverts chinois, des dipsic, des GLM, des Kimi. Et la
[03:23] des dipsic, des GLM, des Kimi. Et la
[03:23] des dipsic, des GLM, des Kimi. Et la troisième couche, ça va être les skills.
[03:25] troisième couche, ça va être les skills.
[03:25] troisième couche, ça va être les skills. Je vous ai beaucoup parler des skills
[03:26] Je vous ai beaucoup parler des skills
[03:26] Je vous ai beaucoup parler des skills sur ma chaîne. Je vous renvoie vers des
[03:27] sur ma chaîne. Je vous renvoie vers des
[03:27] sur ma chaîne. Je vous renvoie vers des vidéos que j'ai déjà produit si vous ne
[03:29] vidéos que j'ai déjà produit si vous ne
[03:29] vidéos que j'ai déjà produit si vous ne savez pas ce que c'est. Pour moi, c'est
[03:30] savez pas ce que c'est. Pour moi, c'est
[03:30] savez pas ce que c'est. Pour moi, c'est une unité fondamentale dans le domaine
[03:31] une unité fondamentale dans le domaine
[03:31] une unité fondamentale dans le domaine de Lia. Ce sont des protocoles écrits
[03:33] de Lia. Ce sont des protocoles écrits
[03:33] de Lia. Ce sont des protocoles écrits que chaque modèle exécutant va pouvoir
[03:35] que chaque modèle exécutant va pouvoir
[03:35] que chaque modèle exécutant va pouvoir lire. Et ce que je vous conseille, c'est
[03:36] lire. Et ce que je vous conseille, c'est
[03:37] lire. Et ce que je vous conseille, c'est au maximum de prévoir que vos
[03:38] au maximum de prévoir que vos
[03:38] au maximum de prévoir que vos sous-agents n'en exécutent que deux ou
[03:39] sous-agents n'en exécutent que deux ou
[03:39] sous-agents n'en exécutent que deux ou trois pour justement préserver la
[03:41] trois pour justement préserver la
[03:41] trois pour justement préserver la qualité de leur fenêtre de contexte.
[03:42] qualité de leur fenêtre de contexte.
[03:42] qualité de leur fenêtre de contexte. Attention, toutefois, les classements
[03:43] Attention, toutefois, les classements
[03:43] Attention, toutefois, les classements bougent très vite. Donc le nom des
[03:45] bougent très vite. Donc le nom des
[03:45] bougent très vite. Donc le nom des modèles que j'ai cité, il compte en
[03:46] modèles que j'ai cité, il compte en
[03:46] modèles que j'ai cité, il compte en réalité beaucoup moins que la règle
[03:48] réalité beaucoup moins que la règle
[03:48] réalité beaucoup moins que la règle d'attribution. Cette règle
[03:49] d'attribution. Cette règle
[03:49] d'attribution. Cette règle d'attribution, c'est que le modèle le
[03:51] d'attribution, c'est que le modèle le
[03:51] d'attribution, c'est que le modèle le plus intelligent doit être au poste de
[03:52] plus intelligent doit être au poste de
[03:52] plus intelligent doit être au poste de chef, ça doit être l'orchestrateur. Et
[03:54] chef, ça doit être l'orchestrateur. Et
[03:54] chef, ça doit être l'orchestrateur. Et les modèles qui sont un petit peu moins
[03:56] les modèles qui sont un petit peu moins
[03:56] les modèles qui sont un petit peu moins intelligents mais qui sont plus
[03:57] intelligents mais qui sont plus
[03:57] intelligents mais qui sont plus compétitifs en terme de prix et
[03:58] compétitifs en terme de prix et
[03:58] compétitifs en terme de prix et peut-être plus rapides, eux, ils passent
[04:00] peut-être plus rapides, eux, ils passent
[04:00] peut-être plus rapides, eux, ils passent sur le rôle d'exécutant. Et ce qui est
[04:02] sur le rôle d'exécutant. Et ce qui est
[04:02] sur le rôle d'exécutant. Et ce qui est fantastique, c'est que depuis 6 mois,
[04:03] fantastique, c'est que depuis 6 mois,
[04:03] fantastique, c'est que depuis 6 mois, ces modèles orchestrateurs, ils sont
[04:04] ces modèles orchestrateurs, ils sont
[04:04] ces modèles orchestrateurs, ils sont devenus tellement forts, tellement
[04:06] devenus tellement forts, tellement
[04:06] devenus tellement forts, tellement intelligents que la barrière technique
[04:07] intelligents que la barrière technique
[04:07] intelligents que la barrière technique est en train de se lever. Ça veut dire
[04:09] est en train de se lever. Ça veut dire
[04:09] est en train de se lever. Ça veut dire qu'on peut leur demander la plupart des
[04:10] qu'on peut leur demander la plupart des
[04:10] qu'on peut leur demander la plupart des choses en langage naturel et on va
[04:11] choses en langage naturel et on va
[04:11] choses en langage naturel et on va obtenir des résultats qui seront très
[04:13] obtenir des résultats qui seront très
[04:13] obtenir des résultats qui seront très qualitatifs. Et je pense que ce passage
[04:15] qualitatifs. Et je pense que ce passage
[04:15] qualitatifs. Et je pense que ce passage impromptu de mon chat mérite à minima un
[04:17] impromptu de mon chat mérite à minima un
[04:17] impromptu de mon chat mérite à minima un petit pouce bleu, voire même un petit
[04:18] petit pouce bleu, voire même un petit
[04:18] petit pouce bleu, voire même un petit commentaire. Alors, qu'est-ce qui rend
[04:19] commentaire. Alors, qu'est-ce qui rend
[04:19] commentaire. Alors, qu'est-ce qui rend le modèle orchestrateur vraiment
[04:20] le modèle orchestrateur vraiment
[04:21] le modèle orchestrateur vraiment efficace ? La mission qu'il faut lui
[04:22] efficace ? La mission qu'il faut lui
[04:22] efficace ? La mission qu'il faut lui donner, ça va être de pouvoir à la fois
[04:24] donner, ça va être de pouvoir à la fois
[04:24] donner, ça va être de pouvoir à la fois briefer les sous-agents, mais aussi
[04:26] briefer les sous-agents, mais aussi
[04:26] briefer les sous-agents, mais aussi doser les efforts des sous-agents et
[04:27] doser les efforts des sous-agents et
[04:27] doser les efforts des sous-agents et bien sûr entretenir une mémoire qui va
[04:30] bien sûr entretenir une mémoire qui va
[04:30] bien sûr entretenir une mémoire qui va vivre dans un système très robuste. Le
[04:32] vivre dans un système très robuste. Le
[04:32] vivre dans un système très robuste. Le modèle orchestrateur, il doit briefer
[04:34] modèle orchestrateur, il doit briefer
[04:34] modèle orchestrateur, il doit briefer comme un très bon manager. Entropique,
[04:36] comme un très bon manager. Entropique,
[04:36] comme un très bon manager. Entropique, l'écrit dans sa documentation : "Chaque
[04:37] l'écrit dans sa documentation : "Chaque
[04:37] l'écrit dans sa documentation : "Chaque sous-agent va avoir besoin d'un
[04:38] sous-agent va avoir besoin d'un
[04:38] sous-agent va avoir besoin d'un objectif, d'un format de rendu, des
[04:40] objectif, d'un format de rendu, des
[04:40] objectif, d'un format de rendu, des outils et des sources à utiliser avec
[04:41] outils et des sources à utiliser avec
[04:41] outils et des sources à utiliser avec des limites claires. Sinon, ce qui va se
[04:43] des limites claires. Sinon, ce qui va se
[04:43] des limites claires. Sinon, ce qui va se passer, c'est qu'ils vont faire le
[04:43] passer, c'est qu'ils vont faire le
[04:44] passer, c'est qu'ils vont faire le travail en double où ils vont laisser
[04:45] travail en double où ils vont laisser
[04:45] travail en double où ils vont laisser des trous." Par ailleurs, ce modèle
[04:46] des trous." Par ailleurs, ce modèle
[04:46] des trous." Par ailleurs, ce modèle orchestrateur, il doit doser l'effort.
[04:48] orchestrateur, il doit doser l'effort.
[04:48] orchestrateur, il doit doser l'effort. S'il a une tâche simple, il va mobiliser
[04:50] S'il a une tâche simple, il va mobiliser
[04:50] S'il a une tâche simple, il va mobiliser un seul agent. S'il doit faire une
[04:51] un seul agent. S'il doit faire une
[04:51] un seul agent. S'il doit faire une comparaison ou une recherche étendue, il
[04:53] comparaison ou une recherche étendue, il
[04:53] comparaison ou une recherche étendue, il vaut mieux partir sur deux à quatre
[04:55] vaut mieux partir sur deux à quatre
[04:55] vaut mieux partir sur deux à quatre sous-agents. Le modèle orchestrateur, il
[04:56] sous-agents. Le modèle orchestrateur, il
[04:56] sous-agents. Le modèle orchestrateur, il doit s'assurer que chacun garde la tête
[04:58] doit s'assurer que chacun garde la tête
[04:58] doit s'assurer que chacun garde la tête claire. Chaque sous-agent travaille dans
[05:00] claire. Chaque sous-agent travaille dans
[05:00] claire. Chaque sous-agent travaille dans sa propre fenêtre de contexte avec sa
[05:02] sa propre fenêtre de contexte avec sa
[05:02] sa propre fenêtre de contexte avec sa mémoire de travail. Il va explorer un
[05:04] mémoire de travail. Il va explorer un
[05:04] mémoire de travail. Il va explorer un terrain assez large et ensuite on va lui
[05:06] terrain assez large et ensuite on va lui
[05:06] terrain assez large et ensuite on va lui demander un résumé de 1000 à 2000 token.
[05:08] demander un résumé de 1000 à 2000 token.
[05:08] demander un résumé de 1000 à 2000 token. Et le chef, lui, ne va garder que des
[05:10] Et le chef, lui, ne va garder que des
[05:10] Et le chef, lui, ne va garder que des conclusions. Sa mémoire, elle doit vivre
[05:11] conclusions. Sa mémoire, elle doit vivre
[05:11] conclusions. Sa mémoire, elle doit vivre dans un fichier. Le modèle, il oublie
[05:13] dans un fichier. Le modèle, il oublie
[05:13] dans un fichier. Le modèle, il oublie tout d'une session à l'autre par défaut.
[05:15] tout d'une session à l'autre par défaut.
[05:15] tout d'une session à l'autre par défaut. Donc il faut demander à ce modèle
[05:16] Donc il faut demander à ce modèle
[05:16] Donc il faut demander à ce modèle orchestrateur de documenter chacune des
[05:18] orchestrateur de documenter chacune des
[05:18] orchestrateur de documenter chacune des réalisations et de garder le fil de ce
[05:21] réalisations et de garder le fil de ce
[05:21] réalisations et de garder le fil de ce qui se passe. [musique] Et d'ailleurs,
[05:22] qui se passe. [musique] Et d'ailleurs,
[05:22] qui se passe. [musique] Et d'ailleurs, pour se faire, il y a un excellent skill
[05:24] pour se faire, il y a un excellent skill
[05:24] pour se faire, il y a un excellent skill de l'excellent matpock que je vous
[05:25] de l'excellent matpock que je vous
[05:25] de l'excellent matpock que je vous recommande qui s'appelle Wayfinder. Je
[05:28] recommande qui s'appelle Wayfinder. Je
[05:28] recommande qui s'appelle Wayfinder. Je vous mettrai les infos en description.
[05:29] vous mettrai les infos en description.
[05:29] vous mettrai les infos en description. Et enfin, pour que l'orchestrateur soit
[05:31] Et enfin, pour que l'orchestrateur soit
[05:31] Et enfin, pour que l'orchestrateur soit vraiment efficace, il doit avoir accès à
[05:32] vraiment efficace, il doit avoir accès à
[05:32] vraiment efficace, il doit avoir accès à des protocoles écrits de très grande
[05:34] des protocoles écrits de très grande
[05:34] des protocoles écrits de très grande qualité, ces fameux skills. Comme ça, il
[05:36] qualité, ces fameux skills. Comme ça, il
[05:36] qualité, ces fameux skills. Comme ça, il va missionner des sous-agents qui ne
[05:38] va missionner des sous-agents qui ne
[05:38] va missionner des sous-agents qui ne vont pas avoir besoin de deviner votre
[05:39] vont pas avoir besoin de deviner votre
[05:39] vont pas avoir besoin de deviner votre méthode. Ils vont tout simplement la
[05:41] méthode. Ils vont tout simplement la
[05:41] méthode. Ils vont tout simplement la lire sur les conseils de l'orchestrateur
[05:43] lire sur les conseils de l'orchestrateur
[05:43] lire sur les conseils de l'orchestrateur et sur cette base-là, ils vont réaliser
[05:44] et sur cette base-là, ils vont réaliser
[05:44] et sur cette base-là, ils vont réaliser un excellent travail. Plusieurs
[05:46] un excellent travail. Plusieurs
[05:46] un excellent travail. Plusieurs sous-agents bien briefés qui vont suivre
[05:48] sous-agents bien briefés qui vont suivre
[05:48] sous-agents bien briefés qui vont suivre des protocoles précis vont tout le temps
[05:49] des protocoles précis vont tout le temps
[05:50] des protocoles précis vont tout le temps battre un seul agent qui sera noyé dans
[05:52] battre un seul agent qui sera noyé dans
[05:52] battre un seul agent qui sera noyé dans un contexte encombré avec des tâche
[05:53] un contexte encombré avec des tâche
[05:53] un contexte encombré avec des tâche multiples. Et ces protocoles écrits qui
[05:55] multiples. Et ces protocoles écrits qui
[05:55] multiples. Et ces protocoles écrits qui sont des skills, c'est des simples
[05:57] sont des skills, c'est des simples
[05:57] sont des skills, c'est des simples dossiers qui sont chargés seulement
[05:58] dossiers qui sont chargés seulement
[05:58] dossiers qui sont chargés seulement quand la tâche le requiert.
[06:00] quand la tâche le requiert.
[06:00] quand la tâche le requiert. Concrètement, un skill, c'est un dossier
[06:02] Concrètement, un skill, c'est un dossier
[06:02] Concrètement, un skill, c'est un dossier avec un fichier skill.md qui va avoir un
[06:04] avec un fichier skill.md qui va avoir un
[06:04] avec un fichier skill.md qui va avoir un nom, une description, des instructions
[06:06] nom, une description, des instructions
[06:06] nom, une description, des instructions et parfois des fichiers de référence et
[06:07] et parfois des fichiers de référence et
[06:07] et parfois des fichiers de référence et des scripts complémentaires. Et ça
[06:09] des scripts complémentaires. Et ça
[06:09] des scripts complémentaires. Et ça fonctionne sous un mécanisme de
[06:10] fonctionne sous un mécanisme de
[06:10] fonctionne sous un mécanisme de divulgation progressif. Ça veut dire que
[06:12] divulgation progressif. Ça veut dire que
[06:12] divulgation progressif. Ça veut dire que l'agent orchestrateur va d'abord lire le
[06:14] l'agent orchestrateur va d'abord lire le
[06:14] l'agent orchestrateur va d'abord lire le nom et la description du skill, puis il
[06:16] nom et la description du skill, puis il
[06:16] nom et la description du skill, puis il va lire le fichier entier seulement s'il
[06:18] va lire le fichier entier seulement s'il
[06:18] va lire le fichier entier seulement s'il estime que la tâche qu'on vient de lui
[06:19] estime que la tâche qu'on vient de lui
[06:19] estime que la tâche qu'on vient de lui demander correspond. [musique] Donc en
[06:20] demander correspond. [musique] Donc en
[06:20] demander correspond. [musique] Donc en résultat, l'agent orchestrateur, il peut
[06:22] résultat, l'agent orchestrateur, il peut
[06:22] résultat, l'agent orchestrateur, il peut disposer d'une multitude de skills sans
[06:25] disposer d'une multitude de skills sans
[06:25] disposer d'une multitude de skills sans encombrer sa mémoire de travail réel,
[06:27] encombrer sa mémoire de travail réel,
[06:27] encombrer sa mémoire de travail réel, son contexte, parce qu'il ne va invoquer
[06:29] son contexte, parce qu'il ne va invoquer
[06:29] son contexte, parce qu'il ne va invoquer les skills que quand il en aura
[06:30] les skills que quand il en aura
[06:30] les skills que quand il en aura réellement besoin. Et depuis le
[06:32] réellement besoin. Et depuis le
[06:32] réellement besoin. Et depuis le lancement des skills, c'est devenu un
[06:33] lancement des skills, c'est devenu un
[06:33] lancement des skills, c'est devenu un standard dans l'industrie de Lia, un
[06:35] standard dans l'industrie de Lia, un
[06:35] standard dans l'industrie de Lia, un standard ouvert, adopté par quasiment
[06:37] standard ouvert, adopté par quasiment
[06:37] standard ouvert, adopté par quasiment tous les acteurs. Au-delà des skills, on
[06:39] tous les acteurs. Au-delà des skills, on
[06:39] tous les acteurs. Au-delà des skills, on peut aussi donner aux sous-agents des
[06:41] peut aussi donner aux sous-agents des
[06:41] peut aussi donner aux sous-agents des accès à des MCP qui vont brancher cet
[06:44] accès à des MCP qui vont brancher cet
[06:44] accès à des MCP qui vont brancher cet agent sur des outils spécifiques. Mais
[06:46] agent sur des outils spécifiques. Mais
[06:46] agent sur des outils spécifiques. Mais un skill, c'est un outil à double
[06:47] un skill, c'est un outil à double
[06:47] un skill, c'est un outil à double tranchant. Il peut t'aider autant qu'il
[06:48] tranchant. Il peut t'aider autant qu'il
[06:48] tranchant. Il peut t'aider autant qu'il peut te nuire. Et ça aussi c'est un
[06:49] peut te nuire. Et ça aussi c'est un
[06:49] peut te nuire. Et ça aussi c'est un phénomène qui est apparu avec les
[06:51] phénomène qui est apparu avec les
[06:51] phénomène qui est apparu avec les derniers modèles frontières parce que au
[06:53] derniers modèles frontières parce que au
[06:53] derniers modèles frontières parce que au début on a eu tendance à créer des
[06:54] début on a eu tendance à créer des
[06:54] début on a eu tendance à créer des skills pour tout et n'importe quoi, mais
[06:55] skills pour tout et n'importe quoi, mais
[06:55] skills pour tout et n'importe quoi, mais on s'est rendu compte que ça pouvait
[06:56] on s'est rendu compte que ça pouvait
[06:56] on s'est rendu compte que ça pouvait aller au détriment de la performance
[06:58] aller au détriment de la performance
[06:58] aller au détriment de la performance d'un modèle. Et d'ailleurs, on a eu
[07:00] d'un modèle. Et d'ailleurs, on a eu
[07:00] d'un modèle. Et d'ailleurs, on a eu plusieurs appels de grande voix dans le
[07:01] plusieurs appels de grande voix dans le
[07:01] plusieurs appels de grande voix dans le domaine de Lia qui nous disaient "Mais
[07:02] domaine de Lia qui nous disaient "Mais
[07:02] domaine de Lia qui nous disaient "Mais supprimez tous vos skills."
[07:03] supprimez tous vos skills."
[07:03] supprimez tous vos skills." Personnellement, j'irai pas jusque là
[07:04] Personnellement, j'irai pas jusque là
[07:04] Personnellement, j'irai pas jusque là parce que je pense que les skills, c'est
[07:05] parce que je pense que les skills, c'est
[07:05] parce que je pense que les skills, c'est aussi votre propriété intellectuelle
[07:07] aussi votre propriété intellectuelle
[07:07] aussi votre propriété intellectuelle unique. Le temps que vous allez passer à
[07:08] unique. Le temps que vous allez passer à
[07:08] unique. Le temps que vous allez passer à construire un skill, un protocole qui
[07:10] construire un skill, un protocole qui
[07:10] construire un skill, un protocole qui correspond exactement à un travail que
[07:12] correspond exactement à un travail que
[07:12] correspond exactement à un travail que vous seul savez faire, c'est en réalité
[07:14] vous seul savez faire, c'est en réalité
[07:14] vous seul savez faire, c'est en réalité hyper précieux. Mais effectivement, les
[07:16] hyper précieux. Mais effectivement, les
[07:16] hyper précieux. Mais effectivement, les conditions qui rendent un skill efficace
[07:17] conditions qui rendent un skill efficace
[07:17] conditions qui rendent un skill efficace aujourd'hui ne sont pas les mêmes que
[07:18] aujourd'hui ne sont pas les mêmes que
[07:18] aujourd'hui ne sont pas les mêmes que quand ce protocole est apparu. Ce qui
[07:20] quand ce protocole est apparu. Ce qui
[07:20] quand ce protocole est apparu. Ce qui marche bien maintenant, c'est d'avoir
[07:21] marche bien maintenant, c'est d'avoir
[07:21] marche bien maintenant, c'est d'avoir des skills courts qui ne contiennent pas
[07:22] des skills courts qui ne contiennent pas
[07:22] des skills courts qui ne contiennent pas trop d'interdiction et qui ne viennent
[07:24] trop d'interdiction et qui ne viennent
[07:24] trop d'interdiction et qui ne viennent pas limiter les capacités du modèle. On
[07:27] pas limiter les capacités du modèle. On
[07:27] pas limiter les capacités du modèle. On a aussi des systèmes comme Hermes agents
[07:29] a aussi des systèmes comme Hermes agents
[07:29] a aussi des systèmes comme Hermes agents qui ont un système de création autonome
[07:31] qui ont un système de création autonome
[07:31] qui ont un système de création autonome des skills où les agents vont créer et
[07:33] des skills où les agents vont créer et
[07:33] des skills où les agents vont créer et améliorer leurs propres skills au gré
[07:35] améliorer leurs propres skills au gré
[07:35] améliorer leurs propres skills au gré des situations rencontrées. Dans mon
[07:36] des situations rencontrées. Dans mon
[07:36] des situations rencontrées. Dans mon expérience, j'ai jamais trouvé ça
[07:37] expérience, j'ai jamais trouvé ça
[07:38] expérience, j'ai jamais trouvé ça incroyablement efficace. Mais dites-moi
[07:39] incroyablement efficace. Mais dites-moi
[07:39] incroyablement efficace. Mais dites-moi en commentaire si vous avez eu une bonne
[07:40] en commentaire si vous avez eu une bonne
[07:40] en commentaire si vous avez eu une bonne expérience avec les skills
[07:42] expérience avec les skills
[07:42] expérience avec les skills autoaméliorant de Hermes agent. Pour ma
[07:44] autoaméliorant de Hermes agent. Pour ma
[07:44] autoaméliorant de Hermes agent. Pour ma part, je pense que la meilleure
[07:45] part, je pense que la meilleure
[07:45] part, je pense que la meilleure approche, c'est de tenir le moins de
[07:47] approche, c'est de tenir le moins de
[07:47] approche, c'est de tenir le moins de skills possible, mais d'avoir des skills
[07:48] skills possible, mais d'avoir des skills
[07:48] skills possible, mais d'avoir des skills extrêmement spécialisés et surtout de
[07:50] extrêmement spécialisés et surtout de
[07:50] extrêmement spécialisés et surtout de s'assurer qu'il n'y ait pas un seul mot
[07:51] s'assurer qu'il n'y ait pas un seul mot
[07:51] s'assurer qu'il n'y ait pas un seul mot en trop à l'intérieur de ces skills.
[07:53] en trop à l'intérieur de ces skills.
[07:53] en trop à l'intérieur de ces skills. Parce que dans mon expérience, plus
[07:54] Parce que dans mon expérience, plus
[07:54] Parce que dans mon expérience, plus votre skill est simple et plus il va
[07:56] votre skill est simple et plus il va
[07:56] votre skill est simple et plus il va être agnostique aux différents modèles
[07:57] être agnostique aux différents modèles
[07:57] être agnostique aux différents modèles et donc il vous permettra de passer de
[07:59] et donc il vous permettra de passer de
[07:59] et donc il vous permettra de passer de Cloud à Chat GPT ou à Gemini sans trop
[08:02] Cloud à Chat GPT ou à Gemini sans trop
[08:02] Cloud à Chat GPT ou à Gemini sans trop de problème. Et par ailleurs, ça va être
[08:03] de problème. Et par ailleurs, ça va être
[08:03] de problème. Et par ailleurs, ça va être douloureux, mais je vous conseille de
[08:04] douloureux, mais je vous conseille de
[08:04] douloureux, mais je vous conseille de passer une après-midi entière à lire
[08:06] passer une après-midi entière à lire
[08:06] passer une après-midi entière à lire chacun de vos skills, surtout si vous
[08:07] chacun de vos skills, surtout si vous
[08:07] chacun de vos skills, surtout si vous les avez obtenu sur l'une des
[08:08] les avez obtenu sur l'une des
[08:08] les avez obtenu sur l'une des bibliothèques publiques parce que le
[08:10] bibliothèques publiques parce que le
[08:10] bibliothèques publiques parce que le skill d'un inconnu, c'est littéralement
[08:12] skill d'un inconnu, c'est littéralement
[08:12] skill d'un inconnu, c'est littéralement le code d'un inconnu que vous allez
[08:13] le code d'un inconnu que vous allez
[08:13] le code d'un inconnu que vous allez exécuter aveuglément sur votre
[08:14] exécuter aveuglément sur votre
[08:14] exécuter aveuglément sur votre ordinateur. Vous pouvez d'ailleurs
[08:16] ordinateur. Vous pouvez d'ailleurs
[08:16] ordinateur. Vous pouvez d'ailleurs auditer en toute simplicité des skills
[08:17] auditer en toute simplicité des skills
[08:17] auditer en toute simplicité des skills avec un modèle frontière en lui
[08:19] avec un modèle frontière en lui
[08:19] avec un modèle frontière en lui demandant tout simplement dans un
[08:20] demandant tout simplement dans un
[08:20] demandant tout simplement dans un prompt. Mais le mieux, c'est votre
[08:21] prompt. Mais le mieux, c'est votre
[08:21] prompt. Mais le mieux, c'est votre vérification personnelle et pourquoi pas
[08:23] vérification personnelle et pourquoi pas
[08:23] vérification personnelle et pourquoi pas n'être dépendant que de vous-même pour
[08:25] n'être dépendant que de vous-même pour
[08:25] n'être dépendant que de vous-même pour créer ces fameux skills. Alors
[08:26] créer ces fameux skills. Alors
[08:26] créer ces fameux skills. Alors justement, comment est-ce qu'on crée un
[08:27] justement, comment est-ce qu'on crée un
[08:27] justement, comment est-ce qu'on crée un skill qui tient la route ? Il y a
[08:28] skill qui tient la route ? Il y a
[08:28] skill qui tient la route ? Il y a évidemment plusieurs méthodes.
[08:29] évidemment plusieurs méthodes.
[08:29] évidemment plusieurs méthodes. Entreopique a publié eux-même Skill
[08:31] Entreopique a publié eux-même Skill
[08:31] Entreopique a publié eux-même Skill Creator qui est un skill qui va créer
[08:32] Creator qui est un skill qui va créer
[08:32] Creator qui est un skill qui va créer d'autres skills, qui a été mis à jour
[08:34] d'autres skills, qui a été mis à jour
[08:34] d'autres skills, qui a été mis à jour plusieurs fois et qui a un protocole de
[08:36] plusieurs fois et qui a un protocole de
[08:36] plusieurs fois et qui a un protocole de mise en place qui est très robuste, qui
[08:37] mise en place qui est très robuste, qui
[08:38] mise en place qui est très robuste, qui permet [musique] aussi de vérifier que
[08:39] permet [musique] aussi de vérifier que
[08:39] permet [musique] aussi de vérifier que la tâche que vous êtes en train
[08:40] la tâche que vous êtes en train
[08:40] la tâche que vous êtes en train d'essayer de formaliser est
[08:41] d'essayer de formaliser est
[08:41] d'essayer de formaliser est effectivement plus efficace avec un
[08:42] effectivement plus efficace avec un
[08:42] effectivement plus efficace avec un skill que 100. Donc skill créateur va
[08:44] skill que 100. Donc skill créateur va
[08:44] skill que 100. Donc skill créateur va avoir plusieurs étapes qui vont vous
[08:46] avoir plusieurs étapes qui vont vous
[08:46] avoir plusieurs étapes qui vont vous permettre de créer un skill. Une
[08:48] permettre de créer un skill. Une
[08:48] permettre de créer un skill. Une excellente méthode également à mon sens.
[08:49] excellente méthode également à mon sens.
[08:49] excellente méthode également à mon sens. Si par exemple vous essayez de créer un
[08:51] Si par exemple vous essayez de créer un
[08:51] Si par exemple vous essayez de créer un skill pour automatiser une tâche que
[08:53] skill pour automatiser une tâche que
[08:53] skill pour automatiser une tâche que vous faites sur votre ordinateur, ça va
[08:55] vous faites sur votre ordinateur, ça va
[08:55] vous faites sur votre ordinateur, ça va être tout simplement d'enregistrer votre
[08:56] être tout simplement d'enregistrer votre
[08:56] être tout simplement d'enregistrer votre écran et d'enregistrer si possible votre
[08:58] écran et d'enregistrer si possible votre
[08:58] écran et d'enregistrer si possible votre voix puis de réaliser cette mission tout
[09:01] voix puis de réaliser cette mission tout
[09:01] voix puis de réaliser cette mission tout en commentant les différentes étapes.
[09:02] en commentant les différentes étapes.
[09:02] en commentant les différentes étapes. Pour moi, [musique] c'est le plus
[09:03] Pour moi, [musique] c'est le plus
[09:03] Pour moi, [musique] c'est le plus efficace notamment si votre skill
[09:04] efficace notamment si votre skill
[09:05] efficace notamment si votre skill intègre du computer use ou l'utilisation
[09:06] intègre du computer use ou l'utilisation
[09:06] intègre du computer use ou l'utilisation d'un navigateur. Et d'ailleurs, il me
[09:08] d'un navigateur. Et d'ailleurs, il me
[09:08] d'un navigateur. Et d'ailleurs, il me semble que Entreopic et Open AI ont tous
[09:10] semble que Entreopic et Open AI ont tous
[09:10] semble que Entreopic et Open AI ont tous les deux intégré ce module de création
[09:12] les deux intégré ce module de création
[09:12] les deux intégré ce module de création par vidéo. Dès que vous utilisez vos
[09:14] par vidéo. Dès que vous utilisez vos
[09:14] par vidéo. Dès que vous utilisez vos skills, si vous vous rendez compte que
[09:15] skills, si vous vous rendez compte que
[09:15] skills, si vous vous rendez compte que le résultat de ce que vous avez produit
[09:17] le résultat de ce que vous avez produit
[09:17] le résultat de ce que vous avez produit n'est pas optimal, profitez-en pour
[09:19] n'est pas optimal, profitez-en pour
[09:19] n'est pas optimal, profitez-en pour corriger l'intelligence artificielle et
[09:21] corriger l'intelligence artificielle et
[09:21] corriger l'intelligence artificielle et après lui demander de modifier votre
[09:23] après lui demander de modifier votre
[09:23] après lui demander de modifier votre skill en conséquence. C'est comme ça que
[09:24] skill en conséquence. C'est comme ça que
[09:24] skill en conséquence. C'est comme ça que vous allez créer un cercle vertueux.
[09:26] vous allez créer un cercle vertueux.
[09:26] vous allez créer un cercle vertueux. Mais attention, rappelez-vous que plus
[09:27] Mais attention, rappelez-vous que plus
[09:27] Mais attention, rappelez-vous que plus vous ajoutez de consignes à l'intérieur
[09:28] vous ajoutez de consignes à l'intérieur
[09:28] vous ajoutez de consignes à l'intérieur de votre skill et plus vous prenez le
[09:29] de votre skill et plus vous prenez le
[09:29] de votre skill et plus vous prenez le risque de détériorer sa qualité. Donc,
[09:31] risque de détériorer sa qualité. Donc,
[09:31] risque de détériorer sa qualité. Donc, il faut toujours trouver le juste
[09:32] il faut toujours trouver le juste
[09:32] il faut toujours trouver le juste équilibre. Mais la concision est la clé.
[09:35] équilibre. Mais la concision est la clé.
[09:35] équilibre. Mais la concision est la clé. Plus vos skills seront courts et plus
[09:36] Plus vos skills seront courts et plus
[09:36] Plus vos skills seront courts et plus ils seront efficaces. Il faut surtout
[09:38] ils seront efficaces. Il faut surtout
[09:38] ils seront efficaces. Il faut surtout pas intégrer dans un skill ce que un
[09:40] pas intégrer dans un skill ce que un
[09:40] pas intégrer dans un skill ce que un modèle frontière sait déjà. Donc la
[09:41] modèle frontière sait déjà. Donc la
[09:41] modèle frontière sait déjà. Donc la meilleure combinaison, c'est de laisser
[09:43] meilleure combinaison, c'est de laisser
[09:43] meilleure combinaison, c'est de laisser Lia rédiger vos skills et de votre côté
[09:45] Lia rédiger vos skills et de votre côté
[09:45] Lia rédiger vos skills et de votre côté de les contrôler, de les relire et les
[09:48] de les contrôler, de les relire et les
[09:48] de les contrôler, de les relire et les trier et sans scrupule pouvoir les
[09:49] trier et sans scrupule pouvoir les
[09:49] trier et sans scrupule pouvoir les supprimer si vous vous rendez compte que
[09:51] supprimer si vous vous rendez compte que
[09:51] supprimer si vous vous rendez compte que en fait ils ne servent plus à rien. Ce
[09:52] en fait ils ne servent plus à rien. Ce
[09:52] en fait ils ne servent plus à rien. Ce temps que vous allez investir sur votre
[09:54] temps que vous allez investir sur votre
[09:54] temps que vous allez investir sur votre bibliothèque de skills, il est
[09:55] bibliothèque de skills, il est
[09:55] bibliothèque de skills, il est inestimable parce que c'est votre
[09:56] inestimable parce que c'est votre
[09:56] inestimable parce que c'est votre savoir-faire, c'est votre propriété
[09:58] savoir-faire, c'est votre propriété
[09:58] savoir-faire, c'est votre propriété intellectuelle portable et vérifiable.
[10:00] intellectuelle portable et vérifiable.
[10:00] intellectuelle portable et vérifiable. C'est votre façon de travailler écrite
[10:02] C'est votre façon de travailler écrite
[10:02] C'est votre façon de travailler écrite noir sur blanc et c'est un format que
[10:03] noir sur blanc et c'est un format que
[10:03] noir sur blanc et c'est un format que vous pouvez emporter d'un outil à
[10:04] vous pouvez emporter d'un outil à
[10:04] vous pouvez emporter d'un outil à l'autre puisque c'est au final un
[10:05] l'autre puisque c'est au final un
[10:05] l'autre puisque c'est au final un fichier skill.md. Donc c'est un fichier
[10:07] fichier skill.md. Donc c'est un fichier
[10:07] fichier skill.md. Donc c'est un fichier texte. Tout est lisible, on peut le
[10:09] texte. Tout est lisible, on peut le
[10:09] texte. Tout est lisible, on peut le vérifier et aujourd'hui les modèles
[10:10] vérifier et aujourd'hui les modèles
[10:11] vérifier et aujourd'hui les modèles frontières concrètement on les loue. On
[10:12] frontières concrètement on les loue. On
[10:12] frontières concrètement on les loue. On les loue à Entropique, on les loue à
[10:13] les loue à Entropique, on les loue à
[10:13] les loue à Entropique, on les loue à Open AI, on les loue à Google, mais vos
[10:15] Open AI, on les loue à Google, mais vos
[10:15] Open AI, on les loue à Google, mais vos skills, vous les posséder pour toujours.
[10:17] skills, vous les posséder pour toujours.
[10:17] skills, vous les posséder pour toujours. Alors comment concrètement vous mettez
[10:19] Alors comment concrètement vous mettez
[10:19] Alors comment concrètement vous mettez en place ce fameux système ? Et bien, en
[10:21] en place ce fameux système ? Et bien, en
[10:21] en place ce fameux système ? Et bien, en réalité, ça ne va pas être si compliqué
[10:22] réalité, ça ne va pas être si compliqué
[10:22] réalité, ça ne va pas être si compliqué que ça. Ce que vous allez faire, c'est
[10:23] que ça. Ce que vous allez faire, c'est
[10:23] que ça. Ce que vous allez faire, c'est que vous allez utiliser l'application
[10:25] que vous allez utiliser l'application
[10:25] que vous allez utiliser l'application desktop de Chat GPT ou de Cloud ou de
[10:27] desktop de Chat GPT ou de Cloud ou de
[10:27] desktop de Chat GPT ou de Cloud ou de Gemini qui sera antiigravity. Vous allez
[10:29] Gemini qui sera antiigravity. Vous allez
[10:29] Gemini qui sera antiigravity. Vous allez aller dans la rubrique Work qui va vous
[10:31] aller dans la rubrique Work qui va vous
[10:31] aller dans la rubrique Work qui va vous permettre de travailler sur des fichiers
[10:32] permettre de travailler sur des fichiers
[10:32] permettre de travailler sur des fichiers de votre propre ordinateur et vous allez
[10:34] de votre propre ordinateur et vous allez
[10:34] de votre propre ordinateur et vous allez tout simplement faire une capture
[10:35] tout simplement faire une capture
[10:35] tout simplement faire une capture d'écran de l'image que je vous mettrai
[10:37] d'écran de l'image que je vous mettrai
[10:37] d'écran de l'image que je vous mettrai sur ma vidéo et vous allez demander à
[10:38] sur ma vidéo et vous allez demander à
[10:38] sur ma vidéo et vous allez demander à votre modèle frontière de vous créer un
[10:40] votre modèle frontière de vous créer un
[10:40] votre modèle frontière de vous créer un skill unique et spécifique à vos propres
[10:43] skill unique et spécifique à vos propres
[10:43] skill unique et spécifique à vos propres cas d'usage qui va mettre en place ce
[10:45] cas d'usage qui va mettre en place ce
[10:45] cas d'usage qui va mettre en place ce mécanisme d'orchestrator. Alors bien
[10:47] mécanisme d'orchestrator. Alors bien
[10:48] mécanisme d'orchestrator. Alors bien sûr, ça n'est qu'un point de départ. Il
[10:49] sûr, ça n'est qu'un point de départ. Il
[10:49] sûr, ça n'est qu'un point de départ. Il y aurait plein d'autres manières de
[10:50] y aurait plein d'autres manières de
[10:50] y aurait plein d'autres manières de mettre cela en place selon la complexité
[10:52] mettre cela en place selon la complexité
[10:52] mettre cela en place selon la complexité du système que vous êtes en train de
[10:53] du système que vous êtes en train de
[10:53] du système que vous êtes en train de produire. Et par ailleurs, si vous
[10:55] produire. Et par ailleurs, si vous
[10:55] produire. Et par ailleurs, si vous utilisez déjà ces modèles frontières, en
[10:57] utilisez déjà ces modèles frontières, en
[10:57] utilisez déjà ces modèles frontières, en réalité, une partie de ce fonctionnement
[10:58] réalité, une partie de ce fonctionnement
[10:58] réalité, une partie de ce fonctionnement sera déjà intégrée. Cette étape-là, elle
[11:00] sera déjà intégrée. Cette étape-là, elle
[11:00] sera déjà intégrée. Cette étape-là, elle va vous permettre de vous assurer que
[11:01] va vous permettre de vous assurer que
[11:01] va vous permettre de vous assurer que l'orchestration aura bien lieu parce que
[11:03] l'orchestration aura bien lieu parce que
[11:03] l'orchestration aura bien lieu parce que certains modèles frontières vont le
[11:04] certains modèles frontières vont le
[11:04] certains modèles frontières vont le faire seul, certes, mais est-ce qu'ils
[11:06] faire seul, certes, mais est-ce qu'ils
[11:06] faire seul, certes, mais est-ce qu'ils vont systématiquement bien le faire ?
[11:07] vont systématiquement bien le faire ?
[11:07] vont systématiquement bien le faire ? J'ai quelques doutes. Pour avoir vu
[11:08] J'ai quelques doutes. Pour avoir vu
[11:08] J'ai quelques doutes. Pour avoir vu notamment Claude utiliser euh des
[11:10] notamment Claude utiliser euh des
[11:10] notamment Claude utiliser euh des sous-agents avec Opus 5. Fable 5.2 pour
[11:13] sous-agents avec Opus 5. Fable 5.2 pour
[11:13] sous-agents avec Opus 5. Fable 5.2 pour des tâches qui ne le méritaient pas,
[11:14] des tâches qui ne le méritaient pas,
[11:14] des tâches qui ne le méritaient pas, j'ai décidé de forcer cette
[11:16] j'ai décidé de forcer cette
[11:16] j'ai décidé de forcer cette orchestration. La deuxième étape, ça va
[11:17] orchestration. La deuxième étape, ça va
[11:17] orchestration. La deuxième étape, ça va être de lister toutes les tâches que
[11:19] être de lister toutes les tâches que
[11:19] être de lister toutes les tâches que vous répétez chaque semaine. Et là, il
[11:20] vous répétez chaque semaine. Et là, il
[11:20] vous répétez chaque semaine. Et là, il va falloir être patient avec vous-même,
[11:22] va falloir être patient avec vous-même,
[11:22] va falloir être patient avec vous-même, réfléchir à vraiment quels sont vos
[11:23] réfléchir à vraiment quels sont vos
[11:23] réfléchir à vraiment quels sont vos irritants, sans se poser de barrières
[11:25] irritants, sans se poser de barrières
[11:25] irritants, sans se poser de barrières techniques pour le moment, réfléchir aux
[11:26] techniques pour le moment, réfléchir aux
[11:26] techniques pour le moment, réfléchir aux tâches que vous menez chaque semaine.
[11:28] tâches que vous menez chaque semaine.
[11:28] tâches que vous menez chaque semaine. Vous pouvez d'ailleurs demander à votre
[11:29] Vous pouvez d'ailleurs demander à votre
[11:29] Vous pouvez d'ailleurs demander à votre modèle habituel d'analyser vos sessions
[11:31] modèle habituel d'analyser vos sessions
[11:31] modèle habituel d'analyser vos sessions passées de ces 30 derniers jours pour
[11:32] passées de ces 30 derniers jours pour
[11:32] passées de ces 30 derniers jours pour essayer d'identifier ces tâches là.
[11:34] essayer d'identifier ces tâches là.
[11:34] essayer d'identifier ces tâches là. Peut-être que ça vous donnera quelques
[11:35] Peut-être que ça vous donnera quelques
[11:35] Peut-être que ça vous donnera quelques idées. Et une fois que vous aurez
[11:36] idées. Et une fois que vous aurez
[11:36] idées. Et une fois que vous aurez identifié ces tâches-là, vous allez
[11:37] identifié ces tâches-là, vous allez
[11:37] identifié ces tâches-là, vous allez choisir les 20 % de ces tâches qui sont
[11:39] choisir les 20 % de ces tâches qui sont
[11:39] choisir les 20 % de ces tâches qui sont les plus importantes. Et là, vous allez
[11:41] les plus importantes. Et là, vous allez
[11:41] les plus importantes. Et là, vous allez créer un skill à la fois pour chacune de
[11:43] créer un skill à la fois pour chacune de
[11:43] créer un skill à la fois pour chacune de ces tâches. Vous allez suivre le
[11:45] ces tâches. Vous allez suivre le
[11:45] ces tâches. Vous allez suivre le protocole de skill creator d'anthropiic
[11:47] protocole de skill creator d'anthropiic
[11:47] protocole de skill creator d'anthropiic ou l'enregistrement d'une vidéo et vous
[11:49] ou l'enregistrement d'une vidéo et vous
[11:49] ou l'enregistrement d'une vidéo et vous allez faire ça minutieusement. Vous
[11:50] allez faire ça minutieusement. Vous
[11:50] allez faire ça minutieusement. Vous allez le faire pour toutes les tâches
[11:52] allez le faire pour toutes les tâches
[11:52] allez le faire pour toutes les tâches qui ont de l'importance et puis ensuite
[11:53] qui ont de l'importance et puis ensuite
[11:53] qui ont de l'importance et puis ensuite vous allez figer votre bibliothèque.
[11:55] vous allez figer votre bibliothèque.
[11:55] vous allez figer votre bibliothèque. Enfin, vous allez tout simplement
[11:57] Enfin, vous allez tout simplement
[11:57] Enfin, vous allez tout simplement utiliser les modèles et vous allez
[11:58] utiliser les modèles et vous allez
[11:58] utiliser les modèles et vous allez améliorer ces skills au fur et à mesure.
[12:00] améliorer ces skills au fur et à mesure.
[12:01] améliorer ces skills au fur et à mesure. Une fois que vous les aurez amélioré, il
[12:02] Une fois que vous les aurez amélioré, il
[12:02] Une fois que vous les aurez amélioré, il faudra aussi les maintenir à chaque
[12:04] faudra aussi les maintenir à chaque
[12:04] faudra aussi les maintenir à chaque nouvelle sortie de modèle ou à chaque
[12:05] nouvelle sortie de modèle ou à chaque
[12:05] nouvelle sortie de modèle ou à chaque fois que vous allez migrer vers un
[12:06] fois que vous allez migrer vers un
[12:06] fois que vous allez migrer vers un nouveau laboratoire, il faudra relire,
[12:08] nouveau laboratoire, il faudra relire,
[12:08] nouveau laboratoire, il faudra relire, tester et supprimer ce qui ne sert plus.
[12:09] tester et supprimer ce qui ne sert plus.
[12:09] tester et supprimer ce qui ne sert plus. Boris Cherny, il conseille même de
[12:11] Boris Cherny, il conseille même de
[12:11] Boris Cherny, il conseille même de repartir de zéro tous les 6 mois. Pour
[12:12] repartir de zéro tous les 6 mois. Pour
[12:12] repartir de zéro tous les 6 mois. Pour lui, il faut même supprimer l'ensemble
[12:14] lui, il faut même supprimer l'ensemble
[12:14] lui, il faut même supprimer l'ensemble de ses skills. Franchement, moi j'irai
[12:15] de ses skills. Franchement, moi j'irai
[12:15] de ses skills. Franchement, moi j'irai pas jusqu'à une solution si extrême,
[12:16] pas jusqu'à une solution si extrême,
[12:17] pas jusqu'à une solution si extrême, mais je pense que vous comprenez le
[12:18] mais je pense que vous comprenez le
[12:18] mais je pense que vous comprenez le principe. Donc, pour ton travail de tous
[12:19] principe. Donc, pour ton travail de tous
[12:19] principe. Donc, pour ton travail de tous les jours, il faut oublier le concept
[12:21] les jours, il faut oublier le concept
[12:21] les jours, il faut oublier le concept dessin d'agent. Ça n'a aucun sens. Ce
[12:22] dessin d'agent. Ça n'a aucun sens. Ce
[12:22] dessin d'agent. Ça n'a aucun sens. Ce qu'il faut, c'est un bon modèle
[12:23] qu'il faut, c'est un bon modèle
[12:23] qu'il faut, c'est un bon modèle orchestrateur qui va invoquer les bons
[12:25] orchestrateur qui va invoquer les bons
[12:25] orchestrateur qui va invoquer les bons sous-agents au bon moment avec les bons
[12:26] sous-agents au bon moment avec les bons
[12:26] sous-agents au bon moment avec les bons skills et les bons outils. Si vous
[12:28] skills et les bons outils. Si vous
[12:28] skills et les bons outils. Si vous mettez ça en place, vous allez avoir des
[12:29] mettez ça en place, vous allez avoir des
[12:29] mettez ça en place, vous allez avoir des résultats phénoménaux et vous n'allez
[12:31] résultats phénoménaux et vous n'allez
[12:31] résultats phénoménaux et vous n'allez pas consommer tout votre usage trop
[12:32] pas consommer tout votre usage trop
[12:32] pas consommer tout votre usage trop rapidement. J'ai mis pas mal de temps à
[12:33] rapidement. J'ai mis pas mal de temps à
[12:33] rapidement. J'ai mis pas mal de temps à préparer cette vidéo. J'espère qu'elle
[12:34] préparer cette vidéo. J'espère qu'elle
[12:35] préparer cette vidéo. J'espère qu'elle vous aura plu. Si c'est le cas,
[12:36] vous aura plu. Si c'est le cas,
[12:36] vous aura plu. Si c'est le cas, n'hésitez pas à mettre un petit pouce
[12:37] n'hésitez pas à mettre un petit pouce
[12:37] n'hésitez pas à mettre un petit pouce bleu pour donner de la force à la
[12:38] bleu pour donner de la force à la
[12:38] bleu pour donner de la force à la chaîne, un commentaire pour me dire ce
[12:39] chaîne, un commentaire pour me dire ce
[12:39] chaîne, un commentaire pour me dire ce que vous en pensez et moi je vous dis à
[12:41] que vous en pensez et moi je vous dis à
[12:41] que vous en pensez et moi je vous dis à très bientôt pour de nouvelles vidéos.
