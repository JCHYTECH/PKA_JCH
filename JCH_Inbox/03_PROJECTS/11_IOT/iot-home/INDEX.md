# IOT Home — Index projet

> Projet créé le 2026-06-06 par [[Araignée]] — enrichi le 2026-06-08 par [[Dobby]]
> État : **ébauche** — à compléter avec JCH

---

## Partie 1 — Serre (prioritaire)

### Contexte

Serre de jardin 3m × 4m (12 m²) chez JCH à Esneux (rue des Renards). Irrigation goutte-à-goutte sur récupération eau de pluie (système Parkside). Fenêtres automatiques existantes. Objectif : automatiser l'arrosage, la ventilation, et le monitoring.

### BOM Serre — [[Araignée]]

**Phase 1 — Alimentation solaire (~61 €)**
- Panneau solaire + régulateur + batterie 12V pour autonomie électrique

**Phase 2 — Capteurs & connectivité (~68 €)**
- 2× capteur humidité sol (Zigbee)
- 1× capteur T°/HR (Sonoff SNZB-02D)
- 1× capteur niveau cuve ultrason (JSN-SR04T)
- ESP32-CAM (timelapse) + ESP32 pont Zigbee

**Phase 3 — Station météo (~80 €)**
- Ecowitt GW1100 + capteurs (T, H, vent, pluie, pression)

**Phase 4 — Arrosage (~30 €)**
- Électrovanne Parkside PBSS1 A1 12V (existante)
- Pompe eau pluie
- Goutteurs + tuyaux + filtre

**Phase 5 — Ventilation (~20 €)**
- Ventilateur axial 12V IP44 pour régulation température

**Budget total serre : ~247 €**

### Logique de pilotage (Home Assistant)

1. 2 capteurs humidité sol → moyenne → si < SEUIL_SEC → arrosage
2. Si pluie détectée (station météo) → arrosage sauté
3. Si T > SEUIL_CHAUD → ventilateur ON
4. Mode manuel disponible depuis dashboard HA

---

## Partie 2 — Maison off-grid (long terme)

### Contexte

Maison off-grid 60 m² bois sur 9 000 m², autonome (énergie, eau). Projet à long terme.

### Pièces et besoins capteurs

| Espace | Capteurs probables | Priorité |
|---|---|---|
| Séjour/[[Cuisine]] | T°/HR, CO2, luminosité | Haute |
| Chambres (2) | T°/HR | Moyenne |
| Salle d'eau | T°/HR, fuite eau | Haute |
| Extérieur | T°/HR, pluie, vent, PIR | Haute |
| Local technique | T°/HR, état batterie, production solaire | Critique |

### Stack probable

- Home Assistant OS sur RPi 5 (ou Yellow)
- Zigbee (intérieur) + LoRa (extérieur/annexes)
- Monitoring solaire Victron (VE.Direct/MQTT)
- Accès distant : Tailscale
- Convergence BOM avec IOT Van + Serre

---

## Prochaines étapes

- [ ] JCH valide le BOM serre d'[[Araignée]]
- [ ] Commande matériel Phase 1+2 serre
- [ ] Relever dimensions et plan de la maison
- [ ] Identifier modèle Victron pour intégration MQTT

## Voir aussi

- `convergence-van-serre-capteurs.md` — achats groupés
- `iot-van/` — architecture de référence
- `MEMORY.md` — section Maison off-grid
