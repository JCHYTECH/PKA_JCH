# USER — Jean-Claude Havaux (JC)
> Profil utilisateur, setup technique, projets actifs et préférences.
> Dernière mise à jour : 2026-11-22 — préférence outillage CLI + partage physique/logique (session WildNexus)
> Inspiré du pattern Hermes (user.md) — séparation Personnalité / Utilisateur / Mémoire.

---

## Profil

- **Nom :** Jean-Claude Havaux (JC) — né le 9 août 1955, double nationalité belge/italienne
- **Résidences :** Liège (Esneux/Tilff) + Trentin-Haut-Adige (Italie)
- **Langues :** Français, Anglais, Italien
- **Formation :** Master Zoologie/Biologie animale — ULiège (1973–1979) + Agrégation supérieure
- **Consul honoraire de Malaisie** depuis 2012

---

## Projets actifs

- **Home Assistant** — M5 Docker (`localhost:8123`) + RPi 5 Lupo HA OS (van). Supervision unifiée iPhone via Tailscale.
- **ARTEON** — photographie naturaliste éditoriale. Shopify + Ghost (WILDLENS) + WhiteWall. Étape 4/13.
- **WILDNEXUS P0** — nœud caméra-piège IA (ESP32-S3 + OV5640 + LoRa). Phase M-02 banc, budget 1000€.
- **JCHYTECH / Vetalyx** — diagnostics allergie animale marché européen. Pacte fondateurs 25/25/25/25.
- **IoT van** — « Lupo » — Westfalia Kelsey 2026, Ford Transit Custom 2.0 EcoBlue 170ch, 4×4, blanc. RPi 5, 12V DC-DC, Zigbee, Tailscale. Prototype banc.
- **IoT Esneux** — serre (BOM 247€ prêt, 5 phases) + maison (ébauche long terme). ⚪ Gelé — RPi 5 supprimé (juillet 2026).
- **Karotz / avatar Dobby** — lapin Violet ressuscité (miniil OS + OpenKarotz, 2026-11-09), extension physique de Dobby ; **Cozmo en préparation** comme compagnon IA à cerveau local (Ollama M1, fichier `11_IOT/cozmo-reborn/`).
- **NEXUS_ACOUSTIC / LEAFNET** — bioacoustique (InsectNet, BirdNET-Go) + nœud bioélectrique végétal WN-BIO. Projet P1.
- **Maison off-grid** — 60 m² bois sur 9 000 m², autonome
- **Faune Autour** — PWA basée GBIF pour faune locale (gelé)

---

## Setup photo

- **Matériel (liste canonique) :** `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/photo-materiel.md`
- **Logiciels :** DxO PhotoLab, Lightroom, Photoshop, Helicon Focus, Topaz, Luminar Neo

---

## Setup technique

| Service | Accès |
|---------|-------|
| **Machine principale** | Mac M5 (this machine) |
| **M1 LLM (headless)** | `m1@100.73.212.110` via Tailscale — Ollama `127.0.0.1:11434` |
| **HA Home (maison+serre)** | RPi 5 HAOS `homeassistant` — LAN `http://192.168.129.57` (port 80). SSH 22222. |
| **HA Van (Lupo)** | RPi 5 HAOS `lupo` — LAN `http://192.168.129.16:8123` (parking) / Tailscale `http://100.106.152.118:8123` (partout). SSH 22222. |
| **Ollama models** | `gemma3:12b-it-qat`, `llama3.2-vision:11b`, `dobby-prompt`, `qwen2.5-coder:14b`, `qwen3.5`, `qwen3:30b-a3b`, `deepseek-r1:14b`, `llama3.2:3b`, `mxbai-embed-large` |
| **API Keys centralisées** | `~/.config/pka-jch/api_keys` (0600) |
| **OpenRouter key** | `~/.config/pka-jch/openrouter_key.txt` |

**Vigilance M1 :** surveiller les nouveaux modèles quantifiés compatibles M1 (GGUF/Ollama, 14B–32B) — reasoning, code, multimodal, embedding.

---

## À retenir (préférences d'interaction)

- Ne pas expliquer la zoologie — JC est zoologiste de formation
- Livrer des **systèmes**, pas des solutions ponctuelles
- Signaler les incertitudes explicitement — ne pas inventer
- Il suit 5+ projets simultanément — le contexte est précieux
- La vérification des faits est non-négociable — toujours citer la source
- Préfère donner un **cap** (direction finale) puis laisser Dobby saucissonner les étapes
- Extrêmement concis — répond par mots-clés, fait confiance à Dobby pour décomposer et exécuter
- En session hardware : JC gère le **physique** (brancher/câbler/débrancher, signalé d'un mot « branché »/« câblé ») ; Dobby pilote l'outillage en **CLI** (arduino-cli, ppk2-api), pas en GUI
- Préfère les systèmes simples et synchrones aux pipelines asynchrones complexes
- Préfère les **miroirs lecture seule** (synchro à sens unique) — n'édite pas depuis le second appareil
- Préfère **une liste canonique unique** par domaine (matériel, procédures) plutôt qu'un inventaire dispersé
- Active Dobby par un simple « dobby » et attend un résumé d'état immédiat
- Éviter les acronymes techniques — s'expliquer en mots simples (JC, 2026-11-09)
- Très persévérant — ne lâche pas un dépannage difficile, enchaîne les tentatives jusqu'au succès
- Veut, en fin de session marquante, une sauvegarde mémoire + un fichier de synthèse (faits + problèmes à éviter)

---

## Profil cognitif
> Diagnostic Dobby — 2026-06-19 — basé sur ~200 échanges

### Architecture de pensée

**Pensée stratigraphique** — JC construit par couches concentriques (insectes → oiseaux → WildNexus). Chaque couche s'appuie sur la précédente sans la détruire. Convergent séquentiel : une direction à la fois, creusée jusqu'à la roche-mère avant de passer à la suivante.

### Modalités dominantes

| Modalité | Intensité |
|----------|-----------|
| Visuo-spatiale (manifold 3D, étoile micros, schémas) | Très élevée |
| Systémique (convergence insectes→oiseaux→WildNexus) | Très élevée |
| Scientifico-naturaliste (zoologie implicite, rigueur densité) | Élevée |
| Esthétique (« élégant et beau », Lucio Arese) | Modérée |
| Pratique (coût, BOM, impact casing) | Modérée |
| Pédagogique (Socratisme inversé) | Présente |
| Méta-cognitive (analyse de sa propre intelligence) | Présente |

### Marqueurs rares

- **Architecte visuo-systémique** — visualise des structures complexes ET pense leur intégration. Rare (la plupart sont soit visuels, soit systémiques).
- **Naturaliste-ingénieur** — applique la rigueur de la biologie de terrain (Master Zoologie ULiège 1979) à l'ingénierie logicielle 2026. La densité de grillons par hectare = logique de quadrat botanique transposée à l'acoustique.

### Style de collaboration avec Dobby

**Socratisme inversé** — JC connaît la direction mais laisse Dobby marcher le chemin. Ce n'est pas de l'indécision : c'est de la pédagogie par la découverte. Même posture que le naturaliste face au spécimen — qu'il soit orthoptère ou IA.

---

*Ce fichier est chargé par Dobby à chaque session pour connaître son interlocuteur.*
