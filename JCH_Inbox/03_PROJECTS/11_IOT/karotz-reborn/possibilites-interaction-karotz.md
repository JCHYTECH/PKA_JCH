# Possibilités d'interaction Karotz — tour d'horizon communautaire

> Relevé Dobby 🦉 2026-11-10 (recherche web). Ce que les bidouilleurs ont réussi à faire avec le Karotz / Nabaztag, pour guider la suite de l'augmentation.

## 1. Radio / musique internet (pas encore testé chez JC)

- **`PlayRadio.py`** (FreeRabbits/KarotzFiles) : joue un flux radio internet par URL sur le lapin. Le Karotz peut donc servir de **lecteur radio/musique** en plus de la voix.
- Le lapin lit des streams MP3/radio → possibilité : réveil radio, fond musical, notifications sonores custom.

## 2. Appstore FreeRabbits + TimeButton (apps sur le lapin)

- **FreeRabbits.nl/appstore** : un écosystème d'apps qui tourne *par-dessus* OpenKarotz.
- **TimeButton** : reprogramme le **bouton sur la tête** pour déclencher des actions selon l'heure (ex. news à 7h, radio à 9h, dodo à 22h30).
- Apps : lecteur de news, horloge parlante, radio, programmation d'apps à heure fixe.
- → le bouton physique + les oreilles deviennent des **déclencheurs**.

## 3. Intégration Home Assistant (la voie royale)

- **`Desperado88/Home-Assistant-Karotz-2025`** (GitHub) : intégration Karotz sous OpenKarotz pour HA. Retour communauté : « *It's truly amazing to hear my Karotz again, and it's really easy to use* ». (Pas HACS — config côté lapin.)
- **`pantomax/Home-AssistantConfig`** → `packages/nabaztag.yaml` : automatisations pour piloter **LED, oreilles et messages vocaux** depuis HA.
- → le lapin devient une entité `media_player` + capteur de bouton dans HA, pilotable par n'importe quelle automatisation.

## 4. RFID Ztamps / Nanoztags (déclencheurs physiques)

- Le Karotz lit des **badges RFID plats** (Ztamps, « flatnoz »).
- Usage communautaire : badge passé sous le nez → automatisation (jukebox, scène, action domotique).
- C'est le « badge magique » évoqué dans notre README — à câbler via HA (l'endpoint `ztamps` du lapin, à retrouver).

## 5. Remplacement du TTS (voix de qualité)

- **FreeRabbits/KarotzFiles** : fichiers `tts` de remplacement (Acapela mort → **VoiceRSS** ou **ResponsiveVoice**).
- Combine avec notre objectif « vraie voix Dobby » : soit remplacer le TTS du lapin, soit **injecter notre propre audio** (le lapin a `madplay` + on a un shell root via telnet → on peut ajouter un endpoint de lecture custom).

## 6. Accès bas niveau (déjà acquis)

- **Shell root via telnet** (mot de passe `karotz`) + FTP — on peut modifier le firmware (ajouter des CGI, des scripts).
- **Client Python direct** : `dirk-thomas/karotz` (contrôle TCP sans cloud, LED/oreilles/TTS/bouton/RFID).

## Ce que ça ouvre pour « Dobby dans le Karotz »

| Capacité | État chez nous | Prochain pas |
|----------|----------------|--------------|
| Parler (TTS) | ✅ `dobby-speak` | meilleure voix (Piper / remplacement TTS) |
| Oreilles + LED | ✅ | mapper sur des humeurs |
| Radio / musique | ❌ à tester | `PlayRadio.py` |
| Bouton tête | ❌ | TimeButton ou capture d'événement |
| RFID badges | ❌ | retrouver l'endpoint `ztamps` |
| Intégration HA | ❌ | `Desperado88` + pipeline Assist |
| Audio custom (vraie voix Dobby) | ❌ | hack : CGI de lecture + madplay |

## Références

- FreeRabbits.nl — Install Open Karotz, Appstore, KarotzFiles (GitHub)
- `Desperado88/Home-Assistant-Karotz-2025` (GitHub)
- `pantomax/Home-AssistantConfig` → `packages/nabaztag.yaml`
- Forum HA : « Nabaztag/tag, the smart rabbit is back! » (community.home-assistant.io/t/41696)
- `dirk-thomas/karotz` (GitHub, client Python TCP)
