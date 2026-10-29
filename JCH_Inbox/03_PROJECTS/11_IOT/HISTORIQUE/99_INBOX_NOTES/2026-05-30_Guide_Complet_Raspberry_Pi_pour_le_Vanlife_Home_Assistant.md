# # Guide Complet : Raspberry Pi pour le Vanlife & Home Assistant

> Exporté depuis Apple Notes — créé le ?, modifié le 2026-05-30 06:06

�ّ܏# Guide Complet : Raspberry Pi pour le Vanlife & Home Assistant

Ce document rassemble l'ensemble des configurations pour installer un Raspberry Pi comme cerveau domotique autonome dans un fourgon aménagé.

---

## 1. Pourquoi le Raspberry Pi en Vanlife ?
Le Raspberry Pi est l'outil idéal pour un véhicule récréatif car :
* Il consomme très peu d'énergie (généralement moins de 15W).
* Il fonctionne en basse tension (5V DC via convertisseur).
* Il est ultra-modulaire et centralise plusieurs fonctions hors-ligne.

---

## 2. Liste des Composants Recommandés

### Le Cœur du Système
* **Raspberry Pi 4 (4 Go) ou Pi 5 (4 Go/8 Go)** : Le Pi 4 chauffe moins ; le Pi 5 offre un maximum de puissance.
* **Boîtier Passif en Aluminium** (ex: *Flirc* ou *Argon ONE*) : Dissipe la chaleur sans ventilateur pour éviter le bruit et l'encrassement par la poussière.
* **Disque SSD M.2 NVMe (128 Go à 1 To)** + Adaptateur/HAT : Remplace la carte MicroSD, trop sensible aux coupures de courant et aux vibrations du véhicule.

### L'Alimentation Électrique (Sécurisée)
* **Convertisseur DC-DC (Buck) 12V vers 5V (USB-C)** : Stabilise la tension de la batterie cellule (qui fluctue entre 11V et 14.4V). Doit délivrer au moins **3A** (Pi 4) ou **5A** (Pi 5).
* **Porte-fusible étanche** + Fusible de 3A ou 5A : À placer au plus près de la batterie auxiliaire.
* **Interrupteur à bascule** : Pour couper proprement le système lors des longues périodes d'hivernage.

### Le Pack de Surveillance Zigbee (~30€)
* **Clé USB Zigbee** (ex: *Sonoff ZBDongle-E* ou *SkyConnect*) : L'antenne à brancher sur le Pi.
* **Capteurs de température/humidité** (ex: *Sonoff SNZB-02D*).
* **Capteurs d'ouverture** (ex: *Sonoff SNZB-04*) : Pour sécuriser les portes ou fenêtres.

---

## 3. Schéma de Branchement Électrique

Le système doit obligatoirement être raccordé à la **batterie auxiliaire** (cellule).

```text
[ Batterie Auxiliaire 12V ]
       │
       ├── (+) Borne Positive ──── [ Fusible 3A/5A ] ──── [ Interrupteur ] ───┐
       │                                                                      │
       └── (-) Borne Négative (Masse) ────────────────────────────────────────┼──────┐
                                                                              │      │
                                                                       ┌──────┴──────┴──────┐
                                                                       │ Convertisseur      │
                                                                       │ DC-DC 12V -> 5V    │
                                                                       └──────┬──────┬──────┘
                                                                              │      │
                                                                              ▼      ▼
                                                                       [ Câble USB-C 5V ]
                                                                              │
                                                                              ▼
                                                                     [ Raspberry Pi 4 / 5 ]
```

### Étapes d'installation :
1. Retirer le fusible de sécurité.
2. Câbler le pôle positif de la batterie vers le fusible, l'interrupteur, puis l'entrée `IN+` du convertisseur.
3. Câbler la masse `(-)` de la batterie vers l'entrée `IN-` du convertisseur.
4. Relier la sortie USB-C du convertisseur au Raspberry Pi.
5. Insérer le fusible et basculer l'interrupteur pour tester la LED rouge (fixe).

---

## 4. Installation de Home Assistant OS (HAOS)

1. Télécharger **Raspberry Pi Imager** sur un ordinateur.
2. Sélectionner : **Choisir l'OS** > **Other specific-purpose OS** > **Home Automation** > **Home Assistant**.
3. Sélectionner le disque SSD branché à l'ordinateur et cliquer sur **Écrire**.
4. Brancher le SSD gravé sur un port USB 3.0 (bleu) du Raspberry Pi.
5. Connecter le Pi au routeur de la maison par câble Ethernet pour le premier démarrage.
6. Après 10-15 minutes, accéder à l'interface via l'adresse : `http://homeassistant.local:8123`.
7. Brancher la clé USB Zigbee (avec une rallonge pour éviter les interférences) et valider la configuration automatique de l'intégration **ZHA (Zigbee Home Automation)**.

---

## 5. Configuration du Point d'Accès Wi-Fi (Hotspot)

Permet de connecter votre téléphone directement au Raspberry Pi dans le van, même en plein désert sans aucun réseau cellulaire.

1. Dans Home Assistant, aller dans **Paramètres** > **Modules (Add-ons)** > **Boutique de modules**.
2. Chercher et installer **"Access Point"** (ou *Local AP*).
3. Aller dans l'onglet **Configuration** du module et adapter le code suivant :

```yaml
ssid: "VanLife_Network"
wpa_passphrase: "MonSuperMotDePasse"
channel: 6
interface: wlan0
```

4. Cliquer sur **Sauvegarder**, cocher **Lancer au démarrage** sur l'onglet Informations, puis cliquer sur **Démarrer**.
5. Connecter le Wi-Fi du smartphone sur ce réseau. L'interface es
