# Skill: [[analyse-outil-ai]]

Statut: `approved`
Proprietaire: `JCH`
Derniere revue: `2026-05-13`

## Quand l'utiliser

Utiliser cette skill quand JCH demande d'analyser un outil, agent, service, framework ou methode IA pour savoir s'il faut s'en inspirer, l'adapter ou l'integrer.

## Objectif

Produire une analyse claire, utile pour decision, avec les points positifs, points negatifs, risques, couts et options d'adaptation interne.

## Entrees requises

- Nom ou URL de l'outil.
- Besoin interne auquel l'outil pourrait repondre.
- Contexte d'usage si connu: personnel, projet, entreprise, automatisation, dev, [[knowledge]] management.

## Procedure

1. Identifier la source officielle: site, documentation, depot, annonce, licence.
2. Resumer ce que l'outil fait vraiment, sans reprendre le marketing tel quel.
3. Isoler les briques interessantes: architecture, memoire, securite, workflow, UX, integrations, automatisation.
4. Evaluer les points positifs pour nos besoins.
5. Evaluer les points negatifs: complexite, securite, cout, dependance, maturite, maintenance.
6. Distinguer trois options:
   - s'en inspirer sans utiliser l'outil;
   - integrer une brique ou un protocole;
   - utiliser l'outil comme composant separe.
7. Conclure par une recommandation concrete.

## Outils autorises

- Recherche web quand l'information est recente ou que l'URL est fournie.
- Lecture de documentation officielle.
- Lecture de depot public si necessaire.
- Creation d'une proposition de gouvernance si une brique merite adaptation.

## Pieges connus

- Ne pas confondre promesse marketing et capacite prouvee.
- Ne pas recommander une integration complete si une adaptation interne suffit.
- Ne pas ignorer le cout de maintenance.
- Ne pas oublier la securite si l'outil execute des commandes, gere des secrets ou se connecte a des messageries.

## Sortie attendue

Format recommande:

```md
## Resume
## Ce qui est interessant
## Points positifs
## Points negatifs
## Risques
## Cout estime
## Options d'adaptation interne
## Recommandation
## Prochaine action
```

## Criteres qualite

- La recommandation est actionnable.
- Les sources sont citees si l'analyse repose sur des informations externes.
- Les risques sont explicites.
- Les adaptations proposees sont proportionnees a nos besoins.

## Decision JCH

- decision: `approved`
- date_decision: `2026-05-13`
- commentaire: `Validee par JCH comme premiere skill interne pour analyser les outils IA et extraire les briques adaptables.`
