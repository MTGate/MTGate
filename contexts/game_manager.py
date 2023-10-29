from contexts.connection_manager import BattlefieldChatter
from globals.externals import pb
from contexts.mtg_game_state import MtgGameState


class StateWrapper:
    def __init__(self):
        self.local_id = None
        self.players = []
        self.zones = []
        self.instances = []
        self.actions = []

    def update_with(self, state_message: pb.GameStateMessage):
        match state_message.type:
            # case pb.GameStateType.GameStateType_Diff:
            case pb.GameStateType.GameStateType_Diff | pb.GameStateType.GameStateType_Full:
                self.state_id = state_message.gameStateId
                for player in state_message.players:
                    self.players += [
                        {
                            "life": player.lifeTotal,
                            "seat_id": player.systemSeatNumber,
                            "max_hand": player.maxHandSize,
                            "team": player.teamId,
                            "controller": player.controllerSeatId,
                            "starting_life": player.startingLifeTotal,
                        }
                    ]
                self.turn_info = {
                    "active_player": state_message.turnInfo.activePlayer,
                    "decision_player": state_message.turnInfo.decisionPlayer,
                }
                for zone in state_message.zones:
                    self.zones += [
                        {
                            "id": zone.zoneId,
                            "type": [
                                name
                                for name, value in pb.ZoneType.items()
                                if value == zone.type
                            ][0],
                            "owner": zone.ownerSeatId,
                            "instances": zone.objectInstanceIds,
                        }
                    ]
                for instance in state_message.gameObjects:
                    self.instances += [
                        {
                            "id": instance.instanceId,
                            "grp_id": instance.grpId,
                            "type": [
                                name
                                for name, value in pb.GameObjectType.items()
                                if value == zone.type
                            ][0],
                            "zone_id": instance.zoneId,
                            "card_types": instance.cardTypes,
                            "color": instance.color,
                            "name": instance.name,
                            "abilities": instance.abilities,
                            "overlay_grp": instance.overlayGrpId,
                        }
                    ]
                for action in state_message.actions:
                    self.actions += [
                        {
                            "seat_id": action.seatId,
                            "type": action.action.actionType,
                            "id": action.action.instanceId,
                        }
                    ]
            case _:
                pass

    def get_zone_cards(self, zone: str, owner_is_me=True):
        zone = [
            zone
            for zone in self.zones
            if zone["type"] == zone
            and (owner_is_me is None or (owner_is_me ^ zone["owner"] == self.local_id))
        ]
        if zone:
            zone = zone[0]
        else:
            return []
        instance_ids = zone["instances"]
        return [
            instance
            for instance in self.instances
            for id in instance_ids
            if instance["id"] == id
        ]


class DefaultStrategy:
    def __init__(self):
        pass

    def decide(self, state, req):
        return state


class GameManager:
    def __init__(self, bf_chatter: BattlefieldChatter, strategy):
        self.bf_chatter = bf_chatter
        self.strategy = strategy or DefaultStrategy()
        self.state = StateWrapper()
        self.input = 0
        self.last_msg = None
        self.last_req = []

    # used in a loop
    def update(self, command):
        if self.bf_chatter.admit():
            msg = self.bf_chatter.queue[-1]
            self.update_state(msg)
            reply = self.decide_reply(
                command, self.strategy.decide(self.state, self.last_req)
            )

            # self.bf_chatter.propose(reply.type, reply.payload)
            return self.state, reply
        return self.state, None

    def update_state(self, raw_message: pb.MatchServiceToClientMessage):
        from textual import log

        if hasattr(raw_message, "greToClientEvent"):
            log(
                "\n".join(
                    name
                    for name, value in pb.GREMessageType.items()
                    for msg in raw_message.greToClientEvent.greToClientMessages
                    if value == msg.type
                )
            )
            for msg in raw_message.greToClientEvent.greToClientMessages:
                match msg.type:
                    case pb.GREMessageType.GREMessageType_ConnectResp:
                        if len(msg.systemSeatIds) == 1:
                            self.state.local_id = msg.systemSeatIds[0]
                    case pb.GREMessageType.GREMessageType_GameStateMessage:
                        log(msg)
                        self.state.update_with(msg.gameStateMessage)
                    case pb.GREMessageType.GREMessageType_ActionsAvailableReq:
                        self.last_req += [msg]
                    case pb.GREMessageType.GREMessageType_ChooseStartingPlayerReq:
                        self.last_req += [msg]
                    case pb.GREMessageType.GREMessageType_DieRollResultsResp:
                        log(
                            "\n".join(
                                [
                                    f"player {roll.systemSeatId} rolls {roll.rollValue}"
                                    for roll in msg.dieRollResultsResp.playerDieRolls
                                ]
                            )
                        )
                    case pb.GREMessageType.GREMessageType_UIMessage:
                        log("UI message")
                    case _:
                        log(msg)

        else:
            log(raw_message)

        self.last_msg = raw_message

        log("quit update_state")

    def decide_reply(self, command, auto_respond) -> pb.ClientToGREMessage | None:
        if not self.last_req:
            return None
        ### TODO: only if the resp is relevent to the req, pop this req
        req = self.last_req.pop()
        match req.type:
            case pb.GREMessageType.GREMessageType_ChooseStartingPlayerReq:
                return pb.ClientToGREMessage(
                    type=pb.ClientMessageType.ClientMessageType_ChooseStartingPlayerResp,
                    gameStateId=req.gameStateId,
                    respId=req.msgId,
                    chooseStartingPlayerResp=pb.ChooseStartingPlayerResp(
                        teamType=req.chooseStartingPlayerReq.teamType,
                        systemSeatId=self.state.local_id,
                        teamId=self.state.local_id,
                    ),
                )

            case _:
                pass
        return None
