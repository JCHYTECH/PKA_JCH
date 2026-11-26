# Mise en pratique — Raspberry Pi Vanlife : du déballage au premier dashboard

> Guide pas-à-pas exécutable. Chaque étape a une validation. Si ça bloque, voir [Troubleshooting](#troubleshooting-rapide).
> Pour les specs détaillées, schémas et code YAML : voir le [[rpi-vanlife-guide-complet|Guide de référence]].

**Dernière mise à jour :** 2026-05-30  
**Temps total estimé :** 3h à 5h (selon expérience)  
**Niveau requis :** savoir dénuder un fil, utiliser un terminal, suivre des instructions

---

## Prérequis

### Outils physiques
- Pince à dénuder ou cutter
- Tournevis cruciforme (pour bornier convertisseur)
- Multimètre (indispensable — pour vérifier la tension avant de brancher le Pi)
- **Testeur USB FNIRSI FNB58** (recommandé — vérifie tension/courant réels, protocole PD, câbles e-mark, power banks)
- Fer à souder + étain (uniquement pour les verrous §8 — pas nécessaire pour le setup de base)
- Gaine thermorétractable ou scotch d'électricien

### Outils logiciels
- Un ordinateur (Mac/PC) avec un port USB
- Câble Ethernet (pour le premier boot — évite les galères Wi-Fi)
- Raspberry Pi Imager (téléchargement gratuit : `raspberrypi.com/software`)

### Compétences
- Savoir lire un schéma électrique simple (+ / - / fusible)
- Savoir ouvrir un terminal et copier-coller une commande
- Pas besoin de savoir coder — les YAML sont fournis prêts à coller

### Matériel
Se référer à la checklist du [[rpi-vanlife-guide-complet#2-checklist-matériel--budget|Guide §2]]. Minimum pour démarrer :
- Raspberry Pi 4 ou 5
- SSD M.2 NVMe + adaptateur HAT
- Convertisseur DC-DC 12V→5V + câble USB-C PD (si Pi 5)
- Clé USB Zigbee + 2 capteurs température

---

## Étape 0 — Préparation (15 min)

**Objectif :** tout déballer, vérifier qu'il ne manque rien, préparer l'espace de travail.

- [ ] Déballer tous les composants sur une table
- [ ] Vérifier la checklist du [[rpi-vanlife-guide-complet#2-checklist-matériel--budget|Guide §2]]
- [ ] Télécharger et installer **Raspberry Pi Imager** sur l'ordinateur
- [ ] Brancher le SSD à l'ordinateur via un adaptateur USB (si le HAT ne fait pas USB)

**Validation :** tous les composants sont physiquement devant toi. L'Imager est installé.

---

## Étape 1 — Alimentation électrique (30 min)

**Objectif :** câbler le convertisseur 12V→5V et vérifier qu'il délivre bien 5V stable **avant** d'y brancher le Pi.

> ⚠️ **Ne branche PAS le Raspberry Pi à cette étape.** On teste d'abord la tension à vide.

### 1.1 Câblage sur table (test)

Si tu n'as pas accès à la batterie cellule du van, utilise une batterie 12V externe ou une alim de labo pour le test.

```
Batterie 12V (+)  ──►  Fusible  ──►  IN+  du convertisseur
Batterie 12V (-)  ──►  IN-  du convertisseur
                              │
                         Sortie USB-C  ──►  (ne rien brancher encore)
```

### 1.2 Test au multimètre

1. Mettre le multimètre en mode **Volts DC (20V)**.
2. Placer les pointes sur la sortie USB-C du convertisseur :
   - Pointe rouge → pin +5V (intérieur du connecteur USB-C, ou plot VCC si bornier)
   - Pointe noire → GND (masse)
3. Mettre sous tension.
4. **Lecture attendue : 5.0V à 5.2V** — stable, sans oscillation.

**Validation :**
- [ ] 5.0V–5.2V au multimètre, stable
- [ ] La LED du convertisseur est allumée (si présente)
- [ ] Pas de chaleur anormale au toucher (juste tiède)

> **Piège Pi 5 :** un convertisseur marqué « 5V/5A » sans USB-C PD délivrera peut-être 5V à vide, mais s'effondrera sous charge. Si possible, tester avec une charge résistive ou un appareil USB-C connu avant le Pi. Voir [[rpi-vanlife-guide-complet#101-alimentation--le-piège-de-lundervoltage|Guide §10.1]].

---

## Étape 2 — Premier boot du Raspberry Pi (sans Home Assistant) (30 min)

**Objectif :** vérifier que le Pi boote, que le SSD est reconnu, et que le système est stable.

> On installe Raspberry Pi OS Lite d'abord — c'est léger, rapide, et permet de valider le hardware avant de passer à Home Assistant.

### 2.1 Graver Raspberry Pi OS Lite sur le SSD

1. Ouvrir **Raspberry Pi Imager**.
2. **Raspberry Pi Device :** sélectionner ton modèle (Pi 4 ou Pi 5).
3. **Operating System :** → Raspberry Pi OS (other) → **Raspberry Pi OS Lite (64-bit)**.
4. **Storage :** sélectionner le SSD.
5. Cliquer sur **Next**.
6. À la question « Use OS customisation ? » → **Edit Settings** :
   - **General :** configurer un hostname (ex: `vanpi`), un utilisateur/mot de passe, et le Wi-Fi local si pas d'Ethernet.
   - **Services :** activer **SSH** (mot de passe ou clé).
7. Cliquer **Yes** pour appliquer, puis **Yes** pour écrire.

### 2.2 Premier boot

1. Insérer le SSD dans le Pi (port USB 3.0 bleu, ou via le HAT).
2. Brancher le câble **Ethernet** au routeur (recommandé) — ou laisser le Wi-Fi configuré dans l'Imager.
3. Brancher l'alimentation USB-C au Pi.
4. La LED rouge (PWR) s'allume fixe. La LED verte (ACT) clignote — c'est bon signe.
5. Attendre 1–2 minutes.

### 2.3 Connexion SSH

```bash
# Depuis l'ordinateur, remplacer vanpi.local par le hostname choisi
ssh pi@vanpi.local
# ou via l'IP si le .local ne fonctionne pas :
ssh pi@192.168.x.x
```

### 2.4 Vérifications

```bash
# Le Pi voit-il le SSD comme disque système ?
lsblk
# → doit montrer le SSD (ex: /dev/sda) monté sur /

# Y a-t-il des erreurs d'alimentation ?
vcgencmd get_throttled
# → doit retourner throttled=0x0
# → si throttled=0x50000 ou 0x50005 : UNDERVOLTAGE → vérifier alim §1

# Température
vcgencmd measure_temp
# → < 50°C au repos = normal

# Mettre à jour le système
sudo apt update && sudo apt upgrade -y
```

**Validation :**
- [ ] SSH fonctionnel
- [ ] `throttled=0x0` (pas d'undervoltage)
- [ ] Température < 50°C au repos
- [ ] Le Pi ne reboot pas tout seul après 10 minutes

> **Piège :** si `throttled` n'est pas `0x0`, NE PAS continuer. Revenir à l'étape 1. Un Pi sous-alimenté corrompra le SSD et rendra le système instable.

---

## Étape 3 — Installation de Home Assistant OS (45 min)

**Objectif :** remplacer Raspberry Pi OS par Home Assistant OS sur le SSD.

### 3.1 Graver HAOS

1. Ré-ouvrir **Raspberry Pi Imager**.
2. **Raspberry Pi Device :** ton modèle.
3. **Operating System :** → Other specific-purpose OS → Home assistants and home automation → **Home Assistant** → **Home Assistant OS (RPi 4/5)**.
4. **Storage :** le SSD.
5. **Next → Edit Settings :**
   - Hostname : `vanpi` (ou ton choix)
   - Configurer Wi-Fi ou laisser Ethernet
   - Activer SSH
6. Écrire. L'Imager va effacer Raspberry Pi OS et installer HAOS.

### 3.2 Premier démarrage HAOS

1. SSD dans le Pi → alimentation → attendre.
2. **C'est long.** HAOS télécharge des conteneurs au premier boot. La LED verte clignote activement.
3. **Temps d'attente : 10 à 20 minutes.** Ne pas débrancher.
4. Depuis l'ordinateur, ouvrir un navigateur : `http://vanpi.local:8123`
   - Si `.local` ne fonctionne pas, utiliser l'IP (trouvable via l'interface du routeur ou `ping vanpi.local`).
5. La page « Preparing Home Assistant » apparaît → attendre qu'elle passe à l'écran de création de compte.

### 3.3 Configuration initiale

1. Créer un compte (nom, mot de passe).
2. Nommer l'installation (ex: « Mon Smart Van »).
3. Localisation : important pour les automatisations (lever/coucher du soleil).
4. Laisser HA découvrir automatiquement les appareils sur le réseau.

**Validation :**
- [ ] `http://vanpi.local:8123` affiche l'interface Home Assistant
- [ ] Compte créé, dashboard par défaut visible
- [ ] Le Pi est resté allumé sans reboot pendant toute l'installation

---

## Étape 4 — Réseau Wi-Fi autonome (20 min)

**Objectif :** le Pi crée son propre réseau Wi-Fi. Le téléphone s'y connecte sans box.

1. Dans HA : **Paramètres → Modules complémentaires → Boutique des modules**.
2. Chercher **Access Point** (ou « Point d'accès Wi-Fi »).
3. Installer. **Ne pas démarrer tout de suite.**
4. Onglet **Configuration :**
   ```yaml
   ssid: VanLife_Network
   # Mot de passe WPA2 d'au moins 8 caractères
   password: TonMotDePasse
   # Canal Wi-Fi — 6 par défaut, changer si interférences
   channel: 6
   ```
5. Démarrer le module.
6. Activer **« Démarrage automatique »** et **« Surveillance »** (Watchdog).

**Validation :**
- [ ] Le réseau Wi-Fi `VanLife_Network` apparaît sur le téléphone
- [ ] Connexion réussie avec le mot de passe
- [ ] Depuis le téléphone connecté au Wi-Fi du van : `http://vanpi.local:8123` fonctionne

> **Note :** une fois connecté au Wi-Fi du van, le téléphone n'a plus internet (sauf si dongle 4G/5G configuré). C'est normal — le Pi est le routeur local, pas une passerelle internet.

---

## Étape 5 — Capteurs Zigbee (20 min)

**Objectif :** connecter les premiers capteurs de température et les voir apparaître dans HA.

### 5.1 Brancher la clé Zigbee

1. Brancher la clé USB Zigbee (Sonoff ZBDongle-E) sur un port USB du Pi.
2. Dans HA : **Paramètres → Appareils et services → Ajouter une intégration**.
3. Chercher **Zigbee Home Automation**.
4. Pour le port série, HA devrait auto-détecter la clé. Si plusieurs choix : prendre `/dev/ttyUSB0` ou celui avec « Sonoff » dans le nom.
5. **Submit.** La clé est configurée.

### 5.2 Appairer un capteur de température

1. Dans HA : **Paramètres → Appareils et services → Zigbee Home Automation → Appareils**.
2. **Ajouter un appareil** (bouton en bas à droite).
3. Sur le capteur Sonoff SNZB-02D : **appui long** sur le bouton (5 secondes) jusqu'à ce que la LED clignote.
4. HA détecte le capteur en quelques secondes. Lui donner un nom (ex: `Température Cellule`).
5. Répéter pour le deuxième capteur (ex: `Température Frigo`).

**Validation :**
- [ ] Les deux capteurs apparaissent dans **Paramètres → Appareils et services → Appareils**
- [ ] Les valeurs de température s'affichent et changent (prendre le capteur dans la main pour voir la température monter)
- [ ] Deux entités sont créées : `sensor.temperature_cellule` et `sensor.temperature_frigo`

> **Les noms exacts des entités** sont visibles dans **Paramètres → Appareils et services → Entités**. C'est ce nom qu'il faudra utiliser dans le dashboard YAML.

---

## Étape 6 — Premier dashboard mobile (15 min)

**Objectif :** remplacer le dashboard par défaut par l'interface van, et la voir sur le téléphone.

1. Dans HA, aller sur le dashboard par défaut (Overview).
2. Cliquer sur les **3 points** (haut droit) → **Modifier le tableau de bord**.
3. Cliquer à nouveau sur les **3 points** → **Éditeur de configuration Raw**.
4. Effacer tout le contenu.
5. Coller le code YAML du [[rpi-vanlife-guide-complet#7-tableau-de-bord-mobile-lovelace|Guide §7]].
6. **Remplacer** les noms d'entités dans le YAML par les vrais noms de tes capteurs :
   - `sensor.temperature_interieur` → le nom réel de ton capteur cellule
   - `sensor.temperature_frigo` → le nom réel de ton capteur frigo
   - Supprimer temporairement les entités que tu n'as pas encore (porte, humidité, GPS)
7. **Enregistrer.** Quitter l'éditeur.
8. Sur le téléphone, ouvrir `http://vanpi.local:8123` → le dashboard apparaît.

**Validation :**
- [ ] Les températures s'affichent sur le dashboard (ordinateur et téléphone)
- [ ] Le dashboard est lisible sur l'écran du téléphone
- [ ] L'alerte frigo n'apparaît pas (température < 7°C)

---

## Étape 7 — Première automatisation : alerte frigo (10 min)

**Objectif :** recevoir une notification si le frigo dépasse 7°C.

1. Dans HA : **Paramètres → Automatisations et scènes → Créer une automatisation**.
2. **Créer une nouvelle automatisation → Page blanche.**
3. Mode YAML (3 points → Éditer en YAML) et coller :
   ```yaml
   alias: Alerte température frigo
   trigger:
     - platform: numeric_state
       entity_id: sensor.temperature_frigo
       above: 7
       for: "00:15:00"
   action:
     - service: notify.persistent_notification
       data:
         title: "⚠️ Alerte Frigo Van"
         message: "Le frigo a dépassé 7°C depuis 15 minutes. Température actuelle : {{ states('sensor.temperature_frigo') }}°C"
   ```
4. **Enregistrer.** L'automatisation est active.

**Test :**
1. Prendre le capteur frigo dans la main → la température monte.
2. Quand elle dépasse 7°C, attendre 15 minutes (ou changer `for: "00:00:00"` pour test immédiat).
3. Une notification apparaît dans HA.

**Validation :**
- [ ] La notification apparaît quand le capteur dépasse 7°C
- [ ] La notification disparaît / ne se redéclenche pas en boucle

---

## Étape 8 — Installation dans le van (1h à 2h)

**Objectif :** transposer le setup de la table au véhicule.

### 8.1 Emplacement du Pi

Choisir un endroit :
- **Au sec** (pas sous une fenêtre qui fuit)
- **Accessible** (pour brancher/débrancher des USB)
- **À l'abri du métal** si GPS (le signal GPS ne traverse pas le métal)
- **Proche de la batterie cellule** (câbles d'alimentation courts = moins de pertes)

### 8.2 Câblage définitif

Même schéma que l'étape 1, mais sur la batterie cellule :

```
Batterie Cellule (+)  ──►  [Fusible 3A/5A au plus près de la batterie]  ──►  [Interrupteur]  ──►  IN+ Convertisseur
Batterie Cellule (-)  ──►  IN- Convertisseur
```

**Règles de sécurité :**
- Le fusible doit être à **moins de 20 cm** de la borne + de la batterie.
- Les câbles doivent être de section suffisante : 1.5 mm² minimum pour 3A.
- Bien serrer les cosses dans le bornier du convertisseur.
- Fixer le convertisseur (il chauffe un peu — ne pas l'enfermer dans un isolant).

### 8.3 Fixation

- Le Pi dans son boîtier aluminium peut être fixé avec du velcro industriel ou des vis.
- Le SSD doit être bien enfiché — les vibrations peuvent le desserrer.
- La clé Zigbee : si le Pi est dans un placard métallique, utiliser une rallonge USB pour sortir la clé.

### 8.4 Vérification finale dans le van

- [ ] Multimètre : 5V stable au convertisseur sur batterie cellule
- [ ] `vcgencmd get_throttled` → `0x0`
- [ ] Dashboard accessible depuis le téléphone sur le Wi-Fi du van
- [ ] Les capteurs Zigbee communiquent (les valeurs s'actualisent)
- [ ] Test : couper l'interrupteur → le Pi s'éteint. Rallumer → le Pi boote normalement

---

## Par où continuer ensuite

Une fois le setup de base fonctionnel dans le van :

1. **GPS** → [[rpi-vanlife-guide-complet#62-gps-tracking|Guide §6.2]]
2. **Capteurs supplémentaires** (porte, humidité) → §6.1
3. **Automatisation tiroirs** → §8.2
4. **Inclinomètre ESP32** → §9.1
5. **Jauges d'eau** → §6.3
6. **Accès distant (Tailscale)** → §5

Chaque extension est indépendante — tu peux les ajouter dans l'ordre qui te convient.

---

## Troubleshooting rapide

| Symptôme | Cause probable | Action |
|----------|---------------|--------|
| LED rouge éteinte, rien ne s'allume | Pas de 5V / fusible grillé / câblage inversé | Multimètre sur la sortie convertisseur. Vérifier fusible. Vérifier polarité. |
| LED rouge allumée mais LED verte fixe (pas de clignotement) | SSD non détecté / image corrompue | Re-graver le SSD. Vérifier qu'il est bien branché. Essayer un autre câble USB. |
| Le Pi boote puis reboot au bout de quelques minutes | **Undervoltage** | `vcgencmd get_throttled` → si ≠ 0x0 : câble USB-C PD obligatoire (Pi 5). Vérifier convertisseur. |
| `http://vanpi.local` ne répond pas | Réseau / DNS local | Essayer l'IP directement. Vérifier le câble Ethernet. Ping `vanpi.local`. |
| `http://vanpi.local:8123` affiche « Preparing Home Assistant » depuis >30 min | HAOS télécharge des conteneurs lentement | Normal si connexion lente. Vérifier que le Pi a internet (Ethernet). Attendre. |
| La clé Zigbee n'est pas détectée | Mauvais port série | Dans HA : Zigbee → Configurer → changer le port série manuellement (`/dev/ttyUSB0`, `/dev/ttyACM0`). |
| Capteur Zigbee ne s'appaire pas | Distance / interférences | Rapprocher le capteur de la clé (< 1m). Réinitialiser le capteur (appui long 10s). |
| Dashboard vide après collage YAML | Noms d'entités incorrects | Vérifier les noms exacts dans **Paramètres → Appareils et services → Entités**. |
| « Database busy » ou HA lent | Corruption DB / carte pleine | Voir [[rpi-vanlife-guide-complet#103-sqlite--le-piège-des-permissions|Guide §10.3]]. Vérifier l'espace disque : `df -h`. |

---

## Références

- [[rpi-vanlife-guide-complet]] — Guide de référence complet (specs, schémas, budgets, code YAML)
- [[2026-05-28_retour-test-maison-rpi-birdnet-mobile]] — Leçons terrain RPi 5 (WildNexus)
- [[BIRDNET_PI_ACCESS]] — Modèle de fiche d'accès (pour créer un `VAN_PI_ACCESS.md`)

---

*Guide pratique généré le 2026-05-30 par [[Dobby]] 🦉 — conçu pour être suivi étape par étape, un soir ou un week-end.*
