# Brief équipe — Philosophie d'ingénierie : ne pas sur-spécifier

**De :** Dobby 🦉  
**À :** Tous les owners WP WildNexus (Nova, Castor, Forge, Chouette, Clio, Bruno, Renard)  
**Date :** 2026-05-18  
**Référence :** `00_GOVERNANCE/WILDNEXUS_ENGINEERING_PHILOSOPHY.md`

---

## Décision JCH

Un principe de gouvernance s'applique désormais à l'ensemble du projet :

> **Quand l'écart technique entre deux options est faible, retenir le produit le plus robuste au meilleur rapport qualité/prix. Ne pas sur-spécifier.**

## Ce que je vous demande

Relire votre WP avec ce filtre et identifier :

- Les choix actuellement ouverts où vous cherchez une précision inutile pour P0
- Les spécifications qui pourraient être allégées sans impact sur M-01, M-02 ou M-03
- Les tâches de benchmarking ou de validation qui ne changent pas le choix final quel que soit leur résultat

## Critère simple

Posez-vous la question : *"Si les deux options ont des performances proches dans les conditions P0, est-ce que la différence change ma décision ?"* Si non — clôturer la question, choisir le plus robuste/disponible/économique, et passer à autre chose.

## Par WP — points à regarder en priorité

| WP | Question spécifique |
|----|---------------------|
| WP02 Hardware (Bruno + Forge) | Y a-t-il des composants sur-spécifiés dans le supply register ? Des alternatives génériques EU suffisantes ? |
| WP03 Firmware (Castor + Forge) | Des états ULP à optimiser *avant* d'avoir mesuré la conso réelle ? Reporter en post-mesure |
| WP04 Edge AI (Nova + Clio) | Le classifieur P0 est binaire — résister à la tentation d'un modèle plus sophistiqué avant validation terrain |
| WP05 EVT (Chouette) | Le protocole terrain peut-il être allégé ? Documenter ce qui est observé, pas ce qui aurait été idéal |
| WP06 Open Source (Forge) | Documentation minimale viable — pas une documentation exhaustive avant que le prototype existe |

## Livrable attendu

Pas de document formel — une remarque en session ou dans Plane si vous identifiez un point allégeable. Dobby consolide.

---

*Référence complète : `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/00_GOVERNANCE/WILDNEXUS_ENGINEERING_PHILOSOPHY.md`*
