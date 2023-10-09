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

import message_pb2 as pb
import json
from google.protobuf import json_format

strategy = clr.RandomStrategy(database=None, logger=None, decisionDelayMs=0)
# aa_req_msg = GreProtobufUtils.GreToClientMessageFromJson(
#     json_format.MessageToJson(pb.GREToClientMessage(
#         type=pb.GREMessageType.GREMessageType_ActionsAvailableReq,
#         systemSeatIds=[2],
#         msgId=19,
#         gameStateId=6,
#         actionsAvailableReq=pb.ActionsAvailableReq(
#             actions=[pb.Action(
#                 actionType=pb.ActionType.ActionType_Pass,
#             )]
#         )
#     ))
# )
ret: list[ClientToGREMessage | None] = []

from System import Action

def from_py_c2s_to_clr_c2s(c2s: pb.ClientToGREMessage) -> ClientToGREMessage:
    return GreProtobufUtils.ClientToGreMessageFromJson(json_format.MessageToJson(c2s))
def from_py_s2c_to_clr_s2c(s2c: pb.GREToClientMessage) -> GREToClientMessage:
    return GreProtobufUtils.GreToClientMessageFromJson(json_format.MessageToJson(s2c))
def from_clr_c2s_to_py_c2s(c2s: ClientToGREMessage) -> pb.ClientToGREMessage:
    msg = pb.ClientToGREMessage()
    json_format.Parse(GreProtobufUtils.ProtobufToJson(c2s), msg)
    return msg
def from_clr_s2c_to_py_s2c(s2c: GREToClientMessage) -> pb.GREToClientMessage:
    msg = pb.GREToClientMessage()
    json_format.Parse(GreProtobufUtils.ProtobufToJson(s2c), msg)
    return msg

from GreClient.Rules import ActionsAvailableRequest, SelectNDecision, \
    DeclareAttackerRequest, AssignBlockerDecision, SelectTargetsDecision
def respond(s2c: pb.GREToClientMessage) -> pb.ClientToGREMessage:
    clr_s2c = from_py_s2c_to_clr_s2c(s2c)
    match s2c.type:
        case pb.GREMessageType.GREMessageType_ActionsAvailableReq:
            req = ActionsAvailableRequest(clr_s2c.ActionsAvailableReq, clr_s2c)
            req.OnSubmit = Action[ClientToGREMessage](lambda msg, ret=ret: ret.append(msg))
            strategy.HandleRequest(req, None)
        case pb.GREMessageType.GREMessageType_SelectNReq:
            req = SelectNDecision(clr_s2c.SelectNReq, clr_s2c)
            req.OnSubmit = Action[ClientToGREMessage](lambda msg, ret=ret: ret.append(msg))
            strategy.HandleRequest(req, None)
        case pb.GREMessageType.GREMessageType_DeclareAttackersReq:
            req = DeclareAttackerRequest(clr_s2c.DeclareAttackersReq, clr_s2c)
            req.OnSubmit = Action[ClientToGREMessage](lambda msg, ret=ret: ret.append(msg))
            strategy.HandleRequest(req, None)
        case pb.GREMessageType.GREMessageType_DeclareBlockersReq:
            req = AssignBlockerDecision(clr_s2c.DeclareBlockersReq, clr_s2c)
            req.OnSubmit = Action[ClientToGREMessage](lambda msg, ret=ret: ret.append(msg))
            strategy.HandleRequest(req, None)
        case pb.GREMessageType.GREMessageType_SelectTargetsReq:
            req = SelectTargetsDecision(clr_s2c.SelectTargetsReq, clr_s2c)
            req.OnSubmit = Action[ClientToGREMessage](lambda msg, ret=ret: ret.append(msg))
            strategy.HandleRequest(req, None)
    if ret:
        return from_clr_c2s_to_py_c2s(ret.pop())
    else:
        return None