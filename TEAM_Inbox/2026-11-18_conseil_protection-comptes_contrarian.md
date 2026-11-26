# Protection des comptes & secrets PKA — stance CONTRARIAN
## « Qu'est-ce qui va foirer, et pourquoi ? »

**2026-11-18 · Contrarian.** Posture : dire où la politique sera vraie sur le papier et fausse dans les faits, et qui casse — JC, la cérémonie, ou le rituel.

---

## 0. Verdict

La politique protège contre la menace d'une vidéo, pas contre celle qui est **déjà arrivée**. Elle ne tue aucune clé compromise, ajoute un rituel que personne ne portera, et son niveau B fabrique un « à moitié protégé » plus dangereux que l'existant.

---

## 1. La règle (1) est un faux soulagement

`credentials-central.md` est **déjà hors git**. Mais le dépôt GitHub est **public** (`MEMORY.md:591`) et la purge d'historique n'a jamais été tranchée : cinq secrets exposés, dont une clé `sk-…`. Un coffre **ne tue pas les clés déjà publiées** ; seule la rotation le fait — et la rotation est rangée au **niveau C**, qu'on repoussera. Effet pervers : JC croit le sujet clos et arrête de regarder.

**Piste :** ligne zéro du niveau A = **rotation des 5 secrets exposés**, *puis* coffre.

---

## 2. L'« inventaire vivant » meurt en trois semaines

35 fichiers Markdown pointent vers `credentials-central.md`, dont des consignes d'agents. Déplacer le fichier casse ces chemins : agents en échec, runbooks qui mentent. JC fera la seule chose rationnelle à court terme — **garder une copie en clair « pour que les scripts marchent »**. Deux sources de vérité, un coffre périmé, et l'illusion qu'il est à jour : plus aucune vérification.

**Piste :** pointeur stable au même chemin (« voir coffre X, entrée Y ») + un **propriétaire de secours** : à 70 ans et mainteneur unique, le rituel trimestriel est la première chose abandonnée.

---

## 3. Le demi-FIDO est plus dangereux que pas de FIDO

6 à 8 comptes souverains × 2 clés = ~14 cérémonies. Abandon réaliste : 2 comptes faits, la clé de secours **au tiroir, non enrôlée partout**. JC se croit protégé et cesse de surveiller — alors qu'un enrôlement unique est une perte **irréversible par construction**. Le niveau B achète une confiance non méritée ; l'insécurité actuelle, elle, ne ment pas.

**Piste :** règle (3) **binaire par compte** — 2 clés enrôlées et prouvées, ou étiquette « non protégé ».

---

## 4. « Pas de SMS en secours » : un verrouillage

La hiérarchie ignore la Belgique réelle : banques, eID/itsme, administrations n'offrent souvent **pas** FIDO2. Couper le SMS avant enrôlement complet = lock-out nocturne d'un non-technique qui ne lira pas la procédure. Le niveau C « couverture totale » est **inatteignable** : JC conclura que la politique est fausse, pas les services.

**Piste :** ordre écrit (clés → codes imprimés → *puis* retrait SMS) + rollback + « qui débloque à 23 h ». Une **préférence**, pas un dogme.

---

## 5. L'automatisation (C) est le canal de fuite

Les agents ont **déjà** recopié des fragments de clés dans des fichiers versionnés. Un agent qui peut tourner une clé peut aussi l'écrire dans un log. Donner l'écriture sur le coffre à 4 agents pour 5 secrets : gain nul, risque nouveau.

---

## 6. Ce que la politique ne couvre pas

FileVault est **off sur l'iMac**, Time Machine sauvegarde le fichier en clair, des fichiers voisins sont en **0644** (`gmail_app_password.txt`, `kimi_key.tx`). Le coffre ne corrige **aucun** de ces chemins. Et le risque dominant à 70 ans n'est pas l'attaquant : c'est l'**incapacité** — sans héritier ni instructions scellées, 2 clés + 1 coffre = perte totale pour la famille.

---

## 7. Recommandation

**A + rotation des secrets exposés + un test de reprise réel sur UN compte** (la boîte mail, jamais la banque). B ensuite, compte par compte. **C : jamais** — de la complexité achetée contre le risque qu'elle crée.
