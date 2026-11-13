# Audit securite hardware/local PKA_JCH

_Date : 2026-05-13_
_Machine : MacBook Pro de JC_
_Scope : controles non destructifs locaux_

## Synthese

Statut global : **ORANGE**

Le Mac principal est correctement protege cote disque systeme : FileVault est actif. Les risques principaux sont autour de l'environnement : absence de destination Time Machine, volume USB externe ExFAT non chiffre, services reseau ouverts sur toutes les interfaces, synchronisations Dropbox/OneDrive actives, et espace disque Data proche de la saturation.

## Constats

| Controle | Resultat | Niveau | Lecture |
|---|---|---:|---|
| FileVault disque systeme | `FileVault: Yes` | Bon | Le disque systeme est protege en cas de vol de la machine |
| Compte admin | `root`, `jchavauxm5`, `_mbsetupuser` | Moyen | `jchavauxm5` est admin; `_mbsetupuser` est present dans le groupe admin |
| Sessions actives | `console`, `ttys000`, `ttys001` pour `jchavauxm5` | Faible | Rien d'anormal, mais sessions terminal multiples ouvertes |
| Time Machine | `No destinations configured` | Eleve | Pas de backup Time Machine configure |
| Volume externe | `/Volumes/JCH_SMALL`, ExFAT, USB, 2 TB, 79.3% utilise | Eleve | ExFAT n'offre pas de chiffrement macOS natif ni permissions Unix robustes |
| Espace disque Data | `/System/Volumes/Data` a 95% | Moyen | Risque operationnel : lenteurs, erreurs d'ecriture, backups difficiles |
| Thunderbolt/USB4 | Aucun appareil Thunderbolt connecte | Bon | Pas de peripherique Thunderbolt actif detecte |
| Services reseau | Plusieurs services en `*:port` | Moyen | Certains services acceptent potentiellement des connexions LAN |
| Cloud sync | Dropbox et OneDrive actifs | Moyen | Verifier que PKA_JCH, secrets, DB et logs ne sont pas synchronises en clair |
| Protection endpoint | Norton services presents et actifs | Bon | Antivirus/endpoint visible dans launchctl |

## Services reseau observes

| Processus | Ports | Bind | Analyse |
|---|---:|---|---|
| [[Apple]] ControlCenter | 5000, 7000 | 
| 
| Epson Event Manager | 2968 | `*` IPv4 | Service imprimante/scanner; fermer si non utilise |
| Dropbox | 17600, 17603 | `127.0.0.1` | Local uniquement |
| Ollama | 11434, 49155 | `127.0.0.1` | Local uniquement, bon |
| [[Vasco]] Digipass bridge | 42579, 42580 | 
| Adobe Desktop / Creative Cloud | ports divers | `127.0.0.1` | Local uniquement |
| OneDrive | 42050 | `::1` | Local IPv6 uniquement |

## Mitigations recommandees

| Priorite | Action | Pourquoi |
|---:|---|---|
| P0 | Configurer une destination Time Machine chiffree | Aujourd'hui, pas de destination Time Machine active |
| P0 | Ne pas stocker secrets/DB PKA en clair sur `JCH_SMALL` | ExFAT n'a pas de protection robuste; perte du disque = fuite potentielle |
| P0 | Verifier Dropbox/OneDrive : exclure PKA_JCH, `.env`, `*.db`, `*.log` | Eviter synchronisation cloud de donnees sensibles |
| P1 | Desactiver Epson Event Manager au demarrage si les boutons scanner Epson ne sont pas utilises | Service expose sur LAN via port 2968; garder seulement si le workflow scan automatique en depend |
| P1 | Verifier AirPlay/Handoff/partage si non necessaires | `ControlCenter` et `rapportd` ecoutent sur toutes les interfaces |
| P1 | Liberer espace disque interne | 95% sur Data est trop haut; viser < 85% |
| P1 | Examiner `_mbsetupuser` dans admin | Confirmer qu'il est attendu; sinon le retirer proprement |
| P2 | Creer un audit hardware mensuel automatise | Repeter ces controles sans refaire tout manuellement |

## Commandes utilisees

- `diskutil info /`
- `diskutil info /Volumes/JCH_SMALL`
- `who`
- `dscl . -read /Groups/admin GroupMembership`
- `lsof -iTCP -sTCP:LISTEN -n -P`
- `ps -p ... -o pid,user,comm,args`
- `tmutil status`
- `tmutil destinationinfo`
- `system_profiler SPThunderboltDataType`
- `df -h`
- `launchctl print-disabled system`

## Limites

- `systemsetup -getremotelogin` et `systemsetup -getremoteappleevents` ont demande un acces administrateur et n'ont pas retourne l'etat directement.
- `system_profiler SPUSBDataType` n'a pas retourne de detail, mais `diskutil` confirme un volume USB externe monte.

## TODO

- [ ] Desactiver Epson Event Manager au demarrage si JCH confirme que les boutons physiques du scanner/imprimante Epson ne sont pas utilises.
