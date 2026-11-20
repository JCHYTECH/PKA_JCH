# PRÉMORTEM — Politique de protection des comptes et secrets PKA

**Date de rédaction :** 18 novembre 2026
**Horizon simulé :** 18 mai 2027 (6 mois)
**Stance :** Prémortem — avocat de l'échec
**Statut de la politique en mai 2027 :** ABANDONNÉE. `credentials-central.md` toujours en clair, désormais accompagné d'un coffre à moitié rempli. Zéro rotation effectuée.

---

## Le post-mortem (mai 2027)

La politique n'est pas morte d'une attaque. Elle est morte d'un **verrouillage de 71 heures** et du discrédit qui a suivi.

Mois 1 : le coffre chiffré est créé, l'inventaire des comptes maîtres est rédigé en trois lignes. Puis la migration s'arrête. Déplacer 60 secrets hors de `credentials-central.md`, c'est risquer de casser les agents qui lisent ce fichier par chemin codé en dur ; JC ne sait pas lesquels. Il décide de migrer « au fil de l'eau ». Personne ne migre jamais au fil de l'eau. `credentials-central.md` survit donc, amputé de 30 %, encore référencé par deux scripts — et le coffre devient la **deuxième source de vérité**, partielle et divergente. La faiblesse d'origine est intacte, simplement doublée.

Mois 2 : les deux clés physiques sont bien enregistrées sur le compte email. Les codes de secours sont imprimés… et rangés dans le coffre. Personne ne relève la circularité.

Mois 3 : **la clé du trousseau est perdue**. La seconde est au fond d'un tiroir ; il ne le sait plus, parce que l'inventaire n'a jamais dit où sont les clés, seulement quelles clés sont « comptes maîtres ». L'email exige une réauthentification pour une mise à jour de machine. Sans SMS, sans code papier accessible, sans passkey de secours, il est dehors. Trois jours à reconstituer des accès par le support, un mot de passe de coffre oublié dans la panique, deux agents IA hors service.

Mois 4 : la réaction. SMS réactivé en secours, mot de passe maître noté sur un post-it, `credentials-central.md` remis à jour « pour ne plus jamais être bloqué ». Le raisonnement de JC est irréfutable : *on m'avait dit que la hiérarchie stricte était plus sûre, elle m'a coûté trois jours.* La politique n'a pas été combattue : elle a été **jugée sur sa seule mauvaise journée**.

Mois 5-6 : plus aucun rituel. La rotation était de toute façon impossible — un cycle manuel sur 12 comptes et 4 machines dépasse sa capacité, et aucune automatisation n'a été livrée.

## Ce qu'on aurait dû faire autrement

1. **Tuer d'abord, durcir ensuite.** Objectif unique du niveau A : que `credentials-central.md` n'existe plus, un jour daté, avec réécriture des références agents et un test « un agent tourne encore ». Un seul point de vérité, jamais deux.
2. **La reprise avant la serrure.** Écrire et faire exécuter par JC *seul* la procédure « je suis dehors » **avant** de retirer le SMS. Tant que deux clés ne sont pas enrôlées ET la reprise chronométrée, le secours provisoire reste.
3. **Inventaire des lieux, pas des comptes.** Une ligne par clé : qui la détient, dans quel tiroir. Et un binôme humain joignable qui détient la clé #2.
4. **Périmètre étroit.** Niveau B sur deux comptes (email + coffre). Le niveau C, couverture totale théorique, a coûté la crédibilité du reste.
5. **Rotation sur événement, pas au calendrier.** Départ, fuite, appareil perdu. Un rituel annuel de 20 minutes tenu vaut mieux qu'une rotation mensuelle abandonnée.
