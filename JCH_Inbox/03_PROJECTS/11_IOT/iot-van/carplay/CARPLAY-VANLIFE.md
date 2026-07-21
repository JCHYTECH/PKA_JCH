# CARPLAY-VANLIFE — Projet CarPlay pour le Stylevan Equinox IV

> **Date :** 2026-06-25 — Dobby 🦉  
> **Statut :** Phase 0 — Conception  
> **Parent :** 11_IOT / iot-van  
> **Spécialistes :** Forge (#12), Cigogne (#28)  
> **Source :** `JCH_Inbox/00_INBOX/CARPLAY/CARPLAY.md` (conversation Gemini brute — 1 535 lignes)

---

## Vision JC

> « Les fiches créées par Cigogne contiennent des données et un parcours GPS. Grâce à CarPlay, les étapes dessinées à l'origine seraient affichées dans Google Maps CarPlay avec la possibilité de choisir des alternatives en roulant, en parlant avec Dobby via Siri connecté à Telegram. »

**En clair :**
1. Avant le départ → Cigogne produit une fiche voyage (ex: Wadden_Vanlife.html)
2. Au volant → les waypoints de la fiche apparaissent dans Google Maps via CarPlay
3. En roulant → JC parle à Siri → Siri relaie à Telegram → Dobby répond (alternatives, météo, camping)
4. Dobby peut modifier le trajet en temps réel (nouveaux waypoints poussés vers Google Maps)

---

## Architecture cible

```
┌─────────────────────────────────────────────────────────────────┐
│                        AVANT LE DÉPART (M5)                      │
│                                                                   │
│  Cigogne 🦩                  Forge 🔨                            │
│  Fiche voyage                Parser HTML → JSON                  │
│  (Wadden_Vanlife.html)  ───▶ waypoints + route                   │
│                                    │                             │
│                                    ▼                             │
│                           carplay_parser.py                      │
│                           Extrait : [{lat, lng, label, type}]    │
│                           + route polyline                       │
│                                    │                             │
│                                    ▼                             │
│                           Google Maps URL builder                │
│                           → URL multi-waypoints                  │
│                           → QR code / lien share                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        AU VOLANT (iPhone + CarPlay)               │
│                                                                   │
│  ┌──────────┐     ┌──────────┐     ┌───────────────────────────┐ │
│  │  Siri    │────▶│Shortcuts │────▶│  Telegram Bot             │ │
│  │ "Dobby,  │     │ iOS      │     │  (scripts/telegram-bot)   │ │
│  │  trouve   │     │          │     │                           │ │
│  │  un       │     │          │     │  Dobby 🦉 traite :       │ │
│  │  camping" │     │          │     │  • Recherche camping      │ │
│  └──────────┘     └──────────┘     │  • Météo étape            │ │
│           │                        │  • Alternatives trajet     │ │
│           │                        │  • Infos spots ornitho     │ │
│           ▼                        └───────────┬───────────────┘ │
│    Réponse vocale                               │                 │
│    (TTS Gemini)                                 ▼                 │
│                                        Réponse texte + GPS       │
│                                           │                      │
│                                           ▼                      │
│                                  Google Maps (CarPlay)           │
│                                  • Affiche waypoints             │
│                                  • Navigation turn-by-turn       │
│                                  • Alternatives proposées        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 2 (FUTUR) — App iOS native              │
│                                                                   │
│  App iOS légère avec extension CarPlay :                         │
│  • CPListTemplate : liste des voyages Cigogne                    │
│  • CPMapTemplate + CPTrip : navigation intégrée                  │
│  • Ouverture Google Maps via URL scheme                          │
│  • Code Swift déjà dans CARPLAY.md (référence)                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1 — Siri + Shortcuts + Telegram (sans app native)

**Pourquoi cette approche d'abord :**
- Zéro code iOS à écrire
- Google Maps fonctionne déjà nativement dans CarPlay
- L'infrastructure Telegram bot existe déjà (`scripts/telegram-bot/bot.py`)
- Les Shortcuts iOS peuvent ouvrir Google Maps avec des waypoints programmatiquement
- JC peut parler à Dobby en roulant dès la Phase 1 terminée

### Étape 1.1 — Parser Cigogne → JSON waypoints (`carplay_parser.py`)

**Input :** Fiche HTML produite par Cigogne (ex: `Wadden_Vanlife.html`)  
**Output :** Fichier JSON structuré avec waypoints + route

```json
{
  "trip": "Mer des Wadden · Vanlife",
  "dates": "25–29 juin 2026",
  "days": [
    {
      "day": "J1 — jeu 25",
      "label": "Namur → Lelystad",
      "google_maps_url": "https://www.google.com/maps/dir/Namur/Lelystad",
      "waypoints": [
        {"lat": 50.4850, "lng": 4.8057, "label": "Namur Ecolys (départ)", "type": "depart"},
        {"lat": 52.4860, "lng": 5.4162, "label": "Lelystad — Camping Uilenweg 11", "type": "lodging"}
      ],
      "route": [[50.4850, 4.8057], [50.6451, 5.5736], "..."]],
      "alternatives": []
    }
  ],
  "all_waypoints": [...],
  "all_route": [[...]]
}
```

**Script à créer :** `scripts/carplay_parser.py`
- Parse le HTML de Cigogne
- Extrait le bloc `<script>` contenant `var pts = [...]` et `var routePts = [...]`
- Génère le JSON
- Construit les URLs Google Maps multi-waypoints

### Étape 1.2 — Commande Dobby `/carplay` dans Telegram Bot

**Nouvelles commandes dans le bot Telegram :**

| Commande | Action |
|----------|--------|
| `/voyage` | Liste les voyages disponibles (parsés depuis les fiches Cigogne) |
| `/etape J2` | Affiche les détails de l'étape J2 (km, temps, spots, restaurants) |
| `/camping` | Cherche les campings proches de la position actuelle (via camping_scout.py) |
| `/alternative` | Propose des alternatives à l'étape en cours (villes, campings, routes) |
| `/meteo` | Météo pour la position actuelle ou l'étape du jour |
| `/maps J2` | Renvoie le lien Google Maps pour l'étape J2 (ouvrable dans CarPlay) |
| `/spot` | Liste les spots photo/ornitho proches |
| `/suivant` | Passe à l'étape suivante du voyage |

**Flux vocal complet :**
```
JC: « Dis Siri, Dobby »           → Siri ouvre Shortcut « Dobby »
JC: « camping »                   → Shortcut envoie "/camping" au bot Telegram
Dobby: « J'ai trouvé 3 campings   → TTS Gemini → lu par Siri dans les haut-parleurs
       dans un rayon de 15 km :       + message texte avec liens Google Maps
       Camping Les Murets 4.3⭐,
       Aire Camping-Car Park 4.5⭐... »
JC: « Les Murets »                → Dobby envoie le lien Google Maps
                                  → Shortcut ouvre Google Maps avec la destination
                                  → CarPlay affiche la navigation
```

### Étape 1.3 — Shortcut iOS « Dobby »

**À créer manuellement sur l'iPhone de JC :**

1. **Shortcut « Dobby »** — activé par « Dis Siri, Dobby »
   - Dictate Text (en français)
   - Envoie le texte au bot Telegram (via l'API Telegram HTTP)
   - Attend la réponse (~3 secondes)
   - Si la réponse contient une URL Google Maps → Open URL
   - Sinon → Speak Text (lecture vocale de la réponse)

2. **Shortcut « Où suis-je »** — activé par « Dis Siri, où suis-je »
   - Get Current Location
   - Envoie `GPS:lat,lng` au bot Telegram
   - Dobby met à jour la position dans le contexte du voyage

### Étape 1.4 — Enrichissement du bot Telegram

**Modifications de `scripts/telegram-bot/bot.py` :**

```python
# Nouvelles commandes à ajouter
async def cmd_voyage(update, context):
    """Liste les voyages disponibles"""
    
async def cmd_etape(update, context):
    """Détails d'une étape (J1, J2...)"""

async def cmd_camping(update, context):
    """Cherche campings proches position"""

async def cmd_alternative(update, context):
    """Propose alternatives à l'étape en cours"""

async def cmd_maps(update, context):
    """Envoie lien Google Maps pour une étape"""

async def cmd_meteo(update, context):
    """Météo pour position actuelle"""
```

**Fichiers à créer dans `scripts/telegram-bot/` :**
- `carplay_commands.py` — nouvelles commandes
- `carplay_state.py` — état du voyage en cours (étape actuelle, position)
- `data/voyages/` — dossiers JSON parsés depuis les fiches Cigogne

---

## Phase 2 — App iOS native avec extension CarPlay

**Quand :** Après validation de la Phase 1 en conditions réelles (1-2 voyages)

### Étape 2.1 — App iOS « Vanlife Navigator »

**Stack :** SwiftUI + CarPlay framework

**Fonctionnalités :**
- Liste des voyages Cigogne (CPListTemplate)
- Détail d'un voyage avec étapes (CPListTemplate avec sections)
- Navigation vers Google Maps (URL scheme `comgooglemaps://`)
- Affichage des waypoints sur la carte (CPMapTemplate si possible)

**Écrans CarPlay :**
```
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Voyages     │    │  Mer des Wadden   │    │  J2 — Lelystad   │
│              │    │                   │    │  → Friedrichskoog│
│ ● Wadden     │───▶│  J1 Namur→Lelystad│───▶│                   │
│   (25-29/06) │    │  J2 Lelystad→Fri. │    │  🚐 420 km       │
│ ● Normandie  │    │  J3 Friedrichskoog│    │  ⏱ 4h30          │
│   (août)     │    │  J4 Retour Liège  │    │                   │
│ ● Baie Somme │    │                   │    │  [▶ Naviguer]    │
│              │    │                   │    │  [🔄 Alt.]      │
└──────────────┘    └──────────────────┘    └──────────────────┘
```

### Étape 2.2 — Code de référence (extrait de CARPLAY.md)

Le document `CARPLAY.md` contient le code Swift complet pour :
- Template d'application CarPlay (CPTemplateApplicationSceneDelegate)
- Recherche de points d'intérêt (MKLocalSearch)
- Calcul d'itinéraire (MKDirections)
- Navigation turn-by-turn (CPNavigationSession + CPManeuver)
- Moteur de rendu cartographique (MKMapView dans UIWindow CarPlay)
- Guidage vocal (AVSpeechSynthesizer avec ducking audio)
- Gestion des interruptions (appels téléphoniques)
- Cache cartes offline (MKMapSnapshotter)
- Déploiement CI/CD (Fastlane)
- Configuration entitlements + Info.plist
- Simulateur CarPlay dans Xcode

**Ces sections sont conservées dans `CARPLAY.md` (archive) et seront utilisées comme référence par Forge en Phase 2.**

### Étape 2.3 — Prérequis Apple

| Prérequis | Statut |
|-----------|--------|
| Apple Developer Program (99€/an) | ⏳ À souscrire |
| CarPlay Maps Entitlement | ⏳ À demander (approbation Apple requise) |
| Mac avec Xcode 16+ | ✅ M5 |
| iPhone pour test | ✅ JC |
| Véhicule compatible CarPlay | ✅ Stylevan Equinox IV (à vérifier) |

---

## Phase 3 — Intégration temps réel (futur)

**Quand :** Après Phase 2 validée

- Position GPS JC → mise à jour automatique du trajet
- Dobby proactif : « Tu approches de Groningen. Tu veux t'arrêter ? Un spot ornitho est à 5 km. »
- Détection déviation : si JC sort de la route prévue → Dobby recalcule
- Intégration météo live → suggestions de repli si pluie
- Partage de position avec Anne (via Telegram)

---

## Plan d'exécution

| # | Action | Spécialiste | Priorité | Estimé |
|---|--------|-------------|----------|--------|
| 1 | Créer `carplay_parser.py` — extraction waypoints depuis fiches Cigogne | Forge | 🔴 P0 | 2-3h |
| 2 | Parser la fiche Wadden → JSON de test | Forge | 🔴 P0 | 30 min |
| 3 | Ajouter commandes `/voyage`, `/etape`, `/maps` au bot Telegram | Forge | 🔴 P0 | 3-4h |
| 4 | Ajouter commandes `/camping`, `/alternative`, `/meteo`, `/spot` | Forge | 🟡 P1 | 3-4h |
| 5 | Créer le Shortcut iOS « Dobby » | JC + Dobby | 🔴 P0 | 30 min |
| 6 | Test en conditions réelles (prochain voyage) | JC | 🟡 P1 | — |
| 7 | Phase 2 : App iOS CarPlay native | Forge | ⚪ P2 | 2-4 semaines |

---

## Fichiers

| Fichier | Rôle |
|---------|------|
| `CARPLAY-VANLIFE.md` | Ce document — projet |
| `CARPLAY.md` | Archive — conversation Gemini brute (1 535 lignes, code Swift complet) |
| `voyages/wadden.json` | Fiche Wadden parsée en JSON (à créer) |
| `scripts/carplay_parser.py` | Parser HTML Cigogne → JSON waypoints (à créer) |
| `scripts/telegram-bot/carplay_commands.py` | Commandes CarPlay pour le bot (à créer) |
| `scripts/telegram-bot/carplay_state.py` | État du voyage en cours (à créer) |

---

## Notes

- **Google Maps vs Apple Plans :** JC a explicitement demandé Google Maps. Google Maps fonctionne nativement dans CarPlay et s'ouvre via URL scheme `comgooglemaps://`. L'app iOS en Phase 2 utilisera Google Maps pour la navigation, pas Apple Plans.
- **Le Shortcut iOS est la pièce manuelle :** À créer sur l'iPhone de JC. Pas automatisable à distance. Dobby guidera JC pas à pas.
- **Le parsing des fiches Cigogne est la première brique :** Sans ça, rien ne fonctionne. Forge est le spécialiste pour ce job.
- **CARPLAY.md reste archivé** comme référence technique — ne pas le modifier, ne pas le jeter. Tout le code Swift utile pour la Phase 2 est dedans.

---

*Document créé par Dobby 🦉 à partir de la vision JC et de l'analyse du document CARPLAY.md (Gemini).*
*Prochaine étape : briefer Forge pour l'Étape 1 (parser + commandes Telegram).*
