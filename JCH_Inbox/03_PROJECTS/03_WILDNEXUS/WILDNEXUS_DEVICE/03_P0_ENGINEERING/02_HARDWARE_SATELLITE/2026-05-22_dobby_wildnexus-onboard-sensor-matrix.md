# WildNexus - Matrice capteurs embarques

**Date :** 2026-05-22  
**Objet :** finaliser les familles de senseurs possibles avant choix architecture  
**Statut :** v0.1 pour discussion JCH  
**Principe :** un capteur n'est accepte que s'il justifie son impact energie, boitier, stockage, IA et transmission.

## 1. Regle de conception

WildNexus ne doit pas embarquer tous les capteurs possibles dans chaque unite.

La bonne architecture est par profils :

- **Satellite Lite** : capteurs essentiels, basse consommation, stockage local, [[LoRa]] metadata.
- **Satellite Smart** : capteurs + IA legere locale, meilleure camera/audio, donnees plus riches.
- **Base Nexus** : capteurs systeme et environnement local, IA lourde, stockage, backhaul, correlation.
- **Module specialise** : audio chauves-souris, thermique, eau/sol, pieges scientifiques.

## 2. Capteurs coeur

| Capteur | Valeur WildNexus | Impact architecture | Energie / donnees | Recommendation |
|---|---|---|---|---|
| Camera visible/IR | Preuve visuelle, comportement, identification humaine, dataset IA | Impose optique, fenetre, IR, stockage, IA vision | Donnees lourdes ; active seulement sur evenement | **Coeur Satellite Lite/Smart** |
| PIR basse conso | Reveil primaire mouvement chaud | Permet deep sleep ; insuffisant seul contre faux positifs | Tres faible conso ; donnees faibles | **Obligatoire camera** |
| Micro audio audible 1 canal | Oiseaux, amphibiens, mammiferes, contexte sonore | Impose port acoustique, windscreen, etancheite differente | Audio lourd si continu ; gerer par fenetres/events | **P0-AUDIO / P1 standard** |
| Temperature + humidite interne | Diagnostic boitier, condensation, qualite donnees | Capteur I2C simple ; aide maintenance | Tres faible | **Obligatoire systeme** |
| Tension batterie / courant | Autonomie, maintenance, diagnostic | Mesure ADC / fuel gauge ; influence alertes | Tres faible | **Obligatoire** |
| RTC precise | Timestamp evenementiel | Necessaire pour correlation multi-capteurs | Tres faible | **Obligatoire** |

## 3. Capteurs environnement utiles

| Capteur | Valeur ecologique | Impact architecture | Risque / remarque | Recommendation |
|---|---|---|---|---|
| Temperature + humidite externe | Contexte activite faune, microclimat | Port expose mais protege ; I2C | Derive si mal ventile ou chauffe boitier | **Recommande P0/P1** |
| Pression barometrique | Meteo locale, fronts, comportement | Simple I2C | Valeur secondaire mais peu couteuse | **Recommande si BME280/BME688** |
| Luminosite / lux | Jour/nuit, phenologie, gestion IR | Fenetre/positionnement ; I2C | Influence par ombrage local | **Recommande** |
| Pluie / wetness | Contexte activite, qualite audio/image | Capteur expose ; encrassement | Maintenance plus elevee | **Option P1** |
| Vent | Qualite audio, meteo locale | Anemometre fragile/visible | Boitier plus encombrant | **A eviter sauf station meteo dediee** |
| Qualite air / VOC | Perturbations, fumee, pollution | Capteurs consomment plus et derivent | Interpretation ecologique faible | **Option faible priorite** |
| CO2 | Faible valeur faune plein air | Consommation, calibration | Peu pertinent exterieur | **Rejeter baseline** |

## 4. Capteurs audio

| Capteur | Usage | Impact architecture | Recommendation |
|---|---|---|---|
| MEMS I2S/PDM audible mono | Oiseaux/amphibiens, contexte | Port acoustique, windscreen, anti-pluie ; acquisition fenetree | **Standard audio** |
| Electret + preamp faible bruit | Meilleure sensibilite oiseaux | Analogique plus delicat, calibration, bruit | **P1 qualite** |
| Double micro audible | Direction approximative, reduction bruit | Plus de donnees, sync, placement mecanique | **P1/P2, pas Lite initial** |
| Micro ultrasonique | Chauves-souris, certains insectes | Sample rate 192-384 kHz, stockage massif, DSP specifique | **Module specialise** |
| Vibration/contact micro | Pluie, activite structurelle, braconnage ? | Risque dual-use, interpretation complexe | **A etudier seulement usage civil clair** |

## 5. Capteurs mouvement / presence

| Capteur | Usage | Impact architecture | Recommendation |
|---|---|---|---|
| PIR | Declenchement mammiferes/oiseaux proches | Tres faible conso ; FOV a aligner camera | **Obligatoire camera** |
| Radar mmWave basse conso | Mouvement sans chaleur, vegetation, vitesse | Plus cher, conso plus haute, traitement | **P1 Smart test** |
| Accelerometre / IMU | Anti-tamper, choc, orientation, chute branche | Tres faible conso ; simple | **Recommande systeme** |
| Magnetometre | Orientation, detection masses metalliques | Risque dual-use ; valeur naturaliste faible | **Non baseline** |
| Capteur ouverture boitier | Maintenance, anti-tamper civil | Simple reed/hall switch | **Recommande si produit [[commercial]]** |

## 6. Position et synchronisation

| Capteur | Usage | Impact architecture | Recommendation |
|---|---|---|---|
| GNSS ponctuel | Position installation, horloge | Antenne, conso ponctuelle, fix lent sous couvert | **Base ou Smart ; Lite option** |
| GNSS 1PPS | Synchronisation precise multi-noeuds | Antenne + discipline RTC ; complexite | **P1/P2 scientifique** |
| NTP via base | Sync locale simple | Depend reseau/base | **Base Nexus** |
| Localisation manuelle via app | Position declarative installation | Zero hardware GNSS satellite | **Suffisant Lite initial** |

## 7. Capteurs image avances

| Capteur | Valeur | Impact architecture | Recommendation |
|---|---|---|---|
| Camera visible/NoIR qualite | Baseline faune | Optique, IR, stockage | **Coeur** |
| IR-cut motorise | Meilleure couleur jour + IR nuit | Piece mobile, conso, fragilite | **Smart/P1** |
| Capteur Sony STARVIS | Meilleure nuit | MIPI/ISP, hardware plus lourd | **Smart prioritaire** |
| Thermique LWIR | Mammiferes nuit, detection sans IR visible | Cout eleve, fenetre germanium, resolution faible | **Module specialise P2** |
| Multispectral/NIR vegetation | Habitat, stress vegetation | Valeur projet annexe, complexite calibration | **Hors baseline** |

## 8. Capteurs sol/eau/habitat

| Capteur | Usage | Impact architecture | Recommendation |
|---|---|---|---|
| Humidite sol | Amphibiens, habitat, restauration | Sonde externe, corrosion, calibration | **Module habitat P1/P2** |
| Temperature sol/eau | Amphibiens, microhabitat | Sonde etanche externe | **Option habitat utile** |
| Niveau eau | Mare/ruisseau, zones humides | Installation specifique | **Module habitat** |
| Conductivite/pH eau | Suivi mare/ruisseau | Maintenance/calibration elevee | **Hors baseline, scientifique** |

## 9. Capteurs systeme et securite civile

| Capteur | Usage | Impact architecture | Recommendation |
|---|---|---|---|
| Humidite interne | Detection fuite/condensation | Tres utile pour maintenance | **Obligatoire** |
| Temperature PCB | Surchauffe, gel, qualite batterie | Simple | **Obligatoire** |
| Courant par rail | Diagnostic camera/audio/modem | Fuel gauge ou sense resistor | **Recommande Smart/Base** |
| Watchdog externe | Recuperation plantage | Pas un senseur biologique, mais critique | **Obligatoire produit** |
| Capteur arrachement / tilt | Anti-vol, maintenance | IMU suffit souvent | **Option [[commercial]]** |

## 10. Tableau de choix par profil

| Capteur | Lite | Smart | Base Nexus | Module specialise |
|---|---:|---:|---:|---:|
| Camera visible/IR | Oui | Oui mieux | Option surveillance base | Selon usage |
| PIR | Oui | Oui | Non necessaire | Selon usage |
| Audio audible mono | Option P0-AUDIO | Oui | Oui possible | Oui |
| Audio stereo/double mic | Non | Option | Oui | Oui |
| Ultrason chauves-souris | Non | Non baseline | Option analyse | Oui |
| Temp/hum interne | Oui | Oui | Oui | Oui |
| Temp/hum externe | Oui | Oui | Oui | Oui |
| Pression/lux | Oui | Oui | Oui | Option |
| IMU anti-tamper | Oui | Oui | Oui | Oui |
| GNSS | Manuel/app | Oui ponctuel | Oui | Oui si scientifique |
| GNSS 1PPS | Non | Option P1 | Oui si sync | Oui |
| mmWave radar | Non | Option test | Non | Option |
| Thermique | Non | Option premium | Non | Oui |
| Sol/eau | Non | Non | Non | Oui |

## 11. Recommandation [[Dobby]]

### Baseline Satellite Lite

- camera visible/IR ;
- PIR ;
- micro audio audible mono si variante P0-AUDIO ;
- temperature/humidite interne ;
- temperature/humidite externe ;
- pression + luminosite si capteur combine ;
- tension batterie ;
- IMU simple ;
- RTC precise ;
- position manuelle via app, GNSS non obligatoire.

### Baseline Satellite Smart

Tout le Lite, plus :

- camera meilleure qualite, idealement MIPI/STARVIS si STM32N6 ou equivalent ;
- micro audible de meilleure qualite ;
- GNSS ponctuel ;
- courant par rail ;
- eventuellement radar mmWave test ;
- eventuellement IR-cut motorise.

### Baseline Base Nexus

- capteurs systeme : temperature, humidite, courant, tension, intrusion boitier ;
- GNSS ou position fixe declaree ;
- stockage SSD/eMMC ;
- modem 4G/5G ;
- eventuellement microphone de reference local ;
- pas besoin de charger la base avec tous les capteurs terrain.

### Modules specialises

- chauves-souris : ultrasonique dedie ;
- zones humides : eau/sol ;
- mammiferes nocturnes premium : thermique ;
- bioacoustique scientifique : double micro / 1PPS / schedule avance.

## 12. Decisions a prendre avant ADR

1. WildNexus accepte-t-il plusieurs profils de satellites des le design, ou un seul boitier universel ?
2. Le micro audible est-il dans le Satellite Lite standard ou dans une variante P0-AUDIO ?
3. Le GNSS est-il embarque dans chaque satellite, ou la position est-elle declaree via app au deploiement ?
4. Veut-on prevoir mecaniquement une option ultrason chauves-souris, ou la traiter comme module separe ?
5. Le capteur thermique est-il un reve P2 ou une option premium a reserver dans le boitier des maintenant ?

## 13. Position actuelle

Je recommande :

- **un socle Lite sobre**, pas universel ;
- **une variante Audio**, pas forcement fusionnee avec tous les noeuds camera ;
- **un Satellite Smart separe** pour IA/camera avancee ;
- **des modules specialises** pour ultrason, thermique, eau/sol.

Le piege serait de fabriquer un seul boitier "tout capteur". Il serait cher, gros, energivore, plus difficile a etancher, et moins elegant qu'un systeme modulaire.

