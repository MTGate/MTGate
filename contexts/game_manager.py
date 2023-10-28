from contexts.connection_manager import BattlefieldChatter
from globals.externals import pb


class DefaultStrategy:
    def __init__(self):
        pass

    def decide(self, state):
        return state


class GameManager:
    def __init__(self, bf_chatter: BattlefieldChatter, strategy):
        self.bf_chatter = bf_chatter
        self.strategy = strategy or DefaultStrategy()
        self.state = None
        self.input = 0
        self.last_msg = None

    # used in a loop
    def update(self, command):
        trans_id = self.bf_chatter.admit()
        if trans_id:
            self.update_state(self.bf_chatter.queue[-1])
            reply = self.decide_reply(command, self.strategy.decide(self.state))
            # self.bf_chatter.propose(reply.type, reply.payload)
            return self.state, reply
        return "nothing", None

    def update_state(self, raw_message: pb.MatchServiceToClientMessage):
        from textual import log

        log(raw_message)
        self.last_msg = raw_message

    def decide_reply(self, command, auto_respond):
        return None
