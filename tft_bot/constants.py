"""Common constants used throughout the codebase, and common groupings of them in array format."""

CONSTANTS = {
    "storage": {"appdata": "%APPDATA%/TFT Bot"},
    "executables": {
        "league": {
            "client_base": r"\LeagueClient.exe",
            "client_ux_base": r"\LeagueClientUx.exe",
            "game_base": r"\Game\League of Legends.exe",
            "client": r"\LeagueClient.exe",
            "client_ux": r"\LeagueClientUx.exe",
            "game": r"\Game\League of Legends.exe",
        },
    },
    "window_titles": {
        "game": "League of Legends (TM) Client",
        "client": "League of Legends",
    },
    "processes": {
        "client": "LeagueClient.exe",
        "client_ux": "LeagueClientUx.exe",
        "game": "League of Legends.exe",
        "rito_client": "RiotClientServices.exe",
    },
    "client": {
        "messages": {
            "failed_to_reconnect": "captures/messages/failed_to_reconnect.png",
            "down_for_maintenance": "captures/messages/down_for_maintenance.png",
            "instant_feedback_report": "captures/messages/instant_feedback_report.png",
            "login_servers_down": "captures/messages/login_servers_down.png",
            "session_expired": "captures/messages/session_expired.png",
            "unexpected_error_with_session": "captures/messages/unexpected_error_with_session.png",
            "unexpected_login_error": "captures/messages/unexpected_login_error.png",
            "buttons": {
                "message_ok": "captures/buttons/message_ok.png",
                "message_exit": {
                    "1": "captures/buttons/message_exit_1.png",
                    "2": "captures/buttons/message_exit_2.png",
                },
            },
        },
    },
    "game": {
        "exit_now": {
            "base": "captures/buttons/exit_now_base.png",
            "highlighted": "captures/buttons/exit_now_highlighted.png",
            "original": "captures/buttons/exit_now_original.png",
            "continue": "captures/buttons/continue.png",
        },
        "settings": "captures/buttons/settings.png",
        "surrender": {
            "surrender_1": "captures/buttons/surrender_1.png",
            "surrender_2": "captures/buttons/surrender_2.png",
        },
        "gamelogic": {
            "choose_an_augment": "captures/buttons/choose_an_augment.png",
            "choose_one": "captures/buttons/choose_one.png",
            "reroll": "captures/buttons/reroll.png",
            "take_all": "captures/buttons/take_all.png",
            "xp_buy": "captures/buttons/xp_buy.png",
            "vote": "captures/buttons/vote.png",
            "recipe": "captures/messages/recipes_text.png",
            "emblem": "captures/messages/unique.png",
        },
        "gold": {
            "0": "captures/gold/0.png",
            "1": "captures/gold/1.png",
            "2": "captures/gold/2.png",
            "3": "captures/gold/3.png",
            "4": "captures/gold/4.png",
            "5": "captures/gold/5.png",
            "6": "captures/gold/6.png",
        },
        "round": {
            "-4": "captures/round/-4.png",
            "1-": "captures/round/1-.png",
            "2-": "captures/round/2-.png",
            "3-": "captures/round/3-.png",
            "4-": "captures/round/4-.png",
            "5-": "captures/round/5-.png",
            "6-": "captures/round/6-.png",
            "1-1": "captures/round/1-1.png",
            "2-2": "captures/round/2-2.png",
            "2-3": "captures/round/2-3.png",
            "2-4": "captures/round/2-4.png",
            "2-5": "captures/round/2-5.png",
            "3-1": "captures/round/3-1.png",
            "3-2": "captures/round/3-2.png",
            "3-3": "captures/round/3-3.png",
            "3-4": "captures/round/3-4.png",
            "3-7": "captures/round/3-7.png",
            "4-6": "captures/round/4-6.png",
            "4-7": "captures/round/4-7.png",
            "6-5": "captures/round/6-5.png",
            "6-6": "captures/round/6-6.png",
            "draft_active": "captures/round/draft_active.png",
            "krugs_inactive": "captures/round/krugs_inactive.png",
            "krugs_active": "captures/round/krugs_active.png",
            "wolves_inactive": "captures/round/wolves_inactive.png",
            "wolves_active": "captures/round/wolves_active.png",
            "birds_inactive": "captures/round/birds_inactive.png",
            "birds_active": "captures/round/birds_active.png",
            "elder_dragon_inactive": "captures/round/elder_dragon_inactive.png",
            "elder_dragon_active": "captures/round/elder_dragon_active.png",
        },
        "round_text": {
            "11", "12", "13", "14",
            "21", "22", "23", "24", "25", "26", "27",
            "31", "32", "33", "34", "35", "36", "37",
            "41", "42", "43", "44", "45", "46", "47",
            "51", "52", "53", "54", "55", "56", "57",
            "61", "62", "63", "64", "65", "66", "67",
            "71", "72", "73", "74", "75", "76", "77",
        },
        "trait": {
            "bastion": "captures/trait/bastion.png",
            "bruiser": "captures/trait/bruiser.png",
            "challenger": "captures/trait/challenger.png",
            "darkin": "captures/trait/darkin.png",
            "deadeye": "captures/trait/deadeye.png",
            "demacia": "captures/trait/demacia.png",
            "empress": "captures/trait/empress.png",
            "freljord": "captures/trait/freljord.png",
            "gunner": "captures/trait/gunner.png",
            "invoker": "captures/trait/invoker.png",
            "ionia": "captures/trait/ionia.png",
            "juggernaut": "captures/trait/juggernaut.png",
            "multicaster": "captures/trait/multicaster.png",
            "noxus": "captures/trait/noxus.png",
            "piltover": "captures/trait/piltover.png",
            "rogue": "captures/trait/rogue.png",
            "shadow_isles": "captures/trait/shadow_isles.png",
            "shurima": "captures/trait/shurima.png",
            "slayer": "captures/trait/slayer.png",
            "sorcerer": "captures/trait/sorcerer.png",
            "strategist": "captures/trait/strategist.png",
            "targon": "captures/trait/targon.png",
            "void": "captures/trait/void.png",
            "wanderer": "captures/trait/wanderer.png",
            "yordle": "captures/trait/yordle.png",
            "zaun": "captures/trait/zaun.png",
        },
        # taken from https://github.com/jfd02/TFT-OCR-BOT/blob/main/game_assets.py
        # "items": {
        #     # components
        #     "BFSword",
        #     "ChainVest",
        #     "GiantsBelt",
        #     "NeedlesslyLargeRod",
        #     "NegatronCloak",
        #     "RecurveBow",
        #     "SparringGloves",
        #     "Spatula",
        #     "TearoftheGoddess",

        #     # full_items
        #     "BilgewaterEmblem","ChallengerEmblem","IoniaEmblem","JuggernautEmblem",
        #     "NoxusEmblem","ShurimaEmblem","SorcererEmblem","VanquisherEmblem",
        #     "AdaptiveHelm","ArchangelsStaff","Bloodthirster","BlueBuff",
        #     "BrambleVest","Crownguard","Deathblade","DragonsClaw",
        #     "EdgeofNight","Evenshroud","GargoyleStoneplate","GiantSlayer",
        #     "Guardbreaker","GuinsoosRageblade","HandofJustice","HextechGunblade",
        #     "InfinityEdge","IonicSpark","JeweledGauntlet","LastWhisper",
        #     "Morellonomicon","NashorsTooth","NightHarvester","ProtectorsVow",
        #     "Quicksilver","RabadonsDeathcap","RapidFirecannon","Redemption",
        #     "RunaansHurricane","SpearofShojin","StatikkShiv","SteraksGage",
        #     "SunfireCape","TacticiansCrown","ThiefsGloves","TitansResolve","WarmogsArmor",

        #     # support_items
        #     "AegisoftheLegion","BansheesVeil","ChaliceofPower","CrestofCinders",
        #     "LocketoftheIronSolari","NeedlesslyBigGem","ObsidianCleaver","RanduinsOmen",
        #     "ShroudofStillness","VirtueoftheMartyr","ZekesHerald","Zephyr","ZzRotPortal",

        #     # ornn_items
        #     "AnimaVisage","BlacksmithsGloves","DeathfireGrasp","DeathsDefiance",
        #     "EternalWinter","GoldCollector","GoldmancersStaff","Hullcrusher",
        #     "InfinityForce","MogulsMail","Muramana","Rocket-PropelledFist",
        #     "SnipersFocus","TrickstersGlass","ZhonyasParadox",

        #     # uncraftable_items
        #     "BastionEmblem","BruiserEmblem","DeadeyeEmblem","FreljordEmblem",
        #     "GunnerEmblem","InvokerEmblem","PiltoverEmblem","RogueEmblem",
        #     "StrategistEmblem","TargonEmblem","VoidEmblem","ZaunEmblem"
        # },
        "coordinates": {
            "board": [
                # extra two slots for champs that may arrive from shared draft
                (707, 651), (839, 651),
                # bottom row
                (966, 651), (903, 571), (962, 494),
                # middle row
                (1091, 651), (1022, 571), (1082, 494),
                # top row
                (1222, 651), (1147, 571), (1198, 494)
            ],
            "bench": [
                (425, 777), (542, 777), (658, 777),
                (778, 777), (892, 777), (1010, 777),
                (1128, 777), (1244, 777), (1359, 777)
            ],
            "items": [
                (273, 753), (348, 737), (289, 692), (356, 676), (307, 631),
                (323, 586), (407, 679), (379, 632), (396, 582), (457, 628)
            ]
        },
        "champions": {
            "trait": {
                "sorcerer": [
                    "ahri",
                    "malzahar",
                    "orianna",
                    "silco",
                    "swain",
                    "taric",
                    "velkoz",
                ],
                "void": [
                    "belveth",
                    "chogath",
                    "kaisa",
                    "kassadin",
                    "malzahar",
                    "reksai",
                    "velkoz",
                ],
            },

            "full": {
                "ahri": "captures/champions/ahri.png",
                "belveth": "captures/champions/belveth.png",
                "chogath": "captures/champions/chogath.png",
                "kaisa": "captures/champions/kaisa.png",
                "kassadin": "captures/champions/kassadin.png",
                "malzahar": "captures/champions/malzahar.png",
                "orianna": "captures/champions/orianna.png",
                "reksai": "captures/champions/reksai.png",
                "silco": "captures/champions/silco.png",
                "swain": "captures/champions/swain.png",
                "taric": "captures/champions/taric.png",
                "velkoz": "captures/champions/velkoz.png",
            }
        }
    },
}

exit_now_images = [
    CONSTANTS["game"]["exit_now"]["base"],
    CONSTANTS["game"]["exit_now"]["highlighted"],
    CONSTANTS["game"]["exit_now"]["original"],
    CONSTANTS["game"]["exit_now"]["continue"],
]

message_exit_buttons = [
    CONSTANTS["client"]["messages"]["buttons"]["message_exit"]["1"],
    CONSTANTS["client"]["messages"]["buttons"]["message_exit"]["2"],
]

league_processes = [
    CONSTANTS["processes"]["client"],
    CONSTANTS["processes"]["client_ux"],
    CONSTANTS["processes"]["game"],
    CONSTANTS["processes"]["rito_client"],
]
