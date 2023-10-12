from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Self

from ..globals.externals import gre

@dataclass
class Timer:
    timer_id: int
    timer_type: gre.TimerType
    remaining_time: float
    total_duration: int
    running: bool
    elapsed_time: bool
    # behavior
    # warning_threshold
    # created_at
    
@dataclass
class Player:
    gre_player_num: int
    team_id: int
    total_life: int
    timers: list[Timer]

class Effect:
    def __init__(self):
        self.blank = True

@dataclass
class CardInstance:
    mana_cost_override: list
    object_type: gre.GameObjectType
    has_summoning_sickness: bool
    is_tapped: bool
    is_damaged: bool
    is_damaged_this_turn: bool
    attack_state: gre.AttackState
    attack_target_id: int
    block_state: gre.BlockState
    blocking_ids: list[int]
    controller: int
    owner: int
    supertypes: list[gre.SuperType]
    card_types: list[gre.CardType]
    subtypes: list[gre.SubType]
    removed_subtypes: list[gre.SubType]
    colors: list[gre.CardColor]
    power: int | None
    toughness: int | None
    damage: int
    loyalty: int | None
    defense: int | None
    object_source_grp_id: int
    title_id: int
    overlay_grp_id: int | None
    actions: list[gre.ActionInfo]
    LoyaltyActivationsRemaining: int | None
    attached_to: int
    additional_cost_ids: set[int]
    referenced_card_title_ids: set[int]
    effects: list[Effect]

@dataclass
class Zone:
    id: int
    zone_type: gre.ZoneType
    visibility: gre.Visibility
    owner: Player
    card_ids: list[int]
    visible_cards: list[CardInstance]

@dataclass
class MtgGameState:
    id: int
    prev_id: int
    zones: list[Zone]
    players: list[Player]
    timers: list
    stage: gre.GameStage

    game_info: gre.GameInfo
    all_cards: dict[int, CardInstance]
    object_ids: set
    attack_info: dict[int, gre.AttackInfo]
    block_info: dict[int, gre.blockInfo]
    actions: list[gre.ActionInfo]
    active_player: int
    current_phase: gre.Phase
    next_phase: gre.Phase # maybe a list?
    current_step: gre.Step
    next_step: gre.Step

    effects: list[Effect]