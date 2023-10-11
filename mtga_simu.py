import requests
import json
import winreg

MTGA_folder = ".."

assembly_path = MTGA_folder + r"/MTGA_Data/Managed/"

import sys
sys.path.append(assembly_path)

import clr
clr.AddReference("Wizards.Mtga.Metadata")
clr.AddReference("Assembly-CSharp")

from Wizards.Mtga import Metadata, Global

client_version = "2023.30.0"
# buildNumber = Metadata.ContentVersionBuildPart
# sourceVersion = Metadata.SourceVersion
# buildInfo = Metadata.BuildInfo
full_client_version = "2023.30.0.4683"

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

uri = requests.get("https://prod.doorbellmat.w2.mtgarena.com/doorbell.config").text

text: str = "https://prod.doorbellmat.w2.mtgarena.com"
if "https://prod" in text:
	doorCode = "46u7OAmyEZ6AtfgaPUHiXNiC55/mrtp3aAmE018KZamDhvr0vZ8mxg=="
else:
	doorCode = "ta4kBQcrBfdGd8AUjrv7lj9pYyA3Kkj9p39byJXuTdTBiZxRC6xgRQ=="
uri += "?code=" + doorCode # ? maybe not

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
client_id = resp.json()["client_id"]
game_id = resp.json()["game_id"]
domain_id = resp.json()["domain_id"]
persona_id = resp.json()["persona_id"]
account_id = resp.json()["account_id"]
# expires_in, token_type, client_id, game_id, domain_id, persona_id, account_id, display_name

# get profile
resp = requests.get("https://api.platform.wizards.com/profile",
					 headers={ "Authorization": f"Bearer {access_token}" })
account_id = resp.json()["accountID"]
# print(f'{client_id=}')
# print(f'{game_id=}')
# print(f'{domain_id=}')
# print(f'{persona_id=}')
# print(f'{account_id=}')

import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_verify_locations('./cert.pem')
#TcpConnection(this._logger, 17, ServicePointManager.ServerCertificateValidationCallback, 0x7FFFFFFF, 5);
from urllib.parse import urlparse
parse_result = urlparse(fdUri)

# panel control

######tcpConnnection		private void ProcessRead(IAsyncResult ar)
class StreamChatter:
    def __init__(self, ssock: ssl.SSLSocket):
        self.buf = b''
        self.flag = ''
        self.reply = {}
        self.ssock = ssock
        self.some_counter = 0
    
    @staticmethod
    def packet_str(data: str) -> bytes:
        byte_length = len(data.encode())
        return bytes([3, 1]) + byte_length.to_bytes(4, 'little') + data.encode()

    # check the inbox, make sure first there should be something
    def check(self) -> bytes:
        try:
            self.buf += self.ssock.recv()
        except TimeoutError:
            pass
        if self.some_counter > 6:
             raise b''
        if len(self.buf) == 0: # timeout test
            self.some_counter += 1
            return b''
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
        self.ssock.send(StreamChatter.packet_str(json.dumps(message, separators=(',', ':'))))

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
			"ClientVersion": full_client_version,
			"Token": access_token,
            "PersonaId": None,
			"ScreenName": None,
			"Roles": None,
			"PlatformId": "Windows"
        })
        if not resp == None and "Payload" in resp:
            session_id = json.loads(resp['Payload'])["SessionId"]
            print("Client panel authenticated.")

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
                    print("Latest used event deck acquired!")
                  # TODO: what is LTP_xxxxx

        if play_deck_id == None:
            raise "111"
        
        resp = chatter.inquire(1000, {})  # getQuests
        quest_msg = None
        if not resp == None and "Payload" in resp:
            quest_msg = json.loads(resp["Payload"])
            for quest in quest_msg["quests"]:
                print(quest["questId"])
                # print(quest["canSwap"])
                print(quest["chestDescription"]["quantity"])
                # TODO:
                # if "canSwap" in quest:
                #     resp = chatter.inquire(1001, {"QuestId": quest["questId"]})  # swapQuests
                    # break

        # resp = chatter.inquire(1200, {})  # PeriodicRewards_GetStatus
        # quest_status_msg = None
        # if not resp == None and "Payload" in resp:
        #     quest_status_msg = json.loads(resp["Payload"])
        # resp = chatter.inquire(624, {"CacheVersion":0, "ShowAllEvents": False})  # Event_GetActiveEventsV2
            
            
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
                print("Extra information acquired!")

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

        chatter.inquire(601, {  # Event_Drop
            "EventName": "Play",
        })

        # frontdoorconnectionAWS -> joinEvent
        resp1 = chatter.inquire(600, {  # Event_Join
            "EventName": "Play",
            "EntryCurrencyType": "None",
            "EntryCurrencyPaid": 0,
            "CustomTokenId": None
        })
        print("Joining event 'standard play'.")
        
        aws_deck, aws_summary = toAwsModel(play_deck_body, play_deck_summary)
        resp2 = chatter.inquire(622, {  # Event_SetDeckV2
            "EventName": "Play",
			"Summary": aws_summary,
			"Deck": aws_deck
        })
        
        # chatter.inquire(623, {  # getCourse
        # })

        if not ("Payload" in resp1 and "Payload" in resp2):
            print(resp1)
            print(resp2)
            raise Exception(b'')
        #assert "Payload" in resp1 and "Payload" in resp2

        resp = chatter.inquire(603, {  # EnterPairing
            "EventName": "Play",
            "EventCode": None,
        })
        print("Entering pairing!")
        print(resp)

        import time
        for _ in range(20):
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
                match_id = resp["MatchInfo"]["MatchId"]
                event_id = resp["MatchInfo"]["EventId"]
                print("Match created!")
                break

# battlefield control

import message_pb2 as pb
from datetime import datetime
class ProtoStreamChatter(StreamChatter):
    def __init__(self, ssock: ssl.SSLSocket):
        self.request_id = 0
        super().__init__(ssock)

    @staticmethod
    def packet_str(data: bytes) -> bytes:
        return bytes([3, 1]) + len(data).to_bytes(4, 'little') + data
    
    # send the req with protobuf serialization
    def speak(self, message: pb.ClientToMatchServiceMessage):
        self.ssock.send(ProtoStreamChatter.packet_str(message.SerializeToString()))

    # send the payload, auto appending the transaction ID, request ID, timestamp
    def propose(self, ty: pb.ClientToMatchServiceMessageType, payload) -> str:
        self.request_id += 1
        trans_id = str(uuid.uuid1())
        self.speak(pb.ClientToMatchServiceMessage(
            requestId=self.request_id,
            timestamp=int((datetime.utcnow() - datetime(1, 1, 1)).total_seconds() * 10 ** 7),
            transactionId=trans_id,
            clientToMatchServiceMessageType=ty,
            payload=payload.SerializeToString()
        ))
        self.reply[trans_id] = []
        return trans_id
    
    # get the resp
    def admit(self) -> str | None:
        resp = self.check()
        if 'valid' == self.flag:
            msg = pb.MatchServiceToClientMessage()
            msg.ParseFromString(resp)
            self.flag = ''
            if msg.transactionId in self.reply:
                self.reply[msg.transactionId] += [msg]
            else:
                self.reply[msg.transactionId] = [msg]
                return msg.transactionId

    def construct_door_connect_request(self) -> pb.ClientToMatchDoorConnectRequest:
        connect_message = pb.ClientToGREMessage(
            type=pb.ClientMessageType.ClientMessageType_ConnectReq,
            systemSeatId=0,
			connectReq=pb.ConnectReq(
                grpVersion=pb.Version(
                    majorVersion=int(client_version.split(".")[0]),
                    minorVersion=int(client_version.split(".")[1])
                ),
				defaultSettings=pb.SettingsMessage(
                    stops=[
                        pb.Stop(
                            stopType=pb.StopType.StopType_UpkeepStep,
                            appliesTo=pb.SettingScope.SettingScope_Team,
                            status=pb.SettingStatus.SettingStatus_Clear
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_DrawStep,
                            appliesTo=pb.SettingScope.SettingScope_Team,
                            status=pb.SettingStatus.SettingStatus_Clear
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_PrecombatMainPhase,
                            appliesTo=pb.SettingScope.SettingScope_Team,
                            status=pb.SettingStatus.SettingStatus_Set
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_BeginCombatStep,
                            appliesTo=pb.SettingScope.SettingScope_Team,
                            status=pb.SettingStatus.SettingStatus_Set
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_DeclareAttackersStep,
                            appliesTo=pb.SettingScope.SettingScope_Team,
                            status=pb.SettingStatus.SettingStatus_Set
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_DeclareBlockersStep,
                            appliesTo=pb.SettingScope.SettingScope_Team,
                            status=pb.SettingStatus.SettingStatus_Set
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_FirstStrikeDamageStep,
                            appliesTo=pb.SettingScope.SettingScope_Team,
                            status=pb.SettingStatus.SettingStatus_Set
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_CombatDamageStep,
                            appliesTo=pb.SettingScope.SettingScope_Team,
                            status=pb.SettingStatus.SettingStatus_Clear
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_EndCombatStep,
                            appliesTo=pb.SettingScope.SettingScope_Team,
                            status=pb.SettingStatus.SettingStatus_Clear
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_PostcombatMainPhase,
                            appliesTo=pb.SettingScope.SettingScope_Team,
                            status=pb.SettingStatus.SettingStatus_Set
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_EndStep,
                            appliesTo=pb.SettingScope.SettingScope_Team,
                            status=pb.SettingStatus.SettingStatus_Clear
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_UpkeepStep,
                            appliesTo=pb.SettingScope.SettingScope_Opponents,
                            status=pb.SettingStatus.SettingStatus_Clear
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_DrawStep,
                            appliesTo=pb.SettingScope.SettingScope_Opponents,
                            status=pb.SettingStatus.SettingStatus_Clear
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_PrecombatMainPhase,
                            appliesTo=pb.SettingScope.SettingScope_Opponents,
                            status=pb.SettingStatus.SettingStatus_Clear
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_BeginCombatStep,
                            appliesTo=pb.SettingScope.SettingScope_Opponents,
                            status=pb.SettingStatus.SettingStatus_Set
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_DeclareAttackersStep,
                            appliesTo=pb.SettingScope.SettingScope_Opponents,
                            status=pb.SettingStatus.SettingStatus_Set
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_DeclareBlockersStep,
                            appliesTo=pb.SettingScope.SettingScope_Opponents,
                            status=pb.SettingStatus.SettingStatus_Set
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_FirstStrikeDamageStep,
                            appliesTo=pb.SettingScope.SettingScope_Opponents,
                            status=pb.SettingStatus.SettingStatus_Set
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_CombatDamageStep,
                            appliesTo=pb.SettingScope.SettingScope_Opponents,
                            status=pb.SettingStatus.SettingStatus_Clear
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_EndCombatStep,
                            appliesTo=pb.SettingScope.SettingScope_Opponents,
                            status=pb.SettingStatus.SettingStatus_Clear
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_PostcombatMainPhase,
                            appliesTo=pb.SettingScope.SettingScope_Opponents,
                            status=pb.SettingStatus.SettingStatus_Clear
                        ),
                        pb.Stop(
                            stopType=pb.StopType.StopType_EndStep,
                            appliesTo=pb.SettingScope.SettingScope_Opponents,
                            status=pb.SettingStatus.SettingStatus_Set
                        ),
                    ],
                    autoPassOption=pb.AutoPassOption.AutoPassOption_ResolveMyStackEffects,
                    graveyardOrder=pb.OrderingType.OrderingType_OrderArbitraryAlways,
                    manaSelectionType=pb.ManaSelectionType.ManaSelectionType_Auto,
                    defaultAutoPassOption=pb.AutoPassOption.AutoPassOption_ResolveMyStackEffects,
                    smartStopsSetting=pb.SmartStopsSetting.SmartStopsSetting_Enable,
                    autoTapStopsSetting=pb.AutoTapStopsSetting.AutoTapStopsSetting_Enable,
                    autoOptionalPaymentCancellationSetting=pb.Setting.Setting_Enable
                ),
				protoVer=max(pb.ProtoVersion.values())
            )
        )
        return pb.ClientToMatchDoorConnectRequest(
            matchId=match_id,
            mcFabricUri=controller_fabric_uri,
            clientToGreMessageBytes=connect_message.SerializeToString(),
        )
    
    def get_gre_client_messages(self, trans_id=None):
        for _ in range(20):
            time.sleep(1)
            if trans_id:
                chatter.admit()
            else:
                trans_id = chatter.admit()
            if trans_id and chatter.reply[trans_id]:
                break
        
        return [msg
            for trans in chatter.reply[trans_id] if hasattr(trans, 'greToClientEvent')
            for msg in trans.greToClientEvent.greToClientMessages]
        
with socket.create_connection(address=(match_endpoint_host, match_endpoint_port)) as sock:
    with context.wrap_socket(sock, server_hostname=match_endpoint_host) as ssock:
        ssock.do_handshake()
        # GREConnection OnMsgReceived
        chatter = ProtoStreamChatter(ssock)
        trans_id = chatter.propose(
            pb.ClientToMatchServiceMessageType.ClientToMatchServiceMessageType_AuthenticateRequest,
            pb.AuthenticateRequest(
                clientId=persona_id,
                playFabSessionTicket=access_token,
                inactivityTimeoutMs=60000,
                clientInfo=pb.ClientInfo(
                    clientType=pb.ClientType.ClientType_User,
                    clientVersion=client_version
                )
            )
        )
        
        for _ in range(20):
            time.sleep(1)
            chatter.admit()
            if chatter.reply[trans_id]:
                print("Duel access authenticated!")
                break
        
        trans_id = chatter.propose(
            pb.ClientToMatchServiceMessageType.ClientToMatchServiceMessageType_ClientToMatchDoorConnectRequest,
            chatter.construct_door_connect_request()
        )

        counter = 0
        for _ in range(20):
            time.sleep(1)
            chatter.admit()
            if chatter.reply[trans_id]:
                counter += 1
                print("Room state updated!")
                if counter >= 2:
                    break
        assert len(chatter.reply[trans_id]) == 2
        choose_starting_req = None
        for msg in chatter.reply[trans_id]:
            if hasattr(msg, "matchGameRoomStateChangedEvent"):
                room_info = msg.matchGameRoomStateChangedEvent.gameRoomInfo
            if hasattr(msg, "greToClientEvent"):
                client_msgs = msg.greToClientEvent.greToClientMessages
        for item in client_msgs:
            match item.type:
                case pb.GREMessageType.GREMessageType_ConnectResp:
                    conn_resp = item.connectResp
                case pb.GREMessageType.GREMessageType_GameStateMessage:
                    game_state = item.gameStateMessage
                case pb.GREMessageType.GREMessageType_DieRollResultsResp:
                    die_roll = item.dieRollResultsResp
                case pb.GREMessageType.GREMessageType_ChooseStartingPlayerReq:
                    choose_starting_req = item
        
        # TODO: game manager init
        # MatchManager -> private void OnMessageReceived(GREToClientMessage msg)
        game_manager = {}
        for item in client_msgs:
            if len(item.systemSeatIds) == 1:
                game_manager["local_player_id"] = item.systemSeatIds[0]
        game_manager["win_condition"] = game_state.gameInfo.matchWinCondition
        game_manager["game_results"] = game_state.gameInfo.results
        game_manager["format"] = game_state.gameInfo.superFormat
        game_manager["variant"] = game_state.gameInfo.variant
        game_manager["current_game_number"] = game_state.gameInfo.gameNumber

        # DieRollResultStateAnnotationParser
        # ChooseStartingPlayerWorkflow 
        if choose_starting_req:
            #auto choose play
            trans_id = chatter.propose(
                pb.ClientToMatchServiceMessageType.ClientToMatchServiceMessageType_ClientToGREMessage,
                pb.ClientToGREMessage(
                    type=pb.ClientMessageType.ClientMessageType_ChooseStartingPlayerResp,
                    gameStateId=choose_starting_req.gameStateId,
                    respId=choose_starting_req.msgId,
                    chooseStartingPlayerResp=pb.ChooseStartingPlayerResp(
                        teamType=choose_starting_req.chooseStartingPlayerReq.teamType,
                        systemSeatId=game_manager["local_player_id"],
                        teamId=game_manager["local_player_id"],
                    )
                )
            )

            gre_msgs = chatter.get_gre_client_messages(trans_id)
            print("Room state updated after your choosing hand!")
            
        else:
            gre_msgs = chatter.get_gre_client_messages()
            print("Room state updated after opponent's choosing hand!")

        mulligan_msg = [msg for msg in gre_msgs if msg.type == pb.GREMessageType.GREMessageType_MulliganReq]
        while not mulligan_msg:
            gre_msgs = chatter.get_gre_client_messages()
            mulligan_msg = [msg for msg in gre_msgs if msg.type == pb.GREMessageType.GREMessageType_MulliganReq]
        mulligan_msg = mulligan_msg[0]

        # no change hands for now
        trans_id = chatter.propose(
            pb.ClientToMatchServiceMessageType.ClientToMatchServiceMessageType_ClientToGREMessage,
            pb.ClientToGREMessage(
                type=pb.ClientMessageType.ClientMessageType_MulliganResp,
                gameStateId=mulligan_msg.gameStateId,
                respId=mulligan_msg.msgId,
                mulliganResp=pb.MulliganResp(
                    decision=pb.MulliganOption.MulliganOption_AcceptHand
                )
            )
        )

        gre_msgs = chatter.get_gre_client_messages(trans_id)
        print("keep all in default.")
        
        # Wotc.Mtga.DuelScene.Interactions.ActionsAvailable.Highlighting
        def highlighted_move(action: pb.Action) -> bool:
            if action == None:
                return False
            # not affordable
            if not ((action.actionType == pb.ActionType.ActionType_Play or action.actionType == pb.ActionType.ActionType_PlayMDFC) or \
                    (len(action.autoTapSolution.autoTapActions) > 0) or \
                    (all([pb.ManaColor.ManaColor_Phyrexian in requirement.color or
                            pb.ManaColor.ManaColor_X in requirement.color
                            for requirement in action.manaCost]))):
                return False
            if action.abilityGrpId == 75081 and action.highlight == pb.HighlightType.HighlightType_Cold and \
                action.actionType == pb.ActionType.ActionType_Activate:
                return False
            if action.highlight == pb.HighlightType.HighlightType_Hot:
                return True
            # shouldn't play, temp unavailable
            # if action.abilityGrpId != 0 and instance.PlayWarnings.Exists((ShouldntPlayData x) => x.AbilityId == action.AbilityGrpId):
            #     return False
            return True

        #  AI_strategy see C# class RandomStrategy() and peers
        from alterego import respond

        class MtgaBot:
            def __init__(self):
                self.state = {}
                pass
            def handle_request(
                      self,
                      req: pb.ActionsAvailableReq,
                      new_state: pb.GameStateMessage | None = None,
                ) -> pb.PerformActionResp | None:
                if new_state:
                    self.update_state(new_state)
                for action in req.actions:
                    if highlighted_move(action):
                        return pb.PerformActionResp(
                            autoPassPriority=pb.AutoPassPriority.AutoPassPriority_Yes,
                            actions=[action]
                        )
                # if can_pass ...

            def update_state(self, new_state):
                pass

            def clr_respond(self, msg):
                return respond(msg)

        bot = MtgaBot()
        gre_msgs = []
        for _ in range(40):
            gre_msgs += chatter.get_gre_client_messages()
            # print(gre_msgs)
            print([name for msg in gre_msgs
                   for name, value in pb.GREMessageType.items() if value == msg.type])
            gre_msgs = [msg
                        for msg in gre_msgs
                        if msg.type in [pb.GREMessageType.GREMessageType_ActionsAvailableReq,
                                        pb.GREMessageType.GREMessageType_SelectTargetsReq,
                                        pb.GREMessageType.GREMessageType_DeclareAttackersReq,
                                        pb.GREMessageType.GREMessageType_SelectNReq,
                                        pb.GREMessageType.GREMessageType_DeclareBlockersReq,
                                        ]
            ]
            # TODO: ClientMessageType_SubmitAttackersReq
            for msg in gre_msgs:
                print(msg)
            else:
                print("No actions for now!")
            # for action_msg in gre_msgs:
                # if act := bot.handle_request(action_msg.actionsAvailableReq):
                #     print(act)
                #     trans_id = chatter.propose(
                #         pb.ClientToMatchServiceMessageType.ClientToMatchServiceMessageType_ClientToGREMessage,
                #         pb.ClientToGREMessage(
                #             type=pb.ClientMessageType.ClientMessageType_PerformActionResp,
                #             gameStateId=action_msg.gameStateId,
                #             respId=action_msg.msgId,
                #             performActionResp=act
                #         )
                #     )
                #     break
            while gre_msgs:
                action_msg = gre_msgs.pop()
                if act := bot.clr_respond(action_msg):
                    print(act)
                    trans_id = chatter.propose(
                        pb.ClientToMatchServiceMessageType.ClientToMatchServiceMessageType_ClientToGREMessage,
                        pb.ClientToGREMessage(
                            type=pb.ClientMessageType.ClientMessageType_PerformActionResp,
                            gameStateId=action_msg.gameStateId,
                            respId=action_msg.msgId,
                            performActionResp=act.performActionResp
                        )
                    )
                    break

                # private void SetupBattlefield(GREToClientMessage connectMessage)