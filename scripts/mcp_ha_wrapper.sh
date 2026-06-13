#!/bin/bash
# Wrapper MCP Home Assistant — lit HASS_HOST et HASS_TOKEN depuis l'environnement
# Usage: deepseek-tui le lance, les variables doivent être exportées dans le shell parent
export HASS_HOST="${HASS_HOST:-http://localhost:8123}"
export HASS_TOKEN="${HASS_TOKEN:?HASS_TOKEN non défini — créer un Long-Lived Access Token dans HA > Profil > Sécurité}"
exec uvx homeassistant-mcp
