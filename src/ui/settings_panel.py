"""
Settings panel — slides in from the right via a right-to-left swipe.
"""
import pygame
from ui.background_manager import BackgroundManager, BACKGROUNDS

# ── Palette ───────────────────────────────────────────────────────────────────
_BG       = (14,  11,   8)
_HEADER   = (28,  20,  10)
_HDR_HI   = (52,  36,  16)
_HDR_SHD  = ( 8,   5,   2)
_ACCENT   = (210, 160,  50)
_SEL      = (240, 200,  80)
_SEL_GLOW = (255, 230, 120)
_TEXT     = (210, 195, 165)
_DIM      = (100,  82,  48)
_BORDER   = ( 44,  32,  14)
_CELL_BG  = ( 20,  15,   9)
_GREEN    = ( 42,  88,  38)
_GREEN_HI = ( 74, 140,  60)
_TAB      = ( 80, 140,  60)


def _draw_mushroom_ornament(surface, cx, cy, col_cap, col_stem):
    pygame.draw.ellipse(surface, col_cap,       (cx - 10, cy - 12, 20, 14))
    pygame.draw.rect(surface,   (210, 195, 165), (cx - 5,  cy - 10,  3,  3))
    pygame.draw.rect(surface,   (210, 195, 165), (cx + 2,  cy -  8,  3,  3))
    pygame.draw.rect(surface,   col_stem,        (cx - 3,  cy +  2,  6,  6))


class SettingsPanel:

    def __init__(self, width, height, config, on_background_change):
        self.width  = width
        self.height = height
        self.config = config
        self.on_background_change = on_background_change

        self.bg_manager  = BackgroundManager(width, height)
        self.selected_bg = config.get('display.background', 'None')
        self._bg_names   = self.bg_manager.get_names()

        self._title_font = pygame.font.Font(None, 48)
        self._label_font = pygame.font.Font(None, 26)
        self._small_font = pygame.font.Font(None, 22)

        self._cols   = 3
        self._thumb_w = 108
        self._thumb_h = 78
        self._cell_w  = (width - 32) // self._cols
        self._cell_h  = self._thumb_h + 38
        self._hdr_h   = 128

        rows = (len(self._bg_names) + self._cols - 1) // self._cols
        self._content_h = self._hdr_h + rows * self._cell_h + 20

        self._scroll_y = 0
        self._thumbs   = {}

    # ── Thumbnails ────────────────────────────────────────────────────────────

    def _get_thumb(self, name):
        if name not in self._thumbs:
            size = (self._thumb_w, self._thumb_h)
            if name == 'None':
                surf = pygame.Surface(size)
                surf.fill((22, 18, 10))
                pygame.draw.line(surf, (70, 56, 30), (0, 0),          (size[0]-1, size[1]-1), 2)
                pygame.draw.line(surf, (70, 56, 30), (size[0]-1, 0),  (0, size[1]-1),         2)
                self._thumbs[name] = surf
            else:
                self._thumbs[name] = self.bg_manager.get_thumbnail(name, size)
        return self._thumbs[name]

    # ── Events ────────────────────────────────────────────────────────────────

    def handle_scroll(self, delta):
        max_scroll = max(0, self._content_h - self.height)
        self._scroll_y = max(0, min(self._scroll_y + delta, max_scroll))

    def handle_tap(self, pos):
        x, y = pos
        adj_y = y + self._scroll_y - self._hdr_h
        if adj_y < 0:
            return
        col = (x - 16) // self._cell_w
        row = adj_y // self._cell_h
        idx = row * self._cols + col
        if 0 <= col < self._cols and 0 <= idx < len(self._bg_names):
            name = self._bg_names[idx]
            self.selected_bg = name
            self.config.set('display.background', name)
            self.on_background_change(name)

    # ── Drawing helpers ───────────────────────────────────────────────────────

    def _draw_header_pattern(self, surface):
        for px in range(4, self.width, 8):
            for py in range(4, 96, 8):
                pygame.draw.rect(surface, _HDR_SHD, (px, py, 2, 2))

    def _draw_section_label(self, surface, text, x, y):
        label_surf = self._label_font.render(text.upper(), True, _GREEN_HI)
        lw, lh = label_surf.get_width(), label_surf.get_height()
        pad_x, pad_y = 10, 4
        tag_rect = pygame.Rect(x - pad_x, y - pad_y, lw + pad_x * 2, lh + pad_y * 2)
        pygame.draw.rect(surface, _GREEN, tag_rect)
        pygame.draw.line(surface, _GREEN_HI,
                         (tag_rect.x, tag_rect.y),      (tag_rect.right, tag_rect.y),      1)
        pygame.draw.line(surface, (20, 44, 16),
                         (tag_rect.x, tag_rect.bottom), (tag_rect.right, tag_rect.bottom), 1)
        surface.blit(label_surf, (x, y))

    def _draw_swipe_tab(self, surface):
        W, H = self.width, self.height
        my   = H // 2
        w    = 10
        h    = 80
        points = [
            (W - 1,         my - h // 2),
            (W - 1 - w,     my - h // 4),
            (W - 1 - w - 6, my),
            (W - 1 - w,     my + h // 4),
            (W - 1,         my + h // 2),
        ]
        pygame.draw.polygon(surface, _TAB,      points)
        pygame.draw.polygon(surface, _GREEN_HI, points, 1)

    # ── Drawing ───────────────────────────────────────────────────────────────

    def draw(self, surface):
        surface.fill(_BG)

        # ── Header — carved wood sign ──
        pygame.draw.rect(surface, _HEADER, (0, 0, self.width, 96))
        self._draw_header_pattern(surface)
        pygame.draw.line(surface, _HDR_HI,  (0,  3), (self.width,  3), 2)
        pygame.draw.line(surface, _HDR_SHD, (0, 93), (self.width, 93), 3)
        pygame.draw.line(surface, _BORDER,  (0, 96), (self.width, 96), 1)

        title = self._title_font.render('Settings', True, _ACCENT)
        surface.blit(title, title.get_rect(center=(self.width // 2, 48)))

        _draw_mushroom_ornament(surface, 22,              48, (160,  40, 20), (220, 190, 140))
        _draw_mushroom_ornament(surface, self.width - 22, 48, (180, 120, 20), (220, 190, 140))

        # ── Section label ──
        if 96 - self._scroll_y > 60:
            self._draw_section_label(surface, 'Background', 16, 100 - self._scroll_y)

        # ── Background grid ──
        for i, name in enumerate(self._bg_names):
            col = i % self._cols
            row = i // self._cols
            cx  = 16 + col * self._cell_w
            cy  = self._hdr_h + row * self._cell_h - self._scroll_y

            if cy + self._cell_h < 0 or cy > self.height:
                continue

            tx = cx + (self._cell_w - self._thumb_w) // 2
            ty = cy + 6

            # Cell inset background
            pygame.draw.rect(surface, _CELL_BG,
                             pygame.Rect(tx - 4, ty - 4, self._thumb_w + 8, self._thumb_h + 8))

            thumb = self._get_thumb(name)
            if thumb:
                surface.blit(thumb, (tx, ty))

            frame = pygame.Rect(tx - 4, ty - 4, self._thumb_w + 8, self._thumb_h + 8)

            if name == self.selected_bg:
                # Three-ring glow
                pygame.draw.rect(surface, _SEL,      frame.inflate(8, 8), 2)
                pygame.draw.rect(surface, _SEL,      frame.inflate(4, 4), 2)
                pygame.draw.rect(surface, _SEL_GLOW, frame, 3)
                pygame.draw.line(surface, _SEL_GLOW,
                                 (frame.x, frame.y), (frame.right, frame.y), 1)
                pygame.draw.line(surface, _SEL_GLOW,
                                 (frame.x, frame.y), (frame.x, frame.bottom), 1)
                # Checkmark badge — bottom-right corner
                bx, by = frame.right - 2, frame.bottom - 2
                badge_r = pygame.Rect(bx - 16, by - 16, 16, 16)
                pygame.draw.rect(surface, _SEL_GLOW, badge_r)
                pygame.draw.rect(surface, _HDR_SHD,  badge_r, 1)
                pygame.draw.line(surface, _HDR_SHD,
                                 (badge_r.x + 3,       badge_r.centery),
                                 (badge_r.centerx - 1, badge_r.bottom - 4), 2)
                pygame.draw.line(surface, _HDR_SHD,
                                 (badge_r.centerx - 1, badge_r.bottom - 4),
                                 (badge_r.right - 3,   badge_r.y + 4), 2)
            else:
                # Chunky frame with bevel
                pygame.draw.rect(surface, _BORDER, frame, 3)
                pygame.draw.line(surface, _HDR_HI,
                                 (frame.x, frame.y),      (frame.right, frame.y),      1)
                pygame.draw.line(surface, _HDR_HI,
                                 (frame.x, frame.y),      (frame.x, frame.bottom),     1)
                pygame.draw.line(surface, _HDR_SHD,
                                 (frame.x, frame.bottom), (frame.right, frame.bottom), 1)
                pygame.draw.line(surface, _HDR_SHD,
                                 (frame.right, frame.y),  (frame.right, frame.bottom), 1)

            # Name label
            name_surf = self._small_font.render(
                name, True, _SEL if name == self.selected_bg else _DIM)
            nr = name_surf.get_rect(centerx=cx + self._cell_w // 2,
                                    top=ty + self._thumb_h + 10)
            if nr.right > self.width - 4:
                nr.right = self.width - 4
            surface.blit(name_surf, nr)

        # ── Swipe-close tab ──
        self._draw_swipe_tab(surface)
