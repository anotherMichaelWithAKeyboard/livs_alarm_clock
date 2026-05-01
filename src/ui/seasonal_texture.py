"""
Faint seasonal background textures drawn programmatically.
"""
import pygame
import random
import math


class SeasonalTexture:

    def __init__(self, width, height, season_name, accent_color):
        self.W = width
        self.H = height
        self._surf = self._generate(season_name, accent_color)

    def _generate(self, season, accent):
        surf = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        r, g, b = accent
        color = (r, g, b, 28)   # very faint
        rng = random.Random(77)  # fixed seed → consistent layout across redraws

        dispatch = {
            'Autumn': self._leaves,
            'Winter': self._snowflakes,
            'Summer': self._beach,
            'Spring': self._flowers,
        }
        dispatch.get(season, lambda *_: None)(surf, color, rng)
        return surf

    # ── Autumn: scattered leaves ───────────────────────────────────────────────

    def _leaves(self, surf, color, rng):
        r, g, b, a = color
        vein_col = (min(255, r + 20), min(255, g + 20), min(255, b + 20), min(255, a + 20))

        for _ in range(32):
            cx  = rng.randint(0, self.W)
            cy  = rng.randint(0, self.H)
            L   = rng.randint(55, 95)              # leaf length
            W   = int(L * rng.uniform(0.36, 0.48)) # half-width at widest point
            ang = rng.uniform(0, math.pi * 2)

            # Leaf outline: elongated pointed oval
            pts = []
            for i in range(28):
                t  = i / 28 * math.pi * 2
                lx = math.cos(t) * L / 2
                ly = math.sin(t) * W
                rx = lx * math.cos(ang) - ly * math.sin(ang)
                ry = lx * math.sin(ang) + ly * math.cos(ang)
                pts.append((cx + rx, cy + ry))
            pygame.draw.polygon(surf, color, pts)

            # Midrib — base to tip
            tip_x  = cx + math.cos(ang) * L / 2
            tip_y  = cy + math.sin(ang) * L / 2
            base_x = cx - math.cos(ang) * L / 2
            base_y = cy - math.sin(ang) * L / 2
            pygame.draw.line(surf, vein_col, (int(base_x), int(base_y)), (int(tip_x), int(tip_y)), 1)

            # Side veins — pairs radiating perpendicular to midrib
            n_veins = rng.randint(5, 7)
            for i in range(1, n_veins):
                t  = i / n_veins
                mx = base_x + (tip_x - base_x) * t
                my = base_y + (tip_y - base_y) * t
                vl = W * math.sin(t * math.pi) * 0.88
                for sign in (1, -1):
                    vex = mx + math.cos(ang + math.pi / 2) * vl * sign
                    vey = my + math.sin(ang + math.pi / 2) * vl * sign
                    pygame.draw.line(surf, vein_col, (int(mx), int(my)), (int(vex), int(vey)), 1)

    # ── Winter: snowflakes ────────────────────────────────────────────────────

    def _snowflakes(self, surf, color, rng):
        for _ in range(65):
            x  = rng.randint(0, self.W)
            y  = rng.randint(0, self.H)
            sz = rng.randint(8, 20)

            for i in range(6):
                a  = i * math.pi / 3
                ex = x + math.cos(a) * sz
                ey = y + math.sin(a) * sz
                pygame.draw.line(surf, color, (int(x), int(y)), (int(ex), int(ey)), 1)

                # Two pairs of ticks along each arm
                for frac in (0.45, 0.72):
                    tx = x + math.cos(a) * sz * frac
                    ty = y + math.sin(a) * sz * frac
                    tl = sz * 0.28
                    for sign in (1, -1):
                        ta = a + sign * math.pi / 3
                        pygame.draw.line(surf, color,
                            (int(tx), int(ty)),
                            (int(tx + math.cos(ta) * tl), int(ty + math.sin(ta) * tl)), 1)

    # ── Summer: beach / sand ──────────────────────────────────────────────────

    def _beach(self, surf, color, rng):
        # Wavy sand-ripple lines across the lower two-thirds
        for i in range(22):
            y_base = int(self.H * 0.32) + i * int(self.H * 0.68 / 22)
            amp    = rng.randint(3, 8)
            wl     = rng.randint(80, 160)
            phase  = rng.uniform(0, math.pi * 2)
            pts    = [(x, y_base + int(amp * math.sin(x / wl * math.pi * 2 + phase)))
                      for x in range(0, self.W, 4)]
            if len(pts) >= 2:
                pygame.draw.lines(surf, color, False, pts, 1)

        # Sparse sunlight glints in upper third
        for _ in range(160):
            gx = rng.randint(0, self.W)
            gy = rng.randint(0, int(self.H * 0.38))
            pygame.draw.circle(surf, color, (gx, gy), 1)

    # ── Spring: small flowers ─────────────────────────────────────────────────

    def _flowers(self, surf, color, rng):
        for _ in range(60):
            x  = rng.randint(0, self.W)
            y  = rng.randint(0, self.H)
            sz = rng.randint(6, 16)

            # 5 petals
            for i in range(5):
                a  = i * math.pi * 2 / 5
                px = x + math.cos(a) * sz
                py = y + math.sin(a) * sz
                pygame.draw.circle(surf, color, (int(px), int(py)), max(2, sz // 2))

            # Centre dot
            pygame.draw.circle(surf, color, (int(x), int(y)), max(2, sz // 4))

    # ── Public API ────────────────────────────────────────────────────────────

    def draw(self, surface):
        surface.blit(self._surf, (0, 0))
