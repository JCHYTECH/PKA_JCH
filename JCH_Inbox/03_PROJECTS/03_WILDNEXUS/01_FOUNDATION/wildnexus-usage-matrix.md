# WildNexus — Usage Matrix

**Version :** v0.1 DRAFT  
**Date :** 2026-05-17  
**Statut :** Draft de travail  
**Propriétaire :** Jean-Claude Havaux — JCHYTECH  
**Owner juridique :** [[Renard]]

---

## 1. Purpose

Cette matrice transforme les principes WildNexus en décisions simples de qualification d'usage.

Elle sert à :
- qualifier rapidement un cas d'usage
- guider la rédaction de la licence et de la politique d'usage
- aider au tri des partenaires, distributeurs et demandes entrantes
- éviter les ambiguïtés entre mission écologique et exploitation technique

Les trois statuts sont :
- **Autorisé** : compatible par défaut avec la mission
- **Conditionnel** : possible sous conditions explicites, revue et validation
- **Interdit** : incompatible avec la mission et refusé

---

## 2. Matrix

| Cas d'usage | Statut | Conditions / limites | Rationale | Owner validation |
|---|---|---|---|---|
| Naturaliste individuel utilisant WildNexus sur terrain privé ou autorisé | Autorisé | Respect du droit local et du RGPD | Cas d'usage cœur du projet | Aucun, hors support standard |
| Association naturaliste déployant un petit réseau local | Autorisé | Respect des obligations terrain et données | Aligné avec la mission biodiversité | Aucun, hors support standard |
| Réserve naturelle, commune rurale, ONG environnementale | Autorisé | Cadre légal local, signalétique si nécessaire | Aligné avec mission et impact | Aucun, hors support standard |
| Université ou institut de recherche sur biodiversité | Autorisé | Respect de la politique d'usage et du RGPD | Usage scientifique compatible | Aucun, hors support standard |
| Contribution technique au code, hardware ou documentation | Autorisé | Respect des règles de contribution et de la licence | Communauté contributive voulue | Maintainers WildNexus |
| Reproduction d'un nœud pour usage personnel ou recherche compatible | Autorisé | Respect intégral de la licence et de la politique d'usage | Auditabilité et reproductibilité du socle | Aucun |
| Intégration d'un capteur additionnel orienté biodiversité | Autorisé | Documentation minimale des interfaces | Extensibilité voulue par design | Maintainers techniques |
| Revente / distribution par partenaire commercial orienté nature | Conditionnel | Contrat, reprise des exclusions d'usage, usage de marque contrôlé | Compatible si l'alignement mission est maintenu | [[Renard]] + JCH |
| Déploiement par bureau d'études environnementales | Conditionnel | Vérification du contexte client et des usages finaux | Peut être aligné, mais dépend des missions réelles | [[Renard]] |
| Utilisation par administration publique non militaire | Conditionnel | Vérifier finalité réelle, gouvernance des données, cadre RGPD | Potentiellement compatible, mais sensible selon usage | [[Renard]] + JCH |
| Intégration dans une plateforme logicielle tierce | Conditionnel | Pas de contournement des exclusions d'usage, pas de fermeture abusive | Compatible seulement si la mission et la conformité restent intactes | [[Renard]] + owner technique |
| Hébergement ou service managé autour de WildNexus | Conditionnel | Contrat, politique de données, exclusions reprises | Acceptable si pas de dérive surveillance/fermeture | [[Renard]] + JCH |
| Utilisation sur sites accueillant du public | Conditionnel | Signalétique, base légale, traitement des images humaines conforme | Sensibilité RGPD accrue | [[Renard]] |
| Export ou partage de données agrégées avec tiers | Conditionnel | Pas de données humaines identifiantes, cadre d'usage clair | Compatible si gouvernance des données maîtrisée | [[Renard]] + JCH |
| Programme de recherche dual-use avec acteur défense | Interdit | Aucune exception | Risque de dévoiement militaire | Refus automatique |
| Détection de drones | Interdit | Aucune exception | Explicitement contraire à NN-05 | Refus automatique |
| Surveillance de périmètre, sécurité de site, protection d'infrastructure | Interdit | Aucune exception | Usage sécuritaire non compatible avec la mission | Refus automatique |
| Reconnaissance de terrain à finalité tactique | Interdit | Aucune exception | Finalité militaire/paramilitaire | Refus automatique |
| Usage pour police militarisée ou maintien de l'ordre armé | Interdit | Aucune exception | Incompatible avec exclusions d'usage | Refus automatique |
| Braconnage, repérage de faune pour destruction ou capture illicite | Interdit | Aucune exception | Contraire à la mission biodiversité | Refus automatique |
| Surveillance humaine générale ou profiling de personnes | Interdit | Aucune exception | Contradictoire avec NN-09 et RGPD | Refus automatique |
| Reconnaissance faciale ou identification humaine | Interdit | Aucune exception | Hors mission, risque juridique élevé | Refus automatique |
| Vente ou transmission d'images de personnes capturées incidentalement | Interdit | Aucune exception | Incompatible RGPD et mission | Refus automatique |
| Fermeture propriétaire d'une version dérivée en contradiction avec la licence | Interdit | Aucune exception | Détruit le caractère publiable et auditabilité du socle | [[Renard]] |

---

## 3. Escalation Rules

Un cas passe automatiquement en **Conditionnel** ou en revue renforcée s'il présente au moins un des signaux suivants :
- acteur public, institutionnel ou grand compte avec finalité floue
- traitement d'images humaines possible ou fréquent
- usage proche de la sécurité, de la surveillance ou du contrôle d'accès
- intégration commerciale à grande échelle
- usage international dans une juridiction sensible
- ambiguïté sur la finalité écologique réelle

Un cas passe automatiquement en **Interdit** s'il présente au moins un des signaux suivants :
- finalité militaire ou para-militaire
- finalité sécuritaire offensive ou défensive
- atteinte probable à la biodiversité
- surveillance humaine incompatible avec la mission
- volonté explicite de contourner les exclusions d'usage

---

## 4. Decision Workflow

1. Identifier l'utilisateur réel et l'usage final, pas seulement l'intermédiaire.
2. Qualifier le cas avec la matrice.
3. Si `Autorisé`, appliquer le flux standard.
4. Si 
5. Si `Interdit`, refuser sans entrer en négociation sur une exception.

Pour les cas `Conditionnels`, la revue documente au minimum :
- acteur
- usage final
- données traitées
- zone géographique
- risques RGPD
- risque de dérive mission
- décision et justification

---

## 5. Immediate Uses Of This Matrix

Cette matrice doit être utilisée pour :
- la première note de licence WildNexus
- la future `usage policy`
- le tri des partenaires et distributeurs
- les FAQ publiques sur ce qui est permis ou non

---

*Document de travail — WildNexus usage matrix — v0.1 DRAFT*
