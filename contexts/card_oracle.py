import requests
import functools
from typing import Optional


@functools.cache
def query(grp_id: int) -> Optional[tuple[str, str, str]]:
    "given GRP id, get name, type, and oracle text"
    try:
        resp = requests.get(f"https://api.scryfall.com/cards/arena/{grp_id}")
        resp = resp.json()
        return (resp["name"], resp["type_line"], resp["oracle_text"])
    except:
        return None
