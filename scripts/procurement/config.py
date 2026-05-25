# scripts/procurement/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Cherche .procurement.env dans home dir (RPi) puis répertoire courant
_env_paths = [
    Path.home() / ".procurement.env",
    Path(".procurement.env"),
]
for _p in _env_paths:
    if _p.exists():
        load_dotenv(_p)
        break

MOUSER_API_KEY: str = os.getenv("MOUSER_API_KEY", "")
MOUSER_CART_API_KEY: str = os.getenv("MOUSER_CART_API_KEY", "")
MOUSER_SEARCH_URL = "https://api.mouser.com/api/v2/search/keyword"
MOUSER_CART_URL = "https://api.mouser.com/api/v1/cart"

ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = "claude-sonnet-4-6"

# Mode simulation si aucune clé Mouser
SIMULATION_MODE: bool = not bool(MOUSER_API_KEY)

# Dossier TEAM_Inbox relatif à la racine PKA
TEAM_INBOX_PATH = Path(__file__).parent.parent.parent / "TEAM_Inbox"
