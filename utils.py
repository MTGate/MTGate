import winreg

def get_reg_val(winreg_modifier: int, loc: str, name: str) -> str:
    '''get values from registry, e.g. get_reg_val
    (winreg.HKEY_CURRENT_USER, r"Software\\Wizards Of The Coast\\MTGA\\",
    "SupplementalInstallID")
    '''
    import ctypes, sys
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if winreg_modifier != winreg.HKEY_CURRENT_USER and not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    try:
        hkey = winreg.OpenKey(winreg_modifier, loc)
    except:
        raise FileNotFoundError(-1)
    try:
        i = 0
        reg_val = ""
        while True:
            try:
                subkey = winreg.EnumValue(hkey, i)
                if name in subkey[0]:
                    reg_val = subkey[1]
                    break
                i += 1
            except OSError:
                break
        winreg.CloseKey(hkey)
        return reg_val
    except :
        winreg.CloseKey(hkey)
        raise WindowsError(-1)

from globals.config import client_version
import requests
import json

def ring_doorbell() -> str:
    '''get front door uri from the doorbell
    '''
    player_id = get_reg_val(winreg.HKEY_CURRENT_USER,
                            r"Software\\Wizards Of The Coast\\MTGA\\",
                            "SupplementalInstallID")
    player_id = str(player_id, 'utf-8')
    doorbell_request = {
        "clientVersion": client_version,
        "environmentKey": "Prod",
        "playerId": player_id,
        "platformKey": "windows"
    }

    uri = requests.get("https://prod.doorbellmat.w2.mtgarena.com/doorbell.config").text

    text: str = "https://prod.doorbellmat.w2.mtgarena.com"
    if "https://prod" in text:
        doorCode = "46u7OAmyEZ6AtfgaPUHiXNiC55/mrtp3aAmE018KZamDhvr0vZ8mxg=="
    else:
        doorCode = "ta4kBQcrBfdGd8AUjrv7lj9pYyA3Kkj9p39byJXuTdTBiZxRC6xgRQ=="
    uri += "?code=" + doorCode

    resp = requests.post(uri, data=json.dumps(doorbell_request, ensure_ascii=False, separators=(',', ':')).encode('utf-8'),
                    headers={"content-type": "application/json"})

    return resp.json()['fdURI']

def fast_login() -> dict:
    refresh_token = get_reg_val(winreg.HKEY_CURRENT_USER,
                            r"Software\\Wizards Of The Coast\\MTGA\\",
                            "WAS-RefreshTokenE")
    import base64
    refresh_token = base64.b64decode(str(refresh_token, 'utf-8'))
    refresh_token = str(refresh_token, 'ascii').strip()

    clientId = "N8QFG8NEBJ5T35FB"
    clientSecret = "VMK1RE8YK6YR4EABJU91"

    header = { "Authorization": f"Basic {str(base64.b64encode(f'{clientId}:{clientSecret}'.encode()), 'utf-8')}",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8" }

    from urllib.parse import urlencode
    resp = requests.post("https://api.platform.wizards.com/auth/oauth/token",
                        headers=header,
                        data=urlencode({"grant_type": "refresh_token", "refresh_token": refresh_token}))

    access_token = resp.json()["access_token"]
    refresh_token = resp.json()["refresh_token"]
    # client_id = resp.json()["client_id"]
    # game_id = resp.json()["game_id"]
    # domain_id = resp.json()["domain_id"]
    # persona_id = resp.json()["persona_id"]
    # account_id = resp.json()["account_id"]

    profile_resp = requests.get("https://api.platform.wizards.com/profile",
                        headers={ "Authorization": f"Bearer {access_token}" })
    account_id = profile_resp.json()["accountID"]

    return resp.json()