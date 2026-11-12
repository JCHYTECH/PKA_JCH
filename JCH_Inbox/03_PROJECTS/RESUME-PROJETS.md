# Résumé des projets — PKA_JCH (03_PROJECTS)

> État consolidé le 2026-11-05 à partir des INDEX, threads et fichiers réellement présents.
> Cette vue privilégie les statuts et prochaines étapes vérifiables ; elle n'utilise plus de notes d'avancement arbitraires.
> Référence de pilotage : `../04_PILOTAGE_STRATEGIQUE/etat-projets.md`.

## Portefeuille

Le portefeuille compte **9 projets** : 1 priorité P0 avec échéance, 1 dossier juridique actif, 6 projets actifs autonomes ou en continu, et 1 projet gelé. `10_FUTURE_INVEST` est archivé et ne figure pas dans ce décompte.

| Projet | Statut courant | État établi et prochaine étape | Entrée |
|---|---|---|---|
| **01_AI_IT_TOOLS** | Actif | Socle Dobby opérationnel : 31 spécialistes + Dobby, mémoire, skills et routage multi-modèles. Prototype Grok validé en `exec` ; TUI Grok et invocation utilisateur `/save` Kimi restent à essayer. | [INDEX](01_AI_IT_TOOLS/INDEX.md) · [thread](01_AI_IT_TOOLS/thread-ai-it-tools.md) |
| **02_ARTEON / WildLens** | Actif — relance | 4 étapes de marque terminées sur 13, 8 en attente et 1 rouge. Six fichiers d'édition WildLens sont présents, sans déduire leur publication du nom de fichier. Ghost est en pause après contact du support ; Instagram est préparé sans publication. | [INDEX](02_ARTEON/INDEX.md) · [WildLens](02_ARTEON/wildlens/INDEX.md) · [thread](02_ARTEON/thread-arteon.md) |
| **03_WILDNEXUS** | Gelé — reprise post-van à replanifier | L'architecture P0 et les recherches existent, mais les preuves matérielles, radio, énergétiques et de compatibilité des pipelines manquent. Le gel couvre DEVICE, INSECTNET et NEXUS_ACOUSTIC ; SOP-10 reste suspendue. | [Vue ombrelle](03_WILDNEXUS/README.md) · [INDEX device](03_WILDNEXUS/WILDNEXUS_DEVICE/INDEX.md) |
| **05_PHOTO_AI_JURY** | Actif | La Phase 0 documente 58 analyses, un score moyen de 73,8/100 et 81 % d'acceptation. La base projet contient 52 enregistrements ; la base configurée dans `PHOTO/` est vide. Réconcilier données et chemins avant une nouvelle fournée, puis activer MCP Lightroom. | [INDEX](05_PHOTO_AI_JURY/INDEX.md) · [thread](05_PHOTO_AI_JURY/thread-photo-ai-jury.md) |
| **06_PHOTO_NATURE** | Actif | Workflow terrain et post-traitement en place, 11 presets Argus stockés. Le correctif `headline` du keyworder est confirmé dans le code depuis le 22/10 ; cette revue ne constitue pas un nouveau traitement d'images. | [INDEX](06_PHOTO_NATURE/INDEX.md) · [thread](06_PHOTO_NATURE/thread-photo-nature.md) |
| **07_TRAVELS** | Actif — planification « en roulant » | Le pipeline DÉCOUVERTES et les fiches destinations continuent ; 647 lieux validés sont consignés. La file de 590 éléments est un journal, avec 50 éléments résiduels à traiter, et non 590 éléments en retard. Les aménagements du van restent en cours. | [INDEX](07_TRAVELS/INDEX.md) · [thread](07_TRAVELS/thread-travels.md) |
| **08_VETALYX** | Actif — juridique | MVP allergie IgE chiens/chats, structuration DIAHO et BP V3 documentés. La réponse v4.1 EN est préparée depuis le 29/10, sans preuve d'envoi. Relecture/traduction, mécanique notariale et qualification AFMPS/FAMHP restent ouvertes. | [INDEX](08_VETALYX/INDEX.md) · [legal](08_VETALYX/legal/INDEX.md) · [thread](08_VETALYX/thread-vetalyx.md) |
| **11_IOT** | P0 van — échéance 15/12/2026 | Le HA du van est Healthy/Supported avec mises à jour sélectives ; WiCAN Pro est physiquement installé, mais son intégration HA avec le RUT240 reste à faire. Un RPi bureau sert le pilote Esneux et deux AirGuard sont appairés. Le second dongle est commandé, sa réception n'est pas confirmée. | [INDEX](11_IOT/INDEX.md) · [thread](11_IOT/thread-iot.md) |
| **12_VENTE_OCCASION** | Actif — Phase 1 | Structure et pipeline léger en place, 6 objets en cours, aucun vendu au dernier état consigné. Photos, publication manuelle et suivi restent à poursuivre. | [INDEX](12_VENTE_OCCASION/INDEX.md) · [thread](12_VENTE_OCCASION/thread-vente.md) |

## Relations et limites communes

- **Chaîne photo** : PHOTO_NATURE fournit la matière terrain, PHOTO_AI_JURY les critiques et presets, ARTEON la marque et les services, WildLens l'acquisition éditoriale. Instagram est seulement une couche de découverte préparée.
- **WildNexus** : INSECTNET et NEXUS_ACOUSTIC sont des pipelines associés au projet ombrelle, pas des chantiers réactivés. Leur reprise suit le signal de JCH et les critères du device ; il ne s'agit pas d'une dépendance technique démontrée à l'IOT du van.
- **IOT** : les anciens totaux de 7 ou 8 capteurs ne décrivent pas le même périmètre. La liste du 01/10 contient 10 articles P1, capteurs et éclairage compris, estimés à environ 121 €. Quantités et budget doivent être revalidés avant commande.
- **Argus** : les 58 analyses sont une métrique historique de Phase 0, pas le nombre de lignes actuellement vérifié en SQLite. Aucun fichier n'a été fusionné ou écrasé pendant cette revue.
- **Documents datés** : un nom de fichier, un brouillon ou une cible technique ne prouve ni une publication, ni un envoi, ni une validation matérielle.

## Hors portefeuille actif

- **10_FUTURE_INVEST** : archivé le 2026-06-23 ; dossier laissé tel quel.
- **WILDMESH, Maison off-grid et FAUNE_AUTOUR** : gelés ou conceptuels selon le pilotage global ; ils ne sont pas des projets actifs supplémentaires.

*Sources : INDEX et threads des neuf projets, `hardware-state.md`, `etat-projets.md`, contrôle SQLite en lecture seule et inspection ciblée du keyworder.*
