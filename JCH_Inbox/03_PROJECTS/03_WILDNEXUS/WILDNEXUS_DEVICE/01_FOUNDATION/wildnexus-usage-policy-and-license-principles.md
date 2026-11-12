# WildNexus — Usage Policy and License Principles

**Version :** v0.3
**Date :** 2026-11-05
**Statut :** cadre de rédaction, pas avis juridique ni texte final
**Propriétaire :** Jean-Claude Havaux — JCHYTECH  
**Owner juridique :** [[Renard]]

## 1. Objet

Ce document cadre la licence du firmware, la politique éthique et les contrats WildNexus. Il ne remplace pas les textes définitifs, les licences des dépendances ni une revue juridique avant publication.

## 2. Décision JCH : MIT + politique éthique

Le firmware WildNexus est destiné à être publié sous **licence MIT**, accompagné d'un fichier `ETHICS.md` et d'une politique d'usage.

Cette direction remplace les anciennes mentions AGPLv3 + licence commerciale et l'expression « dual-license MIT + ETHICS.md ».

Il faut distinguer trois couches :

1. **MIT :** licence de copyright permissive. Elle accorde notamment les droits d'utilisation, modification, fusion, publication, distribution, sous-licence et vente, sous ses conditions de notice.
2. **ETHICS.md et politique d'usage :** expression des valeurs du projet, des usages qu'il refuse et des règles de ses services et partenariats. Ils ne deviennent pas automatiquement des conditions supplémentaires de la licence MIT pour tout tiers en aval.
3. **Contrats :** partenariats, distribution, services, marque et traitement de données peuvent imposer des obligations aux parties contractantes, dans les limites du droit applicable.

Le projet doit donc éviter deux erreurs symétriques : présenter la MIT comme interdisant à elle seule les usages contraires à sa mission, ou présenter `ETHICS.md` comme sans aucune utilité dans la gouvernance et les contrats.

## 3. Ce que l'ouverture doit permettre

Sous réserve des licences propres à chaque objet, le socle doit rester inspectable et reproductible :

- code source, instructions de build et de flash accessibles ;
- schémas, BOM et interfaces documentés ;
- historique de versions et notices de dépendances conservés ;
- contributions externes possibles selon des règles publiques ;
- absence de dépendance binaire opaque non justifiée.

La décision MIT concerne le firmware. Les licences du hardware, de la documentation, des modèles, des datasets et de la marque restent à définir séparément. « Open source » appliqué au code ne signifie pas automatiquement « open hardware » ou données ouvertes.

## 4. Usages proscrits par la politique du projet

Les usages suivants sont incompatibles avec la mission WildNexus et refusés dans ses services, partenariats et distributions officielles :

### Militaire, paramilitaire et sécuritaire

- reconnaissance de terrain ou planification tactique ;
- intégration à un système d'armement ou de police militarisée ;
- surveillance de périmètre ou détection de drones à finalité sécuritaire.

### Atteinte à l'environnement

- braconnage ou repérage de faune pour destruction/capture illicite ;
- contournement de protections environnementales ;
- exploitation des données pour faciliter une atteinte à la biodiversité.

### Exploitation abusive de personnes

- surveillance humaine générale ou profilage ;
- reconnaissance faciale ou identification de personnes ;
- vente ou transmission de captures humaines incidentelles.

Ces proscriptions guident les décisions du projet. Leur opposabilité à un tiers dépend de l'instrument juridique applicable : licence, contrat, marque, conditions de service, droit des données ou autre. Aucune portée juridique n'est présumée.

## 5. Qualification des usages

La matrice `wildnexus-usage-matrix.md` classe les cas selon la politique du projet : autorisé, conditionnel ou interdit.

- **Autorisé :** compatible avec la mission sous réserve du droit local et des règles applicables.
- **Conditionnel :** revue de la finalité, des données, du territoire et du partenaire.
- **Interdit :** refus de partenariat, service ou distribution officielle.

Cette qualification ne réécrit pas les permissions de la MIT. Un fork tiers peut posséder des droits MIT tout en étant refusé comme partenaire officiel ou comme usage conforme à la politique WildNexus.

## 6. Relation avec les contrats et la marque

Les contrats partenaires et commerciaux précisent selon le besoin :

- finalité et usages refusés ;
- règles de distribution et de sous-traitance ;
- confidentialité, RGPD, conservation et sécurité ;
- usage de la marque et interdiction d'apparence d'endorsement ;
- notices, support, garantie et responsabilité ;
- audit, résiliation et traitement des incidents.

Les conditions de services hosted/dashboard peuvent être distinctes de la licence du firmware embarqué.

## 7. Terminologie publique

Formulations correctes :

- « firmware publié sous licence MIT » ;
- « projet accompagné d'une politique éthique et d'usage » ;
- « code inspectable et contributif », si effectivement publié ;
- « hardware/documentation publiés », seulement avec leurs licences propres.

Formulations à éviter :

- « MIT interdit tout usage militaire » ;
- « ETHICS.md est automatiquement contraignant pour tout utilisateur du code » ;
- « licence open source avec restrictions de domaine » comme si le tout restait la MIT/OSI ;
- « open hardware » sans licence matérielle définie ;
- « dual-license » pour décrire MIT + simple politique éthique.

## 8. Gouvernance et livrables avant publication

[[Renard]] et [[Hermine]] préparent la revue ; un conseil externe est mobilisé si nécessaire. JCH valide les choix engageants.

Avant publication :

- texte `LICENSE` MIT avec titulaire et année exacts ;
- `ETHICS.md` et politique d'usage relus ;
- inventaire des dépendances, notices et compatibilités ;
- règles de contribution et de provenance ;
- licences hardware/docs/modèles/données explicitées ou exclusion claire de leur publication ;
- politique de marque et modèles de contrats si nécessaires ;
- cohérence de toutes les fiches et du résumé externe.

## 9. Contrôle d'intégrité

Le dispositif final doit permettre l'auditabilité du socle, exprimer honnêtement la mission, ne pas surstimer la portée juridique de l'éthique et respecter les droits des personnes et des tiers. La mission biodiversité prime, sans transformer une préférence de gouvernance en affirmation juridique fausse.

---

*Révision 2026-11-05 : décision JCH MIT + politique éthique intégrée ; distinction licence, politique et contrats ; anciennes AGPL/dual-license et restrictions automatiques retirées.*
