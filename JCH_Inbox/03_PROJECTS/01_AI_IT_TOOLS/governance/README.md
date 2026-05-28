# Gouvernance agent interne

Ce dossier sert a cadrer les briques inspirees d'Hermes Agent que nous voulons adapter en interne.

Principe central: l'assistant propose, JCH decide. Aucune memoire, skill, automation ou permission ne devient active sans une proposition documentee et validee.

## Flux de decision

1. `PROPOSED`: idee documentee, non active.
2. `APPROVED`: validee par JCH, prete a implementer.
3. `ACTIVE`: utilisee par le systeme.
4. `RETIRED`: retiree, conservee en historique.
5. `REJECTED`: refusee, avec raison documentee.

## Ce que chaque proposition doit expliquer

- Pourquoi: probleme traite, gain attendu, risque evite.
- Comment: fonctionnement concret, fichiers, regles, limites.
- Cout: mise en place, maintenance, complexite, cout API/infra.
- Risques: securite, derive, bruit, dette technique.
- Validation: comment savoir que la brique apporte vraiment de la valeur.

## Regle de controle

Le systeme ne doit jamais s'auto-etendre seul. Il peut suggerer une memoire, une skill, une automation ou une permission, mais la decision finale reste manuelle.

## Structure

- `proposals/`: propositions individuelles a arbitrer.
- `decisions/`: registre des decisions prises.
- `templates/`: format standard des futures propositions.

