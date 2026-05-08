"""
Background tile manager — renders pixel-art tiled backgrounds.
Tile data ported from Mushroom Background Tiles.html.
"""
import pygame


def _rgb(h):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _render_tile(rows, pal, scale):
    w = max(len(r) for r in rows)
    h = len(rows)
    surf = pygame.Surface((w * scale, h * scale))
    surf.fill((0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in pal:
                pygame.draw.rect(surf, _rgb(pal[ch]), (x * scale, y * scale, scale, scale))
    return surf


# ── Tile pixel data (16×16, seamlessly tileable) ─────────────────────────────

T_SPRING_A = [
    'gggggggggggggggg', 'ggGgggggggggGggg', 'gGFGggggggGFGggg', 'ggGgggFggggGgggF',
    'gggggFFFggggggFF', 'ggggggFggggggggF', 'ggggggggGgggggGg', 'gggggggGFGgggGFG',
    'ggGggggGgGggggGg', 'gGFGggggggggFggg', 'ggGgggggggFFFggg', 'gggggggggggFgggg',
    'ggggGgggggggggGg', 'gggGFGggggggGFGg', 'ggggGggggggggGgg', 'gggggggggggggggg',
]
T_SPRING_B = [
    'gggggGgggggggggg', 'ggggGFGgggggGggg', 'ggGggGggggggFggG', 'gGFGgggggFggggGF',
    'ggGgggggFFFggggG', 'gggggggggFggggGg', 'ggFggggggggggGFG', 'gFFFgggggggggGgg',
    'ggFggggGggggggGg', 'gggggggGFGgggFGg', 'gggggggGgGgggggg', 'ggGggggggggggGgg',
    'gGFGggggGggggFGg', 'ggGggggGFGggggGg', 'gggFggggGgggggGg', 'ggFFFggggggggFgg',
]
T_SUMMER_A = [
    'sssssssssspsssss', 'sssspssssssssssp', 'sssssssssssssss.', 'sspsssssssssssss',
    'ssssssssscsssspp', 'sssssssssscssspS', 'sssssspssssssssS', 'sssssssssssssspp',
    'spssssssssssssss', 'sssssssssssspsss', 'ssssspsssssssssp', 'sssssssscssssss.',
    'ssssssssscsssscS', 'sspssssssssssccS', 'ssssssssssssssss', 'sssssspsssspssss',
]
T_SUMMER_B = [
    'ssssssssssssssss', 'spsssssssspsssss', 'ssssssssssssssss', 'ssssssssscsssspp',
    'sspssssssccsssss', 'ssssssssssssssss', 'sssssspssssssspS', 'ssssssssssssssss',
    'spssssssssscsspp', 'ssssssssssscssss', 'sssssssssssssss.', 'ssssspsssssssssp',
    'ssssssssspsssscS', 'ssssssssssssscss', 'sssspssssssssscS', 'ssssssssssssssss',
]
T_AUTUMN_A = [
    'dddddLLddddddddd', 'dddLLLLLddddLLdd', 'ddLLlLLLddLLlLLd', 'dddLLLddddLLLLLd',
    'ddddLddddddLLddd', 'ddddddddddLLdddd', 'dddLLdddddddLLdd', 'ddLLLLddddddLlLd',
    'ddLlLLdddddLLLdd', 'dddLLddddddLLddd', 'ddddddLLddddddLL', 'dddddLLLLddddLLL',
    'ddddLLlLLdddLLlL', 'dddddLLLddddLLLL', 'ddddddLddddddLdd', 'dddddddddddddddd',
]
T_AUTUMN_B = [
    'ddddddddLLddddLL', 'dddLLddLlLLddLLL', 'ddLlLLdLLLddddLL', 'ddLLLLdddLddddLd',
    'dddLLdddddddddDd', 'ddddDdLLLddddDdd', 'dddDDLlLLddDDddd', 'ddDDdLLLddDDdddd',
    'ddDdddLddDdddLLd', 'dDdddddddddddLlL', 'dddLLddddddLLLLL', 'ddLLLLddddddLLLd',
    'ddLlLLdddDddddDd', 'dddLLdddDDddddDD', 'ddddddddDDddddDD', 'ddddddddDdddddDd',
]
T_WINTER_A = [
    'wwwwwwwwwwwwwwww', 'wwwSwwwwwwwwSwww', 'wSSSSwwwwwwSSSSw', 'wwSwSwwwwwwSwSww',
    'wwwwwwwSwwwwwwww', 'wwwwwSSSSwwwwSww', 'wwwwwwSwSwwwSSSS', 'wwwwwwwwwwwwSwSw',
    'wwwSwwwwwwwwwwww', 'wwSSSSwwwwSwwwww', 'wwwSwSwwSSSSwwww', 'wwwwwwwwSwSwwwww',
    'wwwwwwSwwwwwwwwS', 'wwwwSSSSwwwwwSSS', 'wwwwwSwSwwwwwwSw', 'wwwwwwwwwwwwwwww',
]
T_WINTER_B = [
    'wwwwwSwwwwwwwwww', 'wwwwSSSSwwwSwwww', 'wwwwwSwSwSSSSwww', 'wwwwwwwwwSwSwwww',
    'wwSwwwwwwwwwwSww', 'SSSSwwwwwSwSSSSw', 'wSwSwwwwSSSSwSwS', 'wwwwwwwwwSwSwwww',
    'wwwwwwSwwwwwwwww', 'wwwwSSSSwwwwwSww', 'wwwwwSwSwwwSSSSw', 'wwwwwwwwwwwwSwSw',
    'wSwwwwwSwwwwwwww', 'SSSSwSSSSwwwwSww', 'wSwSwwSwSwwwSSSS', 'wwwwwwwwwwwwwSwS',
]
T_FOREST = [
    'mmmmmmmmmmmmmmmm', 'mMmmmmmmmmmmmMmm', 'mmmmmmmRRmmmmmmm', 'mmmMmmRRRRmmmMmm',
    'mmmmmmrRRrmmmmmm', 'mmmmmmmSSmmmmmmM', 'mMmmmmmmmmmmmmmm', 'mmmmmRRmmmmmmmmm',
    'mmmmRRRRmmmMmmmm', 'mmmmrRRrmmmmmmmm', 'mmmmmSSmmmmmmRRm', 'mmMmmmmmmmmmRRRR',
    'mmmmmmmmmmmmrRRr', 'mmmmmmmMmmmmmSSm', 'mmmmmmmmmmmmmmmm', 'mmMmmmmmmmmmmMmm',
]
T_STONE = [
    'GGGGGGGGGGGGGGGG', 'GsssssGsssssGsss', 'GsdddsGsdddsGsdd', 'GsdddsGsdddsGsdd',
    'GsdddsGsdddsGsdd', 'GssssGGGsssGsdds', 'GGGGGsdddssssGGG', 'sssssGsdddsGssss',
    'sdddsGsdddsGsddd', 'sdddsGGsssGGsddd', 'sdddsGsssssGsddd', 'sssssGsdddsGssss',
    'GGGGGsdddsGGGGGG', 'GsssssdddsGsssss', 'GsdddsssssGsdddd', 'GsdddsGGGGGsdddd',
]
T_SKY = [
    'NNNNNNNNNNNNNNNN', 'NNNNSNNNNNNNNNNN', 'NNNNNNNNNNSNNNNN', 'NNSNNNNNNNNNNNNN',
    'NNNNNNNNNSNNNNSN', 'NNNNNNSNNNNNNNNN', 'NSNNNNNNNNNNSNNN', 'NNNNNNNNNNNNNNNN',
    'NNNNSNNNNSNNNNNN', 'NNNNNNNNNNNNNNSN', 'NNNSNNNNNNNNNNNN', 'NNNNNNNNSNNNNNNN',
    'NNNNNNSNNNNNSNNN', 'NSNNNNNNNNNNNNNN', 'NNNNNNNNSNNNNNNN', 'NNNNNSNNNNNNSNNN',
]
T_WOOD = [
    'wwwwwwwwwwwwwwww', 'wPPPPPPPPPPPPPPw', 'wPwwwwwwwwwwwwPw', 'wPwppppPPPpppwPw',
    'wPwwwwwwwwwwwwPw', 'wPPPPPPPPPPPPPPw', 'wwwwwwwwwwwwwwww', 'PPPPPPPPPPPPPPPP',
    'PwwwwwwwwwwwwwwP', 'PwPpppPwwppPwwwP', 'PwwwwwwwwwwwwwwP', 'PPPPPPPPPPPPPPPP',
    'wwwwwwwwwwwwwwww', 'wPPPPPPPPPPPPPPw', 'wPwwppPwppPwwwPw', 'wPPPPPPPPPPPPPPw',
]

# ── Available backgrounds ─────────────────────────────────────────────────────
# (name, tile_rows, palette)
BACKGROUNDS = [
    ('None',          None,       None),
    ('Pink Meadow',   T_SPRING_A, {'g': '#a0d480', 'G': '#80c060', 'F': '#f088b8'}),
    ('Wild Meadow',   T_SPRING_B, {'g': '#a0d480', 'G': '#88c870', 'F': '#e878a8'}),
    ('Sunny Meadow',  T_SPRING_A, {'g': '#b8e090', 'G': '#80c060', 'F': '#f0c050'}),
    ('Beach Sand',    T_SUMMER_A, {'s': '#f0d890', 'p': '#c89860', 'S': '#f898a0', 'c': '#a8b8c8', '.': '#d8c880'}),
    ('Pebble Sand',   T_SUMMER_B, {'s': '#f0d890', 'p': '#c89860', 'S': '#e8a890', 'c': '#909caa', '.': '#d8c880'}),
    ('Pale Sand',     T_SUMMER_A, {'s': '#f8e8a8', 'p': '#d0a070', 'S': '#f8c890', 'c': '#b0c0d0', '.': '#e8d898'}),
    ('Brown Leaves',  T_AUTUMN_A, {'d': '#5a3818', 'L': '#c85020', 'l': '#883010', 'D': '#a04018'}),
    ('Orange Leaves', T_AUTUMN_B, {'d': '#5a3818', 'L': '#e07820', 'l': '#a85008', 'D': '#a85018'}),
    ('Deep Forest',   T_AUTUMN_A, {'d': '#4a2810', 'L': '#a83020', 'l': '#601808', 'D': '#883808'}),
    ('Snowflakes',    T_WINTER_A, {'w': '#d8e0f0', 'S': '#f8f8ff'}),
    ('Heavy Snow',    T_WINTER_B, {'w': '#c8d8ec', 'S': '#ffffff'}),
    ('Frozen Pond',   T_WINTER_A, {'w': '#e0e8f8', 'S': '#a0c0e8'}),
    ('Mushroom Floor',T_FOREST,   {'m': '#3a6020', 'M': '#205010', 'R': '#c83020', 'r': '#882010', 'S': '#f0e0b0'}),
    ('Mossy Stone',   T_STONE,    {'G': '#3a8020', 's': '#888070', 'd': '#5a5040'}),
    ('Starry Sky',    T_SKY,      {'N': '#0a0a30', 'S': '#f8f0a0'}),
    ('Wood Planks',   T_WOOD,     {'w': '#8a5828', 'P': '#5a3010', 'p': '#a07040'}),
]

_TILE_SCALE = 4  # 16×16 tile → 64×64 px rendered tile


class BackgroundManager:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._surf_cache = {}
        self._thumb_cache = {}

    def get_names(self):
        return [name for name, _, _ in BACKGROUNDS]

    def get_surface(self, name):
        if not name or name == 'None':
            return None
        if name in self._surf_cache:
            return self._surf_cache[name]
        entry = next((b for b in BACKGROUNDS if b[0] == name), None)
        if entry is None:
            return None
        _, rows, pal = entry
        tile = _render_tile(rows, pal, _TILE_SCALE)
        tw, th = tile.get_size()
        surf = pygame.Surface((self.width, self.height))
        for ty in range(0, self.height, th):
            for tx in range(0, self.width, tw):
                surf.blit(tile, (tx, ty))
        self._surf_cache[name] = surf
        return surf

    def get_thumbnail(self, name, size):
        key = (name, size)
        if key in self._thumb_cache:
            return self._thumb_cache[key]
        if not name or name == 'None':
            return None
        entry = next((b for b in BACKGROUNDS if b[0] == name), None)
        if entry is None:
            return None
        _, rows, pal = entry
        tile = _render_tile(rows, pal, _TILE_SCALE)
        tw, th = tile.get_size()
        w, h = size
        thumb = pygame.Surface(size)
        for ty in range(0, h, th):
            for tx in range(0, w, tw):
                thumb.blit(tile, (tx, ty))
        self._thumb_cache[key] = thumb
        return thumb
