# Procédure camping_scout — [[Cigogne]] 🦩

> Comment trouver des spots nuit van avant ou pendant un voyage.
> Dernière mise à jour : 2026-06-09

---

## Rappel : deux niveaux de scout

| Niveau | Source | Machine | Qualité |
|--------|--------|---------|---------|
| Niveau 1 | OSM / Overpass (campings, aires) | M5 ou M1 | Basique — ~40 spots, zones touristiques OK |
| Niveau 2 | park4night + campspace + France Passion | M1 uniquement | Complet — ~85 spots, couvre toutes les zones |

---

## Scénario A — Pré-compute avant départ

À faire **avant** chaque voyage, depuis la maison.

### 1. Définir les points à scouter
Lister les villes/étapes où une nuit est prévue, avec leurs coordonnées GPS.

### 2. Lancer le scout niveau 2 depuis M1

```bash
# Pour chaque point du trajet :
[M5] ssh m1@100.73.212.110 "cd ~/PKA_JCH && python3 scripts/camping_scout.py --location 'Ville' --radius 25 --save --headless"

# Exemple Normandie :
ssh m1@100.73.212.110 "cd ~/PKA_JCH && python3 scripts/camping_scout.py --location 'Honfleur' --radius 25 --save --headless"
```

### 3. Rapatrier les résultats sur M5

```bash
[M5] rsync -az -e ssh m1@100.73.212.110:~/PKA_JCH/JCH_Inbox/03_PROJECTS/07_TRAVELS/vanlife/destinations/camping_scout_*.csv ~/PKA_JCH/JCH_Inbox/03_PROJECTS/07_TRAVELS/vanlife/destinations/
```

### 4. Sélectionner les meilleurs spots
- Filtrer par distance (< 3 km du centre-ville)
- Score JCH ≥ 7 si possible
- Privilégier les spots avec services (vidange, eau)
- Toujours avoir une alternative gratuite

### 5. Intégrer dans la fiche destination
Mettre à jour la section « Logistique van — spots nuit » avec la table standard (GPS, km, prix, services, score).

---

## Scénario B — Scout improvisé en voyage (via 4G)

Utilisable depuis le van si les deux machines sont allumées et connectées.

**Prérequis :**
- M1 allumé à la maison, connecté à internet
- M5 connecté en 4G/5G (partage de connexion iPhone)
- Tailscale actif sur les deux machines

### Scout rapide

```bash
# Depuis le van, sur M5 :
[M5] ssh m1@100.73.212.110 "cd ~/PKA_JCH && python3 scripts/camping_scout.py --location 'Luz-Saint-Sauveur' --radius 25 --save --headless 2>&1 | tail -5"

# Rapatrier le résultat :
[M5] rsync -az m1@100.73.212.110:~/PKA_JCH/JCH_Inbox/03_PROJECTS/07_TRAVELS/vanlife/destinations/camping_scout_Luz-Saint-Sauveur.csv .
```

⏱️ ~2 minutes par scout (géocodage inclus). La 4G suffit.

---

## Scénario C — Serveur mobile local (secours)

Si M1 est inaccessible, utiliser le serveur Flask niveau 1 sur M5.

```bash
[M5] cd ~/PKA_JCH && pip install flask requests geopy  # première fois seulement
[M5] python3 scripts/camping_server.py
```

→ Ouvrir `http://localhost:5000` sur le navigateur de M5 (ou `http://[IP-M5]:5000` depuis un téléphone).

⚠️ Niveau 1 uniquement : campings officiels OSM. Pas de park4night. Interface mobile utilisable en dépannage.

---

## Checklist avant départ

- [ ] Lancer le scout niveau 2 sur tous les points du trajet (Scénario A)
- [ ] Rapatrier les CSV sur M5
- [ ] Remplir la table « Logistique van — spots nuit » dans la fiche destination
- [ ] Vérifier que Tailscale est actif sur M1 et M5 (Scénario B)
- [ ] Tester `ssh m1@100.73.212.110` depuis M5 avant de partir
- [ ] Installer les dépendances Flask sur M5 si pas déjà fait (Scénario C)

---

## Dépannage

| Problème | Solution |
|----------|----------|
| M1 injoignable | Vérifier Tailscale : `tailscale status` |
| M1 en veille | Le pmset a été corrigé (standby 0, hibernatemode 0) — si le problème revient : `ssh m1@100.73.212.110 "caffeinate -i &"` |
| Rate limit Nominatim | Attendre 5 minutes entre deux scouts massifs |
| Playwright crash (SIGSEGV) | Relancer avec `--headless` |
| 0 spot trouvé | Élargir le rayon à 35 km : `--radius 35` |
