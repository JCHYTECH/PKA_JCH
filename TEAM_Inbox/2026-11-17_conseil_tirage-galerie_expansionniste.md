# Conseil « pilier tirage / galerie / affiliation » — stance **Expansionniste**

> Dobby 🦉 · conseil du 2026-11-17 · Question motrice : **« Quel upside est-on en train de rater ? »**
> Lecture : `JCH_Inbox/03_PROJECTS/02_ARTEON/strategy/arteon-etat-projet.md`, `.../monetisation-positionnement.md`, `.../analyse-marche-presets.md`, `.../arteon-colonne-vertebrale.md`, `.../plan-action-wildlens.md`, `PHOTO/presets/` (52 XMP), `PHOTO/argus_critique.db`, `TEAM_Inbox/2026-11-16_dobby_conseil-correction-photo_expansionniste.md`.
> Vérifications externes du 17/11 : barèmes d'inscription aux concours photo nature (NPOTY, WPY/NHM, BigPicture, NYPA).

---

## Verdict de stance

**Le cadrage chiffre une boutique. ARTEON est en train de construire une confrérie de photographes naturalistes avec une boutique accrochée dessous — et c'est la confrérie qui vaut de l'argent.**

Le reverse calculation est juste, mais il ne contient qu'un seul terme : `visites × conversion × marge_unitaire`. Quatre des cinq pistes ci-dessous sortent de cette équation : **U1 et U3** ajoutent des revenus qui ne sont pas indexés sur le trafic consommateur (candidatures, membership, B2B, licences), **U2** multiplie la valeur par commande, **U4** divise le CAC en transformant les affiliés en canaux. Aucune ne coûte plus de quelques jours de build : au pire on a dépensé du temps, au mieux on divise par ~3,7 le trafic nécessaire pour la même cible de net — et on rend les 500 €/mois atteignables **sans aucune visite**.

Le point le plus important, et le plus contre-intuitif : **les actifs existants (Argus, Héron, jury) ne sont pas des produits, ce sont des justifications de prix.** Vendus à l'unité (1,90 € l'analyse, « conseil papier ponctuel 60–120 € »), ils restent marginaux. Embarqués dans une édition limitée signée, ils valent ~300 € de premium par vente. C'est l'inverse exact de ce que fait la roadmap actuelle.

---

## Le défaut de cadrage, en une équation

```
Net/mois = V × c × m        ← le cadrage n'optimise que ça
         + R_supply         (photographes qui paient pour entrer / rester)
         + R_B2B            (expositions, licences, murs d'entreprise)
         + R_édition        (AOV × 3,7 à trafic constant)
```

Le cadrage traite `V`, `c` et `m` comme des **données**, alors que ce sont les trois seules variables de croissance. Et il ignore les trois lignes de revenu qui n'ont pas besoin de `V`. Or coût fixe = 51 €/mois : **chaque flux additionnel a un coût marginal quasi nul** (même Shopify, même Ghost, même pipeline Argus). La croissance la moins chère n'est pas en visites — elle est en **revenu par visite** et en **revenu par photographe**.

---

## U1 · Faire payer l'entrée : la galerie est un **concours**, pas un magasin

**Fait vérifié ce jour** : les photographes naturalistes paient déjà, en masse, pour une loterie sans débouché commercial.

- NPOTY : **35 €** pour 20 images (early bird 32 €), 17,50 € pour un portfolio de 6–10 images.
- Wildlife Photographer of the Year (NHM) : **35 £** pour 25 photos.
- BigPicture (California Academy) : **25 $** pour 10 images. New York Photography Awards : 25–40 $/image.

Le ticket d'entrée psychologique du marché est donc **25–35 € par dossier** — et il n'achète aujourd'hui qu'une chance de prix. ARTEON possède l'objet rare qui justifie le même ticket : un **jury de 3 personnes** (déjà prévu) et un **registre du curateur** (déjà dans l'architecture du site, `/affiliation`). La différence avec NPOTY : chez ARTEON, être accepté **ouvre un canal de vente** et une page artiste.

- **Dossier de candidature à 25 € / 10 images** (pré-rapport Argus inclus — coût variable réel ≈ 0,17 $/image, soit ~1,70 € par dossier). Hypothèse prudente : 120 dossiers/an = **3 000 €/an à ~90 % de marge**, l'équivalent de **111 tirages** — sans une seule visite consommateur.
- **Membership « photographe affilié » à 9 €/mois** (page artiste, alertes de vente, recommandations papier Héron, critique Argus mensuelle, rapport de marché). 25 membres en année 1 ≈ **1 350 € sur 6 mois moyens** ; 40 membres = **4 320 €/an récurrent à ~97 %** (coût marginal : un appel Argus + un article Ghost).
- **Ce que ça fait à l'équation** : 500 €/mois de net devient atteignable avec **40 memberships + 10 dossiers/mois — soit zéro visite consommateur** (ou 57 memberships seuls). Le revenu cesse d'être une fonction du trafic, et chaque refus publié augmente la valeur de l'acceptation.
- **Garde-fou obligatoire** (sinon on devient payola et la crédibilité zoologiste, actif racine, meurt) : taux de refus publié chaque trimestre, critères écrits, plafond du nombre de dossiers, remboursement si le dossier n'est pas examiné.

## U2 · Sortir du 120 € unitaire : l'édition limitée signée (AOV × 3,7, trafic constant)

Le tirage ouvert à 120 € a deux défauts structurels que le cadrage ne nomme pas : (a) il est **directement comparable** à WhiteWall en direct et à tout site de print-on-demand — la transparence des prix écrase mécaniquement les 22 % ; (b) il plafonne le net par commande à 27 €, donc il faut ~44 commandes pour 1 200 €/mois.

- **Édition de 12 exemplaires numérotés et signés, certificat + fiche éthique + papier validé par Héron, à 450 €.** À taux de marge constant (22,5 %), une pièce = **~101 € net** ; même en supposant un pass-through WhiteWall de 80 % (le coût progresse plus vite que le prix), on reste à **~90 € net = 3,3× le tirage ouvert**. Trois éditions valent onze tirages.
- **Trafic constant** : sur 20 commandes/mois, un taux de montée en gamme de 15 % = 3 éditions = **+303 € net/mois** au lieu de +81 €.
- **Effet prix** : une pièce numérotée et signée n'est pas comparable. Elle sort le catalogue de la guerre des prix et permet de **remonter le taux de marge** au lieu de le subir — le seul endroit du modèle où la marge peut croître.
- **Effet réputation** : la rareté crée une relation collectionneur (liste d'attente, prévente, second marché). Une clause de revente (5 %) est à arbitrer contre le droit de suite belge : **à ne pas inscrire sans avis juridique**.
- **C'est ici que les actifs se monétisent** : Argus (scores + « pourquoi cette image »), Héron (papier), jury (sélection). Ils ne valent pas 1,90 € l'unité ; ils justifient **+300 €** sur une pièce.

## U3 · Le B2B : une commande = 1 à 2 mois de cible, facturée et sans trafic

Le cadrage ne vend qu'à l'unité, à des particuliers, via un tunnel. Trois offres B2B réutilisent le même catalogue et la même logistique :

- **Exposition clé en main** (20 tirages encadrés + cartels naturalistes + textes de médiation) : **2 500–4 500 €** l'ensemble, part ARTEON 40–50 % ⇒ **1 000–2 000 € net par commande**. Acheteurs : réserves naturelles et parcs, Natagora/DNF, maisons du tourisme et communes, fédérations et clubs photo, festivals nature, lodges et hôtels — et **les clients corporate de VETALYX / DIM3** (vétérinaire, pharma, agro, bureaux d'étude environnement) qui achètent de la nature *documentée* pour leurs murs. Une signature tous les deux mois = **+600 €/mois**, soit plus que la cible entière du cadrage.
- **Licence d'image « naturaliste documentée »** à 3 paliers (web éditorial 45 € / print 180 € / exclusivité territoire-an 900 €). Le différenciateur face à Alamy ou NaturePL n'est pas l'image, c'est **le fichier** : espèce, biotope, comportement, déclaration éthique, EXIF, score Argus. C'est une banque d'images *vérifiée*, dont les contributeurs sont self-service et payés à la commission — pas une rédaction salariée.
- **Index vendable** : la table `analyses` d'Argus (espèce + EXIF + scores) est déjà, en puissance, le moteur de recherche de cette banque. Personne dans la niche ne peut le répliquer sans zoologiste.

## U4 · L'affilié est un **canal d'acquisition**, pas un fournisseur (l'effet de réseau inversé)

Le cadrage traite les photographes comme un approvisionnement à trouver. C'est l'inverse : **chacun est un point de diffusion**. 30 affiliés × ~700 abonnés = **21 000 de portée à CAC zéro**, et un affilié pousse *ses* images avec une énergie qu'aucune campagne ne finance. Les 2 000 visites/mois ne sont pas un budget marketing : c'est un **sous-produit du recrutement** (30 × 70 visites = 2 100).

- **Conséquence sur `c`** : 1 % est un taux de trafic froid sur un catalogue anonyme. Un catalogue curé — page artiste, récit d'espèce, édition limitée — convertit structurellement 2–3×. C'est le seul levier qui améliore le taux sans dépenser un euro de média.
- **Conséquence sur le goulot** : le facteur limitant devient le jury (3 personnes). D'où U1 : Argus pré-filtre les dossiers pour que 12 dossiers/mois restent tenables à trois.
- **Ce qui rend la boucle composée** (et non linéaire) : chaque affilié apporte du catalogue → catalogue plus riche → meilleure conversion → plus d'affiliés intéressés → plus de catalogue. Un tunnel ne compose pas ; un réseau, oui.
- **Contre-mesure indispensable** : code de suivi/UTM par photographe et clause explicite — l'affilié garde son audience, ARTEON garde le client final. Sans ça, le réseau profite à Instagram.

## U5 · La donnée de vente comme oracle (l'actif que personne d'autre n'a)

Croiser les features Argus (espèce, couleur dominante, score d'impact, papier Héron recommandé) avec les ventes réelles produit une connaissance qui n'existe nulle part : **ce qui se vend**, par opposition à ce qui est beau.

- **Usage interne** : calibrage des prix et du catalogue (quelles espèces, quels formats, quels papiers).
- **Usage produit** : « Argus Market Report » mensuel pour les affiliés (« le martin-pêcheur se vend en janvier, le renard en novembre ») — **c'est la justification récurrente des 9 €/mois** de U1.
- **Usage éditorial** : matière gratuite pour WildLens (« les 10 espèces qui se vendent le mieux ») — audience sans temps créatif de JC, exactement le pattern de la « Clinique » du 16/11.
- **Usage licence** : rapport annuel revendable aux labos et marques photo.
- **Réserve factuelle** : `PHOTO/argus_critique.db` est ici un fichier de **0 octet** daté du 2 juillet 2026, alors que `arteon-colonne-vertebrale.md` cite 58 analyses Phase 0 — l'actif data est donc pour l'instant déclaratif. Mais **la décision de schéma coûte 0 € maintenant et est irrécupérable après** : journaliser chaque commande avec les features Argus de l'image dès la première vente. Même logique que la clause A/B du conseil du 16/11.

---

## Ce que ça change à la rentabilité (chiffrage)

Hypothèses : net 27 €/tirage ouvert (donné), ~101 €/édition à 450 €, membership 9 €/mois à 97 %, dossier 25 € à 90 %.

| | **A — cadrage actuel** | **B — composite (mois 6), conversion identique** | **B′ — avec uplift de curation** |
|---|---|---|---|
| Trafic/mois | 2 000 | 1 200 (−40 %) | 1 200 |
| Conversion | 1,0 % | 1,0 % | 1,8 % |
| Commandes/mois | 20 | 12 | ~21 |
| Net retail | 540 € | 11 tirages + 1 édition = **398 €** | 18 tirages + 3 éditions = **789 €** |
| Net supply (memberships + dossiers) | 0 € | **418 €** | **418 €** |
| **Net total /mois** | **540 €** | **816 €** | **1 207 €** |
| Trafic requis pour 1 200 € net | **4 444 visites** | ~2 400 | **~1 200** |
| Trafic requis pour 500 € net | **2 000 visites** | ~300 visites + 40 affiliés | ~170 visites + 40 affiliés |

À **hypothèses de conversion identiques** (2 000 visites/mois, 1 %), le composite fait déjà **×2,2 de net** (1 180 € contre 540 €) : la seule montée en gamme suffit à changer l'ordre de grandeur. Avec l'uplift de curation (1,8 %), c'est **×3,3** — et le trafic nécessaire pour 1 200 € net passe de 4 444 à ~1 200 visites, soit **÷3,7**. Une seule commande B2B (U3) ajoute 600–2 000 € qui ne dépendent d'aucune de ces lignes.

**Ordre de grandeur année 1 (prudent)** : dossiers 3 000 € + memberships 1 350 € + éditions 3 030 € + B2B/licences 3 400 € ≈ **10 800 €**, dont **~7 800 € sans aucune visite consommateur** — contre ~6 000 €/an pour le cadrage actuel, qui exige 24 000 visites/an pour y arriver.

## Classement €/effort (ce qu'il faut faire, dans quel ordre)

| Piste | Revenu an 1 | Marge | Coût marginal | Effort | Verrou |
|---|---|---|---|---|---|
| **U2** Édition limitée | ~3 000 € | 22–45 % | 0 (même WhiteWall) | schéma produit + 1 shoot | signature / expédition physique |
| **U1** Dossiers + membership | ~4 350 € | 90–97 % | Argus + Ghost | 1 page + CGV + grille | taux de refus publié |
| **U3** B2B exposition / licence | ~3 400 € | 40–50 % | 0 | 1 PDF de vente + 10 appels | cycle de vente long |
| **U4** Affiliés = canal | indirect (×2 conversion) | — | 0 | UTM + kit de lancement | recrutement |
| **U5** Donnée de vente | 0 € an 1 | — | ~0 | logging dès J1 | valeur différée |

## Les 4 clauses à coût quasi nul (à inscrire dans la V1, sinon perdues)

1. **Deux prix par œuvre dès la fiche produit** : ouverte + édition de 12. Le schéma doit porter `edition_size`, `edition_number`, `signed`, `certificate_id` — ajoutés après coup, les premières ventes sont des ventes ouvertes non transformables (même mécanique que les paires A/B non capturées du 16/11).
2. **Page `/candidature` payante dès la V1**, même avec trois affiliés. Si la galerie démarre « gratuit pour tous », l'ancre est à 0 et il devient impossible de faire payer un dossier ensuite.
3. **Journaliser chaque commande avec les features Argus de l'image** (espèce, papier Héron recommandé, scores) : c'est U5, et c'est le seul actif que personne dans la niche ne peut copier.
4. **UTM + code affilié par photographe, et clause d'attribution** : l'affilié garde son audience, ARTEON garde le client final (U4) — sinon on finance l'acquisition d'Instagram.

## Ce qui tuerait l'upside

- **Un catalogue mono-artiste** (JC seul, 10 photos) : pas de réseau, pas de sélection, jury décoratif, « concours » inexistant ⇒ U1 et U4 meurent au lancement. **Réseau minimum viable = 8–10 photographes, 3 œuvres chacun, avant l'ouverture publique.**
- **Facturer la candidature sans refuser** : payola. Le taux de refus publié *est* le produit.
- **Un prix unique à 120 €** : l'ancre basse s'installe dès la première vente. L'édition limitée doit exister au lancement, pas « plus tard ».
- **Vendre Argus et Héron à l'unité** (1,90 €) plutôt que de les embarquer comme justification de prix dans l'édition (U2) : on transforme un actif de positionnement en produit de 1,37 € de marge.
