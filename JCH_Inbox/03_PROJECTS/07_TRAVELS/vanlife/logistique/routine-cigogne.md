# Routine de recherche — [[Cigogne]]

Checklist systématique avant de produire une fiche destination. À exécuter dans l'ordre.

---

## 1. Règles de base (non négociables)

- **⏰ Départ voyage :** 10h00 · **Départ étape :** 9h00 · **Retour :** 9h00
- **Jour 1 :** max 4h de route → arrêt nuit + resto
- **Jours suivants :** arrêt après max 7h de route
- **🥐/🥪/🍽️ :** petit-déjeuner van, déjeuner sandwichs van, dîner resto
- **📷 Photos JCH :** aube/crépuscule approximatifs, sans stress — pas de durée comptée
- **🏛️ Anne :** durées de visite et baignade prises en compte dans le planning
- **🌧️ Plans B :** chaque étape extérieure doit avoir une alternative couverte
- **🗺️ Google Maps :** lien 🔗 dans chaque tableau
- **⬛ Carte :** tous les points d'arrêt marqués, nuitées en noir
- **⛴️ Bateau/ferry :** compter navigation aller + retour + temps sur place (~3h) selon horaires marée

---

## 2. Itinéraire & distances

1. Calculer distance Liège → destination (autoroute et sans autoroute)
2. Si > 400 km → chercher 2-3 étapes mi-chemin à ~50% du trajet
3. Pour chaque étape mi-chemin : vérifier JCH (photo) + Anne (patrimoine) + dîner + parking nuit
4. Calculer toutes les distances entre étapes du planning
5. Générer la carte interactive (Leaflet/OSM) avec tous les points

---

## 3. Stationnement nuit

1. **Bases officielles** — WDPA, CDDA, INPN (France), Géoportail Wallonie (Belgique) → trouver toutes les réserves proches de l'itinéraire
2. **Park4Night** — chercher spots avec avis < 3 mois, filtrer « nature » et « gratuit »
3. **Vérifier règlement** — site officiel de la réserve : horaires, interdiction nuit
4. **Street View** — confirmer largeur, pente, panneaux d'interdiction
5. **Signaux d'alerte** — barrière, arrêté préfectoral, amende dans les avis → écarter
6. Si réserve interdite → proposer alternative (parking village, église, aire officielle)

---

## 4. Restaurants (dîner)

1. Chercher sur Google Maps dans la zone de l'étape
2. Filtrer : note ≥ 4.0, avis récents, photos de la salle et de la vue
3. Vérifier : terrasse ou vue, cuisine régionale, fréquentation locale
4. Noter : fourchette de prix, si réservation conseillée
5. Toujours proposer une alternative moins chère

---

## 5. Carte interactive

1. Lister tous les points du trajet avec coordonnées GPS
2. Générer le code Leaflet avec :
   - Tuiles OpenStreetMap
   - Polyligne ocre (#C17F3A) pour le tracé
   - Circle markers : étapes mi-chemin en ocre, autres en ardoise
   - Popups avec le nom du lieu
3. Intégrer dans le HTML via la section `.map-container`

---

## 6. Livrables à produire

| Livrable | Format | Destination |
|---|---|---|
| Fiche détaillée | Markdown | `destinations/Nom.md` |
| Fiche mise en forme | HTML ARTEON | `destinations/Nom_ARTEON.html` |
| Fiche imprimable | PDF A4 | `destinations/Nom_ARTEON.pdf` |
| Mise à jour préférences | Markdown | `PREFERENCES.md` (si nouveau feedback) |

---

## 7. Après le séjour

1. Lire le feedback dans `feedback/YYYY-MM-DD_lieu.md`
2. Mettre à jour `PREFERENCES.md` si nouvelles préférences détectées
3. Noter les spots de nuit qui ont fonctionné ou échoué

---

## 8. Recherche web & avis

Avant de finaliser une proposition, [[Cigogne]] doit « voyager dans sa tête » en consultant :

### Sources web systématiques

| Source | Usage | Priorité |
|---|---|---|
| **TripAdvisor** | Avis restaurants, attractions, photos, classement | ★★★★★ |
| **Google Maps** (avis + photos) | Vérification visuelle, commentaires récents | ★★★★★ |
| **Park4Night** (commentaires) | Retours vanlifeurs, sécurité, bruit | ★★★★★ |
| **Blogs vanlife** | Retours d'expérience, astuces locales | ★★★★ |
| **Offices de tourisme** | Horaires, fermetures, événements | ★★★★ |
| **Instagram / Google Photos** | Photos récentes, état réel des lieux | ★★★ |
| **Forums** (Routard, Voyage Forum) | Discussions, pièges à éviter | ★★★ |

### Vérifications par étape

1. **Restaurant :** TripAdvisor ≥ 4.0, photos salle + vue, avis < 6 mois
2. **Stationnement :** Park4Night + Street View + forums « camping-car nuit [X] »
3. **Visite :** horaires officiels, prix, durée recommandée (TripAdvisor), jours fermeture
4. **Baignade :** qualité eau, température (avis récents), accessibilité
5. **Bateau/ferry :** site officiel la veille (horaires marée)

### Règle d'or

*« Une fiche n'est pas prête tant que [[Cigogne]] n'a pas passé 10 minutes sur TripAdvisor + Google Maps par étape. »*
