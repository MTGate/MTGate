MTGA_folder = ".."

assembly_path = MTGA_folder + r"/MTGA_Data/Managed/"

import sys
sys.path.append(assembly_path)

import clr
clr.AddReference("Wizards.MDN.GreProtobuf.Unity")
clr.AddReference("Google.Protobuf")

from Wotc.Mtgo.Gre.External.Messaging import MatchServiceToClientMessage, \
    CreateMatchGameRoomRequest, MatchGameRoomConfig, GREConfiguration, \
    CLIPSConfiguration, GameStateRedactorConfiguration, TestConfig, \
    TreeOfCongress, AutoRespondPermission, MatchConfig, TimerPackage, \
    TimerConfig, PlayerConfig, CardSkinTuple, TeamConfig, \
    ShuffleRestriction, MatchWinCondition, MulliganType, \
    GameType, GameVariant, \
    AuthenticateRequest, ClientInfo
    
from Google.Protobuf import CodedInputStream, MessageExtensions

def read(buffer: bytes, offset: int, length: int) -> dict:
    stream = CodedInputStream(buffer, offset, length)
    message = MatchServiceToClientMessage()
    message.MergeFrom(stream)
    return json.loads(message.ToString())

import random, uuid, enum
class MatchConfigurator:
    def __init__(self):
        self.MatchGameType = GameType.GameType_Duel
        self.MatchGameVariant = GameVariant.GameVariant_Normal
        self.MatchWinCondition = MatchWinCondition.MatchWinCondition_SingleElimination
        self.MaxHandSize = 7
        self.CastForFree = False
        self.MaxLandPerTurn = 1
        self.MulliganType = MulliganType.MulliganType_Vancouver
        self.StartingSeatId = 0
        self.StartingLifeTotals = []
        self.StartingHandSizes = [ 7, 7 ]
        self.EnableAutoAcceptHand = False
        self.FreeMulliganCount = 0
        self.TimerConfigs = []
        self.PlayerDecks = []

def proto_start() -> bytes:
    ## init config (param in original codes)
    matchConfigurator = MatchConfigurator()
    matchConfigurator.TreeOfCongressEnabledForCreator = False
    matchConfigurator.TreeOfCongressEnabledForJoiner = False
    matchConfigurator.CastForFree = False
    matchConfigurator.UseFullGameStates = False
    matchConfigurator.ShuffleRestriction = ShuffleRestriction.ShuffleRestriction_None
    matchConfigurator.MaxLandPerTurn = 1
    matchConfigurator.StartingSeatId = 0
    matchConfigurator.MatchWinCondition = MatchWinCondition.MatchWinCondition_SingleElimination

    # matchConfigurator.CardSkins = Debug_VanityItemConfig.GetCurrentLocalDebugSkins();
    # matchConfigurator.OpponentCardSkins = Debug_VanityItemConfig.GetCurrentOpponentDebugSkins();
    matchConfigurator.CommandEmblems = {}
    matchConfigurator.MulliganType = MulliganType.MulliganType_London
    matchConfigurator.TimerPackage = TimerPackage.TimerPackage_None

    ## (config body in original codes)
    system_seat_id = 1
    testConfig = TestConfig()
    testConfig.UseZeroManaCostForCasting = matchConfigurator.CastForFree
    testConfig.ShuffleRestriction = matchConfigurator.ShuffleRestriction
    testConfig.StartingPlayer = matchConfigurator.StartingSeatId
    testConfig.EnableAutoAcceptHand = matchConfigurator.EnableAutoAcceptHand
    testConfig.FreeMulliganCount = matchConfigurator.FreeMulliganCount
    if matchConfigurator.TreeOfCongressEnabledForCreator and matchConfigurator.TreeOfCongressEnabledForJoiner:
        testConfig.TreeOfCongress = TreeOfCongress()
        testConfig.AutoRespondPermission = AutoRespondPermission()
        if matchConfigurator.TreeOfCongressEnabledForCreator:
            testConfig.TreeOfCongress.SystemSeatId.Add(1)
            testConfig.AutoRespondPermission.SeatIds.Add(1)
        if matchConfigurator.TreeOfCongressEnabledForJoiner:
            testConfig.TreeOfCongress.SystemSeatId.Add(2)
            testConfig.AutoRespondPermission.SeatIds.Add(2)
    testConfig.UseMaxLandsPerTurn = matchConfigurator.MaxLandPerTurn
    for _ in range(8):
        testConfig.RandomSeeds.Add(int.from_bytes(random.randbytes(4), 'little'))
    testConfig.UseSpecifiedSeed = True
    matchConfig = MatchConfig()
    matchConfig.GameType = matchConfigurator.MatchGameType
    matchConfig.GameVariant = matchConfigurator.MatchGameVariant
    matchConfig.WinCondition = matchConfigurator.MatchWinCondition
    matchConfig.TestConfig = testConfig
    matchConfig.MaxPlayerHandSize = matchConfigurator.MaxHandSize
    matchConfig.MulliganType = matchConfigurator.MulliganType
    if not matchConfigurator.TimerPackage == TimerPackage.TimerPackage_None:
        matchConfig.TimerPackage = enum.Enum(matchConfigurator.TimerPackage)
    else:
        for timerConfig in matchConfigurator.TimerConfigs:
            matchConfig.TimerConfigs.Add(TimerConfig(timerConfig))
    for j in range(len(matchConfigurator.PlayerDecks)):
        num2 = j + 1
        flag = (num2 == 1)
        playerConfig = PlayerConfig()
        playerConfig.SideboardCards.Clear()
        playerConfig.SystemSeatId = num2
        num3 = int(not flag)
        playerConfig.StartingLifeTotal = matchConfigurator.StartingLifeTotals[num3]
        if not matchConfigurator.StartingHandSizes[num3] == 7:
            playerConfig.StartingHandSize = matchConfigurator.StartingHandSizes[num3]
            playerConfig.StartingHandSizeSpecified = True
        deckCollectionDeck = matchConfigurator.PlayerDecks[j]
        playerConfig.DeckCards.Add(deckCollectionDeck.mainDeckCards)
        playerConfig.SideboardCards.Add(deckCollectionDeck.sideboardCards)
        playerConfig.JazzMusicians.Add(deckCollectionDeck.musicians)
        playerConfig.PlayerConfigFieldThirteen = deckCollectionDeck.companion
        card_skins = (matchConfigurator.CardSkins if flag else matchConfigurator.OpponentCardSkins)
        for id in card_skins.keys():
            card_skin_tuple = CardSkinTuple()
            card_skin_tuple.CatalogId = id
            card_skin_tuple.SkinCode = card_skins[id]
            playerConfig.Skins.Add(card_skin_tuple)
        if matchConfigurator.CommandEmblems:
            for num4 in matchConfigurator.CommandEmblems:
                playerConfig.CommandEmblems.Add(num4)
        teamConfig = TeamConfig()
        teamConfig.TeamID = num2
        teamConfig.Players.Add(playerConfig)
        matchConfig.Teams.Add(teamConfig)
    matchGameRoomConfig = MatchGameRoomConfig()
    matchGameRoomConfig.GreConfig = GREConfiguration()
    matchGameRoomConfig.GreConfig.ClipsConfiguration = CLIPSConfiguration()
    matchGameRoomConfig.GreConfig.ClipsConfiguration.EnableMetrics = False
    matchGameRoomConfig.GreConfig.ClipsConfiguration.EnableWatch = False
    matchGameRoomConfig.GreConfig.GameStateRedactorConfiguration = GameStateRedactorConfiguration()
    matchGameRoomConfig.GreConfig.GameStateRedactorConfiguration.EnableForceDiff = not matchConfigurator.UseFullGameStates
    matchGameRoomConfig.GreConfig.GameStateRedactorConfiguration.EnableRedaction = True
    matchGameRoomConfig.MatchConfig = matchConfig
    matchGameRoomConfig.MatchId = str(uuid.uuid1())
    matchGameRoomConfig.IsVisible = True
    matchGameRoomConfig.JoinRoomTimeoutSecs = 3600
    matchGameRoomConfig.PlayerDisconnectTimeoutSecs = 10
    
    payload = CreateMatchGameRoomRequest()
    payload.GameRoomConfig = matchGameRoomConfig
    return bytes(MessageExtensions.ToByteString(payload).ToByteArray())

import json
def read(buffer: bytes, offset: int, length: int) -> dict:
    stream = CodedInputStream(buffer, offset, length)
    message = AuthenticateRequest()
    message.MergeFrom(stream)
    return message.ToString()

# x = b'\x08\x01\x10\x04\x18\xaf\xd1\xa6\xe2\xbe\xd2\xef\xed\x08\x22\x24\x34\x64\x65\x33\x65\x63\x66\x31\x2d\x37\x35\x37\x39\x2d\x34\x39\x33\x31\x2d\x61\x31\x32\x65\x2d\x64\x62\x33\x66\x61\x65\x30\x36\x63\x39\x36\x63\xa2\x06\xda\x07\x0a\x1a\x54\x44\x58\x50\x47\x55\x45\x54\x51\x35\x46\x45\x4a\x47\x46\x45\x4c\x57\x49\x33\x4b\x47\x4f\x4c\x53\x51\x22\xa2\x07\x65\x79\x4a\x68\x62\x47\x63\x69\x4f\x69\x4a\x53\x55\x7a\x49\x31\x4e\x69\x49\x73\x49\x6d\x74\x70\x5a\x43\x49\x36\x49\x6a\x4d\x30\x4e\x6d\x4d\x34\x59\x54\x59\x31\x4e\x54\x42\x6c\x5a\x47\x49\x35\x4d\x44\x52\x6a\x4d\x32\x49\x79\x4e\x57\x49\x33\x4f\x44\x6c\x6d\x4f\x54\x6c\x6c\x4e\x6a\x55\x33\x4f\x44\x41\x34\x4d\x47\x4a\x69\x4f\x54\x55\x69\x4c\x43\x4a\x30\x65\x58\x41\x69\x4f\x69\x4a\x4b\x56\x31\x51\x69\x66\x51\x2e\x65\x79\x4a\x68\x64\x57\x51\x69\x4f\x69\x4a\x4f\x4f\x46\x46\x47\x52\x7a\x68\x4f\x52\x55\x4a\x4b\x4e\x56\x51\x7a\x4e\x55\x5a\x43\x49\x69\x77\x69\x5a\x58\x68\x77\x49\x6a\x6f\x78\x4e\x6a\x6b\x31\x4e\x7a\x4d\x31\x4d\x6a\x55\x34\x4c\x43\x4a\x70\x59\x58\x51\x69\x4f\x6a\x45\x32\x4f\x54\x55\x33\x4d\x7a\x51\x79\x4f\x54\x67\x73\x49\x6d\x6c\x7a\x63\x79\x49\x36\x49\x6c\x4a\x46\x54\x6a\x4d\x7a\x53\x7a\x4e\x47\x56\x46\x5a\x44\x56\x6b\x5a\x4f\x51\x6b\x73\x30\x55\x6c\x52\x55\x57\x6b\x46\x44\x57\x56\x51\x30\x49\x69\x77\x69\x63\x33\x56\x69\x49\x6a\x6f\x69\x56\x45\x52\x59\x55\x45\x64\x56\x52\x56\x52\x52\x4e\x55\x5a\x46\x53\x6b\x64\x47\x52\x55\x78\x58\x53\x54\x4e\x4c\x52\x30\x39\x4d\x55\x31\x45\x69\x4c\x43\x4a\x33\x62\x33\x52\x6a\x4c\x57\x35\x68\x62\x57\x55\x69\x4f\x69\x4a\x36\x59\x57\x4d\x6a\x4e\x44\x59\x78\x4e\x54\x4d\x69\x4c\x43\x4a\x33\x62\x33\x52\x6a\x4c\x57\x52\x76\x62\x57\x34\x69\x4f\x69\x4a\x33\x61\x58\x70\x68\x63\x6d\x52\x7a\x49\x69\x77\x69\x64\x32\x39\x30\x59\x79\x31\x6e\x59\x57\x31\x6c\x49\x6a\x6f\x69\x59\x58\x4a\x6c\x62\x6d\x45\x69\x4c\x43\x4a\x33\x62\x33\x52\x6a\x4c\x57\x5a\x73\x5a\x33\x4d\x69\x4f\x6a\x45\x73\x49\x6e\x64\x76\x64\x47\x4d\x74\x63\x6d\x39\x73\x63\x79\x49\x36\x57\x79\x4a\x4e\x52\x45\x35\x42\x54\x46\x42\x49\x51\x53\x4a\x64\x4c\x43\x4a\x33\x62\x33\x52\x6a\x4c\x58\x42\x79\x62\x58\x4d\x69\x4f\x6c\x74\x64\x4c\x43\x4a\x33\x62\x33\x52\x6a\x4c\x58\x4e\x6a\x63\x48\x4d\x69\x4f\x6c\x73\x69\x5a\x6d\x6c\x79\x63\x33\x51\x74\x63\x47\x46\x79\x64\x48\x6b\x69\x58\x53\x77\x69\x64\x32\x39\x30\x59\x79\x31\x77\x5a\x47\x64\x79\x49\x6a\x6f\x69\x57\x55\x74\x47\x4e\x46\x64\x4a\x4d\x6c\x70\x53\x57\x6b\x51\x33\x52\x45\x74\x57\x52\x7a\x4a\x4f\x55\x7a\x56\x61\x57\x6c\x4e\x4f\x4d\x31\x55\x69\x4c\x43\x4a\x33\x62\x33\x52\x6a\x4c\x58\x4e\x6e\x64\x48\x4d\x69\x4f\x6c\x74\x64\x4c\x43\x4a\x33\x62\x33\x52\x6a\x4c\x58\x4e\x76\x59\x32\x77\x69\x4f\x6e\x74\x39\x4c\x43\x4a\x33\x62\x33\x52\x6a\x4c\x57\x4e\x75\x63\x33\x51\x69\x4f\x6a\x42\x39\x2e\x65\x43\x33\x7a\x47\x72\x68\x44\x6b\x66\x6b\x66\x77\x37\x5a\x62\x62\x48\x72\x76\x6e\x38\x34\x49\x51\x7a\x36\x34\x54\x46\x54\x73\x7a\x36\x4e\x48\x6e\x4b\x66\x78\x58\x76\x61\x6c\x6d\x4c\x68\x4a\x42\x54\x70\x51\x33\x63\x64\x49\x39\x44\x6a\x37\x5f\x38\x7a\x36\x4e\x76\x4f\x53\x77\x6b\x46\x30\x71\x46\x43\x53\x58\x76\x62\x77\x4a\x49\x32\x62\x4b\x62\x6f\x2d\x77\x35\x63\x32\x51\x74\x4e\x59\x42\x30\x5a\x78\x6f\x63\x47\x6e\x31\x70\x72\x6f\x6a\x78\x59\x65\x49\x4b\x69\x38\x62\x6a\x55\x79\x31\x43\x59\x37\x75\x35\x6e\x54\x66\x31\x42\x49\x70\x5a\x59\x63\x30\x5a\x63\x4f\x4f\x6b\x4e\x6e\x6e\x61\x4a\x69\x6e\x70\x56\x4c\x59\x32\x46\x71\x6f\x5f\x6c\x59\x44\x68\x53\x4e\x6b\x35\x45\x5a\x54\x31\x51\x74\x66\x37\x62\x5f\x4c\x4b\x6a\x56\x67\x35\x46\x69\x6d\x41\x4d\x55\x2d\x4e\x53\x6b\x68\x41\x6c\x30\x6f\x65\x41\x31\x53\x64\x36\x41\x5f\x72\x50\x78\x4e\x37\x4f\x77\x39\x5f\x59\x51\x57\x38\x6a\x79\x7a\x4c\x51\x4c\x38\x78\x71\x77\x4f\x67\x4a\x76\x4a\x38\x61\x64\x34\x75\x68\x56\x30\x2d\x55\x6b\x75\x43\x35\x48\x44\x62\x58\x53\x6a\x49\x32\x69\x6b\x59\x6b\x51\x4e\x50\x64\x2d\x50\x32\x75\x58\x74\x4d\x7a\x39\x6d\x4e\x4c\x67\x55\x5a\x70\x6e\x33\x66\x53\x4a\x34\x61\x4b\x67\x71\x77\x58\x58\x68\x45\x7a\x55\x6c\x4c\x71\x6e\x45\x31\x73\x55\x49\x44\x34\x54\x65\x43\x77\x7a\x33\x38\x72\x63\x39\x6b\x56\x30\x59\x55\x35\x56\x4a\x49\x64\x66\x4e\x6e\x57\x6c\x43\x64\x79\x51\x47\x7a\x6f\x68\x74\x67\x28\xe0\xd4\x03\x52\x13\x10\x01\x52\x0f\x32\x30\x32\x33\x2e\x32\x39\x2e\x31\x30\x2e\x34\x36\x37\x30'

# import message_pb2

# a = message_pb2.ClientToMatchServiceMessage()
# a.ParseFromString(x)
# b = message_pb2.AuthenticateRequest()
# b.ParseFromString(a.payload)
# print(a)
# print(b)

import mitmproxy.io
import mitmproxy
flows = mitmproxy.io.read_flows_from_paths(["./simple_traffic1.flow"])
tcps = (flow for flow in flows if isinstance(flow, mitmproxy.tcp.TCPFlow))
duel = next(flow for flow in tcps if flow.server_conn.address[1] == 30003)
packets = list(msg for msg in duel.messages if msg.content.startswith(b'\x03\x01'))

import message_pb2, google.protobuf.message
for pack in packets:
    try:
        if not pack.from_client:
            length = int.from_bytes(pack.content[2: 6], 'little')
            s2c = message_pb2.MatchServiceToClientMessage()
            s2c.ParseFromString(pack.content[6: (length + 6)])
            print(s2c)
        else:
            length = int.from_bytes(pack.content[2: 6], 'little')
            c2s = message_pb2.ClientToMatchServiceMessage()
            c2s.ParseFromString(pack.content[6: (length + 6)])
            for key, val in message_pb2.ClientToMatchServiceMessageType.items():
                if val == c2s.clientToMatchServiceMessageType:
                    name = key.lstrip("ClientToMatchServiceMessageType_")
            if name == 'DoorConnectRequest':
                name = 'ClientToMatchDoorConnectRequest'
            if name == 'GREMessage':
                name = 'ClientToGREMessage'
            if name == 'GREUIMessage':
                name = 'UIMessage'
            c2s_msg_cls = getattr(message_pb2, name)
            c2s_msg = c2s_msg_cls()
            print(name)
            print(c2s.transactionId)
            c2s_msg.ParseFromString(c2s.payload)
            print(c2s_msg)
            if name == 'ClientToMatchDoorConnectRequest':
                gre_msg = message_pb2.ClientToGREMessage()
                gre_msg.ParseFromString(c2s_msg.clientToGreMessageBytes)
                print(gre_msg)
            #print(c2s)
    except google.protobuf.message.DecodeError:
        print(pack)