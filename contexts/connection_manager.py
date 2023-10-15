import ssl
import uuid
import json
import socket
from contextlib import ContextDecorator

class FrontdoorChatter(ContextDecorator):
    '''the tcp connection handling the front door (i.e. the panel of events,
    formats, decks, stores and etc.)
    '''
    def __init__(self, host, port, certfile, timeout=10.0):
        self.host = host
        self.port = port
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_verify_locations(certfile)
        self.sock = None
        self.timeout = timeout

        self.buf = b''
        self.flag = ''
        self.reply = {}
        self.some_counter = 0

    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.sock = self.context.wrap_socket(self.sock, server_hostname=self.host)
        self.sock.do_handshake()
        self.sock.settimeout(self.timeout)
        return self

    def __exit__(self, *exc):
        self.sock.close()
    
    @staticmethod
    def add_header(data: str) -> bytes:
        byte_length = len(data.encode())
        return bytes([3, 1]) + byte_length.to_bytes(4, 'little') + data.encode()

    # check the inbox, make sure first there should be something
    def check(self) -> bytes:
        try:
            self.buf += self.sock.recv()
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
            self.sock.send(bytes([3, 3]) + (4).to_bytes(4, 'little') + self.buf[6: 10])
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
                self.buf += self.sock.recv(length - len(self.buf) + 6)
            self.flag = 'valid'
            temp = self.buf[6:(length+6)]
            self.buf = self.buf[(length+6):]
            return temp
        else:
            raise RuntimeError(self.buf)

    def speak(self, message: dict):
        self.sock.send(FrontdoorChatter.add_header(json.dumps(message, separators=(',', ':'))))

    def ping(self, timestamp=555):
        self.sock.send(bytes([3, 2]) + (4).to_bytes(4, 'little') + timestamp.to_bytes(4, 'little'))

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
    
    def authenticate(self, full_client_version, access_token) -> str:
        resp = self.inquire(0, { # authenticate
			"ClientVersion": full_client_version,
			"Token": access_token,
            "PersonaId": None,
			"ScreenName": None,
			"Roles": None,
			"PlatformId": "Windows"
        })
        if not resp == None and "Payload" in resp:
            session_id = json.loads(resp['Payload'])["SessionId"]
            return "Client panel authenticated."
        else:
            return "Authentication failed."
        
    def join_match(self):
        import gzip
        import base64
        def decompress(content: str) -> dict:
            formats = content
            formats = base64.b64decode(formats)
            return json.loads(gzip.decompress(formats[4:]).decode())

        resp = self.inquire(1910, {}) # getPlayerPreferences
        play_deck_id = None
        if not resp == None and "Payload" in resp:
            for event_deck in json.loads(json.loads(resp["Payload"])["Preferences"]["RecentGamesData"]):
                if event_deck["EventName"] == "Play":
                    play_deck_id = event_deck["DeckId"]

        if play_deck_id == None:
            raise "111"
        
        resp = self.inquire(400, { # getDeck (body)
            "DeckId": play_deck_id
        })
        play_deck_body = None
        if not resp == None and "Payload" in resp:
            play_deck_body = json.loads(resp["Payload"])

        resp = self.inquire(1, {}) # startHook
        deck_summaries = None
        play_deck_summary = None
        if not resp == None:
            if resp["Compressed"] == True:
                resp = decompress(resp["Payload"])
                deck_summaries = resp["DeckSummariesV2"]
                for summary in deck_summaries:
                    if summary["DeckId"] == play_deck_id:
                        play_deck_summary = summary

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

        self.inquire(601, {  # Event_Drop
            "EventName": "Play",
        })

        resp1 = self.inquire(600, {  # Event_Join
            "EventName": "Play",
            "EntryCurrencyType": "None",
            "EntryCurrencyPaid": 0,
            "CustomTokenId": None
        })
        print("Joining event 'standard play'.")
        
        aws_deck, aws_summary = toAwsModel(play_deck_body, play_deck_summary)
        resp2 = self.inquire(622, {  # Event_SetDeckV2
            "EventName": "Play",
			"Summary": aws_summary,
			"Deck": aws_deck
        })

        if not ("Payload" in resp1 and "Payload" in resp2):
            raise Exception(b'')
        #assert "Payload" in resp1 and "Payload" in resp2

        resp = self.inquire(603, {  # EnterPairing
            "EventName": "Play",
            "EventCode": None,
        })
        print("Entering pairing!")
        print(resp)

        import time
        for _ in range(20):
            time.sleep(1)
            resp = self.check()
            if 'valid' == self.flag:
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
                
                return "match created!"
            
import message_pb2 as pb
from datetime import datetime
class BattlefieldChatter(FrontdoorChatter):
    def __init__(self, host, port, certfile, client_version,
                 match_id, fabric_uri, timeout=10.0):
        self.request_id = 0
        self.client_version = client_version
        self.match_id = match_id
        self.fabric_uri = fabric_uri
        super().__init__(host, port, certfile, timeout)
    
    def speak(self, message: pb.ClientToMatchServiceMessage):
        self.ssock.send(BattlefieldChatter.add_header(message.SerializeToString()))

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
                    majorVersion=int(self.client_version.split(".")[0]),
                    minorVersion=int(self.client_version.split(".")[1])
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
            matchId=self.match_id,
            mcFabricUri=self.fabric_uri,
            clientToGreMessageBytes=connect_message.SerializeToString(),
        )
    
    def get_gre_client_messages(self, trans_id=None):
        for _ in range(20):
            import time
            time.sleep(1)
            if trans_id:
                self.admit()
            else:
                trans_id = self.admit()
            if trans_id and self.reply[trans_id]:
                break
        
        return [msg
            for trans in self.reply[trans_id] if hasattr(trans, 'greToClientEvent')
            for msg in trans.greToClientEvent.greToClientMessages]