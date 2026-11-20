# Analyse de transcript — « Tes mots de passe ne suffisent plus : voici comment vraiment protéger tes comptes »

> **Procédure** : `/analyse-transcript` — 3 blocs (Comprendre / Confirmer / Conseiller)
> **Analyste** : Dobby 🦉 (orchestrateur PKA_JCH) — mandat du 2026-11-18
> **Transcript source** : `JCH_Inbox/00_INBOX/2026-11-14_transcript-tes-mots-de-passe-ne-suffisent-plus-voici-commen.md`
> **Couverture de lecture** : 100 % du fichier — 1 056 segments (00:01 → 17:09), dédupliqués en 529 unités de texte utile pour l'analyse
> **Verdict en une phrase** : contenu solide et mesuré sur le fond (la clé FIDO2 matérielle = plus haut niveau d'authentification grand public), à classer en référence technique `01_AI_IT_TOOLS` avec 3 actions P0 directement applicables au « système de protection » de JCH.

---

## 1. Comprendre

### 1.1 Nature

| Attribut | Valeur |
|---|---|
| **Type** | Vidéo YouTube — tutoriel + vulgarisation, avec démonstration écran à partir de [13:18] |
| **Durée** | 17:11 |
| **Langue** | Français |
| **Chaîne / auteur** | Julien Guilloux |
| **Date de publication** | 2026-11-14 |
| **URL** | https://www.youtube.com/watch?v=xtjEEcjLWY8 |
| **Source du transcript** | Sous-titres YouTube auto (1 056 segments ; légères imperfections : répétitions glissantes, mots tronqués — ex. « pourquoi les clés de sécurité sont plus ? » à [02:35] pour « plus sécurisées ? ») |
| **Format** | Monologue face caméra [00:01–13:18] + screencast de configuration réelle [13:18–17:09] |
| **Niveau** | Grand public non technique — l'auteur dit explicitement « pour les moldus » [04:52] et traduit « fonction mathématique » par « moulinette » [04:54] |

**Positionnement dans une série.** Ce n'est pas un contenu isolé : l'auteur renvoie à au moins cinq épisodes antérieurs de sa propre chaîne —

- le SIM swap → [00:58]
- les applications d'authentification (TOTP) → [01:27]
- les passkeys → [02:31]
- la boîte mail Tuta déjà présentée → [13:59]
- le hardware wallet et sa sauvegarde → [17:04]

La vidéo est donc le **maillon « clé physique / FIDO2 »** d'une progression assumée : mot de passe → SMS → application d'authentification → passkey → **clé de sécurité**. Elle s'adresse à quelqu'un qui a déjà gravi les deux premiers étages.

**Style.** Pédagogie par analogie et par démonstration ; pas de peur, pas de FUD. L'auteur désamorce lui-même le sensationnalisme de son titre (voir §2.3).

### 1.2 Thèse

Le mot de passe seul est structurellement compromettable **à distance** (fuite de base, phishing, logiciel espion), et tous les seconds facteurs ne se valent pas : seule une **clé de sécurité matérielle FIDO2** oppose à l'attaquant une barrière physique non exportable, ce qui la rend à la fois résistante au phishing et inexploitable en cas de piratage du service en ligne.

Le prix à payer est un **confort moindre** — il faut porter l'objet, l'enrôler partout, et sa perte est irréversible — d'où la règle centrale de la vidéo : **ne jamais n'enrôler qu'une seule clé, toujours au moins deux** [11:20–12:00].

### 1.3 Points clés (faits, arguments, noms, chiffres)

#### A. Le problème — pourquoi le mot de passe ne suffit plus [00:01–02:00]

- **Trois vecteurs de compromission à distance** cités explicitement : fuites de données, campagnes de phishing, logiciels espions [00:17–00:24].
- **Réutilisation = amplification du dégât** : le pirate rejoue le mot de passe « sur le plus de sites possible » [00:31] (credential stuffing, non nommé comme tel).
- **Codes par SMS — deux failles citées** [00:49–01:05] :
  - interception au niveau du réseau mobile [00:51–00:56] ;
  - **SIM swap** : le pirate se fait passer pour la victime auprès de l'opérateur et fait porter son numéro sur une nouvelle carte SIM [00:58–01:05].
- **Codes par email — pire encore** [01:06–01:21] : si la boîte mail est compromise, le pirate reçoit **tous** les codes *et* peut réinitialiser les mots de passe de tous les services rattachés à cette adresse — « là il ouvre la boîte de Pandore » [01:12–01:19]. C'est l'argument le plus fort de cette section.
- **Applications d'authentification (TOTP)** = « beaucoup plus sécurisées » que SMS/email [01:28–01:32], mais deux limites : **ne protègent pas du phishing** [01:32–01:34] et les codes peuvent être lus si le smartphone est corrompu [01:34–01:38].
- **Nuance explicite de l'auteur, à ne pas perdre** : « ces solutions augmentent **drastiquement** la sécurité… même si tu as le code par SMS, c'est toujours beaucoup plus sécurisé de ne rien avoir » [01:40–01:52]. Le message n'est donc **pas** « le SMS ne sert à rien ».

#### B. Les clés de sécurité — principe [02:01–03:36]

- Objet électronique utilisé **au moment de la connexion** [02:06–02:10], sous plusieurs formes [02:04].
- **Deux modes d'usage** [02:12–02:29] :
  1. **second facteur** : identifiant + mot de passe, puis validation par la clé ;
  2. **passkey** : la clé **remplace** le mot de passe.
- Raison de la supériorité : les secrets sont stockés dans un **« élément sécurisé »**, petit composant électronique conçu pour que les secrets **ne puissent pas être extraits à distance, ni même physiquement** [02:40–02:58].
- Conséquence côté attaquant : il lui faut **l'objet physique *et* le code/PIN ou l'empreinte** qui le déverrouille [02:58–03:13].
- Bascule de nature : d'une sécurité **logicielle** à une sécurité **matérielle** [03:22–03:30].
- **Annonce de l'avantage anti-phishing** [03:30–03:36], démontré plus loin.

#### C. La mécanique cryptographique [03:44–07:24]

- Socle : **cryptographie asymétrique** [03:44–03:48].
- **Enrôlement** [03:56–04:25] : exemple avec une **YubiKey** de la marque **Yubico** [03:57–04:01] sur un compte **Google** — connexion aux paramètres, ajout d'une clé, branchement, sélection, **contact tactile pour confirmer**.
- **Génération** [04:25–04:45] : la clé génère un nombre aléatoire dans un intervalle « astronomiquement grand » ; l'auteur illustre par « beaucoup plus probable de gagner plusieurs fois d'affilée à l'Euro Millions » [04:36–04:43]. *Aucun chiffre, aucun nombre de bits n'est donné.*
- Ce nombre = **clé privée** [04:45–04:48], passé dans une « fonction mathématique » / « moulinette » [04:50–04:54] pour produire la **clé publique** [04:56–04:58].
- **Propriété clé, énoncée comme « très importante »** [05:00–05:18] : la clé privée permet de retrouver la clé publique, **jamais l'inverse** — « ça va dans un sens mais pas dans l'autre ».
- **Une paire de clés par service** [05:38–05:52] : enrôler la clé sur un autre service génère **un autre couple** clé privée/publique. La clé privée **reste dans la clé de sécurité**, ne sort jamais ; seule la clé publique est transmise au service [05:52–06:06].
- **Connexion** [06:16–06:55] : branchement USB ou approche **NFC** du smartphone [06:21–06:25] ; le service envoie un **défi** (*challenge*) = nombre aléatoire **différent à chaque connexion** [06:28–06:32] ; la clé **signe** le défi avec la clé privée [06:34] ; le service **vérifie** la signature avec la clé publique [06:37–06:42].
- Seule cette clé peut produire une signature valable [06:42–06:55] ; **anti-replay** : une ancienne signature ne peut pas être réutilisée [06:55–07:06].
- **Bonus de confidentialité** : si le service est piraté, le hacker n'obtient qu'une **clé publique totalement inutilisable** pour se connecter [07:06–07:24].

#### D. Pourquoi ça bloque le phishing [07:27–08:19]

- Scénario : l'utilisateur arrive sur un **faux site répliquant Google** [07:33–07:41].
- Le navigateur transmet à la clé **l'origine annoncée** (google.com) mais **l'URL réelle diffère** de celle enregistrée lors de l'enrôlement [07:43–08:00].
- La clé **refuse alors de produire une signature valable** → la connexion échoue → l'attaquant ne récupère rien [08:00–08:10].
- Conclusion de l'auteur : « même si je vais sur un faux site, il ne pourra rien m'arriver » [08:12–08:19]. *(Formulation absolue — voir claim C14 en §2.2.)*

#### E. Avantages — les quatre énumérés [08:21–10:01]

1. **2FA plus sécurisé que tous les facteurs classiques** [08:31–08:38] ; pour les comptes **les plus critiques**, « c'est encore mieux que les passkeys qu'on utilisera avec des gestionnaires de mots de passe qui vont utiliser un cloud » [08:40–08:49].
2. **Sécurité matérielle** : les secrets ne sont pas stockés par des solutions logicielles mais par quelque chose **qu'il faut avoir physiquement sur soi** ; « la marge de manœuvre pour un attaquant est beaucoup plus réduite » [08:49–09:20].
3. **Aucun secret partagé en ligne** [09:20–09:46] : un mot de passe est connu du service et devient réutilisable s'il fuit ; avec une clé, le service ne détient qu'une **clé publique inexploitable**.
4. **Reconnaissance par les autorités** : « les autorités de cybersécurité considèrent que les clés de sécurité sont les moyens d'authentification **FIDO** les plus robustes » [09:48–10:01]. *Aucune autorité n'est nommée.*

#### F. Inconvénients — les deux assumés [10:03–12:09]

1. **Moins agréable à utiliser** [10:10–10:27] : il faut enrôler la clé **sur chaque service** et l'avoir **avec soi** à chaque connexion.
2. **Le plus important** [10:29–12:09] : **si tu perds la clé, tu perds les accès qu'elle contient**. Aucune sauvegarde n'est possible **par construction** — sauvegarder supposerait de pouvoir extraire les secrets, ce qui rouvrirait exactement la porte que la protection matérielle referme [10:39–11:05]. La récupération existe mais est « pénible, tu perds du temps » [11:13–11:19].
3. **D'où la règle** [11:20–12:00] : **toujours au moins deux clés** — une clé du quotidien + une **clé de secours** enrôlée **sur chaque service au même moment**. Les deux portent des identifiants différents mais donnent accès aux mêmes comptes.
4. **Retournement assumé** : « ce côté moins pratique, c'est aussi ce qui fait que c'est une solution plus sécurisée » [12:02–12:09].

#### G. Les limites que la clé ne couvre pas [12:09–13:18]

- **Poste infecté** : la clé protège *la connexion*, pas *la session*. Sur un ordinateur compromis, un pirate peut **voler la session une fois la connexion établie** [12:12–12:23].
- **Le facteur le plus faible annule les autres** : si le **SMS reste activé en méthode de secours**, l'attaquant passera par là plutôt que d'attaquer la clé [12:23–12:45]. « Il ne va pas s'embêter à contourner le système le plus compliqué, il va passer par ce qu'il y a de plus simple » [12:45–12:55].
- **Recommandation dérivée** : ne **pas** laisser SMS et clé de sécurité cohabiter sur un compte [12:33–12:43].
- **Limite anthropique** : la clé ne protège pas de « la plus grosse faiblesse de tous les systèmes informatiques » — l'humain, « entre la chaise et le clavier » [13:07–13:16].

#### H. Démonstration et matériel [13:18–17:09]

- **Matériel utilisé pour la démo** : un **hardware wallet** de cryptomonnaies, le **OneKey Pro 2** [13:30–13:46 ; 16:30–16:32] — choisi parce qu'il a un **écran** (plus confortable), mais « exactement le même fonctionnement » [13:32–13:38]. Justification : les portefeuilles crypto reposent déjà sur la cryptographie asymétrique, donc beaucoup savent aussi servir de clé de sécurité [13:46–13:54].
- **Cible de la démo** : une **boîte mail**, considérée comme « le centre de mon activité en ligne » [13:59–14:10] — argument de priorisation intéressant.
- **Prérequis vérifié** : le service doit supporter les clés de sécurité ; « spoiler, oui, c'est le cas pour la majorité » [14:13–14:19]. *(Affirmation non étayée — voir claim C20 en §2.2.)*
- **Chemin dans Tuta** : Paramètres → Connexion → authentification à deux facteurs → ajouter → mot de passe → brancher la clé → déverrouiller → choisir « clé de sécurité » → nommer (**laissé « U2F » par défaut** [14:59 ; 15:25]) → sauvegarder → confirmer sur l'appareil [14:26–15:18].
- **Reconnexion** : le service demande la clé, la détecte, l'utilisateur signe le challenge envoyé par Tuta avec la clé privée, Tuta vérifie avec la clé publique — « c'est pas plus compliqué que ça » [15:27–15:57].
- **Modèles recommandés** [15:59–16:19] : **YubiKey** (Yubico) = la référence ; **Titan** de Google ; « il y en a encore plein d'autres ». Critère retenu : **vérifier la réputation** ; à défaut d'avis éclairé, « les YubiKeys, c'est très bien ».
- **Astuce anti-dépense inutile** [16:20–16:42] : la plupart des hardware wallets (**Ledger**, **Trezor**, OneKey) peuvent servir de clé de sécurité.
- **Exception notée par l'auteur** [16:42–17:09] : les produits **Ledger** permettent une **sauvegarde** — ce qui « va contre le principe des clés de sécurité » vu plus haut, mais rend la restauration possible en cas de perte.

#### I. Ce que la vidéo ne traite pas (périmètre réel)

- **Aucun chiffre** dans toute la vidéo : ni nombre de bits / d'entropie, ni **prix** d'une clé, ni statistique de compromission.
- **Aucune source citée** : ni autorité (ANSSI, CISA, NIST), ni étude, ni lien.
- **Pas de vocabulaire normatif** : la vidéo dit « FIDO » et « U2F », jamais **FIDO2** ni **WebAuthn/CTAP2**. Le « U2F » laissé comme nom de clé [14:59] est le nom du protocole **FIDO1** — daté, mais sans conséquence pratique (simple libellé d'affichage).
- **Pas de codes de secours** : les *recovery codes* à imprimer ne sont jamais évoqués, alors qu'ils sont le filet de sécurité central en cas de perte.
- **Pas de gestionnaire de mots de passe** en tant que tel : mentionné uniquement comme support de passkeys cloud [08:46–08:49] pour dire qu'il est *moins* robuste qu'une clé physique — sans jamais rappeler qu'il est **indispensable** avant de passer aux passkeys (mots de passe uniques par site).
- **Pas de menace ciblée / APT**, pas de durcissement de poste, pas de sauvegarde, pas de gestion du cycle de vie (révocation, inventaire).

---

## 2. Confirmer

### 2.1 Tableau de classement

Légende : ✅ **Établi** (mécanisme normé ou consensus documenté) · ⚠️ **Affirmé par l'auteur** (plausible mais non sourcé, ou dépendant du contexte) · ❓ **Non prouvé** (invérifiable en l'état, aucune source)

| # | Revendication | Repère | Classe | Commentaire |
|---|---|---|---|---|
| C1 | Un mot de passe peut être récupéré à distance (fuites, phishing, spyware) | [00:17–00:24] | ✅ | Consensus. Les trois vecteurs sont correctement nommés. |
| C2 | Réutiliser le même mot de passe amplifie le dégât (rejeu sur d'autres sites) | [00:25–00:33] | ✅ | C'est le *credential stuffing*, mécanisme majeur documenté. |
| C3 | Le code par SMS peut être intercepté au niveau du réseau mobile | [00:51–00:56] | ✅ | Vrai mais **rare** hors IMSI-catcher / SS7 ciblé. Détail non nuancé. |
| C4 | Le code par SMS peut être contourné par SIM swap | [00:56–01:05] | ✅ | Vecteur réel et documenté, en hausse. |
| C5 | Un code par email est pire : la boîte compromise donne tous les codes **et** les réinitialisations | [01:06–01:21] | ✅ | Raisonnement exact : la boîte mail est le compte-souche. |
| C6 | Les applications TOTP sont plus sûres que SMS/email | [01:27–01:32] | ✅ | Consensus. |
| C7 | Les codes TOTP ne protègent pas du phishing | [01:32–01:34] | ✅ | Un site de phishing relaie le code en temps réel. |
| C8 | Toute 2FA (même SMS) vaut mieux que pas de 2FA | [01:40–01:52] | ✅ | Position standard des autorités. |
| C9 | Une clé de sécurité porte un « élément sécurisé » dont les secrets ne sont extractibles ni à distance ni physiquement | [02:40–02:58] | ✅ *(nuance)* | Vrai par conception pour les clés FIDO2 de qualité (secure element). « Ni physiquement » est une **garantie de coût**, pas une impossibilité absolue : des attaques par injection de fautes existent, mais restent très coûteuses et non scalables. |
| C10 | Il faut l'objet **et** un code/PIN ou une empreinte pour l'utiliser | [02:58–03:13] | ✅ | Le PIN/biométrie ne quitte jamais la clé — correctement expliqué ensuite. |
| C11 | Sécurité **matérielle** vs **logicielle** = marge de manœuvre réduite pour l'attaquant | [03:22–03:30] | ✅ | Argument de fond correct. |
| C12 | La clé privée ne sort jamais ; seule la clé publique est transmise au service | [05:52–06:06] | ✅ | Cœur du modèle FIDO2. |
| C13 | La clé privée permet de retrouver la clé publique, jamais l'inverse | [05:00–05:18] | ✅ | Propriété des fonctions à sens unique. |
| C14 | Le défi change à chaque connexion → une ancienne signature n'est pas réutilisable | [06:55–07:06] | ✅ | Anti-replay. **Mais** sa conclusion « même si je vais sur un faux site, il ne pourra rien m'arriver » [08:12–08:19] est **absolue** : un phishing en temps réel peut toujours tromper l'utilisateur, et un poste infecté permet le vol de session — ce que l'auteur reconnaît lui-même plus loin [12:12–12:23]. Légère tension interne. |
| C15 | Un site piraté ne fuit qu'une clé publique inexploitable | [07:06–07:24] | ✅ | Vrai pour les credentials FIDO. Le service détient toutefois les **métadonnées** et, pour les comptes non-FIDO, les mots de passe. |
| C16 | La clé bloque le phishing car l'origine enregistrée ne correspond pas au faux site | [07:43–08:10] | ✅ | *Origin binding* / RP ID. Vulgarisation correcte. |
| C17 | Le nombre aléatoire a une entropie telle qu'on ne retombe jamais dessus — « plus probable de gagner plusieurs fois l'Euro Millions » | [04:25–04:45] | ⚠️ | Ordre de grandeur **plausible** (~256 bits), mais **aucun chiffre n'est donné** : la comparaison est illustrative, pas démontrée. |
| C18 | Les clés de sécurité sont plus sûres que les passkeys synchronisées en cloud, **pour les comptes critiques** | [08:40–08:49] | ⚠️ | Position **défendable et répandue** (une passkey synchronisée est répliquée dans un compte cloud, donc dépend de la sécurité de ce compte), mais ni universelle ni sourcée : les passkeys stockées dans l'enclave du téléphone sont aussi *phishing-resistant*. À traiter comme **opinion argumentée**, pas comme fait établi. |
| C19 | « Les autorités de cybersécurité considèrent les clés FIDO comme les plus robustes » | [09:48–10:01] | ✅ *(fond)* / ⚠️ *(forme)* | Fond exact : le FIDO2 matériel est la référence des recommandations « phishing-resistant MFA ». Mais **aucune autorité n'est nommée** — faiblesse de forme. |
| C20 | « La majorité » des boîtes mail supportent les clés de sécurité | [14:13–14:19] | ❓ | Non étayé. Vrai pour Gmail, Outlook, Proton, Tuta, Fastmail ; **faux ou incertain** pour beaucoup de petites messageries, d'offres FAI et d'Exchange on-prem. À vérifier service par service. |
| C21 | Aucune sauvegarde possible d'une clé de sécurité (par construction) | [10:39–11:05] | ✅ | Vrai pour les credentials **non exportables**. Le raisonnement (sauvegarde ⇒ extraction ⇒ faille) est juste. |
| C22 | Perdre sa clé = perdre ses accès ; la récupération est pénible | [10:33–11:19] | ✅ | Réel. Nuance : la plupart des services offrent des **codes de secours**, que l'auteur n'évoque pas. |
| C23 | Règle : toujours enrôler **au moins deux** clés | [11:20–12:00] | ✅ | Recommandation standard, correctement motivée. |
| C24 | Ne pas laisser le SMS comme méthode de secours quand une clé est active | [12:33–12:55] | ✅ | Évite l'attaque par **downgrade** vers le facteur le plus faible. |
| C25 | La clé ne protège pas d'un poste infecté (vol de session) | [12:12–12:23] | ✅ | Vrai et important — honnêteté de l'auteur sur cette limite. |
| C26 | « La plus grosse vulnérabilité se trouve entre la chaise et le clavier » | [13:07–13:16] | ⚠️ | Doxa de sécurité de l'information, non quantifiée. Principe, pas fait mesuré. |
| C27 | Les hardware wallets (Ledger, Trezor, OneKey) peuvent servir de clé de sécurité | [13:30–13:54 ; 16:20–16:42] | ✅ *(variable)* | Vrai pour de nombreux modèles via FIDO2/U2F — **mais dépend du modèle et du firmware**. Présenté un peu trop comme général. |
| C28 | Les produits Ledger permettent une sauvegarde, donc une restauration des accès en cas de perte | [16:42–17:09] | ⚠️ | **Nuance importante** : ce qui est sauvegardable est la *seed* du wallet crypto, pas le credential FIDO2. Restaurer la seed ne ré-enrôle pas automatiquement la clé auprès du service — il faut **ré-enrôler**. L'auteur laisse entendre une restauration plus large qu'elle ne l'est. |
| C29 | La clé de sécurité peut servir de passkey pour **remplacer** le mot de passe | [02:25–02:29] | ✅ | Correct (FIDO2 resident credentials). Formulé rapidement, mais juste. |
| C30 | « Spoiler : la majorité » des services acceptent les clés de sécurité | [14:13–14:19] | ❓ | Même remarque que C20. Réalité très hétérogène selon les secteurs (banque française en particulier : souvent TOTP/SMS uniquement). |

**Bilan du classement** : sur 30 revendications importantes, **21 sont établies**, **7 sont des affirmations de l'auteur non sourcées mais plausibles**, **2 ne sont pas prouvées** (support des clés par « la majorité » des services). Aucune revendication **fausse** n'a été relevée. Le socle technique (FIDO2 / cryptographie asymétrique / anti-phishing) est exact.

### 2.2 Les trois points où il faut corriger ou nuancer l'auteur

1. **« Il ne pourra rien m'arriver » sur un faux site** [08:12–08:19] — trop absolu. La clé empêche le **vol du secret** et la **réutilisation** de la signature, elle n'empêche pas un **phishing en temps réel** (l'utilisateur valide lui-même) ni le **vol de session** sur un poste compromis (que l'auteur reconnaît à [12:12–12:23]).
2. **La sauvegarde Ledger** [16:42–17:09] — la seed restaure le **wallet crypto**, pas le credential FIDO2 enrôlé chez un service tiers. Le bénéfice réel est plus étroit que ce que la formulation suggère.
3. **« La majorité des boîtes mail supportent les clés »** [14:13–14:19] — à vérifier au cas par cas. Pour un usage PKA, cette affirmation doit être remplacée par un **test réel par service**.

### 2.3 Contrepoints et nuances portés par l'auteur lui-même (à ne pas perdre)

L'auteur est nettement moins sensationnaliste que son titre. Il dit explicitement :

- **Le SMS reste utile** : « c'est toujours beaucoup plus sécurisé de ne rien avoir » [01:50–01:52] — toute 2FA est un progrès.
- **Les applications TOTP sont déjà un vrai progrès** [01:28–01:32], pas un pis-aller méprisable.
- **La clé n'est pas parfaite** : il consacre plus de deux minutes à ses inconvénients [10:03–12:09], dont un qualifié de « le plus important » (la perte).
- **La clé ne protège pas de tout** : poste infecté, facteur de secours dégradé, erreur humaine [12:09–13:18].
- **Le confort sacrifié est le prix de la sécurité** [12:02–12:09] — il l'assume plutôt qu'il ne le déplore.
- **Pas d'obligation d'acheter** : il montre comment réutiliser un hardware wallet déjà possédé pour éviter « une dépense inutile » [16:38–16:42].

**Conséquence pour l'analyse** : le titre (« tes mots de passe ne suffisent plus ») est une accroche ; le **corps** du propos est un guide d'hygiène raisonnable, avec une hiérarchie des facteurs assumée et des limites explicites. Il ne faut donc **pas** en tirer un discours alarmiste du type « tout est compromis ». Le sous-texte opérationnel est : *tes comptes critiques méritent un facteur matériel, et le vrai risque est la perte, pas l'attaque*.
---

## 3. Conseiller

### 3.1 Routing PKA

| Destination | Contenu | Justification |
|---|---|---|
| **`JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/99_REFERENCES/protection-comptes_2026-11-14/`** *(chemin réel — le préfixe `03_PROJECTS/…` de la consigne est relatif à `JCH_Inbox/`)* | `transcript.md` (transcript dédupliqué) + `analyse-dobby.md` (ce document) + `inventaire-comptes-souverains.md` + `tableau-migration-2fa.md` | Même convention que `danger-modeles-ia-locaux_2026-11-15/`, `karpathy-hackertube_2026-11-14/`, `tv-privacy-acr_2026-11-07/` : un dossier par source dans `99_REFERENCES/` |
| `01_AI_IT_TOOLS/INDEX.md` | 1 ligne dans le tableau « Structure » ou une entrée de référence | Traçabilité de la source |
| `04_PILOTAGE_STRATEGIQUE/instructions-systeme.md` | Règle « 2 clés physiques minimum + pas de SMS en secours » | Élément de gouvernance personnelle durable |
| `11_IOT/` + `JCH_PRIVATE/` | **Pas de ce transcript** — le sujet y est transverse ; les décisions vont dans `04_PILOTAGE` | Éviter la duplication |

### 3.2 Impact croisé sur les projets

| Projet / actif | Impact | Pourquoi |
|---|---|---|
| `01_AI_IT_TOOLS` (socle) | 🔴 **Critique** | Le PKA repose sur des prestataires cloud (GitHub, fournisseurs LLM, Google/Apple). La compromission d'un compte « souverain » (mail, GitHub, gestionnaire) compromettrait l'ensemble des agents et automatisations. C'est le nœud à protéger en premier. |
| `JCH_PRIVATE/credentials-central.md` | 🔴 **Critique** | Voir §3.3 — ce fichier contient des **mots de passe en clair** (comptes Home Assistant, WiFi du van, etc.). Le sujet n'est pas couvert tel quel par la vidéo, mais c'est la faiblesse la plus flagrante du « système de protection » actuel. |
| `~/.config/pka-jch/api_keys` (0600) | 🔴 **Critique** | Bonne pratique (permissions 0600) mais **secret local en clair, non chiffré, non sauvegardé et sans rotation**. Une clé API fuitée = accès facturé. Les clés FIDO2 ne le protègent pas : c'est un sujet **coffre de secrets**, pas authentification. |
| `11_IOT` (Home Assistant M5 / Lupo) | 🟡 **Élevé** | HA expose des comptes locaux (M5 Docker, Lupo RPi). La règle « ne jamais exposer HA publiquement » + Tailscale est la bonne réponse architecturale. HA ne supporte **pas nativement** les clés FIDO2 → la cible réaliste est **TOTP + mot de passe unique en coffre**, pas une YubiKey. |
| `02_ARTEON`, `08_VETALYX`, `10_FUTURE_INVEST`, `12_VENTE_OCCASION` | 🟡 **Élevé** | Comptes à composante financière/juridique (banque, plateformes, marchés publics, dépôts de vente). Candidats naturels à une clé physique **si le service le supporte** — souvent limité en France (TOTP/SMS dominant côté banque). |
| `03_WILDNEXUS` (devices, firmware, cloud) | 🟡 **Élevé** | Chaînes d'outils et comptes fournisseurs (fabricants, comptes développeur). Un compte de build compromis compromet des devices. |
| `05_PHOTO_AI_JURY`, `06_PHOTO_NATURE`, `07_TRAVELS` | 🟢 **Modéré** | Comptes secondaires, faible rayon d'impact. Les passkeys suffisent ; clé physique non prioritaire. |
| Guard anti prompt-injection / gouvernance agents | 🟢 **Modéré** | La vidéo ne traite pas ce sujet. Le lien est indirect : un **poste de travail infecté** contourne le meilleur facteur ([12:12–12:23]) — donc l'hygiène de la machine qui héberge les agents reste dans le périmètre. |
| Sauvegardes / reprise après sinistre | ⚪ **Hors scope vidéo** | Aucun contenu sur la sauvegarde. À traiter séparément. |

### 3.3 Captures de connaissance — recommandations concrètes et actionnables

#### a) Hiérarchie des facteurs (à retenir telle quelle)

```
Faible  ──────────────────────────────────────────────────►  Fort
SMS / email  <  TOTP (app)  <  passkey synchronisée  <  passkey matérielle / clé FIDO2
   ↑ phishing      ↑ phishing      ↑ phishing-resistant      ↑ phishing-resistant
   ↑ SIM swap      ↑ poste/mobile   mais répliquée en cloud    secret non exportable
```

**Règle PKA** : *on ne descend jamais dans cette échelle ; on ne mélange jamais deux étages sur un même compte* (pas de SMS en secours d'une clé).

#### b) Le concept structurant : les comptes « souverains »

Un **compte souverain** est un compte dont la compromission permet de récupérer tous les autres. Chez JCH, l'inventaire probable tient en 6 à 8 lignes :

1. la **boîte mail principale** (celle qui reçoit les réinitialisations) — l'auteur la nomme « le centre de mon activité en ligne » [14:03–14:10] ;
2. l'**identifiant Apple** (MacBook + iPhone = facteur de confiance implicite) ;
3. le **compte Google** ;
4. le **gestionnaire de mots de passe** (s'il n'existe pas encore : c'est le prérequis n°1) ;
5. **GitHub** / forge de code (souvent lié aux déploiements) ;
6. le **domaine + DNS / registrar** ;
7. les **comptes bancaires en ligne** ;
8. le **compte Tailscale / accès distant** (car il commande l'accès au réseau PKA).

*Méthode de vérification* : pour chacun, se demander « si quelqu'un prend ce compte, qu'est-ce qu'il peut réinitialiser d'autre ? ». Tout compte dont la réponse dépasse « ce compte seul » est souverain.

#### c) Les règles issues de la vidéo, directement transposables

| Règle | Source | Application JCH |
|---|---|---|
| **Deux clés physiques minimum, enrôlées ensemble** | [11:20–12:00] | 1 clé au quotidien (trousseau) + 1 clé de secours **hors du domicile** (coffre, proche, ou boîte sécurisée) — pas les deux au même endroit, sinon la règle ne sert à rien. |
| **Aucun SMS/email en méthode de secours** dès qu'une clé est active | [12:33–12:55] | À faire **après** l'enrôlement des 2 clés, jamais avant — sinon on se verrouille dehors. |
| **Codes de secours imprimés et stockés hors-ligne** | *lacune de la vidéo* | À générer service par service et à ranger avec la clé de secours. **C'est le filet que la vidéo oublie.** |
| **Vérifier que le service supporte FIDO2 avant de compter dessus** | [14:13–14:19] | À tester réellement : HA, banque, plateformes métier. |
| **Un hardware wallet existant peut servir de clé** | [16:20–16:42] | Évite un achat si JCH possède déjà un Ledger/Trezor. Vérifier le support FIDO2 **du modèle exact**. |
| **La clé ne protège pas d'un poste infecté** | [12:12–12:23] | L'hygiène du MacBook (mises à jour, pas de sideload, mot de passe de session, FileVault) reste dans le périmètre. |

#### d) Le cas particulier des secrets PKA (hors périmètre de la vidéo, mais prioritaire)

La vidéo traite de **l'authentification aux comptes en ligne**. Elle ne traite pas du **stockage de secrets applicatifs** — or c'est là que se situe la faille la plus concrète du PKA :

- `JCH_PRIVATE/credentials-central.md` contient des mots de passe **en clair** (plusieurs comptes Home Assistant, réseaux WiFi du van, etc.) ;
- `~/.config/pka-jch/api_keys` est protégé par les permissions (0600) mais reste du **texte clair** : pas de chiffrement au repos, pas de versioning de rotation.

**Ce qu'il faut retenir** : une YubiKey ne corrige **pas** ces deux points. La réponse adaptée est un **coffre chiffré** (gestionnaire de mots de passe, macOS Keychain verrouillé, ou `age`/`sops` + une clé maîtresse déverrouillée par passkey matérielle). Les deux sujets sont **complémentaires** : la clé physique déverrouille le coffre, le coffre protège les secrets — mais dans cet ordre de mise en œuvre, le coffre est **plus urgent**.

#### e) Ce qu'il ne faut PAS acheter / PAS faire

- **Ne pas acheter de clé avant d'avoir un gestionnaire de mots de passe** : une clé sans mots de passe uniques par site ne protège presque rien (le mot de passe reste réutilisé et phishable par ailleurs).
- **Ne pas enrôler une seule clé** « pour tester » sur un compte critique.
- **Ne pas activer la clé sur un service dont on n'a pas d'abord généré les codes de secours**.
- **Ne pas compter sur la clé pour le poste de travail** ni pour les secrets locaux (cf. §3.3.d).

### 3.4 Actions priorisées

| ID | Priorité | Action | Responsable | Critère de done |
|---|---|---|---|---|
| **A1** | 🔴 **P0** | **Auditer et coffrer les secrets PKA** : sortir les mots de passe en clair de `JCH_PRIVATE/credentials-central.md` vers un coffre chiffré, ne laisser dans le fichier que des **pointeurs** (`→ coffre : entrée « HA M5 »`). Idem pour `~/.config/pka-jch/api_keys` (chiffrement au repos + note de rotation). | **Dobby** (proposition + script de migration) → **JCH** (validation) | Plus aucun secret en clair dans un fichier versionné ; `credentials-central.md` ne contient plus que des références. |
| **A2** | 🔴 **P0** | **Établir l'inventaire des comptes souverains** (cf. §3.3.b) et l'état 2FA actuel de chacun (aucun / SMS / email / TOTP / passkey / clé). | **JCH** (accès) + **Dobby** (tenue du tableau) | `inventaire-comptes-souverains.md` rempli, 100 % des lignes avec un état 2FA daté. |
| **A3** | 🔴 **P0** | **Enrôler 2 clés FIDO2** sur les 3 comptes souverains les plus critiques (boîte mail principale, identifiant Apple, GitHub *ou* Google), **puis** désactiver SMS/email en secours, **puis** générer et imprimer les codes de secours. | **JCH** | 3 comptes avec 2 clés enrôlées + codes de secours imprimés + SMS désactivé. |
| **A4** | 🟠 **P1** | **Créer la fiche de référence** `99_REFERENCES/protection-comptes_2026-11-14/` : transcript dédupliqué + cette analyse + tableau de migration. | **Dobby** | Dossier créé, 3 fichiers, ligne ajoutée dans `INDEX.md`. |
| **A5** | 🟠 **P1** | **Tester le support FIDO2 par service réel** (HA, banque, plateformes métier) et consigner le résultat — ne pas se fier à « la majorité » de la vidéo (claim C20/C30). | **Dobby** | Colonne « support FIDO2 vérifié » complétée dans l'inventaire, avec la date du test. |
| **A6** | 🟠 **P1** | **Formaliser la règle de gouvernance** : « comptes souverains = 2 clés minimum, pas de SMS en secours, codes de secours hors-ligne » dans `04_PILOTAGE_STRATEGIQUE/instructions-systeme.md`. | **Dobby** (rédaction) → **JCH** (validation) | Règle présente dans le fichier de gouvernance et référencée depuis `MEMORY.md`. |
| **A7** | 🟡 **P2** | **Étendre la couverture** : passkeys matérielles ou clés sur les comptes secondaires (photo, travels, vente). | **JCH** | Couverture ≥ 80 % des comptes de l'inventaire avec un facteur non-SMS. |
| **A8** | 🟡 **P2** | **Tester la reprise après perte** : simuler la perte de la clé principale sur **un compte non critique** (ex. compte photo) et restaurer l'accès avec la clé de secours + codes. | **JCH** | Procédure de restauration écrite et validée une fois, sans perte de compte. |
| **A9** | 🟡 **P2** | **Vérifier le support FIDO2 d'un hardware wallet déjà possédé** (Ledger/Trezor) pour éviter un achat. | **JCH** | Décision écrite : achat de 2 YubiKey **ou** réutilisation. |
| **A10** | ⚪ **P3** | **Note de veille** : rattacher ce sujet aux épisodes amont de la série (SIM swap, TOTP, passkeys) quand ils seront analysés, pour constituer une référence « hygiène numérique » cohérente. | **Dobby** | Entrée de veille créée. |

### 3.5 Réserves à porter au dossier

- **La vidéo n'est pas une source normative.** Aucune autorité n'est citée, aucun chiffre n'est donné. Pour un usage PKA durable, il faudra **adosser les règles à une source primaire** (documentation FIDO Alliance / WebAuthn, recommandations d'une autorité nationale) au moment de rédiger la règle de gouvernance (A6).
- **Le contexte français est plus contraignant que la vidéo ne le laisse croire.** L'écosystème bancaire et administratif français est encore majoritairement TOTP/SMS. La stratégie réaliste est **hétérogène** : clé physique là où c'est possible, TOTP ailleurs, jamais rien.
- **Le risque n°1 identifié pour JCH n'est pas couvert par la vidéo** : les secrets applicatifs stockés en clair (A1). C'est l'action à traiter en premier, indépendamment de tout achat de matériel.

---

*Fin de l'analyse — 3 blocs traités, 30 revendications classées, 10 actions priorisées.*
