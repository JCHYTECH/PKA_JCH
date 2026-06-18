BRIEF — [[Forge]] 🦦 + [[Nova]] 🦋 — 2026-06-14
═══════════════════════════════════════════

PRIORITY : high
DEADLINE : 2026-06-21

MISSION
Créer un test harness firmware qui lit des images depuis la SD, exécute l'inférence MobileNet-SSD sur ESP32-S3, et produit un benchmark recall/précision/latence — sans attendre la caméra OV5640.

CONTEXTE
L'ADR-010 R4 exige un benchmark IA sur matériel cible avant fermeture M-02. La caméra OV5640 est commandée mais pas encore livrée. Ce harness remplace la source caméra par des images pré-stockées sur SD, permettant de débloquer le benchmark immédiatement. Le code d'inférence est le même que celui qui sera utilisé avec l'OV5640 — seul le point d'entrée image change.

ENTRÉES DISPONIBLES
- Skill wildnexus-edge-ai-cv (modèles, résolutions, seuils)
- Brief original du 2026-06-08 (specs benchmark ADR-010)
- ADR-010 §R4 — critères de succès (>90% recall humain jour, >80% nuit IR, <5% FP faune, latence <2s)
- ESP32-S3-DevKitC-1 N8R8 déjà reçu (×2)
- microSD SanDisk Extreme 32GB disponible

LIVRABLE ATTENDU

[[Forge]] :
- Fichier firmware : 03_P0_ENGINEERING/05_SIMULATION/test_harness/wn_test_harness.ino
- Intégration TFLite Micro + modèle quantifié INT8 (MobileNetV3-Small ou équivalent)
- Boucle de benchmark : pour chaque image SD → décoder 224×224 → inference → timer → log
- Format résultats CSV : filename, predicted_class, confidence, latency_ms, ram_free

[[Nova]] :
- Jeu de test (30 images) dans test_images/ sur SD :
  - 8× humain jour (5m, 10m), 6× humain nuit IR
  - 8× faune (cerf, sanglier, [[renard]]), 4× faux positifs (tronc, rocher)
  - Annotations ground truth intégrées dans les noms de fichier
- Mesurer recall/précision par classe et conditions

Livrable commun : rapport 2026-06-XX_forge_nova_wildnexus-edge-ai-benchmark-harness.md dans TEAM_Inbox/

CONTRAINTES
- Modèle TFLite doit tenir en PSRAM (< 8 MB)
- Résolution inference : 224×224 (si latence > 2s, tester aussi 160×160)
- Pas besoin de la caméra OV5640 — tout passe par SD
- Le harness doit être réutilisable quand la caméra arrivera (swap source image)

INTERACTIONS
- Consulter le skill wildnexus-edge-ai-cv pour les specs modèle
- [[Fourmi]] 🐜 peut flasher le firmware et insérer la SD si besoin
- [[Dobby]] peut tester la logique du harness dans Wokwi (sans l'inférence TFLite)
