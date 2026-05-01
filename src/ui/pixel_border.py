"""
Seasonal mushroom people border — ported from HTML pixel-art source.
"""
import pygame
import random
import math
from typing import Dict, List

CHAR_SC  = 3   # screen pixels per sprite pixel (characters)
FLORA_SC = 2   # screen pixels per sprite pixel (flora)

SKIN  = '#f2c07a'
EYE   = '#1e0e04'
MOUTH = '#b05840'
OUTL  = '#2a1604'
WHITE = '#f8f4e8'
SHOE  = '#2a1604'
SG    = '#4a9030'
SD    = '#2a6018'


def _rgb(h: str):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _cp(R, r, G, g) -> Dict:
    return {'R': R, 'r': r, 'W': WHITE, 'S': SKIN, 's': '#cc9050',
            'e': EYE, 'm': MOUTH, 'G': G, 'g': g, 'B': OUTL, 'X': SHOE,
            'l': EYE, 'o': '#c05840', 'O': '#903020',
            'k': '#201008', 'Y': '#f8d820', 'C': '#f8d020', 'c': '#6a3a08'}


def _render(rows: List[str], pal: Dict, sc: int) -> pygame.Surface:
    w = max(len(r) for r in rows)
    h = len(rows)
    surf = pygame.Surface((w * sc, h * sc), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.' and ch in pal:
                pygame.draw.rect(surf, _rgb(pal[ch]), (x * sc, y * sc, sc, sc))
    return surf


DOT2 = 'RRWRRWRR'
DOT3 = 'RWRWRWRR'


def _cap(t: str, dot: str) -> List[str]:
    return {
        'A': ['..RRRR..', '.RRRRRR.', 'RRRRRRRR', dot, 'RRRRRRRR', '.rRRRRr.'],
        'B': ['.RRRRRR.', 'RRRRRRRR', dot, '.rRRRRr.'],
        'C': ['...RR...', '..RRRR..', '.RRRRRR.', 'RRRRRRRR', dot, 'RRRRRRRR', '.rRRRRr.'],
        'D': ['....R...', '..RRRR..', 'RRRRRRRR', dot, '.rRRRRr.'],
        'E': ['.R.RR.R.', 'RRRRRRRR', 'RRRRRRRR', dot, '.rRRRRr.'],
    }[t]


BODY = ['.BBBBBB.', '.SSSSSS.', '.SeSSes.', '.SSmSSS.', '.BBBBBB.', '.GGGGGG.', '..GGGG..']
LA   = ['..G..G..', '..X..X..']
LB   = ['.G....G.', '.X....X.']
LQ   = ['..GG.GG.', '...X.X..']
LC   = ['G......G', 'X......X']


def _char_frames(cap_t: str, dot: str, anim: str):
    cap = _cap(cap_t, dot)
    return (
        cap + BODY + LA,
        cap + BODY + (LQ if anim == 'bob' else LB),
        cap + BODY + LC,
    )


# ── Flora pixel rows ──────────────────────────────────────────────────────────
TULIP  = ['..PP..','.PPPP.','.PPPP.','PPPPPP','.pPPp.','..pp..','..GG..','..GG..','.gGG..','..GG..','..GG..','..GG..','..GG..','..GG..']
DAISY  = ['..W.W...','.WWYWWW.','WWYYYWWW','.WWYWWW.','..W.W...','...G....','...G....','..GGG...','...G....','...G....','...G....','...G....','...G....']
ROSE   = ['..PP..','.PPPP.','PPPPPP','PpPpPP','.PPPP.','..pp..','..GG..','..GG..','.gGG..','..GG..','..GG..','..GG..','..GG..']
SUNFL  = ['..YYY...','.YYYYYY.','YYYcccYY','YYYcccYY','YYYcccYY','.YYYYYY.','..YYY...','...GG...','...GG...','..GGG...','...GG...','...GG...','...GG...','...GG...']
POPPY  = ['..PP..','.PPPP.','PPPPPP','PPPkPP','PPkkPP','.PPkP.','..GG..','..GG..','..GG..','..GG..','..GG..','..GG..']
LAVEND = ['.LLll.','LLLlll','.LLll.','.LLll.','.LLll.','..GG..','..GG..','..GG..','.gG...','..GG..','..GG..','..GG..','..GG..','..GG..']
CHRY   = ['..PPPP..','.PPPPPP.','PPPPPPPP','PPPpPPPP','PPPPPPPP','.PPPPPP.','..PPPP..','...GG...','..GGG...','...GG...','...GG...','...GG...','...GG...']
MARI   = ['..PPP..','.PPPPP.','PPPPPPP','PPPpPPP','.PPPPP.','..PPP..','...GG..','...GG..','..gGG..','...GG..','...GG..','...GG..']
LEAF   = ['..LLLL..','.LLLLLL.','LLLLLLLL','LlLLLLlL','.LLLLLL.','..LLLL..','...LL...','...ll...']
HOLLY  = ['..GG.GG.','.GGGGGGG','GGGGGGGG','.GGGGGGG','..GG.GG.','...RRR..','...RRR..','....GG..','....GG..','....GG..','....GG..']
PINE   = ['....T....','...TTT...','..TTTTT..','.TTTTTTT.','TTTTTTTTT','....B....','....B....','....B....']
SNOWFL = ['....S....','..S.S.S..','...SSS...','SSSSSSSSS','...SSS...','..S.S.S..','....S....']
BLBELL = ['.BBBB.','BBBBBB','BbBBbB','.BBBB.','..BB..','..GG..','.GGG..','..GG..','..GG..','..GG..','..GG..','..GG..']
CHERRY = ['..PP..','.PPPP.','PPPPPP','PPpPPP','.PPPP.','..pp..','..GG..','..GG..','.gGG..','..GG..','..GG..','..GG..','..GG..','..GG..']

# ── Season data ───────────────────────────────────────────────────────────────
# chars: (name, R, r, G, g, anim, spd, delay, cap_t)
# flora: (name, rows, pal_dict, anim_cls, dur, delay)
_SPRING = {
    'chars': [
        ('Cherry Blossom','#f0a8c8','#b06888','#3a8830','#1a5818','walk',3.0,-0.0,'A'),
        ('Meadow',        '#70c860','#388820','#c080d0','#804898','bob', 0.9,-0.4,'A'),
        ('April Rain',    '#c090e0','#8050b8','#2888a8','#107888','wig', 0.55,-0.8,'A'),
        ('Dewdrop',       '#88e0b0','#408868','#e07878','#b03838','walk',2.8,-1.2,'A'),
        ('Breezy',        '#b0e0f0','#608898','#e09030','#a05010','bob', 1.0,-1.6,'A'),
        ('Chanterelle',   '#e8a020','#a06008','#3a7020','#1a4010','bob', 1.1,-2.0,'E'),
        ('Oyster',        '#d0c8b0','#909080','#607848','#304020','walk',3.2,-2.4,'B'),
        ('Fairy Ring',    '#c890f0','#9060c8','#30c090','#108060','wig', 0.52,-2.8,'D'),
        ('Spring Fawn',   '#c0a060','#806030','#70b040','#408010','bob', 1.3,-3.2,'C'),
    ],
    'flora': [
        ('Cherry Blossom', CHERRY, {'P':'#f8c0d8','p':'#e080a0','G':SG,'g':SD}, 'bop',    1.7,-0.0),
        ('Pink Tulip',     TULIP,  {'P':'#f090c8','p':'#c06888','G':SG,'g':SD}, 'sway',   2.2,-0.5),
        ('Daisy',          DAISY,  {'W':WHITE,'Y':'#f0d020','G':SG,'g':SD},     'bop',    1.5,-1.0),
        ('Lavender',       LAVEND, {'L':'#c090e8','l':'#9060c0','G':SG,'g':SD}, 'quiver', 1.1,-0.3),
        ('Pink Rose',      ROSE,   {'P':'#f080b0','p':'#b04870','G':SG,'g':SD}, 'sway',   2.6,-0.7),
    ],
}
_SUMMER = {
    'chars': [
        ('Sunbeam',  '#e8c020','#a07808','#2050c8','#0e30a0','walk',2.4,-0.0,'A'),
        ('Beach',    '#e06830','#a03810','#20a870','#107840','walk',2.7,-0.3,'A'),
        ('Tropical', '#e02020','#981010','#20c840','#108820','bob', 0.7,-0.6,'A'),
        ('Garden',   '#c020a0','#881060','#88c020','#508010','wig', 0.4,-0.9,'A'),
        ('Lagoon',   '#20b8e0','#0870a0','#e07030','#a03808','walk',2.2,-1.2,'A'),
        ("Caesar's", '#e07820','#a04808','#d0a010','#907008','walk',2.6,-1.5,'C'),
        ('Deathcap', '#a0c860','#608030','#201808','#100c04','wig', 0.45,-1.8,'B'),
        ('Coral',    '#f06060','#b03030','#2080b0','#104878','bob', 0.75,-2.1,'D'),
        ('Goldcap',  '#f0c030','#a08010','#306820','#184010','walk',2.9,-2.4,'C'),
    ],
    'flora': [
        ('Sunflower',    SUNFL, {'Y':'#f8d020','c':'#6a3a08','G':SG,'g':SD}, 'sway', 3.0,-0.0),
        ('Red Rose',     ROSE,  {'P':'#d02020','p':'#901010','G':SG,'g':SD}, 'sway', 2.4,-0.4),
        ('Poppy',        POPPY, {'P':'#d82020','k':'#201008','G':SG,'g':SD}, 'bop',  1.4,-0.8),
        ('Red Tulip',    TULIP, {'P':'#c82020','p':'#901010','G':SG,'g':SD}, 'sway', 2.0,-0.2),
        ('Yellow Daisy', DAISY, {'W':'#f8f0a0','Y':'#f0b020','G':SG,'g':SD},'bop',  1.6,-0.6),
    ],
}
_AUTUMN = {
    'chars': [
        ('Harvest','#e06020','#a02808','#8a2018','#5a0808','bob', 1.4,-0.0,'A'),
        ('Russet', '#9a3818','#6a1808','#c87820','#906008','walk',4.2,-0.5,'A'),
        ('Maple',  '#8a1010','#5a0808','#d0a020','#906808','bob', 1.6,-1.0,'A'),
        ('Amber',  '#c85020','#904010','#402890','#201860','walk',3.8,-1.5,'A'),
        ('Cider',  '#b84010','#802008','#6a4818','#3a2808','bob', 1.2,-2.0,'A'),
        ('Porcini','#8a5028','#5a2810','#d08020','#906010','bob', 1.5,-2.5,'C'),
        ('Inkcap', '#201008','#100804','#e0d090','#a09050','wig', 0.7,-3.0,'D'),
        ('Honey',  '#c09030','#806010','#6a3818','#3a1808','walk',4.5,-3.5,'B'),
        ('Witch',  '#601878','#380848','#180e0a','#080604','wig', 0.65,-4.0,'C'),
    ],
    'flora': [
        ('Chrysanth.',  CHRY, {'P':'#e07820','p':'#a04010','G':SG,'g':SD}, 'quiver',1.0,-0.0),
        ('Marigold',    MARI, {'P':'#f0a020','p':'#c06808','G':SG,'g':SD}, 'bop',   1.8,-0.3),
        ('Fallen Leaf', LEAF, {'L':'#e05818','l':'#a02808','G':SG,'g':SD}, 'sway',  3.5,-0.6),
        ('Orange Tulip',TULIP,{'P':'#e06820','p':'#a03808','G':SG,'g':SD}, 'sway',  2.8,-0.9),
        ('Amber Rose',  ROSE, {'P':'#d07020','p':'#904010','G':SG,'g':SD}, 'quiver',1.3,-0.2),
    ],
}
_WINTER = {
    'chars': [
        ('Frost',    '#e0e8f8','#a0b0c8','#1a2860','#0a1438','wig',  0.42,-0.0,'A'),
        ('Blizzard', '#78c0e0','#3888b0','#d0d8e8','#a0a8c0','bob',  1.6,-0.4,'A'),
        ('Cozy',     '#5828c0','#2810a0','#c02020','#880808','wig',  0.48,-0.8,'A'),
        ('Midnight', '#101840','#080e28','#78c0e0','#3888b0','walk', 3.6,-1.2,'A'),
        ('Icicle',   '#b0e0f8','#6098c0','#102848','#080e28','bob',  1.8,-1.6,'A'),
        ('Ghost',    '#d0e8f8','#90b0d0','#8090a8','#485868','bob',  2.8,-2.0,'C'),
        ('Velvet',   '#e07020','#a04010','#1a1018','#0a080e','bob',  1.3,-2.4,'B'),
        ('Parasol',  '#d8d0c0','#989080','#302820','#201808','walk', 4.0,-2.8,'B'),
        ('Sprite',   '#70c0e8','#3080b0','#c0c8d0','#808898','wig',  0.4,-3.2,'D'),
    ],
    'flora': [
        ('Holly',     HOLLY,  {'G':'#1a7820','R':'#d82020'},                           'quiver',1.4,-0.0),
        ('Pine Tree', PINE,   {'T':'#267828','B':'#7a4020'},                           'sway',  4.5,-0.5),
        ('Snowflake', SNOWFL, {'S':'#b8d8f8'},                                         'bop',   2.0,-1.0),
        ('Bluebell',  BLBELL, {'B':'#2858d8','b':'#0e30a0','G':SG,'g':SD},             'sway',  2.3,-0.3),
        ('Ice Tulip', TULIP,  {'P':'#a0c8e8','p':'#6090c0','G':'#3060a0','g':'#183868'},'sway', 2.6,-0.8),
    ],
}

SEASON_MAP = {'Spring': _SPRING, 'Summer': _SUMMER, 'Autumn': _AUTUMN, 'Winter': _WINTER}

# ── Royals ────────────────────────────────────────────────────────────────────
KING_ROWS = [
    '..C.C.C.','CCCCCCCC','..RRRR..',
    '.RRRRRR.','RRRRRRRR','RRWRRWRR','RRRRRRRR','.rRRRRr.',
    '.BBBBBB.','.SSSSSS.','.SeSSes.','.SSmSSS.','.BBBBBB.',
    'Z.PPPPPP','Z.PPPPPP','Z..P..P.','...X..X.',
]
KING_PAL = {'C':'#f8d020','R':'#a02010','r':'#700808','W':WHITE,'S':SKIN,'s':'#cc9050',
            'e':EYE,'m':MOUTH,'B':OUTL,'X':SHOE,'Z':'#c8a010','P':'#7028b0'}

QUEEN_ROWS = [
    '..C.C.C.','CCCCCCCC',
    '..PPPP..','.PPPPPP.','PPPPPPPP','PPwPPwPP','PPPPPPPP','.pPPPPp.',
    '.BBBBBB.','.SSSSSS.','.SeSSes.','.SSmSSS.','.BBBBBB.',
    '.DDDDDD.','DDDDDDDD','DDDDDDDD','.DDDDDD.','..D..D..','..X..X..',
]
QUEEN_PAL = {'C':'#f8d020','P':'#f080b8','p':'#b04880','w':WHITE,'S':SKIN,'s':'#cc9050',
             'e':EYE,'m':MOUTH,'B':OUTL,'X':SHOE,'D':'#e050a0'}


class PixelBorder:

    def __init__(self, screen_w, screen_h, theme=None):
        self.W = screen_w
        self.H = screen_h
        season_name = theme.get('name', 'Spring') if theme else 'Spring'
        season = SEASON_MAP.get(season_name, _SPRING)
        random.seed(42)
        self._sprites = self._build_border(season)

    # ── Sprite builders ───────────────────────────────────────────────────────

    def _make_char(self, char_data, idx):
        _, R, r, G, g, anim, _spd, _delay, cap_t = char_data
        pal = _cp(R, r, G, g)
        dot = DOT2 if idx % 2 == 0 else DOT3
        fA, fB, _fC = _char_frames(cap_t, dot, anim)
        return [_render(fA, pal, CHAR_SC), _render(fB, pal, CHAR_SC)], anim

    def _make_flora(self, flora_data):
        _, rows, pal, anim_cls, _dur, _delay = flora_data
        return _render(rows, pal, FLORA_SC), 'flora_' + anim_cls

    # ── Border layout ─────────────────────────────────────────────────────────

    def _build_border(self, season):
        sprites = []
        char_pool  = [self._make_char(c, i)  for i, c in enumerate(season['chars'])]
        flora_pool = [self._make_flora(f)     for f in season['flora']]

        king_s  = _render(KING_ROWS,  KING_PAL,  CHAR_SC)
        queen_s = _render(QUEEN_ROWS, QUEEN_PAL, CHAR_SC)
        royals  = [([king_s, king_s], 'bob'), ([queen_s, queen_s], 'wig')]

        ci = [0]

        def pick_char():
            if random.random() < 0.02:
                return random.choice(royals)
            entry = char_pool[ci[0] % len(char_pool)]
            ci[0] += 1
            return entry

        def pick_flora():
            return random.choice(flora_pool)

        def add(surfs, anim, x, y):
            sprites.append({
                'frames': surfs, 'anim': anim,
                'x': x, 'y': y,
                'phase': random.uniform(0, math.pi * 2),
            })

        # Top border — characters + flora, staggered vertically
        x = 8
        top_extent = 0   # track bottommost pixel used
        while x < self.W - 8:
            y_off = random.randint(0, 13)
            if random.random() < 0.55:
                surfs, anim = pick_char()
                if x + surfs[0].get_width() > self.W:
                    break
                y = 2 + y_off
                add(surfs, anim, x, y)
                top_extent = max(top_extent, y + surfs[0].get_height())
                x += surfs[0].get_width() + random.randint(8, 26)
            else:
                fs, fa = pick_flora()
                if x + fs.get_width() > self.W:
                    break
                y = 2 + y_off
                add([fs], fa, x, y)
                top_extent = max(top_extent, y + fs.get_height())
                x += fs.get_width() + random.randint(6, 16)

        # Bottom border — characters + flora, staggered vertically
        x = 8
        bot_extent = self.H   # track topmost pixel used
        while x < self.W - 8:
            y_off = random.randint(0, 13)
            if random.random() < 0.55:
                surfs, anim = pick_char()
                if x + surfs[0].get_width() > self.W:
                    break
                h = surfs[0].get_height()
                y = self.H - h - 2 - y_off
                add(surfs, anim, x, y)
                bot_extent = min(bot_extent, y)
                x += surfs[0].get_width() + random.randint(8, 26)
            else:
                fs, fa = pick_flora()
                if x + fs.get_width() > self.W:
                    break
                y = self.H - fs.get_height() - 2 - y_off
                add([fs], fa, x, y)
                bot_extent = min(bot_extent, y)
                x += fs.get_width() + random.randint(6, 16)

        # Side borders start/end just outside the top/bottom sprite extents
        side_top = top_extent + 6
        side_bot = bot_extent - 6

        # Left border — flora only
        y = side_top
        while y < side_bot:
            fs, fa = pick_flora()
            add([fs], fa, 4, y)
            y += fs.get_height() + random.randint(8, 22)

        # Right border — flora only
        y = side_top
        while y < side_bot:
            fs, fa = pick_flora()
            add([fs], fa, self.W - fs.get_width() - 4, y)
            y += fs.get_height() + random.randint(8, 22)

        return sprites

    # ── Public API ────────────────────────────────────────────────────────────

    def draw(self, surface):
        self.draw_animated(surface, 0)

    def draw_animated(self, surface, frame_count):
        t  = pygame.time.get_ticks() / 1000.0
        gf = (frame_count // 6) % 2   # toggle every ~200ms at 30fps

        for sp in self._sprites:
            surfs, anim = sp['frames'], sp['anim']
            x, y, ph   = sp['x'], sp['y'], sp['phase']

            surf = surfs[gf % len(surfs)]

            dy = 0
            if anim in ('bob', 'float'):
                dy = int(math.sin(t * math.pi + ph) * 3)
            elif anim == 'wig':
                dy = int(math.sin(t * math.pi * 1.4 + ph) * 2)
            elif anim.startswith('flora_'):
                sub = anim[6:]
                if sub == 'bop':
                    dy = int(math.sin(t * math.pi * 1.25 + ph) * 2)
                elif sub == 'quiver':
                    dy = int(math.sin(t * math.pi * 1.67 + ph) * 1)

            surface.blit(surf, (x, y + dy))
