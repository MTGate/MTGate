import requests
import json
import winreg

client_version = "2023.29.10"
MTGA_folder = ".."

def get_reg_val(winreg_modifier: int, loc: str, name: str) -> str:
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

# obtain from reg
player_id = get_reg_val(winreg.HKEY_CURRENT_USER,
						r"Software\\Wizards Of The Coast\\MTGA\\",
						"SupplementalInstallID")
player_id = str(player_id, 'utf-8')
# probably only useful when updating
# install_id = get_reg_val(winreg.HKEY_LOCAL_MACHINE,
# 						 r"Software\\WOW6432Node\\Wizards of the Coast\\",
						#  "userID")


# ring the door bell

# Coroutine_GameStartup -> FindEnvironment -> (read config or) default,
# default name is "Prod" (or "default-prod-environment-that-is-not-a-magic-string"?)
doorbell_request = {
	"clientVersion": client_version,
	"environmentKey": "Prod",
	"playerId": player_id,
	"platformKey": "windows"
}

text: str = "https://prod.doorbellmat.w2.mtgarena.com"
if "https://prod" in text:
	doorCode = "46u7OAmyEZ6AtfgaPUHiXNiC55/mrtp3aAmE018KZamDhvr0vZ8mxg=="
else:
	doorCode = "ta4kBQcrBfdGd8AUjrv7lj9pYyA3Kkj9p39byJXuTdTBiZxRC6xgRQ=="
uri = "https://doorbellprod.azurewebsites.net/api/ring?code=" + doorCode

resp = requests.post(uri, data=json.dumps(doorbell_request, ensure_ascii=False, separators=(',', ':')).encode('utf-8'),
				  headers={"content-type": "application/json"})

# get the front door uri
fdUri = resp.json()['fdURI']

print(fdUri)

# get login token
refresh_token = get_reg_val(winreg.HKEY_CURRENT_USER,
						r"Software\\Wizards Of The Coast\\MTGA\\",
						"WAS-RefreshTokenE")
import base64
refresh_token = base64.b64decode(str(refresh_token, 'utf-8'))
refresh_token = str(refresh_token, 'ascii').strip()

# fast login  //  WizardsAccountsClient.LogIn_Fast()
import uuid
# session_id = str(uuid.uuid1())
# # BILoggingUtils.SendWithDefaults
# def sendDefaults(event_type: str, data: dict) -> dict:
# 	data.update({
# 		"RegionId": "CHN",
# 		"InstallId": player_id,
# 		"PersonaId": player_id,
# 		"AccountId": player_id,
# 		"ClientPlatform": "Windows",
# 		"AppSessionId": session_id,
# 	})
# 	transaction_id = str(uuid.uuid1())
# 	from datetime import datetime
# 	payload = json.dumps({
# 		"EventType": 0x48, # type.generic
# 		"EventName": event_type,
# 		"EventTime": datetime.utcnow().isoformat().replace("+00:00", "Z"),
# 		"Data": data
# 	}, separators=(',', ':'))
# 	return {
# 		"id": transaction_id,
# 		"request": {
# 			"Type": 0x778, #  ECmdType.LogBusinessEvents in FrontDoorConnectionAWS.LogBusinessEvent
# 			"TransId": transaction_id,
# 			"Payload": payload,
# 		}
# 	}
# from PAPA.GetDefaultEnvironment()
clientId = "N8QFG8NEBJ5T35FB"
clientSecret = "VMK1RE8YK6YR4EABJU91"
# epicWASClientId = "2186e6b404a54e6fa062c4f37febb22d"
# epicWASClientSecret = "12fd208919fa46cdaebb797174a05c25"
# steamClientId = "AW2T7QJ7ZJEAXGOQUUYVEK5PYE"
# steamClientSecret = "AFSSE6DSIJGHRPCY3QICRK57BQ"

header = { "Authorization": f"Basic {str(base64.b64encode(f'{clientId}:{clientSecret}'.encode()), 'utf-8')}",
		  "Content-Type": "application/x-www-form-urlencoded; charset=utf-8" }

from urllib.parse import urlencode
resp = requests.post("https://api.platform.wizards.com/auth/oauth/token",
					 headers=header,
					 data=urlencode({"grant_type": "refresh_token", "refresh_token": refresh_token}))

access_token = resp.json()["access_token"]
refresh_token = resp.json()["refresh_token"]
# expires_in, token_type, client_id, game_id, domain_id, persona_id, account_id, display_name

# get profile
resp = requests.get("https://api.platform.wizards.com/profile",
					 headers={ "Authorization": f"Bearer {access_token}" })
account_id = resp.json()["accountID"]
print(account_id)


def packet_str(data: str) -> bytes:
	byte_length = len(data.encode())
	return bytes([3, 1]) + byte_length.to_bytes(4, 'little') + data.encode()

import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_verify_locations('./cert.pem')
#TcpConnection(this._logger, 17, ServicePointManager.ServerCertificateValidationCallback, 0x7FFFFFFF, 5);
from urllib.parse import urlparse
parse_result = urlparse(fdUri)

######tcpConnnection		private void ProcessRead(IAsyncResult ar)
class StreamChatter:
    def __init__(self, ssock: ssl.SSLSocket):
        self.buf = b''
        self.flag = ''
        self.reply = {}
        self.ssock = ssock
    
    # check the inbox, make sure first there should be something
    def check(self) -> bytes:
        try:
            self.buf += self.ssock.recv()
        except TimeoutError:
            pass
        if len(self.buf) < 6:
            raise RuntimeError(self.buf)
        if self.buf[0] == 0x03 and self.buf[1] == 0x02: # ping
            length = int.from_bytes(self.buf[2:6], 'little')
            assert length == 4
            self.ssock.send(bytes([3, 3]) + (4).to_bytes(4, 'little') + self.buf[6: 10])
            self.buf = self.buf[10:]
            self.flag = 'ping'
            return b''
        elif self.buf[0] == 0x03 and self.buf[1] == 0x03: # pong
            self.buf = self.buf[10:]
            self.flag = 'pong'
            return b''
        elif self.buf[0] == 0x03 and self.buf[1] == 0x01: # msg
            length = int.from_bytes(self.buf[2:6], 'little')
            while length > len(self.buf) - 6:
                self.buf += self.ssock.recv(length - len(self.buf) + 6)
            self.flag = 'valid'
            temp = self.buf[6:(length+6)]
            self.buf = self.buf[(length+6):]
            return temp
        else:
            raise RuntimeError(self.buf)

    def speak(self, message: dict):
        self.ssock.send(packet_str(json.dumps(message, separators=(',', ':'))))

    def ping(self, timestamp=555):
        self.ssock.send(bytes([3, 2]) + (4).to_bytes(4, 'little') + timestamp.to_bytes(4, 'little'))

    def inquire(self, ty: int, payload: dict) -> dict | None:
        trans_id = str(uuid.uuid1())
        self.speak({"Type": ty, "TransId": trans_id, "Payload":
                    json.dumps(payload, separators=(',', ':'))})
        while self.flag != 'valid':
            resp = self.check()
        resp = json.loads(resp.decode())
        self.flag = ''
        if resp['TransId'] == trans_id:
            return resp
        else:
            self.reply[(ty, trans_id)] = None
            self.reply[(resp["Type"], resp["TransId"])] = resp
            return None
        
with socket.create_connection(address=(parse_result.hostname, parse_result.port)) as sock:
    with context.wrap_socket(sock, server_hostname=parse_result.hostname) as ssock:
        ssock.do_handshake()
        ssock.settimeout(10.0)

        chatter = StreamChatter(ssock)

        resp = chatter.inquire(0, { # authenticate
			"ClientVersion": "2023.29.10.4670",
			"Token": access_token,
            "PersonaId": None,
			"ScreenName": None,
			"Roles": None,
			"PlatformId": "Windows"
        })
        if not resp == None and "Payload" in resp:
            session_id = json.loads(resp['Payload'])["SessionId"]

        import gzip
        def decompress(content: str) -> dict:
            formats = resp["Payload"]
            formats = base64.b64decode(formats)
            #print(int.from_bytes(formats[0:4], 'little'))
            return json.loads(gzip.decompress(formats[4:]).decode())

        # resp = chatter.inquire(6, {}) # getFormats
        # if not resp == None:
        #     if resp["Compressed"] == True:
        #         formats = resp["Payload"]
        #         formats = base64.b64decode(formats)
        #         print(int.from_bytes(formats[0:4], 'little'))
        #         formats = json.loads(gzip.decompress(formats[4:]).decode())

        resp = chatter.inquire(1910, {}) # getPlayerPreferences
        play_deck_id = None
        if not resp == None and "Payload" in resp:
            for event_deck in json.loads(json.loads(resp["Payload"])["Preferences"]["RecentGamesData"]):
                if event_deck["EventName"] == "Play":
                    play_deck_id = event_deck["DeckId"]
                  # TODO: what is LTP_xxxxx

        if play_deck_id == None:
            raise "111"

        resp = chatter.inquire(400, { # getDeck (body)
            "DeckId": play_deck_id
        })
        play_deck_body = None
        if not resp == None and "Payload" in resp:
            play_deck_body = json.loads(resp["Payload"])

        resp = chatter.inquire(1, {}) # startHook
        deck_summaries = None
        play_deck_summary = None
        if not resp == None:
            if resp["Compressed"] == True:
                resp = decompress(resp["Payload"])
                # with open('./sample_hook.json', 'w') as f:
                #     f.write(json.dumps(resp, indent=4))
                deck_summaries = resp["DeckSummariesV2"]
                for summary in deck_summaries:
                    if summary["DeckId"] == play_deck_id:
                        play_deck_summary = summary

		# AwsEventServiceWrapper.SubmitEventDeck -> toAwsModel
        def toAwsModel(deck_body: dict, deck_summary: dict) -> (dict, dict):
            summary = deck_summary
            if "IsCompanionValid" in summary:
                summary["IsCompanionValid"] = False
            summary["FormatLegalities"] = {}
            if not "Avatar" in summary["PreferredCosmetics"]:
                summary["PreferredCosmetics"]["Avatar"] = None
            if not "Sleeve" in summary["PreferredCosmetics"]:
                summary["PreferredCosmetics"]["Sleeve"] = None
            if not "Pet" in summary["PreferredCosmetics"]:
                summary["PreferredCosmetics"]["Pet"] = None
            if not "Emotes" in summary["PreferredCosmetics"]:
                summary["PreferredCosmetics"]["Emotes"] = []
            summary["DeckValidationSummaries"] = []
            summary["NetDeckFolderId"] = None
            summary["IsNetDeck"] = False
            deck = deck_body
            deck["DoPreferReducedSideboard"] = False
            return deck, summary
        
        aws_deck, aws_summary = toAwsModel(play_deck_body, play_deck_summary)
        resp1 = chatter.inquire(622, {  # getPlayerPreferences
            "EventName": "Play",
			"Summary": aws_summary,
			"Deck": aws_deck
        })
        
        resp2 = chatter.inquire(623, {  # getCourse
            "EventName": "Play",
			"Summary": aws_summary,
			"Deck": aws_deck
        })

        assert "Payload" in resp1 and "Payload" in resp2

        resp = chatter.inquire(603, {  # EnterPairing
            "EventName": "Play",
            "EventCode": None,
        })
        print(resp)

        import time
        for _ in range(10):
            time.sleep(1)
            resp = chatter.check()
            if 'valid' == chatter.flag:
                resp = json.loads(resp.decode())
                print(resp)

                # Matchmaking.onMatchCreated, MatchSceneManager.onMatchReady
                resp = json.loads(resp["Payload"])
                controller_fabric_uri = resp["MatchInfo"]["McFabricId"]
                match_endpoint_host = resp["MatchInfo"]["MatchEndpointHost"]
                match_endpoint_port = resp["MatchInfo"]["MatchEndpointPort"]
                opponent_screen_name = resp["MatchInfo"]["OpponentScreenName"]
                # opponentIsWotc, Battlefield, OpponentRankingClass, ClientMetadata,
                # OpponentEmotesSelection, OpponentEmotesSelection, OpponentPetSelection,
                # PetSelection, OpponentSleeveSelection, OpponentAvatarSelection,
                # AvatarSelection,
                matchId = resp["MatchInfo"]["MatchId"]
                eventId = resp["MatchInfo"]["EventId"]

assembly_path = MTGA_folder + "/" + r"./MTGA_Data/Managed/"

import sys
sys.path.append(assembly_path)

import clr
clr.AddReference("Wizards.MDN.GreProtobuf.Unity")
clr.AddReference("Google.Protobuf")

from Wotc.Mtgo.Gre.External.Messaging import MatchServiceToClientMessage
from Google.Protobuf import CodedInputStream

def read(buffer: bytes, offset: int, length: int) -> dict:
    stream = CodedInputStream(buffer, offset, length)
    message = MatchServiceToClientMessage()
    message.MergeFrom(stream)
    return json.loads(message.ToString())

class ProtoStreamChatter(StreamChatter):
    def speak(self, message: dict):
        self.ssock.send(packet_str(json.dumps(message, separators=(',', ':'))))


    def proto_inquire(self, ty: int, payload: dict) -> dict:
        trans_id = str(uuid.uuid1())
        self.speak({"Type": ty, "TransId": trans_id, "Payload":
                    json.dumps(payload, separators=(',', ':'))})
        while self.flag != 'valid':
            resp = self.check()
        resp = json.loads(resp.decode())
        self.flag = ''
        if resp['TransId'] == trans_id:
            return resp
        else:
            self.reply[(ty, trans_id)] = None
            self.reply[(resp["Type"], resp["TransId"])] = resp
            return None

with socket.create_connection(address=(match_endpoint_host, match_endpoint_port)) as sock:
    with context.wrap_socket(sock, server_hostname=match_endpoint_host) as ssock:
        ssock.do_handshake()
        # GREConnection OnMsgReceived
        from google.protobuf.internal.decoder import ReadTag, ReadInt32
        chatter = StreamChatter(ssock)
        