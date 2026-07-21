# Brief — Contournement Cloudflare pour les outils PKA

**De :** [[Dobby]] 🦉  
**À :** [[Forge]] 🦦  
**Date :** 2026-06-21  
**Priorité :** 🟡 Medium — impacte la vérification des données shopping/procurement  
**Projet :** 01_AI_IT_TOOLS — Amélioration outillage PKA

---

## Problème

Les outils de consultation web intégrés à DeepSeek TUI (`fetch_url` et `web.run`) sont **bloqués par Cloudflare JS Challenge** lorsqu'ils tentent d'accéder à certains sites (raspberrypi.com, Amazon, Kubii, etc.).

**Impact concret :** impossible de vérifier un prix, une disponibilité ou une spec technique sur un site protégé sans basculer sur des revendeurs tiers (Pimoroni) ou des sources non-officielles. Inacceptable au regard de la règle « Vérification avant affirmation » (SOUL.md).

**Root cause :** les requêtes émanent d'IPs datacenter, immédiatement classées comme non-navigateur par Cloudflare.

---

## Solutions identifiées

### Solution 1 : FlareSolverr (proxy anti-Cloudflare)

Proxy open-source qui résout automatiquement les challenges Cloudflare JS et retourne le contenu de la page. S'exécute en conteneur Docker.

- **Repo :** https://github.com/FlareSolverr/FlareSolverr
- **Port exposé :** 8191
- **Usage :** POST `http://localhost:8191/v1` → retourne la page décodée
- **Stack :** Python + headless Chrome, ~50 Mo RAM idle
- **Intégration PKA :** `fetch_url` ou `curl` peut router via ce proxy. Compatible avec n'importe quel outil HTTP.

**Avantages :**
- Gratuit, maintenu activement
- Résout la majorité des sites Cloudflare
- S'intègre dans la stack Docker existante sur M5 (HA, Zigbee2MQTT, Mosquitto)
- Pas de configuration complexe

**Limites :**
- Ne résout pas le contenu chargé en AJAX après interaction utilisateur (dropdowns Shopify, sélecteurs de variants)
- Maintenance nécessaire lors des mises à jour de l'algo Cloudflare (~tous les 3-6 mois)

### Solution 2 : Playwright MCP Server (navigateur complet pilotable)

Navigateur Chromium headless avec fingerprint réaliste, pilotable via MCP (Model Context Protocol). Plus puissant que FlareSolverr — peut interagir avec des formulaires, cliquer sur des dropdowns, attendre des chargements AJAX.

- **Repo :** https://github.com/executeautomation/mcp-playwright (ou équivalent)
- **Stack :** Node.js + Chromium, ~300 Mo disque, ~200 Mo RAM
- **Intégration PKA :** connecté comme MCP server → outils PKA peuvent piloter le navigateur

**Avantages :**
- Passe Cloudflare ET les interactions AJAX (variants Shopify, prix conditionnels)
- Intégration native MCP (pas besoin de wrapper)
- Peut prendre des screenshots pour inspection visuelle

**Limites :**
- Plus lourd que FlareSolverr (Chromium complet)
- Nécessite Node.js (déjà présent sur M5)
- Configuration initiale plus longue

### Solution 3 : Bridge Chrome DevTools Protocol local

Le M5 a déjà Chrome installé. On peut lancer Chrome en mode debug (`--remote-debugging-port=9222`) et interagir via le DevTools Protocol.

**Avantages :**
- Zéro installation, navigateur déjà présent
- Fingerprint 100% réel (navigateur Mac M5 avec cookies, sessions)
- Pas de consommation additionnelle significative

**Limites :**
- Chrome doit être ouvert
- Configuration manuelle à chaque redémarrage (pas headless natif sans flags)
- Solution ad hoc, moins robuste que les deux ci-dessus

---

## Recommandation

**Court terme (< 1h) : FlareSolverr**
- Déploiement Docker sur M5, port 8191
- Commande test : `curl -X POST http://localhost:8191/v1 -H "Content-Type: application/json" -d '{"cmd":"request.get","url":"https://www.raspberrypi.com/products/raspberry-pi-5/"}'`
- Intégration dans `fetch_url` via proxy (si supporté) ou wrapper script `bin/`

**Moyen terme (1-2h) : Playwright MCP**
- Installation du package npm `@anthropic/mcp-playwright` ou équivalent
- Configuration comme MCP server dans `~/.deepseek/config.toml`
- Test sur Pimoroni pour extraction des prix variants Shopify

**Stratégie combinée :**
- FlareSolverr → 90% des cas (sites Cloudflare simples, pages statiques)
- Playwright MCP → 10% restants (AJAX, interactions, formulaires)

**Coût :** 0€ (open-source)  
**Maintenance :** ~30 min tous les 3 mois (mise à jour FlareSolverr ou Chromium)

---

## Critères de succès

1. `fetch_url` ou un outil PKA peut extraire le prix d'un Pi 5 sur raspberrypi.com
2. Même résultat sur Amazon, Kubii, et autres sites Cloudflare
3. Le temps de consultation n'augmente pas de plus de 5 secondes vs direct
4. Aucune dégradation des services Docker existants (HA, Zigbee2MQTT)

---

## Prérequis vérifiés avant démarrage

- [ ] Docker opérationnel sur M5 (HA + Zigbee2MQTT + Mosquitto tournent déjà)
- [ ] Espace disque disponible pour ~500 Mo (Chromium + FlareSolverr)
- [ ] Port 8191 et 9222 disponibles sur localhost
- [ ] Node.js présent sur M5 (vérifier version pour Playwright)
