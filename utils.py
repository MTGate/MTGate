import winreg


def get_reg_val(winreg_modifier: int, loc: str, name: str) -> str:
    """get values from registry, e.g. get_reg_val
    (winreg.HKEY_CURRENT_USER, r"Software\\Wizards Of The Coast\\MTGA\\",
    "SupplementalInstallID")
    """
    import ctypes, sys

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if winreg_modifier != winreg.HKEY_CURRENT_USER and not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )

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
    except:
        winreg.CloseKey(hkey)
        raise WindowsError(-1)


from globals.config import client_version
import requests
import json


def ring_doorbell() -> str:
    """get front door uri from the doorbell"""
    player_id = get_reg_val(
        winreg.HKEY_CURRENT_USER,
        r"Software\\Wizards Of The Coast\\MTGA\\",
        "SupplementalInstallID",
    )
    player_id = str(player_id, "utf-8")
    doorbell_request = {
        "clientVersion": client_version,
        "environmentKey": "Prod",
        "playerId": player_id,
        "platformKey": "windows",
    }

    uri = requests.get("https://prod.doorbellmat.w2.mtgarena.com/doorbell.config").text

    text: str = "https://prod.doorbellmat.w2.mtgarena.com"
    if "https://prod" in text:
        doorCode = "46u7OAmyEZ6AtfgaPUHiXNiC55/mrtp3aAmE018KZamDhvr0vZ8mxg=="
    else:
        doorCode = "ta4kBQcrBfdGd8AUjrv7lj9pYyA3Kkj9p39byJXuTdTBiZxRC6xgRQ=="
    uri += "?code=" + doorCode

    resp = requests.post(
        uri,
        data=json.dumps(
            doorbell_request, ensure_ascii=False, separators=(",", ":")
        ).encode("utf-8"),
        headers={"content-type": "application/json"},
    )

    return resp.json()["fdURI"]


def fast_login() -> dict:
    refresh_token = get_reg_val(
        winreg.HKEY_CURRENT_USER,
        r"Software\\Wizards Of The Coast\\MTGA\\",
        "WAS-RefreshTokenE",
    )
    import base64

    refresh_token = base64.b64decode(str(refresh_token, "utf-8"))
    refresh_token = str(refresh_token, "ascii").strip()

    clientId = "N8QFG8NEBJ5T35FB"
    clientSecret = "VMK1RE8YK6YR4EABJU91"

    header = {
        "Authorization": f"Basic {str(base64.b64encode(f'{clientId}:{clientSecret}'.encode()), 'utf-8')}",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    }

    from urllib.parse import urlencode

    resp = requests.post(
        "https://api.platform.wizards.com/auth/oauth/token",
        headers=header,
        data=urlencode({"grant_type": "refresh_token", "refresh_token": refresh_token}),
    )

    access_token = resp.json()["access_token"]
    refresh_token = resp.json()["refresh_token"]
    # client_id = resp.json()["client_id"]
    # game_id = resp.json()["game_id"]
    # domain_id = resp.json()["domain_id"]
    # persona_id = resp.json()["persona_id"]
    # account_id = resp.json()["account_id"]

    # profile_resp = requests.get("https://api.platform.wizards.com/profile",
    #                     headers={ "Authorization": f"Bearer {access_token}" })
    # account_id = profile_resp.json()["accountID"]

    return resp.json()


def fast_login_retry() -> dict:
    refresh_token = get_reg_val(
        winreg.HKEY_CURRENT_USER,
        r"Software\\Wizards Of The Coast\\MTGA\\",
        "WAS-RefreshTokenE",
    )
    import base64

    refresh_token = base64.b64decode(str(refresh_token, "utf-8"))
    refresh_token = str(refresh_token, "ascii").strip()

    clientId = "N8QFG8NEBJ5T35FB"
    clientSecret = "VMK1RE8YK6YR4EABJU91"

    header = {
        "Authorization": f"Basic {str(base64.b64encode(f'{clientId}:{clientSecret}'.encode()), 'utf-8')}",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    }

    from urllib.parse import urlencode

    from globals.config import api_ip_pool

    for ipaddr in api_ip_pool:
        resp = None
        try:
            resp = requests.post(
                f"https://{ipaddr}/auth/oauth/token",
                headers=header,
                data=urlencode(
                    {"grant_type": "refresh_token", "refresh_token": refresh_token}
                ),
            )
        except:
            continue
        else:
            break
    if not resp:
        raise TimeoutError

    access_token = resp.json()["access_token"]
    refresh_token = resp.json()["refresh_token"]


def pseudo_fast_login() -> dict:
    return {
        "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQwNGMxYzYxNTkwNDBmZGRhN2FlYjI0ODViOWU0MTBlZDM0ZDJkMDgiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJOOFFGRzhORUJKNVQzNUZCIiwiZXhwIjoxNjk4NDgxNDE2LCJpYXQiOjE2OTg0ODA0NTYsImlzcyI6IlJFTjMzSzNGVFZDVkZOQks0UlRUWkFDWVQ0Iiwic3ViIjoiVERYUEdVRVRRNUZFSkdGRUxXSTNLR09MU1EiLCJ3b3RjLW5hbWUiOiJ6YWMjNDYxNTMiLCJ3b3RjLWRvbW4iOiJ3aXphcmRzIiwid290Yy1nYW1lIjoiYXJlbmEiLCJ3b3RjLWZsZ3MiOjEsIndvdGMtcm9scyI6WyJNRE5BTFBIQSJdLCJ3b3RjLXBybXMiOltdLCJ3b3RjLXNjcHMiOlsiZmlyc3QtcGFydHkiXSwid290Yy1wZGdyIjoiWUtGNFdJMlpSWkQ3REtWRzJOUzVaWlNOM1UiLCJ3b3RjLXNndHMiOltdLCJ3b3RjLXNvY2wiOnt9LCJ3b3RjLWNuc3QiOjB9.XXwAsFSSdAJ68S4kxITvecLBxnRUCplDpzGhfYVTODRoxg00ohzJhwEYJySfLfU-w9uyI4upF061PlreMoqAKy2fNHDqv7CueHuYPMPVYZ0CcaTcvlFBSkKn0XEoUJTGgaWEITwzzAAIJ5lnTp8Dk56ayIuWZ2Eh8aAH9Fv8NGKD33MAN2MSxtOOOxSAnJChzrlvQhjsQoWdIV9m1taHHAxlCpUa5P5b75WB3V0P1Aw8PwN1YUtIgwYGFKThp6rplh1i7HqkUNryz1xWm1va9bEJoMT3x1O32YhEyyd-Pt5b6pulbZhrQkBCaiBTMRh03X7m2ahuuHni9iZ2nbGAyw",
        "refresh_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjM0NmM4YTY1NTBlZGI5MDRjM2IyNWI3ODlmOTllNjU3ODA4MGJiOTUiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJOOFFGRzhORUJKNVQzNUZCIiwiZXhwIjoxNjk5NjkwMDU2LCJpYXQiOjE2OTg0ODA0NTYsImlzcyI6IlJFTjMzSzNGVFZDVkZOQks0UlRUWkFDWVQ0Iiwic3ViIjoiVERYUEdVRVRRNUZFSkdGRUxXSTNLR09MU1EiLCJ3b3RjLWRvbW4iOiJ3aXphcmRzIiwid290Yy1zY3BzIjpbImZpcnN0LXBhcnR5Il0sIndvdGMtZmxncyI6MSwid290Yy1wZGdyIjoiWUtGNFdJMlpSWkQ3REtWRzJOUzVaWlNOM1UiLCJ3b3RjLXNvY2wiOnt9LCJ3b3RjLWNuc3QiOjB9.MC4nvifTgw54Uuh1pQax7rOwcyIJOfNcogHTmQLzpYB2whnAVGsIypboyexnMffUfpaw5K_z8FsM0PbWZtHX5eWoWm6Ez4HmODF3yAGuTi1qIe9onfFhCySdY6wMsVBrTq2y41pfvxJqTp7-99LWDjfTuH71GwRKUpLSkSWiWtCFeYfnxzgDLF3zWcyNEdjNtCXyF0-vp8Z62qjx3pb-dETbA7R5I0poq2ankXvUx28fymjbfA6KOFrQ-tAu7a7RLTdtUT7z2RyVf8w8Z6gYxza4oJiMtgicON1MUbTY-fqV15w83JIOqnPp2WOWQeGfJ4t7XzBipdYJns0yDqORkw",
        "expires_in": 900,
        "token_type": "Bearer",
        "client_id": "N8QFG8NEBJ5T35FB",
        "game_id": "arena",
        "domain_id": "wizards",
        "persona_id": "TDXPGUETQ5FEJGFELWI3KGOLSQ",
        "account_id": "REN33K3FTVCVFNBK4RTTZACYT4",
        "display_name": "zac#46153",
    }
