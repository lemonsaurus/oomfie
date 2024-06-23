# List of all classes and specs
LONGCLASS_TO_SHORTCLASS = {
    "Havoc Demon Hunter": "dh_havoc",
    "Vengeance Demon Hunter": "dh_vengeance",
    "Blood Death Knight": "dk_blood",
    "Frost Death Knight": "dk_frost",
    "Unholy Death Knight": "dk_unholy",
    "Balance Druid": "druid_balance",
    "Feral Druid": "druid_feral",
    "Guardian Druid": "druid_guardian",
    "Restoration Druid": "druid_resto",
    "Augmentation Evoker": "evoker_augmentation",
    "Devastation Evoker": "evoker_devastation",
    "Preservation Evoker": "evoker_preservation",
    "Beast Mastery Hunter": "hunter_bm",
    "Marksmanship Hunter": "hunter_mm",
    "Survival Hunter": "hunter_survival",
    "Arcane Mage": "mage_arcane",
    "Fire Mage": "mage_fire",
    "Frost Mage": "mage_frost",
    "Brewmaster Monk": "monk_brewmaster",
    "Mistweaver Monk": "monk_mistweaver",
    "Windwalker Monk": "monk_ww",
    "Holy Paladin": "paladin_holy",
    "Protection Paladin": "paladin_protection",
    "Retribution Paladin": "paladin_ret",
    "Discipline Priest": "priest_disc",
    "Holy Priest": "priest_holy",
    "Shadow Priest": "priest_shadow",
    "Assassination Rogue": "rogue_assa",
    "Outlaw Rogue": "rogue_outlaw",
    "Subtlety Rogue": "rogue_sub",
    "Elemental Shaman": "shaman_elem",
    "Enhancement Shaman": "shaman_enhancement",
    "Restoration Shaman": "shaman_resto",
    "Affliction Warlock": "warlock_affli",
    "Demonology Warlock": "warlock_demono",
    "Destruction Warlock": "warlock_destru",
    "Arms Warrior": "warrior_arms",
    "Fury Warrior": "warrior_fury",
    "Protection Warrior": "warrior_prot",
}

CLASS_ICONS = {
    "dh_havoc":"1254379358664130580",
    "dh_vengeance":"1254379360090325072",
    "dk_blood":"1254379361352683583",
    "dk_frost":"1254379362883735653",
    "dk_unholy":"1254379365064638474",
    "druid_balance":"1254379366427918407",
    "druid_feral":"1254379367849656400",
    "druid_guardian":"1254379369053425726",
    "druid_resto":"1254379370999709726",
    "evoker_augmentation":"1254379373000396852",
    "evoker_devastation":"1254379526591348827",
    "evoker_preservation":"1254379377064411219",
    "hunter_bm":"1254379574104686652",
    "hunter_mm":"1254379380357070890",
    "hunter_survival":"1254379588067524648",
    "mage_arcane":"1254379383892869192",
    "mage_fire":"1254379610725023745",
    "mage_frost":"1254379388154155039",
    "monk_brewmaster":"1254379655222530060",
    "monk_mistweaver":"1254379390914007071",
    "monk_ww":"1254379640307449946",
    "paladin_holy":"1254379395108311040",
    "paladin_protection":"1254379397712973906",
    "paladin_ret":"1254379677553000541",
    "priest_disc":"1254379401358082069",
    "priest_holy":"1254379701074399234",
    "priest_shadow":"1254379404847484978",
    "rogue_assa":"1254379751322161196",
    "rogue_outlaw":"1254379408483946517",
    "rogue_sub":"1254379412758073354",
    "shaman_elem":"1254379780988600441",
    "shaman_enhancement":"1254379416201592972",
    "shaman_resto":"1254379789079416862",
    "warlock_affli":"1254379419229884477",
    "warlock_demono":"1254379807207194655",
    "warlock_destru":"1254379422488727674",
    "warrior_arms":"1254379837808705607",
    "warrior_fury":"1254379425672200273",
    "warrior_prot":"1254379830024081479",
    "treat":"1249357314834698261",
}

CLASS_BREAKDOWN = {
    "Blood Death Knight": ("Death Knight", "Blood"),
    "Frost Death Knight": ("Death Knight", "Frost"),
    "Unholy Death Knight": ("Death Knight", "Unholy"),
    "Havoc Demon Hunter": ("Demon Hunter", "Havoc"),
    "Vengeance Demon Hunter": ("Demon Hunter", "Vengeance"),
    "Balance Druid": ("Druid", "Balance"),
    "Feral Druid": ("Druid", "Feral"),
    "Guardian Druid": ("Druid", "Guardian"),
    "Restoration Druid": ("Druid", "Restoration"),
    "Devastation Evoker": ("Evoker", "Devastation"),
    "Preservation Evoker": ("Evoker", "Preservation"),
    "Augmentation Evoker": ("Evoker", "Augmentation"),
    "Beast Mastery Hunter": ("Hunter", "Beast Mastery"),
    "Marksmanship Hunter": ("Hunter", "Marksmanship"),
    "Survival Hunter": ("Hunter", "Survival"),
    "Arcane Mage": ("Mage", "Arcane"),
    "Fire Mage": ("Mage", "Fire"),
    "Frost Mage": ("Mage", "Frost"),
    "Brewmaster Monk": ("Monk", "Brewmaster"),
    "Mistweaver Monk": ("Monk", "Mistweaver"),
    "Windwalker Monk": ("Monk", "Windwalker"),
    "Holy Paladin": ("Paladin", "Holy"),
    "Protection Paladin": ("Paladin", "Protection"),
    "Retribution Paladin": ("Paladin", "Retribution"),
    "Discipline Priest": ("Priest", "Discipline"),
    "Holy Priest": ("Priest", "Holy"),
    "Shadow Priest": ("Priest", "Shadow"),
    "Assassination Rogue": ("Rogue", "Assassination"),
    "Outlaw Rogue": ("Rogue", "Outlaw"),
    "Subtlety Rogue": ("Rogue", "Subtlety"),
    "Elemental Shaman": ("Shaman", "Elemental"),
    "Enhancement Shaman": ("Shaman", "Enhancement"),
    "Restoration Shaman": ("Shaman", "Restoration"),
    "Affliction Warlock": ("Warlock", "Affliction"),
    "Demonology Warlock": ("Warlock", "Demonology"),
    "Destruction Warlock": ("Warlock", "Destruction"),
    "Arms Warrior": ("Warrior", "Arms"),
    "Fury Warrior": ("Warrior", "Fury"),
    "Protection Warrior": ("Warrior", "Protection"),
}

TANK = [
    "Blood Death Knight",
    "Vengeance Demon Hunter",
    "Guardian Druid",
    "Brewmaster Monk",
    "Protection Paladin",
    "Protection Warrior"
]

HEALER = [
    "Restoration Druid",
    "Preservation Evoker",
    "Mistweaver Monk",
    "Holy Paladin",
    "Discipline Priest",
    "Holy Priest",
    "Restoration Shaman"
]

DPS = [
    "Frost Death Knight",
    "Unholy Death Knight",
    "Havoc Demon Hunter",
    "Balance Druid",
    "Feral Druid",
    "Devastation Evoker",
    "Augmentation Evoker",
    "Beast Mastery Hunter",
    "Marksmanship Hunter",
    "Survival Hunter",
    "Arcane Mage",
    "Fire Mage",
    "Frost Mage",
    "Windwalker Monk",
    "Retribution Paladin",
    "Shadow Priest",
    "Assassination Rogue",
    "Outlaw Rogue",
    "Subtlety Rogue",
    "Elemental Shaman",
    "Enhancement Shaman",
    "Affliction Warlock",
    "Demonology Warlock",
    "Destruction Warlock",
    "Arms Warrior",
    "Fury Warrior"
]

MELEE = [
    "Frost Death Knight",
    "Unholy Death Knight",
    "Havoc Demon Hunter",
    "Feral Druid",
    "Windwalker Monk",
    "Retribution Paladin",
    "Assassination Rogue",
    "Outlaw Rogue",
    "Subtlety Rogue",
    "Enhancement Shaman",
    "Survival Hunter",
    "Arms Warrior",
    "Fury Warrior"
]

RANGED = [
    "Balance Druid",
    "Devastation Evoker",
    "Augmentation Evoker",
    "Beast Mastery Hunter",
    "Marksmanship Hunter",
    "Arcane Mage",
    "Fire Mage",
    "Frost Mage",
    "Shadow Priest",
    "Elemental Shaman",
    "Affliction Warlock",
    "Demonology Warlock",
    "Destruction Warlock"
]

CLASS_SPECS_FULL = [
    "Blood Death Knight",
    "Frost Death Knight",
    "Unholy Death Knight",
    "Havoc Demon Hunter",
    "Vengeance Demon Hunter",
    "Balance Druid",
    "Feral Druid",
    "Guardian Druid",
    "Restoration Druid",
    "Devastation Evoker",
    "Preservation Evoker",
    "Augmentation Evoker",
    "Beast Mastery Hunter",
    "Marksmanship Hunter",
    "Survival Hunter",
    "Arcane Mage",
    "Fire Mage",
    "Frost Mage",
    "Brewmaster Monk",
    "Mistweaver Monk",
    "Windwalker Monk",
    "Holy Paladin",
    "Protection Paladin",
    "Retribution Paladin",
    "Discipline Priest",
    "Holy Priest",
    "Shadow Priest",
    "Assassination Rogue",
    "Outlaw Rogue",
    "Subtlety Rogue",
    "Elemental Shaman",
    "Enhancement Shaman",
    "Restoration Shaman",
    "Affliction Warlock",
    "Demonology Warlock",
    "Destruction Warlock",
    "Arms Warrior",
    "Fury Warrior",
    "Protection Warrior"
]

CLASSES = [
    "DEATH KNIGHT",
    "DEMON HUNTER",
    "DRUID",
    "EVOKER",
    "HUNTER",
    "MAGE",
    "MONK",
    "PALADIN",
    "PRIEST",
    "ROGUE",
    "SHAMAN",
    "WARLOCK",
    "WARRIOR"
]

CLASS_TO_SPECS = {
    "DEATH KNIGHT": [
        "Blood Death Knight",
        "Frost Death Knight",
        "Unholy Death Knight"
    ],
    "DEMON HUNTER": [
        "Havoc Demon Hunter",
        "Vengeance Demon Hunter"
    ],
    "DRUID": [
        "Balance Druid",
        "Feral Druid",
        "Guardian Druid",
        "Restoration Druid"
    ],
    "EVOKER": [
        "Devastation Evoker",
        "Preservation Evoker",
        "Augmentation Evoker"
    ],
    "HUNTER": [
        "Beast Mastery Hunter",
        "Marksmanship Hunter",
        "Survival Hunter"
    ],
    "MAGE": [
        "Arcane Mage",
        "Fire Mage",
        "Frost Mage"
    ],
    "MONK": [
        "Brewmaster Monk",
        "Mistweaver Monk",
        "Windwalker Monk"
    ],
    "PALADIN": [
        "Holy Paladin",
        "Protection Paladin",
        "Retribution Paladin"
    ],
    "PRIEST": [
        "Discipline Priest",
        "Holy Priest",
        "Shadow Priest"
    ],
    "ROGUE": [
        "Assassination Rogue",
        "Outlaw Rogue",
        "Subtlety Rogue"
    ],
    "SHAMAN": [
        "Elemental Shaman",
        "Enhancement Shaman",
        "Restoration Shaman"
    ],
    "WARLOCK": [
        "Affliction Warlock",
        "Demonology Warlock",
        "Destruction Warlock"
    ],
    "WARRIOR": [
        "Arms Warrior",
        "Fury Warrior",
        "Protection Warrior"
    ]
}