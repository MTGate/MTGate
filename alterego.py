MTGA_folder = ".."

assembly_path = MTGA_folder + r"/MTGA_Data/Managed/"

import sys
sys.path.append(assembly_path)

import clr
clr.AddReference("Assembly-CSharp")
clr.AddReference("Wizards.MDN.GreProtobuf.Unity")
clr.AddReference("Google.Protobuf")

from Wotc.Mtgo.Gre.External.Messaging import GREToClientMessage, \
    ClientToGREMessage, GREMessageType, ActionType, ManaColor
from GreClient.Rules import ActionsAvailableRequest, MtgGameState, GreInterface
from Wizards.MDN.GreProtobuf import GreProtobufUtils

import message_pb2
import json
from google.protobuf import json_format

database = None
strategy = clr.RandomStrategy(database, logger=None, decisionDelayMs=0)
aa_req_msg = GreProtobufUtils.GreToClientMessageFromJson(
    json_format.MessageToJson(message_pb2.GREToClientMessage(
        type=message_pb2.GREMessageType.GREMessageType_ActionsAvailableReq,
        systemSeatIds=[2],
        msgId=19,
        gameStateId=6,
        actionsAvailableReq=message_pb2.ActionsAvailableReq(
            actions=[message_pb2.Action(
                actionType=message_pb2.ActionType.ActionType_Pass,
            )]
        )
    ))
)
base = ActionsAvailableRequest(aa_req_msg.ActionsAvailableReq, aa_req_msg)
ret: ClientToGREMessage | None = None
# base.OnSubmit = lambda msg, ret=ret: (ret := msg)
strategy.HandleRequest(base, None)
print(base._passAction)