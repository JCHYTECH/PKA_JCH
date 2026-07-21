# Brief — [[Renard]] 🦊 : Garantie véhicule & modification électronique

**De :** [[Dobby]] 🦉  
**Date :** 2026-05-30  
**Contexte :** Projet Vanlife IOT — intégration domotique Home Assistant

---

## Situation

JCH possède un **Stylevan Origin Equinox 4** (fourgon aménagé neuf sur porteur Ford). Il souhaite ajouter un **ESP32 en parallèle sur le bornier CBE** (centrale électronique de gestion des fluides) pour lire les niveaux d'eau propre et eaux usées dans Home Assistant.

La modification consiste à :
- Connecter un ESP32 + convertisseur ADC aux bornes du bornier CBE
- **Lecture passive uniquement** — aucun signal envoyé au bus du véhicule
- Aucune coupure ni soudure sur le faisceau d'origine (connexion en parallèle via bornier ou pin header)
- Le panneau Montaz d'origine continue de fonctionner normalement

## Questions

1. **Garantie constructeur Stylevan** : une connexion en parallèle sur le bornier CBE (lecture seule, sans modification du câblage d'origine) est-elle considérée comme une modification annulant la garantie ?
2. **Garantie porteur Ford** : l'ESP32 se connecte à la batterie cellule (auxiliaire), pas à la batterie moteur. Impact sur la garantie Ford ?
3. **Assurance** : l'ajout d'un équipement électronique basse tension (5V/3.3V) connecté au circuit 12V cellule doit-il être déclaré ? Impact en cas de sinistre ?
4. **Homologation / conformité** : un ESP32 est un composant électronique grand public non certifié automobile. Risque réglementaire en Belgique ?

## Contraintes

- Analyse rapide (quelques points clés, pas un avis formel)
- JCH ne veut pas risquer la garantie d'un véhicule neuf
- Si risque → on abandonne la lecture parallèle et on reste sur des capteurs externes (ultrasons JSN-SR04T)

## Références

- [[rpi-vanlife-guide-complet]] — contexte du projet
- [[rpi-vanlife-mode-emploi]] — étapes d'installation
