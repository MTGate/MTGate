from contexts.connection_manager import BattlefieldChatter
from globals.externals import pb
from contexts.mtg_game_state import CardInstance, MtgGameState, Player, Zone

"""
{
    "transactionId": "c371bc63-41e9-41fc-adb7-527fd283f823",
    "timestamp": "1698578266387",
    "greToClientEvent": {
        "greToClientMessages": [
            {
                "type": "GREMessageType_ConnectResp",
                "systemSeatIds": [2],
                "msgId": 381,
                "gameStateId": 259,
                "connectResp": {
                    "status": "ConnectionStatus_Success",
                    "protoVer": "ProtoVersion_PersistentAnnotations",
                    "settings": {
                        "stops": [
                            {
                                "stopType": "StopType_UpkeepStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_UpkeepStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_DrawStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_DrawStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_PrecombatMainPhase",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Set",
                            },
                            {
                                "stopType": "StopType_PrecombatMainPhase",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_BeginCombatStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Set",
                            },
                            {
                                "stopType": "StopType_BeginCombatStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Set",
                            },
                            {
                                "stopType": "StopType_DeclareAttackersStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Set",
                            },
                            {
                                "stopType": "StopType_DeclareAttackersStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Set",
                            },
                            {
                                "stopType": "StopType_DeclareBlockersStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Set",
                            },
                            {
                                "stopType": "StopType_DeclareBlockersStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Set",
                            },
                            {
                                "stopType": "StopType_CombatDamageStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_CombatDamageStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_EndCombatStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_EndCombatStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_PostcombatMainPhase",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Set",
                            },
                            {
                                "stopType": "StopType_PostcombatMainPhase",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_EndStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_EndStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Set",
                            },
                            {
                                "stopType": "StopType_FirstStrikeDamageStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Set",
                            },
                            {
                                "stopType": "StopType_FirstStrikeDamageStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Set",
                            },
                        ],
                        "autoPassOption": "AutoPassOption_ResolveMyStackEffects",
                        "graveyardOrder": "OrderingType_OrderArbitraryAlways",
                        "manaSelectionType": "ManaSelectionType_Auto",
                        "defaultAutoPassOption": "AutoPassOption_ResolveMyStackEffects",
                        "smartStopsSetting": "SmartStopsSetting_Enable",
                        "autoTapStopsSetting": "AutoTapStopsSetting_Enable",
                        "autoOptionalPaymentCancellationSetting": "Setting_Enable",
                        "manaPaymentStrategyType": "ManaPaymentStrategyType_Auto",
                        "transientStops": [
                            {
                                "stopType": "StopType_UpkeepStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_UpkeepStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_DrawStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_DrawStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_PrecombatMainPhase",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_PrecombatMainPhase",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_BeginCombatStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_BeginCombatStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_DeclareAttackersStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_DeclareAttackersStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_DeclareBlockersStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_DeclareBlockersStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_CombatDamageStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_CombatDamageStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_EndCombatStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_EndCombatStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_PostcombatMainPhase",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_PostcombatMainPhase",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_EndStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_EndStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_FirstStrikeDamageStep",
                                "appliesTo": "SettingScope_Team",
                                "status": "SettingStatus_Clear",
                            },
                            {
                                "stopType": "StopType_FirstStrikeDamageStep",
                                "appliesTo": "SettingScope_Opponents",
                                "status": "SettingStatus_Clear",
                            },
                        ],
                        "autoSelectReplacementSetting": "Setting_Enable",
                        "stackAutoPassOption": "AutoPassOption_Clear",
                    },
                    "deckMessage": {
                        "deckCards": [
                            82752,
                            82761,
                            82761,
                            82761,
                            82761,
                            82761,
                            82761,
                            82761,
                            82761,
                            82761,
                            82761,
                            87586,
                            87586,
                            87586,
                            87586,
                            87586,
                            80166,
                            80166,
                            80166,
                            80166,
                            78828,
                            78828,
                            78828,
                            78828,
                            80161,
                            82651,
                            86902,
                            86902,
                            86902,
                            86902,
                            82495,
                            82495,
                            82495,
                            78781,
                            82080,
                            79464,
                            79464,
                            79464,
                            79433,
                            79433,
                            83956,
                            80408,
                            80408,
                            80408,
                            80408,
                            79448,
                            79448,
                            84488,
                            84488,
                            83942,
                            86974,
                            86974,
                            82496,
                            86722,
                            86722,
                            86722,
                            79708,
                            79708,
                            79706,
                            82222,
                        ],
                        "sideboardCards": [82711],
                    },
                    "grpVersion": {"majorVersion": 2023, "minorVersion": 30},
                    "greVersion": {
                        "majorVersion": 2023,
                        "minorVersion": 30,
                        "buildVersion": 1,
                    },
                    "skins": [
                        {"catalogId": 78828, "skinCode": "DA"},
                        {"catalogId": 82495, "skinCode": "DA"},
                        {"catalogId": 78781, "skinCode": "DA"},
                    ],
                },
            },
            {
                "type": "GREMessageType_GameStateMessage",
                "systemSeatIds": [2],
                "msgId": 378,
                "gameStateId": 259,
                "gameStateMessage": {
                    "type": "GameStateType_Full",
                    "gameStateId": 259,
                    "gameInfo": {
                        "matchID": "b942d658-db58-460a-82f2-ded01928be77",
                        "gameNumber": 1,
                        "stage": "GameStage_Play",
                        "type": "GameType_Duel",
                        "variant": "GameVariant_Normal",
                        "matchState": "MatchState_GameInProgress",
                        "matchWinCondition": "MatchWinCondition_SingleElimination",
                        "maxTimeoutCount": 4,
                        "maxPipCount": 3,
                        "timeoutDurationSec": 30,
                        "superFormat": "SuperFormat_Constructed",
                        "mulliganType": "MulliganType_London",
                        "deckConstraintInfo": {
                            "minDeckSize": 60,
                            "maxDeckSize": 250,
                            "maxSideboardSize": 7,
                        },
                    },
                    "teams": [{"id": 1, "playerIds": [1]}, {"id": 2, "playerIds": [2]}],
                    "players": [
                        {
                            "lifeTotal": 21,
                            "systemSeatNumber": 1,
                            "maxHandSize": 7,
                            "turnNumber": 5,
                            "teamId": 1,
                            "timerIds": [1, 2, 3, 4, 5, 6],
                            "controllerSeatId": 1,
                            "controllerType": "ControllerType_Player",
                            "timeoutCount": 1,
                            "pipCount": 2,
                            "startingLifeTotal": 20,
                        },
                        {
                            "lifeTotal": 14,
                            "systemSeatNumber": 2,
                            "maxHandSize": 7,
                            "turnNumber": 6,
                            "teamId": 2,
                            "timerIds": [7, 8, 9, 10, 11, 12],
                            "controllerSeatId": 2,
                            "controllerType": "ControllerType_Player",
                            "timeoutCount": 1,
                            "pipCount": 2,
                            "startingLifeTotal": 20,
                        },
                    ],
                    "turnInfo": {
                        "phase": "Phase_Combat",
                        "step": "Step_DeclareBlock",
                        "turnNumber": 11,
                        "activePlayer": 2,
                        "priorityPlayer": 2,
                        "decisionPlayer": 2,
                        "nextPhase": "Phase_Combat",
                        "nextStep": "Step_CombatDamage",
                    },
                    "zones": [
                        {
                            "zoneId": 18,
                            "type": "ZoneType_Revealed",
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 1,
                        },
                        {
                            "zoneId": 19,
                            "type": "ZoneType_Revealed",
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                        },
                        {
                            "zoneId": 24,
                            "type": "ZoneType_Suppressed",
                            "visibility": "Visibility_Public",
                        },
                        {
                            "zoneId": 25,
                            "type": "ZoneType_Pending",
                            "visibility": "Visibility_Public",
                        },
                        {
                            "zoneId": 26,
                            "type": "ZoneType_Command",
                            "visibility": "Visibility_Public",
                        },
                        {
                            "zoneId": 27,
                            "type": "ZoneType_Stack",
                            "visibility": "Visibility_Public",
                        },
                        {
                            "zoneId": 28,
                            "type": "ZoneType_Battlefield",
                            "visibility": "Visibility_Public",
                            "objectInstanceIds": [
                                359,
                                358,
                                351,
                                350,
                                337,
                                335,
                                334,
                                317,
                                316,
                                314,
                                306,
                                305,
                                296,
                                294,
                                288,
                                286,
                                311,
                                329,
                                330,
                                340,
                                347,
                            ],
                        },
                        {
                            "zoneId": 29,
                            "type": "ZoneType_Exile",
                            "visibility": "Visibility_Public",
                        },
                        {
                            "zoneId": 30,
                            "type": "ZoneType_Limbo",
                            "visibility": "Visibility_Public",
                            "objectInstanceIds": [
                                357,
                                336,
                                237,
                                348,
                                312,
                                181,
                                297,
                                304,
                                236,
                            ],
                        },
                        {
                            "zoneId": 31,
                            "type": "ZoneType_Hand",
                            "visibility": "Visibility_Private",
                            "ownerSeatId": 1,
                            "objectInstanceIds": [331, 171, 169],
                            "viewers": [1],
                        },
                        {
                            "zoneId": 32,
                            "type": "ZoneType_Library",
                            "visibility": "Visibility_Hidden",
                            "ownerSeatId": 1,
                            "objectInstanceIds": [
                                182,
                                183,
                                184,
                                185,
                                186,
                                187,
                                188,
                                189,
                                190,
                                191,
                                192,
                                193,
                                194,
                                195,
                                196,
                                197,
                                198,
                                199,
                                200,
                                201,
                                202,
                                203,
                                204,
                                205,
                                206,
                                207,
                                208,
                                209,
                                210,
                                211,
                                212,
                                213,
                                214,
                                215,
                                216,
                                217,
                                218,
                                219,
                                220,
                                221,
                                222,
                                223,
                                224,
                                225,
                                177,
                                176,
                                179,
                                180,
                            ],
                        },
                        {
                            "zoneId": 33,
                            "type": "ZoneType_Graveyard",
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 1,
                            "objectInstanceIds": [345, 327],
                        },
                        {
                            "zoneId": 34,
                            "type": "ZoneType_Sideboard",
                            "visibility": "Visibility_Private",
                            "ownerSeatId": 1,
                            "viewers": [1],
                        },
                        {
                            "zoneId": 35,
                            "type": "ZoneType_Hand",
                            "visibility": "Visibility_Private",
                            "ownerSeatId": 2,
                            "objectInstanceIds": [226],
                            "viewers": [2],
                        },
                        {
                            "zoneId": 36,
                            "type": "ZoneType_Library",
                            "visibility": "Visibility_Hidden",
                            "ownerSeatId": 2,
                            "objectInstanceIds": [
                                238,
                                239,
                                240,
                                241,
                                242,
                                243,
                                244,
                                245,
                                246,
                                247,
                                248,
                                249,
                                250,
                                251,
                                252,
                                253,
                                254,
                                255,
                                256,
                                257,
                                258,
                                259,
                                260,
                                261,
                                262,
                                263,
                                264,
                                265,
                                266,
                                267,
                                268,
                                269,
                                270,
                                271,
                                272,
                                273,
                                274,
                                275,
                                276,
                                277,
                                278,
                                279,
                                280,
                                281,
                                282,
                                283,
                                284,
                                285,
                            ],
                        },
                        {
                            "zoneId": 37,
                            "type": "ZoneType_Graveyard",
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "objectInstanceIds": [300, 292],
                        },
                        {
                            "zoneId": 38,
                            "type": "ZoneType_Sideboard",
                            "visibility": "Visibility_Private",
                            "ownerSeatId": 2,
                            "viewers": [2],
                        },
                    ],
                    "gameObjects": [
                        {
                            "instanceId": 226,
                            "grpId": 79464,
                            "type": "GameObjectType_Card",
                            "zoneId": 35,
                            "visibility": "Visibility_Private",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "superTypes": ["SuperType_Legendary"],
                            "cardTypes": ["CardType_Planeswalker"],
                            "color": ["CardColor_White"],
                            "viewers": [2],
                            "loyalty": {"value": 3},
                            "name": 557446,
                            "abilities": [7, 147809, 147810, 147811, 147812, 114],
                            "overlayGrpId": 79464,
                            "loyaltyUsed": {},
                        },
                        {
                            "instanceId": 286,
                            "grpId": 80408,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "cardTypes": ["CardType_Land"],
                            "subtypes": [
                                "SubType_Forest",
                                "SubType_Plains",
                                "SubType_Island",
                            ],
                            "name": 567910,
                            "abilities": [1002, 1001, 1005, 76735, 1293],
                            "overlayGrpId": 80408,
                        },
                        {
                            "instanceId": 288,
                            "grpId": 87582,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 1,
                            "controllerSeatId": 1,
                            "superTypes": ["SuperType_Basic"],
                            "cardTypes": ["CardType_Land"],
                            "subtypes": ["SubType_Swamp"],
                            "isTapped": true,
                            "name": 653,
                            "abilities": [1003],
                            "overlayGrpId": 87582,
                        },
                        {
                            "instanceId": 292,
                            "grpId": 82495,
                            "type": "GameObjectType_Card",
                            "zoneId": 37,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "cardTypes": ["CardType_Sorcery"],
                            "color": ["CardColor_White"],
                            "name": 617985,
                            "abilities": [153182],
                            "overlayGrpId": 82495,
                            "skinCode": "DA",
                            "baseSkinCode": "DA",
                        },
                        {
                            "instanceId": 294,
                            "grpId": 80408,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "cardTypes": ["CardType_Land"],
                            "subtypes": [
                                "SubType_Forest",
                                "SubType_Plains",
                                "SubType_Island",
                            ],
                            "name": 567910,
                            "abilities": [1002, 1001, 1005, 76735, 1293],
                            "overlayGrpId": 80408,
                        },
                        {
                            "instanceId": 296,
                            "grpId": 83948,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 1,
                            "controllerSeatId": 1,
                            "cardTypes": ["CardType_Land"],
                            "isTapped": true,
                            "name": 32656,
                            "abilities": [76572, 1211],
                            "overlayGrpId": 83948,
                        },
                        {
                            "instanceId": 297,
                            "grpId": 86791,
                            "type": "GameObjectType_Card",
                            "zoneId": 30,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 1,
                            "controllerSeatId": 1,
                            "cardTypes": ["CardType_Enchantment"],
                            "color": ["CardColor_Black"],
                            "name": 731463,
                            "abilities": [168806, 168716, 168807],
                            "overlayGrpId": 86791,
                        },
                        {
                            "instanceId": 300,
                            "grpId": 84488,
                            "type": "GameObjectType_Card",
                            "zoneId": 37,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "cardTypes": ["CardType_Creature"],
                            "subtypes": ["SubType_Spirit"],
                            "color": ["CardColor_Green"],
                            "power": {"value": 1},
                            "toughness": {"value": 1},
                            "name": 702594,
                            "abilities": [166710, 166711],
                            "overlayGrpId": 84488,
                        },
                        {
                            "instanceId": 304,
                            "grpId": 82761,
                            "type": "GameObjectType_Card",
                            "zoneId": 30,
                            "visibility": "Visibility_Private",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "superTypes": ["SuperType_Basic"],
                            "cardTypes": ["CardType_Land"],
                            "subtypes": ["SubType_Plains"],
                            "viewers": [2],
                            "name": 648,
                            "abilities": [1001],
                            "overlayGrpId": 82761,
                        },
                        {
                            "instanceId": 305,
                            "grpId": 82761,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "superTypes": ["SuperType_Basic"],
                            "cardTypes": ["CardType_Land"],
                            "subtypes": ["SubType_Plains"],
                            "isTapped": true,
                            "name": 648,
                            "abilities": [1001],
                            "overlayGrpId": 82761,
                        },
                        {
                            "instanceId": 306,
                            "grpId": 78829,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "cardTypes": ["CardType_Enchantment"],
                            "color": ["CardColor_White"],
                            "name": 545706,
                            "abilities": [1456],
                            "overlayGrpId": 78829,
                            "skinCode": "DA",
                            "baseSkinCode": "DA",
                            "othersideGrpId": 78828,
                        },
                        {
                            "instanceId": 311,
                            "grpId": 79097,
                            "type": "GameObjectType_Token",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "cardTypes": ["CardType_Creature"],
                            "subtypes": ["SubType_Human"],
                            "color": ["CardColor_White"],
                            "power": {"value": 2},
                            "toughness": {"value": 2},
                            "isTapped": true,
                            "attackState": "AttackState_Attacking",
                            "blockState": "BlockState_Blocked",
                            "attackInfo": {
                                "targetId": 1,
                                "damageOrdered": true,
                                "orderedBlockers": [{"instanceId": 351}],
                            },
                            "objectSourceGrpId": 78828,
                            "name": 333,
                            "parentId": 310,
                            "overlayGrpId": 79097,
                            "skinCode": "DA",
                            "baseSkinCode": "DA",
                        },
                        {
                            "instanceId": 314,
                            "grpId": 78632,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 1,
                            "controllerSeatId": 1,
                            "cardTypes": ["CardType_Land"],
                            "name": 530669,
                            "abilities": [145461, 1211],
                            "overlayGrpId": 78632,
                        },
                        {
                            "instanceId": 316,
                            "grpId": 87586,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "superTypes": ["SuperType_Basic"],
                            "cardTypes": ["CardType_Land"],
                            "subtypes": ["SubType_Forest"],
                            "isTapped": true,
                            "name": 647,
                            "abilities": [1005],
                            "overlayGrpId": 87586,
                        },
                        {
                            "instanceId": 317,
                            "grpId": 78828,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "cardTypes": ["CardType_Enchantment"],
                            "color": ["CardColor_White"],
                            "name": 545703,
                            "abilities": [146582],
                            "overlayGrpId": 78828,
                            "skinCode": "DA",
                            "baseSkinCode": "DA",
                            "othersideGrpId": 78829,
                        },
                        {
                            "instanceId": 327,
                            "grpId": 86791,
                            "type": "GameObjectType_Card",
                            "zoneId": 33,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 1,
                            "controllerSeatId": 1,
                            "cardTypes": ["CardType_Enchantment"],
                            "color": ["CardColor_Black"],
                            "name": 731463,
                            "abilities": [168806, 168716, 168807],
                            "overlayGrpId": 86791,
                        },
                        {
                            "instanceId": 329,
                            "grpId": 79097,
                            "type": "GameObjectType_Token",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "cardTypes": ["CardType_Creature"],
                            "subtypes": ["SubType_Human"],
                            "color": ["CardColor_White"],
                            "power": {"value": 2},
                            "toughness": {"value": 2},
                            "isTapped": true,
                            "attackState": "AttackState_Attacking",
                            "blockState": "BlockState_Blocked",
                            "attackInfo": {
                                "targetId": 1,
                                "damageOrdered": true,
                                "orderedBlockers": [{"instanceId": 334}],
                            },
                            "objectSourceGrpId": 78828,
                            "name": 333,
                            "parentId": 322,
                            "overlayGrpId": 79097,
                            "skinCode": "DA",
                            "baseSkinCode": "DA",
                        },
                        {
                            "instanceId": 330,
                            "grpId": 79097,
                            "type": "GameObjectType_Token",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "cardTypes": ["CardType_Creature"],
                            "subtypes": ["SubType_Human"],
                            "color": ["CardColor_White"],
                            "power": {"value": 2},
                            "toughness": {"value": 2},
                            "isTapped": true,
                            "attackState": "AttackState_Attacking",
                            "blockState": "BlockState_Unblocked",
                            "attackInfo": {"targetId": 1, "damageOrdered": true},
                            "objectSourceGrpId": 78828,
                            "name": 333,
                            "parentId": 321,
                            "overlayGrpId": 79097,
                            "skinCode": "DA",
                            "baseSkinCode": "DA",
                        },
                        {
                            "instanceId": 334,
                            "grpId": 79545,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 1,
                            "controllerSeatId": 1,
                            "cardTypes": ["CardType_Creature", "CardType_Enchantment"],
                            "subtypes": ["SubType_Rat", "SubType_Rogue"],
                            "color": ["CardColor_Black"],
                            "power": {"value": 2},
                            "toughness": {"value": 2},
                            "blockState": "BlockState_Blocking",
                            "blockInfo": {
                                "attackerIds": [329],
                                "damageOrdered": true,
                                "orderedAttackers": [{"instanceId": 329}],
                            },
                            "name": 557730,
                            "abilities": [142, 147916],
                            "overlayGrpId": 79545,
                            "othersideGrpId": 79544,
                        },
                        {
                            "instanceId": 335,
                            "grpId": 87584,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 1,
                            "controllerSeatId": 1,
                            "superTypes": ["SuperType_Basic"],
                            "cardTypes": ["CardType_Land"],
                            "subtypes": ["SubType_Mountain"],
                            "isTapped": true,
                            "name": 1250,
                            "abilities": [1004],
                            "overlayGrpId": 87584,
                        },
                        {
                            "instanceId": 336,
                            "grpId": 82761,
                            "type": "GameObjectType_Card",
                            "zoneId": 30,
                            "visibility": "Visibility_Private",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "superTypes": ["SuperType_Basic"],
                            "cardTypes": ["CardType_Land"],
                            "subtypes": ["SubType_Plains"],
                            "viewers": [2],
                            "name": 648,
                            "abilities": [1001],
                            "overlayGrpId": 82761,
                        },
                        {
                            "instanceId": 337,
                            "grpId": 82761,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "superTypes": ["SuperType_Basic"],
                            "cardTypes": ["CardType_Land"],
                            "subtypes": ["SubType_Plains"],
                            "isTapped": true,
                            "name": 648,
                            "abilities": [1001],
                            "overlayGrpId": 82761,
                        },
                        {
                            "instanceId": 340,
                            "grpId": 79097,
                            "type": "GameObjectType_Token",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "cardTypes": ["CardType_Creature"],
                            "subtypes": ["SubType_Human"],
                            "color": ["CardColor_White"],
                            "power": {"value": 2},
                            "toughness": {"value": 2},
                            "isTapped": true,
                            "attackState": "AttackState_Attacking",
                            "blockState": "BlockState_Unblocked",
                            "attackInfo": {"targetId": 1, "damageOrdered": true},
                            "objectSourceGrpId": 78828,
                            "name": 333,
                            "parentId": 339,
                            "overlayGrpId": 79097,
                            "skinCode": "DA",
                            "baseSkinCode": "DA",
                        },
                        {
                            "instanceId": 345,
                            "grpId": 86791,
                            "type": "GameObjectType_Card",
                            "zoneId": 33,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 1,
                            "controllerSeatId": 1,
                            "cardTypes": ["CardType_Enchantment"],
                            "color": ["CardColor_Black"],
                            "name": 731463,
                            "abilities": [168806, 168716, 168807],
                            "overlayGrpId": 86791,
                        },
                        {
                            "instanceId": 347,
                            "grpId": 79097,
                            "type": "GameObjectType_Token",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "cardTypes": ["CardType_Creature"],
                            "subtypes": ["SubType_Human"],
                            "color": ["CardColor_White"],
                            "power": {"value": 2},
                            "toughness": {"value": 2},
                            "isTapped": true,
                            "attackState": "AttackState_Attacking",
                            "blockState": "BlockState_Unblocked",
                            "attackInfo": {"targetId": 1, "damageOrdered": true},
                            "objectSourceGrpId": 78828,
                            "name": 333,
                            "parentId": 338,
                            "overlayGrpId": 79097,
                            "skinCode": "DA",
                            "baseSkinCode": "DA",
                        },
                        {
                            "instanceId": 350,
                            "grpId": 87584,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 1,
                            "controllerSeatId": 1,
                            "superTypes": ["SuperType_Basic"],
                            "cardTypes": ["CardType_Land"],
                            "subtypes": ["SubType_Mountain"],
                            "isTapped": true,
                            "name": 1250,
                            "abilities": [1004],
                            "overlayGrpId": 87584,
                        },
                        {
                            "instanceId": 351,
                            "grpId": 86936,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 1,
                            "controllerSeatId": 1,
                            "cardTypes": ["CardType_Creature"],
                            "subtypes": ["SubType_Dragon"],
                            "color": ["CardColor_Red"],
                            "power": {"value": 4},
                            "toughness": {"value": 4},
                            "hasSummoningSickness": true,
                            "blockState": "BlockState_Blocking",
                            "blockInfo": {
                                "attackerIds": [311],
                                "damageOrdered": true,
                                "orderedAttackers": [{"instanceId": 311}],
                            },
                            "name": 731922,
                            "abilities": [8, 14, 116867],
                            "overlayGrpId": 86936,
                            "skinCode": "DA",
                            "baseSkinCode": "DA",
                        },
                        {
                            "instanceId": 352,
                            "grpId": 86937,
                            "type": "GameObjectType_Adventure",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 1,
                            "controllerSeatId": 1,
                            "cardTypes": ["CardType_Instant"],
                            "subtypes": ["SubType_Adventure"],
                            "color": ["CardColor_Black"],
                            "name": 731924,
                            "abilities": [168958],
                            "parentId": 351,
                            "overlayGrpId": 86937,
                        },
                        {
                            "instanceId": 357,
                            "grpId": 80166,
                            "type": "GameObjectType_Card",
                            "zoneId": 30,
                            "visibility": "Visibility_Private",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "cardTypes": ["CardType_Artifact"],
                            "color": ["CardColor_White"],
                            "viewers": [2],
                            "name": 567064,
                            "abilities": [149359, 149360, 149361],
                            "overlayGrpId": 80166,
                        },
                        {
                            "instanceId": 358,
                            "grpId": 82761,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "superTypes": ["SuperType_Basic"],
                            "cardTypes": ["CardType_Land"],
                            "subtypes": ["SubType_Plains"],
                            "name": 648,
                            "abilities": [1001],
                            "overlayGrpId": 82761,
                        },
                        {
                            "instanceId": 359,
                            "grpId": 80166,
                            "type": "GameObjectType_Card",
                            "zoneId": 28,
                            "visibility": "Visibility_Public",
                            "ownerSeatId": 2,
                            "controllerSeatId": 2,
                            "cardTypes": ["CardType_Artifact"],
                            "color": ["CardColor_White"],
                            "name": 567064,
                            "abilities": [149359, 149360, 149361],
                            "overlayGrpId": 80166,
                        },
                    ],
                    "prevGameStateId": 258,
                    "timers": [
                        {
                            "timerId": 1,
                            "type": "TimerType_Prologue",
                            "durationSec": 120,
                            "behavior": "TimerBehavior_TakeControl",
                            "warningThresholdSec": 30,
                        },
                        {
                            "timerId": 2,
                            "type": "TimerType_Epilogue",
                            "durationSec": 145,
                            "behavior": "TimerBehavior_TakeControl",
                            "warningThresholdSec": 30,
                        },
                        {
                            "timerId": 3,
                            "type": "TimerType_ActivePlayer",
                            "durationSec": 61,
                            "behavior": "TimerBehavior_TakeControl",
                            "warningThresholdSec": 30,
                        },
                        {
                            "timerId": 4,
                            "type": "TimerType_NonActivePlayer",
                            "durationSec": 61,
                            "elapsedSec": 2,
                            "behavior": "TimerBehavior_TakeControl",
                            "warningThresholdSec": 30,
                            "elapsedMs": 2127,
                        },
                        {
                            "timerId": 5,
                            "type": "TimerType_Inactivity",
                            "durationSec": 150,
                            "behavior": "TimerBehavior_Timeout",
                            "warningThresholdSec": 30,
                        },
                        {
                            "timerId": 6,
                            "type": "TimerType_Delay",
                            "durationSec": 2,
                            "behavior": "TimerBehavior_StartDelayedTimer",
                        },
                        {
                            "timerId": 7,
                            "type": "TimerType_Prologue",
                            "durationSec": 120,
                            "behavior": "TimerBehavior_TakeControl",
                            "warningThresholdSec": 30,
                        },
                        {
                            "timerId": 8,
                            "type": "TimerType_Epilogue",
                            "durationSec": 145,
                            "behavior": "TimerBehavior_TakeControl",
                            "warningThresholdSec": 30,
                        },
                        {
                            "timerId": 9,
                            "type": "TimerType_ActivePlayer",
                            "durationSec": 121,
                            "elapsedSec": 84,
                            "running": true,
                            "behavior": "TimerBehavior_TakeControl",
                            "warningThresholdSec": 30,
                            "elapsedMs": 84274,
                        },
                        {
                            "timerId": 10,
                            "type": "TimerType_NonActivePlayer",
                            "durationSec": 45,
                            "behavior": "TimerBehavior_TakeControl",
                            "warningThresholdSec": 30,
                        },
                        {
                            "timerId": 11,
                            "type": "TimerType_Inactivity",
                            "durationSec": 150,
                            "elapsedSec": 70,
                            "running": true,
                            "behavior": "TimerBehavior_Timeout",
                            "warningThresholdSec": 30,
                            "elapsedMs": 70820,
                        },
                        {
                            "timerId": 12,
                            "type": "TimerType_Delay",
                            "durationSec": 2,
                            "behavior": "TimerBehavior_StartDelayedTimer",
                        },
                    ],
                    "update": "GameStateUpdate_SendAndRecord",
                    "actions": [
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Cast",
                                "instanceId": 226,
                                "manaCost": [
                                    {"color": ["ManaColor_Generic"], "count": 2},
                                    {"color": ["ManaColor_White"], "count": 2},
                                ],
                            },
                        },
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1001,
                                "sourceId": 286,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3622,
                                                "color": "ManaColor_White",
                                                "srcInstanceId": 286,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1001,
                                            }
                                        ]
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1001,
                                "sourceId": 294,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3623,
                                                "color": "ManaColor_White",
                                                "srcInstanceId": 294,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1001,
                                            }
                                        ]
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1001,
                                "sourceId": 305,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3624,
                                                "color": "ManaColor_White",
                                                "srcInstanceId": 305,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1001,
                                            }
                                        ]
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1001,
                                "sourceId": 358,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3625,
                                                "color": "ManaColor_White",
                                                "srcInstanceId": 358,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1001,
                                            }
                                        ]
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1001,
                                "sourceId": 337,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3626,
                                                "color": "ManaColor_White",
                                                "srcInstanceId": 337,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1001,
                                            }
                                        ]
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1002,
                                "sourceId": 286,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3627,
                                                "color": "ManaColor_Blue",
                                                "srcInstanceId": 286,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1002,
                                            }
                                        ]
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1002,
                                "sourceId": 294,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3628,
                                                "color": "ManaColor_Blue",
                                                "srcInstanceId": 294,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1002,
                                            }
                                        ]
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 1,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1003,
                                "sourceId": 288,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3629,
                                                "color": "ManaColor_Black",
                                                "srcInstanceId": 288,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1003,
                                            }
                                        ]
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 1,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1004,
                                "sourceId": 350,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3630,
                                                "color": "ManaColor_Red",
                                                "srcInstanceId": 350,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1004,
                                            }
                                        ]
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 1,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1004,
                                "sourceId": 335,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3631,
                                                "color": "ManaColor_Red",
                                                "srcInstanceId": 335,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1004,
                                            }
                                        ]
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1005,
                                "sourceId": 286,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3632,
                                                "color": "ManaColor_Green",
                                                "srcInstanceId": 286,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1005,
                                            }
                                        ]
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1005,
                                "sourceId": 294,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3633,
                                                "color": "ManaColor_Green",
                                                "srcInstanceId": 294,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1005,
                                            }
                                        ]
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1005,
                                "sourceId": 316,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3634,
                                                "color": "ManaColor_Green",
                                                "srcInstanceId": 316,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1005,
                                            }
                                        ]
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 1,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1211,
                                "sourceId": 296,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3635,
                                                "color": "ManaColor_Black",
                                                "srcInstanceId": 296,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1211,
                                            }
                                        ]
                                    },
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3636,
                                                "color": "ManaColor_Red",
                                                "srcInstanceId": 296,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1211,
                                            }
                                        ],
                                        "optionIndex": 1,
                                    },
                                ],
                            },
                        },
                        {
                            "seatId": 1,
                            "action": {
                                "actionType": "ActionType_Activate_Mana",
                                "abilityGrpId": 1211,
                                "sourceId": 314,
                                "manaPaymentOptions": [
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3637,
                                                "color": "ManaColor_Black",
                                                "srcInstanceId": 314,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1211,
                                            }
                                        ]
                                    },
                                    {
                                        "mana": [
                                            {
                                                "manaId": 3638,
                                                "color": "ManaColor_Red",
                                                "srcInstanceId": 314,
                                                "specs": [
                                                    {"type": "ManaSpecType_Predictive"}
                                                ],
                                                "abilityGrpId": 1211,
                                            }
                                        ],
                                        "optionIndex": 1,
                                    },
                                ],
                            },
                        },
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Activate",
                                "abilityGrpId": 149359,
                                "sourceId": 359,
                                "manaCost": [
                                    {
                                        "color": ["ManaColor_White"],
                                        "count": 1,
                                        "abilityGrpId": 149359,
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Activate",
                                "abilityGrpId": 149360,
                                "sourceId": 359,
                                "manaCost": [
                                    {
                                        "color": ["ManaColor_White"],
                                        "count": 2,
                                        "abilityGrpId": 149360,
                                    }
                                ],
                            },
                        },
                        {
                            "seatId": 2,
                            "action": {
                                "actionType": "ActionType_Activate",
                                "abilityGrpId": 149361,
                                "sourceId": 359,
                                "manaCost": [
                                    {
                                        "color": ["ManaColor_White"],
                                        "count": 5,
                                        "abilityGrpId": 149361,
                                    }
                                ],
                            },
                        },
                    ],
                    "persistentAnnotations": [
                        {
                            "id": 5,
                            "affectorId": 28,
                            "affectedIds": [359, 358],
                            "type": ["AnnotationType_EnteredZoneThisTurn"],
                        },
                        {
                            "id": 137,
                            "affectorId": 4002,
                            "affectedIds": [301],
                            "type": ["AnnotationType_Counter"],
                            "details": [
                                {
                                    "key": "count",
                                    "type": "KeyValuePairValueType_int32",
                                    "valueInt32": [3],
                                },
                                {
                                    "key": "counter_type",
                                    "type": "KeyValuePairValueType_int32",
                                    "valueInt32": [108],
                                },
                            ],
                        },
                        {
                            "id": 192,
                            "affectorId": 4003,
                            "affectedIds": [306],
                            "type": ["AnnotationType_Counter"],
                            "details": [
                                {
                                    "key": "count",
                                    "type": "KeyValuePairValueType_int32",
                                    "valueInt32": [3],
                                },
                                {
                                    "key": "counter_type",
                                    "type": "KeyValuePairValueType_int32",
                                    "valueInt32": [161],
                                },
                            ],
                        },
                        {
                            "id": 309,
                            "affectorId": 4004,
                            "affectedIds": [317],
                            "type": ["AnnotationType_Counter"],
                            "details": [
                                {
                                    "key": "count",
                                    "type": "KeyValuePairValueType_int32",
                                    "valueInt32": [2],
                                },
                                {
                                    "key": "counter_type",
                                    "type": "KeyValuePairValueType_int32",
                                    "valueInt32": [161],
                                },
                            ],
                        },
                        {
                            "id": 339,
                            "affectorId": 334,
                            "affectedIds": [334],
                            "type": ["AnnotationType_Qualification"],
                            "details": [
                                {
                                    "key": "SourceParent",
                                    "type": "KeyValuePairValueType_int32",
                                    "valueInt32": [334],
                                },
                                {
                                    "key": "grpid",
                                    "type": "KeyValuePairValueType_int32",
                                    "valueInt32": [142],
                                },
                                {
                                    "key": "QualificationSubtype",
                                    "type": "KeyValuePairValueType_int32",
                                    "valueInt32": [0],
                                },
                                {
                                    "key": "QualificationType",
                                    "type": "KeyValuePairValueType_int32",
                                    "valueInt32": [40],
                                },
                            ],
                        },
                        {
                            "id": 418,
                            "affectorId": 306,
                            "affectedIds": [347, 311, 329, 340, 330],
                            "type": [
                                "AnnotationType_ModifiedToughness",
                                "AnnotationType_ModifiedPower",
                                "AnnotationType_LayeredEffect",
                            ],
                            "details": [
                                {
                                    "key": "effect_id",
                                    "type": "KeyValuePairValueType_int32",
                                    "valueInt32": [7003],
                                }
                            ],
                        },
                    ],
                },
            },
            {
                "type": "GREMessageType_ActionsAvailableReq",
                "systemSeatIds": [2],
                "msgId": 379,
                "gameStateId": 259,
                "prompt": {"promptId": 2},
                "actionsAvailableReq": {
                    "actions": [
                        {
                            "actionType": "ActionType_Cast",
                            "grpId": 79464,
                            "instanceId": 226,
                            "facetId": 226,
                            "manaCost": [
                                {"color": ["ManaColor_Generic"], "count": 2},
                                {"color": ["ManaColor_White"], "count": 2},
                            ],
                            "shouldStop": true,
                        },
                        {
                            "actionType": "ActionType_Activate",
                            "grpId": 80166,
                            "instanceId": 359,
                            "facetId": 359,
                            "abilityGrpId": 149359,
                            "manaCost": [
                                {
                                    "color": ["ManaColor_White"],
                                    "count": 1,
                                    "abilityGrpId": 149359,
                                }
                            ],
                            "shouldStop": true,
                            "autoTapSolution": {
                                "autoTapActions": [
                                    {
                                        "instanceId": 358,
                                        "abilityGrpId": 1001,
                                        "manaPaymentOption": {
                                            "mana": [
                                                {
                                                    "manaId": 3615,
                                                    "color": "ManaColor_White",
                                                    "srcInstanceId": 358,
                                                    "specs": [
                                                        {
                                                            "type": "ManaSpecType_Predictive"
                                                        }
                                                    ],
                                                    "abilityGrpId": 1001,
                                                }
                                            ]
                                        },
                                    }
                                ]
                            },
                            "uniqueAbilityId": 331,
                        },
                        {
                            "actionType": "ActionType_Activate",
                            "grpId": 80166,
                            "instanceId": 359,
                            "facetId": 359,
                            "abilityGrpId": 149360,
                            "manaCost": [
                                {
                                    "color": ["ManaColor_White"],
                                    "count": 2,
                                    "abilityGrpId": 149360,
                                }
                            ],
                            "shouldStop": true,
                            "autoTapSolution": {
                                "autoTapActions": [
                                    {
                                        "instanceId": 358,
                                        "abilityGrpId": 1001,
                                        "manaPaymentOption": {
                                            "mana": [
                                                {
                                                    "manaId": 3615,
                                                    "color": "ManaColor_White",
                                                    "srcInstanceId": 358,
                                                    "specs": [
                                                        {
                                                            "type": "ManaSpecType_Predictive"
                                                        }
                                                    ],
                                                    "abilityGrpId": 1001,
                                                }
                                            ]
                                        },
                                    },
                                    {
                                        "instanceId": 286,
                                        "abilityGrpId": 1001,
                                        "manaPaymentOption": {
                                            "mana": [
                                                {
                                                    "manaId": 3612,
                                                    "color": "ManaColor_White",
                                                    "srcInstanceId": 286,
                                                    "specs": [
                                                        {
                                                            "type": "ManaSpecType_Predictive"
                                                        }
                                                    ],
                                                    "abilityGrpId": 1001,
                                                }
                                            ]
                                        },
                                    },
                                ]
                            },
                            "uniqueAbilityId": 332,
                        },
                        {
                            "actionType": "ActionType_Activate_Mana",
                            "grpId": 80408,
                            "instanceId": 286,
                            "facetId": 286,
                            "abilityGrpId": 1001,
                            "manaPaymentOptions": [
                                {
                                    "mana": [
                                        {
                                            "manaId": 3612,
                                            "color": "ManaColor_White",
                                            "srcInstanceId": 286,
                                            "specs": [
                                                {"type": "ManaSpecType_Predictive"}
                                            ],
                                            "abilityGrpId": 1001,
                                        }
                                    ]
                                }
                            ],
                            "isBatchable": true,
                            "uniqueAbilityId": 255,
                        },
                        {
                            "actionType": "ActionType_Activate_Mana",
                            "grpId": 80408,
                            "instanceId": 286,
                            "facetId": 286,
                            "abilityGrpId": 1002,
                            "manaPaymentOptions": [
                                {
                                    "mana": [
                                        {
                                            "manaId": 3617,
                                            "color": "ManaColor_Blue",
                                            "srcInstanceId": 286,
                                            "specs": [
                                                {"type": "ManaSpecType_Predictive"}
                                            ],
                                            "abilityGrpId": 1002,
                                        }
                                    ]
                                }
                            ],
                            "isBatchable": true,
                            "uniqueAbilityId": 254,
                        },
                        {
                            "actionType": "ActionType_Activate_Mana",
                            "grpId": 80408,
                            "instanceId": 286,
                            "facetId": 286,
                            "abilityGrpId": 1005,
                            "manaPaymentOptions": [
                                {
                                    "mana": [
                                        {
                                            "manaId": 3619,
                                            "color": "ManaColor_Green",
                                            "srcInstanceId": 286,
                                            "specs": [
                                                {"type": "ManaSpecType_Predictive"}
                                            ],
                                            "abilityGrpId": 1005,
                                        }
                                    ]
                                }
                            ],
                            "isBatchable": true,
                            "uniqueAbilityId": 256,
                        },
                        {
                            "actionType": "ActionType_Activate_Mana",
                            "grpId": 80408,
                            "instanceId": 294,
                            "facetId": 294,
                            "abilityGrpId": 1001,
                            "manaPaymentOptions": [
                                {
                                    "mana": [
                                        {
                                            "manaId": 3613,
                                            "color": "ManaColor_White",
                                            "srcInstanceId": 294,
                                            "specs": [
                                                {"type": "ManaSpecType_Predictive"}
                                            ],
                                            "abilityGrpId": 1001,
                                        }
                                    ]
                                }
                            ],
                            "isBatchable": true,
                            "uniqueAbilityId": 269,
                        },
                        {
                            "actionType": "ActionType_Activate_Mana",
                            "grpId": 80408,
                            "instanceId": 294,
                            "facetId": 294,
                            "abilityGrpId": 1002,
                            "manaPaymentOptions": [
                                {
                                    "mana": [
                                        {
                                            "manaId": 3618,
                                            "color": "ManaColor_Blue",
                                            "srcInstanceId": 294,
                                            "specs": [
                                                {"type": "ManaSpecType_Predictive"}
                                            ],
                                            "abilityGrpId": 1002,
                                        }
                                    ]
                                }
                            ],
                            "isBatchable": true,
                            "uniqueAbilityId": 268,
                        },
                        {
                            "actionType": "ActionType_Activate_Mana",
                            "grpId": 80408,
                            "instanceId": 294,
                            "facetId": 294,
                            "abilityGrpId": 1005,
                            "manaPaymentOptions": [
                                {
                                    "mana": [
                                        {
                                            "manaId": 3620,
                                            "color": "ManaColor_Green",
                                            "srcInstanceId": 294,
                                            "specs": [
                                                {"type": "ManaSpecType_Predictive"}
                                            ],
                                            "abilityGrpId": 1005,
                                        }
                                    ]
                                }
                            ],
                            "isBatchable": true,
                            "uniqueAbilityId": 270,
                        },
                        {
                            "actionType": "ActionType_Activate_Mana",
                            "grpId": 82761,
                            "instanceId": 358,
                            "facetId": 358,
                            "abilityGrpId": 1001,
                            "manaPaymentOptions": [
                                {
                                    "mana": [
                                        {
                                            "manaId": 3615,
                                            "color": "ManaColor_White",
                                            "srcInstanceId": 358,
                                            "specs": [
                                                {"type": "ManaSpecType_Predictive"}
                                            ],
                                            "abilityGrpId": 1001,
                                        }
                                    ]
                                }
                            ],
                            "isBatchable": true,
                            "uniqueAbilityId": 330,
                        },
                        {"actionType": "ActionType_Pass"},
                        {"actionType": "ActionType_FloatMana"},
                    ],
                    "inactiveActions": [
                        {
                            "actionType": "ActionType_Activate",
                            "grpId": 80166,
                            "instanceId": 359,
                            "facetId": 359,
                            "abilityGrpId": 149361,
                            "manaCost": [
                                {
                                    "color": ["ManaColor_White"],
                                    "count": 5,
                                    "abilityGrpId": 149361,
                                }
                            ],
                            "uniqueAbilityId": 333,
                        },
                        {
                            "actionType": "ActionType_Activate_Mana",
                            "grpId": 82761,
                            "instanceId": 305,
                            "facetId": 305,
                            "abilityGrpId": 1001,
                            "uniqueAbilityId": 288,
                        },
                        {
                            "actionType": "ActionType_Activate_Mana",
                            "grpId": 87586,
                            "instanceId": 316,
                            "facetId": 316,
                            "abilityGrpId": 1005,
                            "uniqueAbilityId": 295,
                        },
                        {
                            "actionType": "ActionType_Activate_Mana",
                            "grpId": 82761,
                            "instanceId": 337,
                            "facetId": 337,
                            "abilityGrpId": 1001,
                            "uniqueAbilityId": 314,
                        },
                    ],
                },
            },
        ]
    },
}
"""


class StateWrapper:
    @property
    def local_id(self):
        return self.state.local_id

    @local_id.setter
    def local_id(self, value):
        self.state.local_id = value

    def __init__(self):
        self.state = MtgGameState(local_id=1, zones=[], players=[], all_cards={})

    def update_zone(self, zone: pb.ZoneInfo):
        selected_zone = [z for z in self.state.zones if z.id == zone.zoneId]
        if selected_zone:
            selected_zone = selected_zone[0]
            selected_zone.instance_ids = (
                zone.objectInstanceIds if zone.objectInstanceIds else []
            )
        else:
            self.state.zones.append(
                Zone(
                    id=zone.zoneId,
                    type=zone.type,
                    visibility=zone.visibility if zone.visibility else None,
                    owner=zone.ownerSeatId if zone.ownerSeatId else None,
                    instance_ids=zone.objectInstanceIds
                    if zone.objectInstanceIds
                    else [],
                    visible_cards=[],
                )
            )

    def update_player(self, player: pb.PlayerInfo):
        select_player = [
            p for p in self.state.players if p.gre_player_num == player.systemSeatNumber
        ]
        if select_player:
            select_player = select_player[0]
            select_player.total_life = player.lifeTotal
            # TODO
        else:
            self.state.players.append(
                Player(
                    gre_player_num=player.systemSeatNumber,
                    team_id=player.teamId,
                    total_life=player.lifeTotal,
                    timers=[],
                )
            )

    def update_instance(self, instance: pb.GameObjectInfo):
        if instance.instanceId in self.state.all_cards and (
            inst := self.state.all_cards[instance.instanceId]
        ):
            inst.overlay_grp_id = instance.overlayGrpId
            inst.name = instance.name
        else:
            self.state.all_cards[instance.instanceId] = CardInstance(
                id=instance.instanceId,
                grp_id=instance.grpId,
                name=instance.name,
                overlay_grp_id=instance.overlayGrpId,
            )

    def update_timer(self, timer_message: pb.TimerStateMessage):
        pass

    def update_with(self, state_message: pb.GameStateMessage):
        match state_message.type:
            case pb.GameStateType.GameStateType_Diff | pb.GameStateType.GameStateType_Full:
                # self.state_id = state_message.gameStateId
                for player in state_message.players:
                    self.update_player(player)
                # self.turn_info = {
                #     "active_player": state_message.turnInfo.activePlayer,
                #     "decision_player": state_message.turnInfo.decisionPlayer,
                # }
                for zone in state_message.zones:
                    self.update_zone(zone)
                for instance in state_message.gameObjects:
                    self.update_instance(instance)
                # for action in state_message.actions:
                #     self.actions += [
                #         {
                #             "seat_id": action.seatId,
                #             "type": action.action.actionType,
                #             "id": action.action.instanceId,
                #         }
                #     ]
            case _:
                from textual import log

                log(state_message)

    def get_zone_cards(self, zone_type: str, owner_is_me=True):
        zone_type = dict(pb.ZoneType.items())[zone_type]
        zone = [
            zone
            for zone in self.state.zones
            if zone.type == zone_type
            and (
                owner_is_me is None
                or zone.owner is None
                or (owner_is_me ^ (zone.owner != self.state.local_id))
            )
        ]
        if zone:
            zone = zone[0]
        else:
            return []
        instance_ids = zone.instance_ids
        return [
            c
            if id in self.state.all_cards and (c := self.state.all_cards[id])
            else CardInstance(id=id, grp_id=0, name="unknown", overlay_grp_id="unknown")
            for id in instance_ids
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
        self.last_choices = []

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
                        self.state.update_with(msg.gameStateMessage)
                    case pb.GREMessageType.GREMessageType_TimerStateMessage:
                        self.state.update_timer(msg.timerStateMessage)
                    case pb.GREMessageType.GREMessageType_MulliganReq:
                        self.last_req += [msg]
                    case pb.GREMessageType.GREMessageType_ActionsAvailableReq:
                        self.last_req += [msg]
                    case pb.GREMessageType.GREMessageType_ChooseStartingPlayerReq:
                        self.last_req += [msg]
                    case pb.GREMessageType.GREMessageType_PromptReq:
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

    def get_available_options(self, req: pb.GREToClientMessage = None) -> str:
        if req == None and self.last_req:
            req = self.last_req[-1]
        if req == None:
            return str(self.last_choices)

        def highlighted_move(action: pb.Action) -> bool:
            if action == None:
                return False
            # not affordable
            if not (
                (
                    action.actionType == pb.ActionType.ActionType_Play
                    or action.actionType == pb.ActionType.ActionType_PlayMDFC
                )
                or (len(action.autoTapSolution.autoTapActions) > 0)
                or (
                    all(
                        [
                            pb.ManaColor.ManaColor_Phyrexian in requirement.color
                            or pb.ManaColor.ManaColor_X in requirement.color
                            for requirement in action.manaCost
                        ]
                    )
                )
            ):
                return False
            if (
                action.abilityGrpId == 75081
                and action.highlight == pb.HighlightType.HighlightType_Cold
                and action.actionType == pb.ActionType.ActionType_Activate
            ):
                return False
            if action.highlight == pb.HighlightType.HighlightType_Hot:
                return True
            # shouldn't play, temp unavailable
            # if action.abilityGrpId != 0 and instance.PlayWarnings.Exists((ShouldntPlayData x) => x.AbilityId == action.AbilityGrpId):
            #     return False
            return True

        from textual import log

        log(f"pending req: {req}")
        self.last_choices = [req]
        match req.type:
            case pb.GREMessageType.GREMessageType_ActionsAvailableReq:
                self.last_choices = [
                    action
                    for action in req.actionsAvailableReq.actions
                    if highlighted_move(action)
                ]
                return str(self.last_choices)
            case pb.GREMessageType.GREMessageType_MulliganReq:
                return str(req)
            case pb.GREMessageType.GREMessageType_ChooseStartingPlayerReq:
                return str(req)
            case _:
                return str(req)

    def decide_reply(self, command, auto_respond) -> pb.ClientToGREMessage | None:
        from textual import log

        if not self.last_req:
            return None
        ### TODO: only if the resp is relevent to the req, pop this req
        req = self.last_req.pop()
        try:
            log(f"here is {command=}")
            choice_num = int(command)
            if choice_num in self.last_choices:
                choice = self.last_choices[choice_num]
                self.last_choices = []
                log(choice)
                return pb.ClientToGREMessage(
                    type=pb.ClientMessageType.ClientMessageType_PerformActionResp,
                    gameStateId=req.gameStateId,
                    respId=req.msgId,
                    performActionResp=pb.PerformActionResp(
                        autoPassPriority=pb.AutoPassPriority.AutoPassPriority_Yes,
                        actions=[choice],
                    ),
                )
        except:
            pass

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
            case pb.GREMessageType.GREMessageType_MulliganReq:
                return pb.ClientToGREMessage(
                    type=pb.ClientMessageType.ClientMessageType_MulliganResp,
                    gameStateId=req.gameStateId,
                    respId=req.msgId,
                    mulliganResp=pb.MulliganResp(
                        decision=pb.MulliganOption.MulliganOption_AcceptHand
                    ),
                )
            case _:
                pass
        return None
