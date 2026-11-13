# Karotz Reborn — Avatar physique de Dobby 🦉

> **Objectif** : ressusciter le Karotz (lapin connecté Violet / ex-Nabaztag) et en faire l'extension physique de Dobby — un assistant IA ludique incarné dans un objet sympathique.
> **Projet ombrelle** : `11_IOT` · **Hub** : M5 (Dobby pilote) + Karotz sur le réseau local.
> **Statut** : 🟢 opérationnel — flash + OpenKarotz OK (2026-11-09). Voir [`resurrection-karotz-2026-11-09.md`](resurrection-karotz-2026-11-09.md).

---

## Vision

Dobby (orchestrateur PKA, sur M5) pilote le Karotz comme **avatar physique** :
- **voix** : TTS → haut-parleur du lapin (Dobby « parle »)
- **oreilles** : mouvements (gestes, expressions)
- **LED / ventre** : états visuels (notification, humeur)
- **webcam** : présence, photos
- **RFID** : lecture de Ztamps/Nanoztags (déclencheurs physiques)

Le Karotz redevient un objet vivant, piloté par l'IA locale — zéro cloud Violet, serveur auto-hébergé.

---

## Ressource principale

**miniil.be** — « Ressusciter votre lapin Karotz avec miniil Karotz OS et miniil's OpenKarotz » :
https://www.miniil.be/karotz/guides-pratiques-et-documentations/ressuciter-votre-lapin-karotz-avec-miniil-karotz-os-et-miniils-openkarotz

- **miniil Karotz OS** : firmware modifié, base communautaire.
- **miniil's OpenKarotz** : interface web retravaillée pour contrôler le lapin.

---

## Méthode (résumé du guide)

1. **Clé USB** : télécharger `usbkey.zip`, formater FAT32, décompresser.
2. **Éditer `waitfornetwork.sh`** : IP (fixe libre), DNS (8.8.8.8), GW (routeur), NM (255.255.255.0), SSID, PWD.
3. **Flasher** : Karotz éteint → insérer la clé (port USB arrière) → démarrer. Messages vocaux pendant l'installation (copie sons → madplay → firmware → réseau → OpenKarotz). Ne **jamais éteindre** pendant le flash.
4. **Vérifier** : `setuplog.txt` sur la clé.
5. **Redémarrer** sans clé → connexion WiFi → interface web OpenKarotz à l'IP choisie → installer via navigateur.

---

## Contraintes techniques (à retenir)

- ⚠️ **WiFi WPA obligatoire** : le Karotz ne supporte **pas le WPA2 seul** (confirmé par miniil en commentaire). Il faut un AP en **WPA/WPA2 mixte**. → vérifier la config routeur/AP **avant** de flasher, sinon blocage sur LED bleue.
- **IP fixe libre** sur le réseau local (pas de conflit).
- **LED** : bleu = connexion en cours · vert = connecté · son joué à la connexion.

---

## État / prochaines étapes

- [x] Localiser le Karotz (retrouvé par JC).
- [x] Vérifier qu'il s'allume — 2026-11-09 : **oreilles bougent et se mettent verticales** (moteurs OK, hardware de base vivant).
- [x] Vérifier la LED — 2026-11-09 : **rouge** = erreur. C'est **normal** : le firmware d'origine cherche les serveurs Violet (morts) → il tombe en erreur. Confirme que le matériel tourne (alim ✅ oreilles ✅ LED ✅).
- [x] Vérifier la config WiFi — 2026-11-09 : **WPA (TKIP)** sur RUT240 dédié (le WPA2 seul ne marche pas).
- [x] Réunir la config réseau (SSID, mot de passe, IP, passerelle, masque) → `CONFIG-RESEAU-KAROTZ.md`.
- [x] Préparer la clé USB + `waitfornetwork.sh` (avec le correctif `inetd`).
- [x] Flasher miniil Karotz OS + installer OpenKarotz — 2026-11-09 ✅.
- [x] Intégration Dobby — tests d'interaction HTTP : TTS / oreilles / LED / sons / photo ✅ (2026-11-10, voir « API vérifiée » ci-dessous).

---

## Intégration — feuille de route HA

Le Karotz s'intègre le mieux **via Home Assistant** (déjà opérationnel chez JC). Voir **[`integration-home-assistant.md`](integration-home-assistant.md)** pour le détail. En résumé :

1. **OpenKarotz** (flash USB) → interface web à l'IP locale.
2. **HA** : intégration native OpenKarotz (Media Player + boutons) OU script `Desperado88/Home-Assistant-Karotz-2025` (HACS, oreilles synchronisées).
3. **Pipeline Assist** : entrée vocale (téléphone / Atom Echo ~15 € — le micro du Karotz est médiocre) → IA → sortie `media_player.karotz` (le lapin parle).

## Le cerveau : Dobby vs IA-HA (à trancher)

- **Dobby = cerveau** (vision JC) : Dobby (DeepSeek, M5) génère le texte → HA TTS → `media_player.karotz`. Plus personnel, mais il faut une passerelle Dobby→HA en **écriture** (le relais MCP actuel est lecture seule).
- **IA-HA = cerveau** : OpenAI/Anthropic Conversation natif dans HA, pipeline autonome. Plus simple à démarrer, mais le « cerveau » est un ChatGPT générique, pas Dobby.

**Reco Dobby** : faire les étapes 1–2 (flash + intégration HA) communes aux deux, démarrer avec l'IA-HA pour valider la voix, puis remplacer le cerveau par Dobby une fois la plomberie en place.

## API vérifiée — commandes HTTP (2026-11-10)

Le lapin se pilote en `curl` sur `http://192.168.129.250/cgi-bin/...` :

- **Parler (TTS)** : `tts?text=bonjour%20JC` → `{"played":true,"voicelanguage":"fr","voicegender":"female"}` (~3 s).
- **Oreilles** : `ears?left=16&right=16` (valeurs 0–16) · `ears_reset`.
- **LED** : `leds?action=light&color=FF0000&period=500&pulse=1` (color en hex, period en ms).
- **Sons** : `sound_list` (liste) · `sound?id=bip1` (jouer un id).
- **Photo** : `snapshot` (sauvegarde un `.jpg` sur le lapin, renvoie le nom).
- ⚠️ `moods` obsolète → renvoie vers `/cgi-bin/apps/moods`.
- ⚠️ `webcam` = flux MJPEG (dans un navigateur, pas `curl`).

## Passerelle Dobby → Karotz (`bin/dobby-speak`)

Dobby (M5) pilote le lapin via un script unique : Dobby **pense** le texte, le script le pousse vers le TTS du lapin.

```bash
bin/dobby-speak "bonjour JC"           # le lapin prononce le texte
echo "bonjour JC" | bin/dobby-speak    # texte via stdin
bin/dobby-speak --ears 16,16 "salut"   # oreilles + parler
bin/dobby-speak --ears reset           # oreilles au repos
bin/dobby-speak --led FF0000           # LED rouge
bin/dobby-speak --sound bip1           # joue un son
bin/dobby-speak --health               # test de connexion
```

- Script : `scripts/karotz_speak.py` (stdlib uniquement, zéro dépendance).
- Config env : `KAROTZ_IP` (défaut `192.168.129.250`), `KAROTZ_PORT`, `KAROTZ_RETRIES` (défaut 3), `KAROTZ_RETRY_DELAY` (défaut 5 s) — le retry absorbe le WiFi intermittent.
- La réflexion reste chez **Dobby** ; ce script ne fait que **parler** (porte-parole).

## Limites

- **Micro NON utilisable comme entrée vocale** (constat 2026-11-10) : l'API locale OpenKarotz n'expose **aucun endpoint de capture audio** (`record`, `micro`, `voice`, `audio`, `stt`, `speech`… → tous 404). Le seul truc audio-entrant est `ears?action=listen` = détection de bruit/clap pour bouger les oreilles (un geste, pas de STT). Le micro d'origine (mono, médiocre) servait aux messages vocaux via le **cloud Violet**, mort. → **Entrée vocale via micro Mac/Whisper, téléphone ou Atom Echo.**
- **Latence 2–4 s** (réseau → IA → audio).

---

## Références

- Guide miniil (ci-dessus) · OpenKarotz / communauté · docs Karotz (RFID Ztamps, API historique).
