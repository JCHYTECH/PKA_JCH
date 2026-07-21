# IOT Maison — Domotique Off-Grid

> Créé le 2026-06-22 par [[Dobby]] — extrait de `iot-home/`
> Hub partagé avec `iot-serre/` — RPi 5 + Home Assistant à Esneux
> Statut : **ébauche long terme**

---

## Contexte

Maison off-grid 60 m² bois sur 9 000 m², autonome (énergie, eau). Projet à long terme.

---

## Architecture

```
[Capteurs maison] ←→ [Zigbee / LoRa] ←→ [RPi 5 HA] ←→ [Dashboard]
                                              ↕ (même hub)
                                        [iot-serre/]
```

---

## Pièces et besoins capteurs

| Espace | Capteurs probables | Priorité |
|---|---|---|
| Séjour/Cuisine | T°/HR, CO2, luminosité | Haute |
| Chambres (2) | T°/HR | Moyenne |
| Salle d'eau | T°/HR, fuite eau | Haute |
| Extérieur | T°/HR, pluie, vent, PIR | Haute |
| Local technique | T°/HR, état batterie, production solaire | Critique |

---

## Stack

- Home Assistant OS sur RPi 5 (partagé avec serre)
- Zigbee (intérieur) + LoRa (extérieur/annexes)
- Monitoring solaire Victron (VE.Direct/MQTT)
- Accès distant : Tailscale

---

## Prochaines étapes

- [ ] Relever dimensions et plan de la maison
- [ ] Identifier modèle Victron pour intégration MQTT
- [ ] BOM capteurs maison
- [ ] Intégration dashboard commun serre + maison

---

## Liens

- `_shared/hub-esneux.md` — Infrastructure partagée
- `iot-serre/` — Automatisation serre (même hub)
- `iot-van/` — Domotique vanlife (hub séparé)

---

*Généré par Dobby 🦉 — 2026-06-22*
