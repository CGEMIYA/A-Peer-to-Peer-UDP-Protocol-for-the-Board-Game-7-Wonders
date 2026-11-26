
from dataclasses import dataclass

PLAYER_COUNTS = (3, 4, 5, 6, 7)          # min_players .. max_players (RFC 1.3)
RAW = ("WOOD", "ORE", "STONE", "CLAY")
MANUFACTURED = ("GLASS", "PAPYRUS", "TEXTILE")
RESOURCES = RAW + MANUFACTURED
SCIENCE_SYMBOLS = ("TABLET", "COMPASS", "GEAR")
COLORS = ("BROWN", "GREY", "BLUE", "YELLOW", "GREEN", "RED", "PURPLE")


@dataclass(frozen=True)
class Card:
    name: str
    age: int
    color: str
    cost: dict
    effects: tuple
    chain_from: tuple      # building any ONE of these earlier makes this card free
    chain_to: tuple        # cards this card makes free (reverse of chain_from)
    counts: dict           # {players: copies in the deck}; None for guilds


@dataclass(frozen=True)
class Stage:
    index: int             # 1-based, in the order stages must be built
    cost: dict
    effects: tuple


@dataclass(frozen=True)
class Wonder:
    name: str
    side: str              # "A" or "B"
    starting_resource: str
    stages: tuple


# ---- effect constructors ---------------------------------------------------
def produce(**resources):
    return {"kind": "produce", "resources": resources}

def choice(*options, sellable=True):
    return {"kind": "produce_choice", "options": tuple(options), "sellable": sellable}

def vp(n):
    return {"kind": "vp", "amount": n}

def shields(n):
    return {"kind": "shields", "amount": n}

def science(symbol):
    return {"kind": "science", "symbol": symbol}

def science_any():
    return {"kind": "science_any"}

def coins(n):
    return {"kind": "coins", "amount": n}

def discount(resources, sides):
    return {"kind": "trade_discount", "resources": tuple(resources), "sides": tuple(sides)}

def per_card(what, scope, coins=0, vp=0):
    return {"kind": "per_card", "what": what, "scope": tuple(scope), "coins": coins, "vp": vp}

def build_from_discard():
    return {"kind": "build_from_discard"}

def free_build_each_age():
    return {"kind": "free_build_each_age"}

def play_last_card():
    return {"kind": "play_last_card"}

def copy_neighbor_guild():
    return {"kind": "copy_neighbor_guild"}

def card(name, age, color, cost, effects, chain_from=(), chain_to=(), counts=None):
    return Card(name, age, color, cost, tuple(effects), tuple(chain_from), tuple(chain_to),
                None if counts is None else dict(zip(PLAYER_COUNTS, counts)))

def stage(index, cost, effects):
    return Stage(index, cost, tuple(effects))

def wonder(name, side, starting_resource, stages):
    return Wonder(name, side, starting_resource, tuple(stages))


# CARDS
AGE_1_CARDS = [
    card('Clay Pit', 1, 'BROWN', {'coins': 1}, [choice('ORE', 'CLAY')], counts=(1, 1, 1, 1, 1)),
    card('Clay Pool', 1, 'BROWN', {}, [produce(CLAY=1)], counts=(1, 1, 2, 2, 2)),
    card('Excavation', 1, 'BROWN', {'coins': 1}, [choice('STONE', 'CLAY')], counts=(0, 1, 1, 1, 1)),
    card('Forest Cave', 1, 'BROWN', {'coins': 1}, [choice('WOOD', 'ORE')], counts=(0, 0, 1, 1, 1)),
    card('Lumber Yard', 1, 'BROWN', {}, [produce(WOOD=1)], counts=(1, 2, 2, 2, 2)),
    card('Mine', 1, 'BROWN', {'coins': 1}, [choice('STONE', 'ORE')], counts=(0, 0, 0, 1, 1)),
    card('Ore Vein', 1, 'BROWN', {}, [produce(ORE=1)], counts=(1, 2, 2, 2, 2)),
    card('Stone Pit', 1, 'BROWN', {}, [produce(STONE=1)], counts=(1, 1, 2, 2, 2)),
    card('Timber Yard', 1, 'BROWN', {'coins': 1}, [choice('WOOD', 'STONE')], counts=(1, 1, 1, 1, 1)),
    card('Tree Farm', 1, 'BROWN', {'coins': 1}, [choice('WOOD', 'CLAY')], counts=(0, 0, 0, 1, 1)),
    card('Glassworks', 1, 'GREY', {}, [produce(GLASS=1)], counts=(1, 1, 1, 2, 2)),
    card('Loom', 1, 'GREY', {}, [produce(TEXTILE=1)], counts=(1, 1, 1, 2, 2)),
    card('Press', 1, 'GREY', {}, [produce(PAPYRUS=1)], counts=(1, 1, 1, 2, 2)),
    card('East Trading Post', 1, 'YELLOW', {}, [discount(('WOOD', 'ORE', 'STONE', 'CLAY'), ('RIGHT',))], chain_to=('Forum',), counts=(1, 1, 1, 1, 2)),
    card('Marketplace', 1, 'YELLOW', {}, [discount(('GLASS', 'PAPYRUS', 'TEXTILE'), ('LEFT', 'RIGHT'))], chain_to=('Caravansery',), counts=(1, 1, 1, 2, 2)),
    card('Tavern', 1, 'YELLOW', {}, [coins(5)], counts=(0, 1, 2, 2, 3)),
    card('West Trading Post', 1, 'YELLOW', {}, [discount(('WOOD', 'ORE', 'STONE', 'CLAY'), ('LEFT',))], chain_to=('Forum',), counts=(1, 1, 1, 1, 2)),
    card('Altar', 1, 'BLUE', {}, [vp(2)], chain_to=('Temple',), counts=(1, 1, 2, 2, 2)),
    card('Baths', 1, 'BLUE', {'STONE': 1}, [vp(3)], chain_to=('Aqueduct',), counts=(1, 1, 1, 1, 2)),
    card('Pawnshop', 1, 'BLUE', {}, [vp(3)], counts=(0, 1, 1, 1, 2)),
    card('Theater', 1, 'BLUE', {}, [vp(2)], chain_to=('Statue',), counts=(1, 1, 1, 2, 2)),
    card('Apothecary', 1, 'GREEN', {'TEXTILE': 1}, [science('COMPASS')], chain_to=('Stables', 'Dispensary'), counts=(1, 1, 2, 2, 2)),
    card('Scriptorium', 1, 'GREEN', {'PAPYRUS': 1}, [science('TABLET')], chain_to=('Courthouse', 'Library'), counts=(1, 2, 2, 2, 2)),
    card('Workshop', 1, 'GREEN', {'GLASS': 1}, [science('GEAR')], chain_to=('Archery Range', 'Laboratory'), counts=(1, 1, 1, 1, 2)),
    card('Barracks', 1, 'RED', {'ORE': 1}, [shields(1)], counts=(1, 1, 2, 2, 2)),
    card('Guard Tower', 1, 'RED', {'CLAY': 1}, [shields(1)], counts=(1, 2, 2, 2, 2)),
    card('Stockade', 1, 'RED', {'WOOD': 1}, [shields(1)], counts=(1, 1, 1, 1, 2)),
]

AGE_2_CARDS = [
    card('Brickyard', 2, 'BROWN', {'coins': 1}, [produce(CLAY=2)], counts=(1, 2, 2, 2, 2)),
    card('Foundry', 2, 'BROWN', {'coins': 1}, [produce(ORE=2)], counts=(1, 2, 2, 2, 2)),
    card('Quarry', 2, 'BROWN', {'coins': 1}, [produce(STONE=2)], counts=(1, 2, 2, 2, 2)),
    card('Sawmill', 2, 'BROWN', {'coins': 1}, [produce(WOOD=2)], counts=(1, 2, 2, 2, 2)),
    card('Glassworks', 2, 'GREY', {}, [produce(GLASS=1)], counts=(1, 1, 2, 2, 2)),
    card('Loom', 2, 'GREY', {}, [produce(TEXTILE=1)], counts=(1, 1, 2, 2, 2)),
    card('Press', 2, 'GREY', {}, [produce(PAPYRUS=1)], counts=(1, 1, 2, 2, 2)),
    card('Bazar', 2, 'YELLOW', {}, [per_card(('GREY',), ('SELF', 'LEFT', 'RIGHT'), coins=2)], counts=(0, 1, 1, 1, 2)),
    card('Caravansery', 2, 'YELLOW', {'WOOD': 2}, [choice('WOOD', 'STONE', 'ORE', 'CLAY', sellable=False)], chain_from=('Marketplace',), chain_to=('Lighthouse',), counts=(1, 1, 2, 3, 3)),
    card('Forum', 2, 'YELLOW', {'CLAY': 2}, [choice('GLASS', 'PAPYRUS', 'TEXTILE', sellable=False)], chain_from=('East Trading Post', 'West Trading Post'), chain_to=('Haven',), counts=(1, 1, 1, 2, 3)),
    card('Vineyard', 2, 'YELLOW', {}, [per_card(('BROWN',), ('SELF', 'LEFT', 'RIGHT'), coins=1)], counts=(1, 1, 1, 2, 2)),
    card('Aqueduct', 2, 'BLUE', {'STONE': 3}, [vp(5)], chain_from=('Baths',), counts=(1, 1, 1, 1, 2)),
    card('Courthouse', 2, 'BLUE', {'CLAY': 2, 'TEXTILE': 1}, [vp(4)], chain_from=('Scriptorium',), counts=(1, 1, 2, 2, 2)),
    card('Statue', 2, 'BLUE', {'WOOD': 1, 'ORE': 2}, [vp(4)], chain_from=('Theater',), chain_to=('Gardens',), counts=(1, 1, 1, 1, 2)),
    card('Temple', 2, 'BLUE', {'WOOD': 1, 'CLAY': 1, 'GLASS': 1}, [vp(3)], chain_from=('Altar',), chain_to=('Pantheon',), counts=(1, 1, 1, 2, 2)),
    card('Dispensary', 2, 'GREEN', {'ORE': 2, 'GLASS': 1}, [science('COMPASS')], chain_from=('Apothecary',), chain_to=('Arena', 'Lodge'), counts=(1, 2, 2, 2, 2)),
    card('Laboratory', 2, 'GREEN', {'CLAY': 2, 'PAPYRUS': 1}, [science('GEAR')], chain_from=('Workshop',), chain_to=('Siege Workshop', 'Observatory'), counts=(1, 1, 2, 2, 2)),
    card('Library', 2, 'GREEN', {'STONE': 2, 'TEXTILE': 1}, [science('TABLET')], chain_from=('Scriptorium',), chain_to=('Senate', 'University'), counts=(1, 1, 1, 2, 2)),
    card('School', 2, 'GREEN', {'WOOD': 1, 'PAPYRUS': 1}, [science('TABLET')], chain_to=('Academy', 'Study'), counts=(1, 1, 1, 1, 2)),
    card('Archery Range', 2, 'RED', {'WOOD': 2, 'ORE': 1}, [shields(2)], chain_from=('Workshop',), counts=(1, 1, 1, 2, 2)),
    card('Stables', 2, 'RED', {'WOOD': 1, 'ORE': 1, 'CLAY': 1}, [shields(2)], chain_from=('Apothecary',), counts=(1, 1, 2, 2, 2)),
    card('Training Ground', 2, 'RED', {'WOOD': 1, 'ORE': 2}, [shields(2)], chain_to=('Circus',), counts=(0, 1, 1, 2, 3)),
    card('Walls', 2, 'RED', {'STONE': 3}, [shields(2)], chain_to=('Fortifications',), counts=(1, 1, 1, 1, 2)),
]

AGE_3_CARDS = [
    card('Arena', 3, 'YELLOW', {'ORE': 1, 'STONE': 2}, [per_card('WONDER_STAGE', ('SELF',), coins=3, vp=1)], chain_from=('Dispensary',), counts=(1, 1, 2, 2, 3)),
    card('Chamber of Commerce', 3, 'YELLOW', {'CLAY': 2, 'PAPYRUS': 1}, [per_card(('GREY',), ('SELF',), coins=2, vp=2)], counts=(0, 1, 1, 2, 2)),
    card('Haven', 3, 'YELLOW', {'WOOD': 1, 'ORE': 1, 'TEXTILE': 1}, [per_card(('BROWN',), ('SELF',), coins=1, vp=1)], chain_from=('Forum',), counts=(1, 2, 2, 2, 2)),
    card('Lighthouse', 3, 'YELLOW', {'STONE': 1, 'GLASS': 1}, [per_card(('YELLOW',), ('SELF',), coins=1, vp=1)], chain_from=('Caravansery',), counts=(1, 1, 1, 2, 2)),
    card('Gardens', 3, 'BLUE', {'WOOD': 1, 'CLAY': 2}, [vp(5)], chain_from=('Statue',), counts=(1, 2, 2, 2, 2)),
    card('Palace', 3, 'BLUE', {'WOOD': 1, 'ORE': 1, 'STONE': 1, 'CLAY': 1, 'GLASS': 1, 'PAPYRUS': 1, 'TEXTILE': 1}, [vp(8)], counts=(1, 1, 1, 1, 2)),
    card('Pantheon', 3, 'BLUE', {'ORE': 1, 'CLAY': 2, 'GLASS': 1, 'PAPYRUS': 1, 'TEXTILE': 1}, [vp(7)], chain_from=('Temple',), counts=(1, 1, 1, 2, 2)),
    card('Senate', 3, 'BLUE', {'WOOD': 2, 'ORE': 1, 'STONE': 1}, [vp(6)], chain_from=('Library',), counts=(1, 1, 2, 2, 2)),
    card('Town Hall', 3, 'BLUE', {'ORE': 1, 'STONE': 2, 'GLASS': 1}, [vp(6)], counts=(1, 1, 2, 3, 3)),
    card('Academy', 3, 'GREEN', {'STONE': 3, 'GLASS': 1}, [science('COMPASS')], chain_from=('School',), counts=(1, 1, 1, 1, 2)),
    card('Lodge', 3, 'GREEN', {'CLAY': 2, 'PAPYRUS': 1, 'TEXTILE': 1}, [science('COMPASS')], chain_from=('Dispensary',), counts=(1, 1, 1, 2, 2)),
    card('Observatory', 3, 'GREEN', {'ORE': 2, 'GLASS': 1, 'TEXTILE': 1}, [science('GEAR')], chain_from=('Laboratory',), counts=(1, 1, 1, 1, 2)),
    card('Study', 3, 'GREEN', {'WOOD': 1, 'PAPYRUS': 1, 'TEXTILE': 1}, [science('GEAR')], chain_from=('School',), counts=(1, 1, 2, 2, 2)),
    card('University', 3, 'GREEN', {'WOOD': 2, 'GLASS': 1, 'PAPYRUS': 1}, [science('TABLET')], chain_from=('Library',), counts=(1, 2, 2, 2, 2)),
    card('Arsenal', 3, 'RED', {'WOOD': 2, 'ORE': 1, 'TEXTILE': 1}, [shields(3)], counts=(1, 2, 2, 2, 3)),
    card('Circus', 3, 'RED', {'ORE': 1, 'STONE': 3}, [shields(3)], chain_from=('Training Ground',), counts=(0, 1, 2, 3, 3)),
    card('Fortifications', 3, 'RED', {'ORE': 3, 'STONE': 1}, [shields(3)], chain_from=('Walls',), counts=(1, 1, 1, 1, 2)),
    card('Siege Workshop', 3, 'RED', {'WOOD': 1, 'CLAY': 3}, [shields(3)], chain_from=('Laboratory',), counts=(1, 1, 2, 2, 2)),
]

GUILD_CARDS = [  # Age III only; not in the count table (see build_deck)
    card('Builders Guild', 3, 'PURPLE', {'STONE': 2, 'CLAY': 2, 'GLASS': 1}, [per_card('WONDER_STAGE', ('SELF', 'LEFT', 'RIGHT'), vp=1)]),
    card('Craftsmens Guild', 3, 'PURPLE', {'ORE': 2, 'STONE': 2}, [per_card(('GREY',), ('LEFT', 'RIGHT'), vp=2)]),
    card('Magistrates Guild', 3, 'PURPLE', {'WOOD': 3, 'STONE': 1, 'TEXTILE': 1}, [per_card(('BLUE',), ('LEFT', 'RIGHT'), vp=1)]),
    card('Philosophers Guild', 3, 'PURPLE', {'CLAY': 3, 'PAPYRUS': 1, 'TEXTILE': 1}, [per_card(('GREEN',), ('LEFT', 'RIGHT'), vp=1)]),
    card('Scientists Guild', 3, 'PURPLE', {'WOOD': 2, 'ORE': 2, 'PAPYRUS': 1}, [science_any()]),
    card('Shipowners Guild', 3, 'PURPLE', {'WOOD': 3, 'GLASS': 1, 'PAPYRUS': 1}, [per_card(('BROWN', 'GREY', 'PURPLE'), ('SELF',), vp=1)]),
    card('Spies Guild', 3, 'PURPLE', {'CLAY': 3, 'GLASS': 1}, [per_card(('RED',), ('LEFT', 'RIGHT'), vp=1)]),
    card('Strategists Guild', 3, 'PURPLE', {'ORE': 2, 'STONE': 1, 'TEXTILE': 1}, [per_card('DEFEAT_TOKEN', ('LEFT', 'RIGHT'), vp=1)]),
    card('Traders Guild', 3, 'PURPLE', {'GLASS': 1, 'PAPYRUS': 1, 'TEXTILE': 1}, [per_card(('YELLOW',), ('LEFT', 'RIGHT'), vp=1)]),
    card('Workers Guild', 3, 'PURPLE', {'WOOD': 1, 'ORE': 2, 'STONE': 1, 'CLAY': 1}, [per_card(('BROWN',), ('LEFT', 'RIGHT'), vp=1)]),
]

WONDERS = [
    wonder('Alexandria', 'A', 'GLASS', [
        stage(1, {'STONE': 2}, [vp(3)]),
        stage(2, {'ORE': 2}, [choice('WOOD', 'STONE', 'ORE', 'CLAY', sellable=False)]),
        stage(3, {'GLASS': 2}, [vp(7)]),
    ]),
    wonder('Alexandria', 'B', 'GLASS', [
        stage(1, {'CLAY': 2}, [choice('WOOD', 'STONE', 'ORE', 'CLAY', sellable=False)]),
        stage(2, {'WOOD': 2}, [choice('GLASS', 'PAPYRUS', 'TEXTILE', sellable=False)]),
        stage(3, {'STONE': 3}, [vp(7)]),
    ]),
    wonder('Babylon', 'A', 'CLAY', [
        stage(1, {'CLAY': 2}, [vp(3)]),
        stage(2, {'WOOD': 3}, [science_any()]),
        stage(3, {'CLAY': 4}, [vp(7)]),
    ]),
    wonder('Babylon', 'B', 'CLAY', [
        stage(1, {'CLAY': 1, 'TEXTILE': 1}, [vp(3)]),
        stage(2, {'WOOD': 2, 'GLASS': 1}, [play_last_card()]),
        stage(3, {'CLAY': 3, 'PAPYRUS': 1}, [science_any()]),
    ]),
    wonder('Ephesos', 'A', 'PAPYRUS', [
        stage(1, {'STONE': 2}, [vp(3)]),
        stage(2, {'WOOD': 2}, [coins(9)]),
        stage(3, {'PAPYRUS': 2}, [vp(7)]),
    ]),
    wonder('Ephesos', 'B', 'PAPYRUS', [
        stage(1, {'STONE': 2}, [vp(2), coins(4)]),
        stage(2, {'WOOD': 2}, [vp(3), coins(4)]),
        stage(3, {'GLASS': 1, 'PAPYRUS': 1, 'TEXTILE': 1}, [vp(5), coins(4)]),
    ]),
    wonder('Gizah', 'A', 'STONE', [
        stage(1, {'STONE': 2}, [vp(3)]),
        stage(2, {'WOOD': 3}, [vp(5)]),
        stage(3, {'STONE': 4}, [vp(7)]),
    ]),
    wonder('Gizah', 'B', 'STONE', [
        stage(1, {'WOOD': 2}, [vp(3)]),
        stage(2, {'STONE': 3}, [vp(5)]),
        stage(3, {'CLAY': 3}, [vp(5)]),
        stage(4, {'STONE': 4, 'PAPYRUS': 1}, [vp(7)]),
    ]),
    wonder('Halikarnassus', 'A', 'TEXTILE', [
        stage(1, {'CLAY': 2}, [vp(3)]),
        stage(2, {'ORE': 3}, [build_from_discard()]),
        stage(3, {'TEXTILE': 2}, [vp(7)]),
    ]),
    wonder('Halikarnassus', 'B', 'TEXTILE', [
        stage(1, {'ORE': 2}, [vp(2), build_from_discard()]),
        stage(2, {'CLAY': 3}, [vp(1), build_from_discard()]),
        stage(3, {'GLASS': 1, 'PAPYRUS': 1, 'TEXTILE': 1}, [build_from_discard()]),
    ]),
    wonder('Olympia', 'A', 'WOOD', [
        stage(1, {'WOOD': 2}, [vp(3)]),
        stage(2, {'STONE': 2}, [free_build_each_age()]),
        stage(3, {'ORE': 2}, [vp(7)]),
    ]),
    wonder('Olympia', 'B', 'WOOD', [
        stage(1, {'WOOD': 2}, [discount(('WOOD', 'ORE', 'STONE', 'CLAY'), ('LEFT', 'RIGHT'))]),
        stage(2, {'STONE': 2}, [vp(5)]),
        stage(3, {'ORE': 2, 'TEXTILE': 1}, [copy_neighbor_guild()]),
    ]),
    wonder('Rhodos', 'A', 'ORE', [
        stage(1, {'WOOD': 2}, [vp(3)]),
        stage(2, {'CLAY': 3}, [shields(2)]),
        stage(3, {'ORE': 4}, [vp(7)]),
    ]),
    wonder('Rhodos', 'B', 'ORE', [
        stage(1, {'STONE': 3}, [vp(3), shields(1), coins(3)]),
        stage(2, {'ORE': 4}, [vp(4), shields(1), coins(4)]),
    ]),
]

ALL_CARDS = AGE_1_CARDS + AGE_2_CARDS + AGE_3_CARDS + GUILD_CARDS
