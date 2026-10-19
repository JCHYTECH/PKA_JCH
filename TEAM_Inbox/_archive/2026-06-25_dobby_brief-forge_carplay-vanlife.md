BRIEF — Forge 🔨 — 2026-06-25
════════════════════════════════

PRIORITY : high
DEADLINE : 2026-06-30

MISSION
Créer le parser HTML→JSON pour les fiches voyage de Cigogne et ajouter les commandes CarPlay au bot Telegram.

CONTEXTE
JC veut que les fiches de voyage produites par Cigogne (ex: Wadden_Vanlife.html) soient exploitables dans Google Maps via CarPlay. Le projet CARPLAY-VANLIFE est documenté dans `11_IOT/iot-van/carplay/CARPLAY-VANLIFE.md`. Phase 1 = zéro app iOS, tout passe par le bot Telegram existant + un Shortcut iOS que JC créera sur son iPhone.

ENTRÉES DISPONIBLES
- `11_IOT/iot-van/carplay/CARPLAY-VANLIFE.md` — document projet complet (architecture, phases, spécifications)
- `11_IOT/iot-van/carplay/CARPLAY.md` — archive Gemini avec code Swift complet (91 KB, référence Phase 2 uniquement)
- `07_TRAVELS/Wadden_Vanlife.html` — fiche Cigogne existante avec waypoints GPS (Leaflet, var pts, var routePts)
- `scripts/telegram-bot/bot.py` — bot Telegram existant (Gemini, texte+voix+photos+TTS)
- `scripts/telegram-bot/dobby_context.py` — contexte système du bot

LIVRABLE ATTENDU

1. **`scripts/carplay_parser.py`** — Script Python :
   - Input : chemin vers un fichier HTML produit par Cigogne
   - Parse le bloc `<script>` pour extraire `var pts = [...]` et `var routePts = [...]`
   - Génère un JSON structuré (format dans CARPLAY-VANLIFE.md § Étape 1.1)
   - Construit les URLs Google Maps multi-waypoints pour chaque étape
   - Output : `11_IOT/iot-van/carplay/voyages/{nom}.json`

2. **`scripts/telegram-bot/carplay_commands.py`** — Module Python :
   - `/voyage` — liste les voyages disponibles (scan `voyages/*.json`)
   - `/etape J2` — détails d'une étape (km, temps, spots, restaurants, lien Maps)
   - `/maps J2` — renvoie le lien Google Maps pour une étape (⚠️ doit ouvrir Google Maps, pas Apple Plans)
   - `/suivant` — passe à l'étape suivante du voyage en cours l

3. **`scripts/telegram-bot/carplay_state.py`** — Gestion état :
   - Voyage actif, étape courante, position GPS si fournie
   - Persistance dans `conversation.db` (table `carplay_state`)

4. **Parser fiche Wadden → JSON** comme test de validation

5. **Intégration dans `bot.py`** — enregistrer les nouvelles commandes

DESTINATION
- Scripts dans `scripts/`
- JSON voyage dans `11_IOT/iot-van/carplay/voyages/`
- Rapport de livraison dans `TEAM_Inbox/2026-06-XX_forge_carplay-parser.md`

CONTRAINTES
- Google Maps, pas Apple Plans — les URLs doivent utiliser `https://www.google.com/maps/dir/...` ou le scheme `comgooglemaps://`
- Le format JSON doit être stable — il servira à la Phase 2 (app iOS)
- Le bot Telegram tourne sur M5 en launchd — ne pas casser l'existant
- Les commandes `/camping`, `/alternative`, `/meteo`, `/spot` sont P1 (pas bloquantes pour le test)

INTERACTIONS
- Cigogne 🦩 — pour valider que le parser couvre bien le format de ses fiches
- Dobby 🦉 — pour tester les commandes Telegram
