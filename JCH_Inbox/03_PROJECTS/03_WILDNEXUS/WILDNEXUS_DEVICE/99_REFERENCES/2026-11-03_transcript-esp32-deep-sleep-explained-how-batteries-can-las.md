# Transcript — « ESP32 Deep Sleep Explained: How Batteries Can Last Months »

- **Source** : Rolling Bob
- **URL** : https://youtu.be/U5gBRJZVOBo
- **Durée** : 04:55
- **Date** : 2026-11-03
- **Moteur** : Whisper local (small, faster-whisper)
- **Segments** : 160

---

[00:00] Le plan monitor de l'esp32 vérifie l'huile, le sensor reading et les wets.
[00:05] Si la prochaine reading est 10 minutes à l'arrivée, pourquoi garder la whole chip à l'arrivée jusqu'à ce point ?
[00:09] Le sleep deep permet à l'esp32 de tourner la plupart de son hardware entre les readings.
[00:14] Avec le right circuit et suffisamment de temps à dormir, le projet peut rassembler sur les batteries pour un mois.
[00:19] Pour finir ce long, le circuit de la whole doit utiliser très peu d'énergie pendant les wets.
[00:25] Tout d'abord, regardez l'origine de l'esp32 chip.
[00:27] La radio utilise environ 95 à 100 milliampses à l'aide d'une Wi-Fi.
[00:32] Lorsque la sending est expérimentée, liste environ 180 à 240 milliampses sous la condition de test.
[00:38] Un milliamp est un unité d'électricité.
[00:40] Le changement de l'électricité fonctionne comme un chip.
[00:43] Donc, ce n'est pas le cas pour nous, c'est l'avantage de l'utilisation d'un jour.
[00:47] Imaginez tourner de la lumière et des appliances dans une maison avant l'air.
[00:51] Vous vivez un petit cliquet à l'alarmée pour que cela peut vous réveiller dans le matin.
[00:55] Dipsleep fonctionne de manière similaire.
[00:57] L'esp32 tournera ses principaux processeurs.
[01:00] La plupart sont en train de travailler.
[01:02] Et la radio.
[01:03] Une petite partie peut rester.
[01:05] Pour garder le temps et réveiller le chip.
[01:07] Vous dites ce qu'il faut réveiller avant d'aller dormir.
[01:10] Pour l'original chip, liste expérimentée,
[01:12] il y a environ 10 microamps avec un timer de sleep.
[01:15] Et une petite partie de l'alarmée s'étend.
[01:17] 10 microamps c'est juste 100 millimètres.
[01:20] C'est l'alarmée pour le chip avec ces pièces.
[01:24] Les autres de l'alarmée peuvent encore utiliser.
[01:26] Le timer peut réveiller notre monitor plan après 10 minutes.
[01:30] Le programme commence.
[01:31] Réveil le sensor.
[01:32] L'alarmée s'étend à Wi-Fi.
[01:34] Et réveille le résultat.
[01:35] Ensuite, il s'étend à nouveau.
[01:36] La radio s'étend durant l'alarmée.
[01:39] Donc, un message de Wi-Fi ne peut pas le réveiller.
[01:42] Un bouton ou l'alarmée peut aussi réveiller l'alarmée
[01:44] par une pin de suite.
[01:46] Sur l'alarmée original ESP32,
[01:47] seulement certaines pièces peuvent faire ceci durant le sleep.
[01:51] Checkez quelles pièces votre exacte chip supporte avant de le réveiller.
[01:55] Certaines chips ESP32 aussi supportent l'alarmée quand tu touches la pin de sensor.
[01:59] Quand l'alarmée ESP32 s'étend du sleep,
[02:01] le principal programme normal commence à nouveau.
[02:04] Ça ne tient pas de où il s'est arrêté.
[02:06] Si tu utilises l'alarmée,
[02:07] la partie de l'alarmée s'étend à nouveau.
[02:10] Tu dois être prêt pour le réveiller.
[02:12] Les valeurs dans la mémoire normal sont perdues.
[02:15] Tu peux sauver un petit peu d'alarmée dans une spécificité spéciale
[02:18] appelée RTC mémoire.
[02:19] Pensez sur ça,
[02:20] comme si vous ayez des notes avant le bed.
[02:22] Les valeurs restent là-dedans,
[02:24] durant le deep sleep,
[02:25] jusqu'à ce que l'alarmée soit en puissance.
[02:27] Les conditions que l'alarmée peut survivre
[02:29] peuvent être sauvées en flash.
[02:31] Un type de mémoire qui garde l'alarmée sans puissance.
[02:34] Maintenant imaginez que le circuit
[02:36] utilise une avantage de 100 milliamps
[02:39] pendant 2 secondes.
[02:41] Il utilise ensuite 0.1 milliamps
[02:43] quand il dormit pendant 9 minutes
[02:44] et 58 secondes.
[02:46] Ce qui fait 10 minutes de cycle.
[02:48] Ces valeurs sont faites par exemple
[02:50] pour tout ce qui est puissant par l'alarmée.
[02:52] Ils ne sont pas les mesures
[02:53] d'un bord particulier.
[02:54] Parmi l'alarmée,
[02:55] l'avantage de l'alarmée
[02:56] est à peu près 0.43 milliamps.
[02:58] Suppose que l'alarmée
[03:00] peut s'appliquer à 2000 milliamps à l'heure.
[03:02] Divider la capacité
[03:04] par l'avantage de l'alarmée
[03:05] donne à peu près 192 jours,
[03:07] un peu plus de 6 mois.
[03:08] Si le circuit utilise 100 milliamps,
[03:11] tout le temps,
[03:12] la calculation donnerait
[03:13] juste 20 heures.
[03:15] Ce résultat de 6 mois
[03:16] est un estimateur.
[03:17] Les 2 secondes doivent s'intéresser
[03:18] à commencer,
[03:19] lire le sensor,
[03:20] connecter la Wi-Fi
[03:22] et envoyer le data.
[03:23] Si le travail tient plus longtemps,
[03:24] la batterie s'étend plus vite.
[03:26] Les résultats
[03:27] aussi dépendent de la batterie
[03:28] et de la capacité de l'alarmée
[03:30] que l'on peut utiliser.
[03:31] Metsz l'alarmée
[03:32] durant l'avantage de l'alarmée
[03:33] et de l'alarmée
[03:34] pour obtenir un estimateur utile
[03:35] pour votre projet.
[03:36] Le bord de l'alarmée
[03:37] tient aussi.
[03:38] Il peut avoir un power light,
[03:40] un chip utilisé pour l'USB programmation,
[03:42] et un régulateur qui supplie
[03:43] la bonne vitesse.
[03:44] Pour mettre le USB 32
[03:46] à dormir,
[03:46] ne se tourne automatiquement
[03:48] de ces parties séparées.
[03:49] Ils peuvent continuer à utiliser le power,
[03:51] dépendant de l'alarmée
[03:52] et de la façon dont c'est poweré.
[03:53] Le même va pour tout ce qui est connecté
[03:55] à l'alarmée.
[03:56] Supposent un sensor
[03:57] ajoute 1 milliampes
[03:58] tout le temps.
[03:59] Dans notre exemple,
[04:00] ça fait l'avantage
[04:01] de 0.43 à
[04:03] 1.43 milliamps.
[04:05] La batterie estimée
[04:06] s'étend de 192 jours
[04:08] à 58 jours.
[04:09] Check le sensor
[04:10] ainsi que le USB 32.
[04:12] La batterie s'étend aussi
[04:14] à donner un connecteur constrain
[04:15] et wireless.
[04:16] Si votre projet doit être connecté,
[04:18] autres modes de poursaving
[04:19] sont mieux appréciés.
[04:20] Avec le right setting,
[04:21] ces modes peuvent maintenir la connecteur.
[04:24] Un monitor plan
[04:25] peut dormir entre les readings.
[04:26] Un ordinateur
[04:27] pour une commande instée
[04:28] wireless
[04:29] a besoin d'une approche différente.
[04:30] Pour notre monitor plan,
[04:31] la batterie est simple.
[04:33] Réveillez,
[04:34] mesurez,
[04:34] envoiez et dormez.
[04:36] Finissez le travail rapidement.
[04:37] Puis,
[04:38] maintenez le tout le circuit
[04:39] en utilisant de très peu de pouvoirs
[04:41] jusqu'à la prochaine reading.
[04:42] C'est ce que le plan s'est checké
[04:44] sans tenir le USB 32
[04:46] avec tout le temps.
[04:47] Donc, si cette vidéo est
[04:48] utile pour vous,
[04:49] n'hésitez pas à cliquer le like
[04:50] et à vous abonner.
[04:52] Et je vais vous voir
[04:52] dans une autre vidéo.
[04:53] Merci.
