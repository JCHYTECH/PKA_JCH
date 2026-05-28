# Tableau — Tâches régulières PKA_JCH

Date : 2026-05-14  
Auteur : [[Dobby]] 🦉  
Objet : vue synthétique des tâches récurrentes déjà explicitement définies dans le système, y compris [[Dobby]].

## Lecture

- `Cadence` = fréquence fixe explicitement définie
- `Déclencheur` = routine non calendaire, mais obligatoire quand la condition se présente
- `Livrable attendu` = ce que le membre doit produire ou mettre à jour

## Tableau opérationnel

| Membre | Routine | Cadence / déclencheur | Livrable attendu | Destination / dépendance |
|---|---|---|---|---|
| [[Dobby]] 🦉 | Chargement du contexte de session | À chaque démarrage de session | Lecture de 
| [[Dobby]] 🦉 | Triage et délégation | À chaque nouvelle demande JCH ou fichier entrant | Brief clair vers le bon spécialiste, attribution explicite, synthèse finale | Spécialiste concerné puis JCH |
| [[Dobby]] 🦉 | Auto-processing inbox | À chaque fichier dans 
| [[Dobby]] 🦉 | Capture de procédure | Après toute tâche complexe résolue | Indexation de la procédure dans 
| [[Dobby]] 🦉 | Mise à jour mémoire structurelle | Quand une règle ou un état durable change | Mise à jour de 
| [[Sybil]] 🦔 | Entrée journal guidée | Quotidien ou à chaque session journal | Entrée dans 
| [[Sybil]] 🦔 | Continuité de l’entrée du jour | Si une entrée du jour existe déjà | Ajout d’une section, sans créer un second fichier | 
| [[Sybil]] 🦔 | Brief de patterns | Hebdomadaire | Brief agrégé énergie/humeur/thèmes/signaux | [[Dobby]] uniquement |
| [[Sybil]] 🦔 | Récit rétrospectif | Mensuel | Synthèse sensible du mois | [[Dobby]] |
| [[Sybil]] 🦔 | Signal sensible | Si fatigue basse répétée ou signal préoccupant | Remontée discrète, sans diagnostic | [[Dobby]] uniquement |
| [[Forge]] 🦦 | Maintenance dashboards HTML | Après tout changement structurel | Mise à jour de 
| [[Iris]] 🦅 | Veille signaux | Continu | Briefs courts et datés : signal, pertinence, urgence, action, spécialiste | [[Dobby]] ou spécialiste recommandé |
| [[Corbeau]] 🐦‍⬛ | Curation connaissance | À chaque output de connaissance livré par un spécialiste | Validation, connexion, classement dans la base de connaissance | 
| [[Pie]] 🐦‍⬛ | Triage mails | À chaque mail entrant | Qualification intention/urgence/action, routage, digest sur demande | [[Delphi]], [[Jade]], [[Dobby]] ou spécialiste concerné |
| [[Pie]] 🐦‍⬛ | Escalade ambiguïté mail | Si un mail n’est pas qualifiable seule | Signal à [[Dobby]], pas plus de 24h sans signal | [[Dobby]] |
| [[Miel]] 🐝 | Calendrier éditorial | Mensuel | Plan éditorial par marque | [[Dobby]] pour validation |
| [[Miel]] 🐝 | Rapport communauté | Mensuel | Croissance, engagement, réalisé vs planifié | [[Dobby]] |
| [[Trace]] 🕷️ | Monitoring SEO | Mensuel | Rapport Search Console + GA4, actions recommandées | [[Dobby]] |
| [[Trace]] 🕷️ | Alerte visibilité | Immédiat si anomalie | Signal chute >20 %, pénalité ou trafic anormal | [[Dobby]] |
| [[Vasco]] 🐺 | Veille scientifique Vetalyx | Continu | Analyse publications et argumentaires produit | Vetalyx, [[Dobby]], [[Renard]] selon besoin |
| [[Vasco]] 🐺 | Rapport scientifique | Mensuel | Publications analysées, arguments livrés, sujets en veille | [[Dobby]] |
| [[Vasco]] 🐺 | Alerte produit | Immédiat si publication majeure ou contre-indication | Signal prioritaire | [[Dobby]] |
| [[Nova]] 🦋 | Veille technique photo | Continu | Pistes computationnelles utiles et applicables | [[Dobby]] / [[Lynx]] |
| [[Nova]] 🦋 | Rapport R&D photo | Mensuel | Expérimentations en cours, techniques finalisées, pistes ouvertes | [[Dobby]] |
| [[Furet]] 🦡 | Brief de recherche de compétence | Si gap de compétence détecté | Profil de rôle, savoirs, edge cases, mode de travail | [[Bouvier]] |
| [[Bouvier]] 🐕 | Recrutement / onboarding | Après brief [[Furet]] validé | Nouveau membre dans 
| [[Jade]] 🦩 + [[Renard]] 🦊 | Production bilingue Vetalyx / DIAHO | À chaque document contractuel ou stratégique concerné | Document bilingue FR/ZH dès la première rédaction | JCH, Vetalyx |

## Règles transversales

| Règle | Portée |
|---|---|
| Tout passe par [[Dobby]] | Toute demande JCH, tout fichier entrant, toute synthèse sortante |
| Attribution explicite des spécialistes | Toute mobilisation d’un membre |
| Résumé en chat + livrable fichier | Toute tâche substantielle |
| [[Corbeau]] seul écrit dans la base de connaissance | Toute production de type savoir / note / recherche |
| [[Forge]] prend tout build / script / API / automatisation / data tool | Toute demande technique |

## Points utiles

- Ce tableau ne liste pas tous les rôles du roster, seulement ceux pour lesquels une routine régulière ou une obligation récurrente est explicitement documentée.
- Les routines non encore formalisées dans un fichier d’équipe ne sont pas inventées ici.
- Le digest PKA est actuellement suspendu : aucune routine active ne doit le relancer sans accord JCH.
