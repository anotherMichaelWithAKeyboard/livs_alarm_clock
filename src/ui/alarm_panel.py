"""
Multi-step alarm setup panel — slides in from the left via swipe gesture.
Steps: 0 Destination  1 Arrival & Mode  2 Route  3 Preparation  4 Confirm
"""
import threading
import pygame
from pathlib import Path
from datetime import datetime, timedelta

from services.alarm_logic import AlarmCalculator
from services.nominatim import NominatimGeocoder

BG        = (12,  18,  22)
SURFACE   = (20,  30,  36)
SURFACE_B = (28,  42,  50)
ITEM_BG   = (24,  36,  44)
ITEM_SEL  = (30,  55,  65)
TEXT      = (210, 225, 215)
MUTED     = (100, 130, 118)
DIVIDER   = (30,  46,  54)
ACCENT    = ( 80, 185, 160)
WARN      = (240, 195,  60)

STEP_COLORS = [
    ( 74, 180, 100),   # Step 0 Destination  — Forest Green
    ( 80, 185, 160),   # Step 1 Arrival      — Glowshroom Teal
    (120, 130, 210),   # Step 2 Route        — Twilight Indigo
    (200, 140,  80),   # Step 3 Preparation  — Warm Ember
    (220, 190,  80),   # Step 4 Confirm      — Firefly Gold
]

KB_BG         = (  8,  12,  15)
KB_KEY        = ( 28,  42,  52)
KB_HI         = ( 42,  62,  76)
KB_SHD        = ( 10,  16,  20)
BTN_GREEN     = ( 40, 110,  75)
BTN_GREEN_HI  = ( 60, 150, 100)
BTN_GREEN_SHD = ( 20,  60,  40)
BTN_GRAY      = ( 38,  52,  60)
BTN_GRAY_HI   = ( 58,  76,  88)
BTN_GRAY_SHD  = ( 16,  24,  30)
SUG_BG        = ( 15,  22,  28)
SUG_CHIP      = ( 30,  50,  60)

HEADER_H   = 64
FOOTER_H   = 64
ITEM_H     = 68
ITEM_GAP   = 6
SUG_H      = 44
STEP_NAMES = ["Destination", "Arrival & Mode", "Route", "Preparation", "Confirm"]
N_STEPS    = len(STEP_NAMES)

_DEJAVU_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_KB_ROWS = [
    list("1234567890"),
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM") + ["BKSP"],
    ["CANCEL", ",", ".", "SPACE", "DONE"],
]
_KB_BOT_WIDTHS = [2, 1, 1, 4, 2]

_DEBOUNCE_MS = 600


# ── Module-level drawing helpers ──────────────────────────────────────────────

def _darken(color, amount):
    return tuple(max(0, c - amount) for c in color)


def _ribbon_dim(color):
    return tuple(max(0, c // 3) for c in color)


def _draw_star(surf, cx, cy, r_outer, r_inner, color, width=0):
    import math
    points = []
    for i in range(12):
        angle = math.pi / 6 * i - math.pi / 2
        r = r_outer if i % 2 == 0 else r_inner
        points.append((int(cx + r * math.cos(angle)), int(cy + r * math.sin(angle))))
    pygame.draw.polygon(surf, color, points, width)


def _draw_icon_car(surf, rect, color):
    cx, cy = rect.centerx, rect.centery
    pygame.draw.polygon(surf, color, [
        (cx - 18, cy + 6), (cx + 18, cy + 6), (cx + 18, cy - 2),
        (cx + 10, cy - 10), (cx - 10, cy - 10), (cx - 18, cy - 2),
    ])
    pygame.draw.polygon(surf, _darken(color, 40), [
        (cx - 8, cy - 8), (cx + 8, cy - 8), (cx + 12, cy - 3), (cx - 12, cy - 3),
    ])
    for wx in (cx - 10, cx + 10):
        pygame.draw.circle(surf, KB_SHD, (wx, cy + 7), 5)
        pygame.draw.circle(surf, MUTED,  (wx, cy + 7), 3)


def _draw_icon_bus(surf, rect, color):
    cx, cy = rect.centerx, rect.centery
    pygame.draw.rect(surf, color, pygame.Rect(cx - 14, cy - 12, 28, 20), border_radius=3)
    for wx in (cx - 10, cx - 2, cx + 6):
        pygame.draw.rect(surf, _darken(color, 50), (wx, cy - 9, 5, 7))
    for wx in (cx - 8, cx + 8):
        pygame.draw.circle(surf, KB_SHD, (wx, cy + 10), 4)
        pygame.draw.circle(surf, MUTED,  (wx, cy + 10), 2)
    pygame.draw.rect(surf, _darken(color, 30), (cx - 12, cy - 14, 24, 4))


def _draw_icon_cycle(surf, rect, color):
    cx, cy = rect.centerx, rect.centery
    pygame.draw.circle(surf, color, (cx - 11, cy + 4), 9, 2)
    pygame.draw.circle(surf, color, (cx + 11, cy + 4), 9, 2)
    pygame.draw.line(surf, color, (cx - 11, cy + 4), (cx,      cy - 8), 2)
    pygame.draw.line(surf, color, (cx + 11, cy + 4), (cx,      cy - 8), 2)
    pygame.draw.line(surf, color, (cx - 11, cy + 4), (cx + 11, cy + 4), 2)
    pygame.draw.line(surf, color, (cx - 4,  cy - 8), (cx + 4,  cy - 8), 2)
    pygame.draw.line(surf, color, (cx + 9,  cy - 4), (cx + 14, cy - 6), 2)
_MIN_QUERY   = 3

_ROUTE_TYPES = [(0, "Train"), (1, "Tram"), (2, "Bus")]


class AlarmPanel:

    def __init__(self, screen_w, screen_h, alarm_manager, alarm_config, journey_planner):
        self.W  = screen_w
        self.H  = screen_h
        self.alarm_manager   = alarm_manager
        self.alarm_config    = alarm_config
        self.journey_planner = journey_planner

        self.CY = HEADER_H
        self.CH = screen_h - HEADER_H - FOOTER_H

        self._f_big   = pygame.font.Font(None, 90)
        self._f_title = pygame.font.Font(None, 40)
        self._f_label = pygame.font.Font(None, 34)
        self._f_body  = pygame.font.Font(None, 28)
        self._f_small = pygame.font.Font(None, 24)

        if Path(_DEJAVU_PATH).exists():
            self._f_icon28 = pygame.font.Font(_DEJAVU_PATH, 28)
            self._f_icon20 = pygame.font.Font(_DEJAVU_PATH, 20)
        else:
            self._f_icon28 = self._f_body
            self._f_icon20 = self._f_small

        self._geocoder = NominatimGeocoder()
        self._reset()

    # ── Public API ─────────────────────────────────────────────────────────

    def load(self):
        plan   = self.alarm_config.plan
        dests  = self.alarm_config.destinations
        starts = self.alarm_config.starting_points

        saved = plan.get("destination")
        self._dest_idx  = next((i for i, d in enumerate(dests)  if d["name"] == saved), None)
        saved_s = plan.get("start_location", "Home")
        self._start_idx = next((i for i, s in enumerate(starts) if s["name"] == saved_s), 0)

        arr = plan.get("arrival_time", "09:00")
        try:
            h, m = map(int, arr.split(":"))
        except Exception:
            h, m = 9, 0
        self._arr_h        = h
        self._arr_m        = m
        self._transport    = plan.get("transport_mode", "public_transport")
        self._journey_mins = plan.get("journey_minutes", 45)
        self._fluffer_sel  = set(plan.get("fluffer_selected", []))
        self._snooze_count = plan.get("snooze_count", 0)
        self._snooze_dur   = plan.get("snooze_duration", 9)
        self._step         = 0
        self._scroll_y     = 0
        self._routes       = []
        self._route_idx    = None
        self._summary      = None

    def handle_scroll(self, delta):
        if self._kb_active:
            return
        self._scroll_y = max(0, self._scroll_y + delta)

    def handle_tap(self, pos):
        """Returns True if the panel should close."""
        x, y = pos

        if self._kb_active:
            kb_top  = self.H // 2
            sug_top = kb_top - SUG_H
            if y >= kb_top:
                self._tap_keyboard(x, y)
            elif y >= sug_top and self._suggestions:
                self._tap_suggestion(x, y)
            return False

        third = self.W // 3
        if y >= self.H - FOOTER_H:
            if x < third:
                if self._step == 0:
                    return True
                self._go_back()
            elif x >= self.W - third:
                if self._can_advance():
                    if self._step == N_STEPS - 1:
                        self._save()
                        return True
                    self._go_next()
            return False

        logical_y = (y - self.CY) + self._scroll_y
        handlers = {
            0: self._tap_dest,
            1: self._tap_arrival,
            2: self._tap_route,
            3: self._tap_fluffer,
            4: self._tap_confirm,
        }
        handlers.get(self._step, lambda *_: None)(x, logical_y)
        return False

    def draw(self, surf):
        self._poll_suggestions()
        surf.fill(BG)
        self._draw_header(surf)

        if self._kb_active:
            content_h = max(1, self.H // 2 - self.CY)
            content = surf.subsurface(pygame.Rect(0, self.CY, self.W, content_h))
            content.fill(BG)
            self._draw_step(content)
            self._draw_keyboard(surf)
            self._draw_suggestion_strip(surf)
        else:
            self._draw_footer(surf)
            content = surf.subsurface(pygame.Rect(0, self.CY, self.W, self.CH))
            content.fill(BG)
            self._draw_step(content)

    # ── Internal ───────────────────────────────────────────────────────────

    def _reset(self):
        self._step         = 0
        self._scroll_y     = 0
        self._dest_idx     = None
        self._start_idx    = 0
        self._arr_h        = 9
        self._arr_m        = 0
        self._transport    = "public_transport"
        self._journey_mins = 45
        self._routes       = []
        self._route_idx    = None
        self._fluffer_sel  = set()
        self._snooze_count = 0
        self._snooze_dur   = 9
        self._summary      = None
        # Keyboard
        self._kb_active    = False
        self._kb_text      = ""
        self._kb_field     = None   # "dest" | "start" | "stop_search"
        self._kb_edit_idx  = None
        # Suggestions (address autocomplete + PTV stop search)
        self._suggestions       = []
        self._suggestion_data   = []  # parallel stop objects when kb_field=="stop_search"
        self._suggest_inflight  = False
        self._suggest_tick      = 0
        # Route step setup state
        self._route_type_sel    = 1   # default Tram (common in inner Melbourne)
        self._stop_searching    = False

    def _draw_step(self, surf):
        {
            0: self._draw_dest,
            1: self._draw_arrival,
            2: self._draw_route,
            3: self._draw_fluffer,
            4: self._draw_confirm,
        }.get(self._step, lambda _: None)(surf)

    def _sy(self, raw_y):
        return raw_y - self._scroll_y

    def _arrival_dt(self):
        now = datetime.now()
        dt = now.replace(hour=self._arr_h, minute=self._arr_m, second=0, microsecond=0)
        if dt <= now:
            dt += timedelta(days=1)
        return dt

    def _ptv(self):
        """Return the PTVService if available, else None."""
        return getattr(self.journey_planner, "ptv_service", None) if self.journey_planner else None

    def _can_advance(self):
        return not (self._step == 0 and self._dest_idx is None)

    def _go_next(self):
        if self._step == 1 and self._transport != "public_transport":
            self._step = 3
        else:
            self._step = min(self._step + 1, N_STEPS - 1)
        self._scroll_y = 0
        if self._step == 2:
            self._fetch_routes()
        elif self._step == 4:
            self._compute_summary()

    def _go_back(self):
        if self._step == 3 and self._transport != "public_transport":
            self._step = 1
        else:
            self._step = max(self._step - 1, 0)
        self._scroll_y = 0

    def _fetch_routes(self):
        self._routes = []
        if self._transport != "public_transport":
            return
        arrival = self._arrival_dt()
        route_configs = self.alarm_config.plan.get("route_configs", [])
        if route_configs and self.journey_planner:
            self._routes = self.journey_planner.find_routes(route_configs, arrival, count=5)

    def _compute_summary(self):
        arrival = self._arrival_dt()
        fluffer = self.alarm_config.total_fluffer_minutes(list(self._fluffer_sel)) if self._fluffer_sel else 0
        self._summary = AlarmCalculator.full_summary(
            arrival=arrival,
            journey_minutes=self._journey_mins,
            fluffer_minutes=fluffer,
            snooze_count=self._snooze_count,
            snooze_duration=self._snooze_dur,
        )

    def _save(self):
        if not self._summary:
            self._compute_summary()
        alarm_dt = self._summary["alarm_time"]

        dests = self.alarm_config.destinations
        dest_name = dests[self._dest_idx]["name"] if self._dest_idx is not None and dests else None
        if dest_name:
            self.alarm_config.use_destination(dest_name)

        starts = self.alarm_config.starting_points
        start_name = starts[self._start_idx]["name"] if starts else "Home"

        self.alarm_config.update_plan(
            destination=dest_name,
            start_location=start_name,
            arrival_time=f"{self._arr_h:02d}:{self._arr_m:02d}",
            transport_mode=self._transport,
            journey_minutes=self._journey_mins,
            fluffer_selected=list(self._fluffer_sel),
            snooze_count=self._snooze_count,
            snooze_duration=self._snooze_dur,
            alarm_time=alarm_dt.strftime("%H:%M"),
        )

        if self.alarm_manager.alarms:
            self.alarm_manager.alarms[0].update({
                "hour": alarm_dt.hour,
                "minute": alarm_dt.minute,
                "enabled": True,
            })
            self.alarm_manager.save_alarms()
        else:
            self.alarm_manager.add_alarm(alarm_dt.hour, alarm_dt.minute)

    # ── Nominatim / PTV suggestions ────────────────────────────────────────

    def _poll_suggestions(self):
        if not self._kb_active or self._suggest_inflight or self._suggest_tick == 0:
            return
        min_len = 2 if self._kb_field == "stop_search" else _MIN_QUERY
        if len(self._kb_text) < min_len:
            self._suggestions    = []
            self._suggestion_data = []
            self._suggest_tick   = 0
            return
        if pygame.time.get_ticks() - self._suggest_tick < _DEBOUNCE_MS:
            return
        self._suggest_tick    = 0
        self._suggest_inflight = True
        query = self._kb_text

        if self._kb_field == "stop_search":
            self._search_ptv_stops_async(query)
        else:
            def _cb(results):
                self._suggestions      = results[:4]
                self._suggest_inflight = False
            self._geocoder.search_async(query, _cb)

    def _search_ptv_stops_async(self, query):
        ptv = self._ptv()
        if not ptv:
            self._suggest_inflight = False
            return
        route_type = self._route_type_sel

        def _fetch():
            try:
                stops = ptv.search_stops(query, route_types=[route_type])
                labels, data = [], []
                for stop in stops[:4]:
                    stop_id = stop.get("stop_id")
                    name    = stop.get("stop_name", "").strip()
                    suburb  = stop.get("stop_suburb", "").strip()
                    if stop_id and name:
                        labels.append(f"{name}, {suburb}" if suburb else name)
                        data.append({"stop_id": stop_id, "name": name})
                self._suggestions      = labels
                self._suggestion_data  = data
            except Exception:
                self._suggestions     = []
                self._suggestion_data = []
            finally:
                self._suggest_inflight = False

        threading.Thread(target=_fetch, daemon=True).start()

    def _draw_suggestion_strip(self, surf):
        kb_top  = self.H // 2
        sug_top = kb_top - SUG_H

        pygame.draw.rect(surf, SUG_BG, (0, sug_top, self.W, SUG_H))
        pygame.draw.line(surf, DIVIDER, (0, sug_top), (self.W, sug_top))
        pygame.draw.line(surf, ACCENT,  (0, kb_top),  (self.W, kb_top), 2)

        if self._suggest_inflight and not self._suggestions:
            label = "Searching stops…" if self._kb_field == "stop_search" else "Searching…"
            ls = self._f_small.render(label, True, MUTED)
            surf.blit(ls, ls.get_rect(center=(self.W // 2, sug_top + SUG_H // 2)))
            return

        if not self._suggestions:
            if self._kb_field == "stop_search":
                hint = "Type 2+ characters to search stops"
            else:
                hint = "Type 3+ characters for address suggestions"
            ls = self._f_small.render(hint, True, MUTED)
            surf.blit(ls, ls.get_rect(center=(self.W // 2, sug_top + SUG_H // 2)))
            return

        n   = len(self._suggestions)
        pad = 6
        chip_w = (self.W - pad * (n + 1)) // n
        for i, sug in enumerate(self._suggestions):
            cx = pad + i * (chip_w + pad)
            chip_r = pygame.Rect(cx, sug_top + 6, chip_w, SUG_H - 12)
            pygame.draw.rect(surf, SUG_CHIP, chip_r, border_radius=8)
            pygame.draw.rect(surf, ACCENT,   chip_r, 1, border_radius=8)
            ts = self._f_small.render(sug, True, TEXT)
            avail = chip_r.w - 12
            if ts.get_width() > avail:
                ts = ts.subsurface(pygame.Rect(0, 0, avail, ts.get_height()))
            surf.blit(ts, ts.get_rect(midleft=(chip_r.x + 6, chip_r.centery)))

    def _tap_suggestion(self, x, y):
        kb_top  = self.H // 2
        sug_top = kb_top - SUG_H
        n = len(self._suggestions)
        if n == 0:
            return
        pad    = 6
        chip_w = (self.W - pad * (n + 1)) // n
        for i in range(n):
            cx = pad + i * (chip_w + pad)
            if cx <= x < cx + chip_w and sug_top + 6 <= y < kb_top - 6:
                if self._kb_field == "stop_search" and i < len(self._suggestion_data):
                    # Save this stop as a route_config
                    stop = self._suggestion_data[i]
                    self.alarm_config.add_route_config(
                        route_type=self._route_type_sel,
                        stop_id=stop["stop_id"],
                        journey_minutes=self._journey_mins,
                        label=stop["name"],
                    )
                    self._kb_active       = False
                    self._kb_text         = ""
                    self._kb_field        = None
                    self._suggestions     = []
                    self._suggestion_data = []
                    self._suggest_tick    = 0
                    self._fetch_routes()
                else:
                    # Fill address text field
                    self._kb_text      = self._suggestions[i]
                    self._suggestions  = []
                    self._suggest_tick = 0
                return

    # ── On-screen keyboard ─────────────────────────────────────────────────

    def _kb_key_rects(self):
        kb_y    = self.H // 2
        kb_h    = self.H - kb_y
        input_h = 44
        gap     = 4
        pad     = 6
        n_rows  = len(_KB_ROWS)
        area_h  = kb_h - input_h - gap
        row_h   = area_h // n_rows
        key_h   = row_h - gap

        rects = []
        for ri, row in enumerate(_KB_ROWS):
            ry = kb_y + input_h + ri * row_h + gap // 2
            if ri == n_rows - 1:
                unit_w = (self.W - 2 * pad) / sum(_KB_BOT_WIDTHS)
                cx = pad
                for key, units in zip(row, _KB_BOT_WIDTHS):
                    kw = int(unit_w * units) - gap
                    rects.append((pygame.Rect(cx, ry, kw, key_h), key))
                    cx += int(unit_w * units)
            else:
                n = len(row)
                unit_w = (self.W - 2 * pad) / n
                for ki, key in enumerate(row):
                    kx = pad + int(ki * unit_w)
                    kw = int(unit_w) - gap
                    rects.append((pygame.Rect(kx, ry, kw, key_h), key))
        return rects

    def _draw_keyboard(self, surf):
        kb_y = self.H // 2
        pygame.draw.rect(surf, KB_BG, (0, kb_y, self.W, self.H - kb_y))

        input_rect = pygame.Rect(8, kb_y + 4, self.W - 16, 36)
        pygame.draw.rect(surf, ITEM_BG, input_rect, border_radius=6)
        pygame.draw.rect(surf, ACCENT,  input_rect, 2, border_radius=6)

        if self._kb_text:
            disp = self._kb_text + "│"
            ts = self._f_label.render(disp, True, TEXT)
            avail_w = input_rect.w - 16
            if ts.get_width() > avail_w:
                ts = ts.subsurface(pygame.Rect(ts.get_width() - avail_w, 0, avail_w, ts.get_height()))
            surf.blit(ts, ts.get_rect(midleft=(input_rect.x + 8, input_rect.centery)))
        else:
            if self._kb_field == "stop_search":
                prompt = "Stop name or street…"
            elif self._kb_field == "dest":
                prompt = "New destination…"
            else:
                prompt = "Departure location…"
            ps = self._f_body.render(prompt, True, MUTED)
            surf.blit(ps, ps.get_rect(midleft=(input_rect.x + 8, input_rect.centery)))

        for rect, key in self._kb_key_rects():
            if key == "DONE":
                bg = BTN_GREEN
            elif key == "CANCEL":
                bg = (70, 28, 28)
            elif key == "BKSP":
                bg = (50, 36, 36)
            else:
                bg = KB_KEY
            self._draw_key(surf, rect, bg)

            if key == "BKSP":
                self._draw_bksp_icon(surf, rect)
            elif key == "CANCEL":
                self._draw_x_icon(surf, rect)
            elif key == "SPACE":
                ls = self._f_small.render("space", True, MUTED)
                surf.blit(ls, ls.get_rect(center=rect.center))
            elif key == "DONE":
                ls = self._f_body.render("Done", True, TEXT)
                surf.blit(ls, ls.get_rect(center=rect.center))
            else:
                ls = self._f_body.render(key, True, TEXT)
                surf.blit(ls, ls.get_rect(center=rect.center))

    def _tap_keyboard(self, x, y):
        text_changed = False
        for rect, key in self._kb_key_rects():
            if rect.collidepoint(x, y):
                if key == "DONE":
                    self._kb_done()
                elif key == "CANCEL":
                    self._kb_active       = False
                    self._kb_text         = ""
                    self._kb_field        = None
                    self._kb_edit_idx     = None
                    self._suggestions     = []
                    self._suggestion_data = []
                    self._suggest_tick    = 0
                elif key == "BKSP":
                    self._kb_text = self._kb_text[:-1]
                    text_changed  = True
                elif key == "SPACE":
                    self._kb_text += " "
                    text_changed   = True
                else:
                    self._kb_text += key
                    text_changed   = True
                break

        if text_changed:
            self._suggestions     = []
            self._suggestion_data = []
            self._suggest_tick    = pygame.time.get_ticks()

    def _kb_done(self):
        text = self._kb_text.strip()

        if self._kb_field == "stop_search":
            # Close keyboard; if they had typed something, trigger a search
            # (results will show in suggestion strip on next open, or they
            #  already selected via chip — just close cleanly here)
            self._kb_active       = False
            self._kb_text         = ""
            self._kb_field        = None
            self._suggestions     = []
            self._suggestion_data = []
            self._suggest_tick    = 0
            return

        if text:
            if self._kb_field == "dest":
                if self._kb_edit_idx is not None:
                    old = self.alarm_config.destinations[self._kb_edit_idx]["name"]
                    self.alarm_config.update_destination(old, text, text)
                else:
                    self.alarm_config.add_destination(text, text)
                for i, d in enumerate(self.alarm_config.destinations):
                    if d["name"] == text:
                        self._dest_idx = i
                        break
            elif self._kb_field == "start":
                if self._kb_edit_idx is not None:
                    old = self.alarm_config.starting_points[self._kb_edit_idx]["name"]
                    self.alarm_config.update_starting_point(old, text, text)
                else:
                    self.alarm_config.add_starting_point(text, text)
                for i, s in enumerate(self.alarm_config.starting_points):
                    if s["name"] == text:
                        self._start_idx = i
                        break

        self._kb_active       = False
        self._kb_text         = ""
        self._kb_field        = None
        self._kb_edit_idx     = None
        self._suggestions     = []
        self._suggestion_data = []
        self._suggest_tick    = 0

    # ── Icon drawing ───────────────────────────────────────────────────────

    @staticmethod
    def _draw_bksp_icon(surf, rect):
        cx, cy = rect.centerx - 2, rect.centery
        pygame.draw.line(surf, TEXT, (cx - 9, cy), (cx + 9, cy), 2)
        pygame.draw.line(surf, TEXT, (cx - 9, cy), (cx - 3, cy - 5), 2)
        pygame.draw.line(surf, TEXT, (cx - 9, cy), (cx - 3, cy + 5), 2)

    @staticmethod
    def _draw_x_icon(surf, rect):
        cx, cy = rect.centerx, rect.centery
        m, c = 7, (255, 160, 160)
        pygame.draw.line(surf, c, (cx - m, cy - m), (cx + m, cy + m), 2)
        pygame.draw.line(surf, c, (cx + m, cy - m), (cx - m, cy + m), 2)

    @staticmethod
    def _draw_pencil_icon(surf, rect):
        cx, cy = rect.centerx, rect.centery
        pygame.draw.polygon(surf, (160, 185, 255), [
            (cx + 4, cy - 9), (cx + 9, cy - 4), (cx - 4, cy + 9), (cx - 9, cy + 4),
        ])
        pygame.draw.polygon(surf, (240, 220, 180), [
            (cx - 4, cy + 9), (cx - 9, cy + 4), (cx - 12, cy + 12),
        ])
        pygame.draw.polygon(surf, (220, 110, 110), [
            (cx + 3, cy - 11), (cx + 7, cy - 7), (cx + 9, cy - 9), (cx + 5, cy - 13),
        ])

    # ── Tap handlers ───────────────────────────────────────────────────────

    _EDIT_BTN_W  = 40
    _EDIT_BTN_H  = 36
    _EDIT_BTN_OX = 50

    def _edit_btn_rect_surf(self, item_raw_y):
        sy = self._sy(item_raw_y)
        return pygame.Rect(
            self.W - self._EDIT_BTN_OX,
            sy + (ITEM_H - self._EDIT_BTN_H) // 2,
            self._EDIT_BTN_W,
            self._EDIT_BTN_H,
        )

    def _edit_btn_hit(self, x, ly, item_raw_y):
        btn_ly_top = item_raw_y + (ITEM_H - self._EDIT_BTN_H) // 2
        return (
            self.W - self._EDIT_BTN_OX <= x <= self.W - self._EDIT_BTN_OX + self._EDIT_BTN_W
            and btn_ly_top <= ly < btn_ly_top + self._EDIT_BTN_H
        )

    def _tap_dest(self, x, ly):
        dests  = self.alarm_config.destinations
        starts = self.alarm_config.starting_points
        y = 34
        for i, d in enumerate(dests):
            if self._edit_btn_hit(x, ly, y):
                self._kb_field    = "dest"
                self._kb_text     = d["name"]
                self._kb_edit_idx = i
                self._kb_active   = True
                return
            if y <= ly < y + ITEM_H:
                self._dest_idx = i
                return
            y += ITEM_H + ITEM_GAP
        if y <= ly < y + ITEM_H:
            self._kb_field    = "dest"
            self._kb_text     = ""
            self._kb_edit_idx = None
            self._kb_active   = True
            return
        y += ITEM_H + ITEM_GAP
        y += 20
        y += 24
        for i, s in enumerate(starts):
            if self._edit_btn_hit(x, ly, y):
                self._kb_field    = "start"
                self._kb_text     = s["name"]
                self._kb_edit_idx = i
                self._kb_active   = True
                return
            if y <= ly < y + ITEM_H:
                self._start_idx = i
                return
            y += ITEM_H + ITEM_GAP
        if y <= ly < y + ITEM_H:
            self._kb_field    = "start"
            self._kb_text     = ""
            self._kb_edit_idx = None
            self._kb_active   = True
            return

    def _tap_arrival(self, x, ly):
        cx = self.W // 2
        for col_x, is_hour in ((cx - 130, True), (cx + 130, False)):
            if 30 <= ly < 74 and col_x - 45 <= x < col_x + 45:
                if is_hour:
                    self._arr_h = (self._arr_h + 1) % 24
                else:
                    self._arr_m = (self._arr_m + 5) % 60
                return
            if 175 <= ly < 219 and col_x - 45 <= x < col_x + 45:
                if is_hour:
                    self._arr_h = (self._arr_h - 1) % 24
                else:
                    self._arr_m = (self._arr_m - 5) % 60
                return
        bw = (self.W - 60) // 3
        if 262 <= ly < 306:
            if 30 <= x < 30 + bw:
                self._transport = "drive"
            elif x < 30 + bw * 2:
                self._transport = "public_transport"
            else:
                self._transport = "cycle"
        elif 338 <= ly < 382:
            if x < self.W // 2:
                self._journey_mins = max(5,   self._journey_mins - 5)
            else:
                self._journey_mins = min(180, self._journey_mins + 5)

    def _tap_route(self, x, ly):
        ptv = self._ptv()
        has_configs = bool(self.alarm_config.plan.get("route_configs"))

        if self._routes:
            # Departure list
            y = 34
            for i in range(len(self._routes)):
                if y <= ly < y + ITEM_H:
                    self._route_idx    = i
                    self._journey_mins = self._routes[i].get("journey_minutes", self._journey_mins)
                    return
                y += ITEM_H + ITEM_GAP

        elif ptv:
            # Setup mode (or PTV configured but departures unavailable)
            # Transport type buttons: y=30, h=44
            bw = (self.W - 60) // 3
            if 30 <= ly < 74:
                if 30 <= x < 30 + bw:
                    self._route_type_sel = 0
                elif x < 30 + bw * 2:
                    self._route_type_sel = 1
                else:
                    self._route_type_sel = 2
                return
            # Search button: y=108, h=52
            if 108 <= ly < 160:
                self._kb_field  = "stop_search"
                self._kb_text   = ""
                self._kb_active = True
                return
            # Journey time: y=194, h=44
            if 194 <= ly < 238:
                if x < self.W // 2:
                    self._journey_mins = max(5,   self._journey_mins - 5)
                else:
                    self._journey_mins = min(180, self._journey_mins + 5)

        elif not ptv:
            # No-PTV mode: only journey time adjustable
            if 220 <= ly < 264:
                if x < self.W // 2:
                    self._journey_mins = max(5,   self._journey_mins - 5)
                else:
                    self._journey_mins = min(180, self._journey_mins + 5)

    def _tap_fluffer(self, x, ly):
        y = 34
        for act in self.alarm_config.fluffer_activities:
            if y <= ly < y + ITEM_H:
                name = act["name"]
                if name in self._fluffer_sel:
                    self._fluffer_sel.discard(name)
                else:
                    self._fluffer_sel.add(name)
                return
            y += ITEM_H + ITEM_GAP

    def _tap_confirm(self, x, ly):
        mid = self.W // 2
        if 230 <= ly < 274:
            self._snooze_count = max(0,  self._snooze_count - 1) if x < mid else min(10, self._snooze_count + 1)
            self._compute_summary()
        elif 285 <= ly < 329:
            self._snooze_dur = max(1,  self._snooze_dur - 1) if x < mid else min(30, self._snooze_dur + 1)
            self._compute_summary()

    # ── Drawing helpers ────────────────────────────────────────────────────

    def _item(self, surf, raw_y, label, sub=None, selected=False, checked=None, editable=False):
        sy = self._sy(raw_y)
        if sy + ITEM_H < 0 or sy > self.CH:
            return
        r = pygame.Rect(10, sy, self.W - 20, ITEM_H)
        step_color = STEP_COLORS[self._step]
        pygame.draw.rect(surf, ITEM_SEL if selected else ITEM_BG, r, border_radius=6)
        if selected:
            pygame.draw.rect(surf, step_color, r, 2, border_radius=6)

        # Left ribbon
        ribbon_r = pygame.Rect(r.x, r.y + 4, 4, r.h - 8)
        pygame.draw.rect(surf, step_color if selected else _ribbon_dim(step_color),
                         ribbon_r, border_radius=2)

        tx = r.x + 20
        if checked is not None:
            cb = pygame.Rect(r.x + 20, r.centery - 13, 26, 26)
            pygame.draw.rect(surf, step_color if checked else BTN_GRAY, cb, border_radius=6)
            if checked:
                cs = self._f_icon20.render("✓", True, TEXT)
                surf.blit(cs, cs.get_rect(center=cb.center))
            tx = cb.right + 12

        text_max_x = r.right - (self._EDIT_BTN_OX + 4 if editable else 10)
        off = 10 if sub else 0

        ls = self._f_label.render(label, True, TEXT)
        lr = ls.get_rect(midleft=(tx, r.centery - off))
        if lr.right > text_max_x and text_max_x > lr.x:
            ls = ls.subsurface(pygame.Rect(0, 0, text_max_x - lr.x, ls.get_height()))
        surf.blit(ls, lr.topleft)

        if sub:
            ss = self._f_small.render(sub, True, MUTED)
            sr = ss.get_rect(midleft=(tx, r.centery + 14))
            if sr.right > text_max_x and text_max_x > sr.x:
                ss = ss.subsurface(pygame.Rect(0, 0, text_max_x - sr.x, ss.get_height()))
            surf.blit(ss, sr.topleft)

        if editable:
            btn = self._edit_btn_rect_surf(raw_y)
            pygame.draw.rect(surf, (50, 55, 80), btn, border_radius=6)
            pygame.draw.rect(surf, DIVIDER, btn, 1, border_radius=6)
            self._draw_pencil_icon(surf, btn)

    def _section(self, surf, raw_y, text):
        sy = self._sy(raw_y)
        if -20 < sy < self.CH:
            col = STEP_COLORS[self._step]
            ls  = self._f_small.render(text, True, col)
            surf.blit(ls, (16, sy))
            pygame.draw.line(surf, col,
                             (16, sy + ls.get_height() + 1),
                             (16 + ls.get_width(), sy + ls.get_height() + 1), 1)

    def _row_ctrl(self, surf, raw_y, label):
        r = pygame.Rect(10, self._sy(raw_y), self.W - 20, 44)
        self._draw_carved_button(surf, r, border_radius=4)
        col = STEP_COLORS[self._step]
        ms = self._f_title.render("-", True, col)
        surf.blit(ms, ms.get_rect(midleft=(r.x + 20, r.centery)))
        ls = self._f_label.render(label, True, TEXT)
        surf.blit(ls, ls.get_rect(center=r.center))
        ps = self._f_title.render("+", True, col)
        surf.blit(ps, ps.get_rect(midright=(r.right - 20, r.centery)))

    # ── Header / footer ────────────────────────────────────────────────────

    def _draw_star_strip(self, surf, y, h):
        pygame.draw.rect(surf, SURFACE_B, (0, y, self.W, h))
        for i, cx in enumerate(range(12, self.W - 8, 28)):
            cy = y + h // 2
            if i % 3 == 0:
                pygame.draw.line(surf, TEXT,  (cx - 3, cy), (cx + 3, cy), 1)
                pygame.draw.line(surf, TEXT,  (cx, cy - 3), (cx, cy + 3), 1)
            else:
                pygame.draw.rect(surf, MUTED, (cx, cy, 2, 2))

    def _draw_progress_path(self, surf):
        dot_r  = 5
        glow_r = 8
        path_y = HEADER_H - 14
        gap    = (self.W - 40) // (N_STEPS - 1)
        sx     = 20
        pygame.draw.line(surf, DIVIDER,
                         (sx, path_y), (sx + gap * (N_STEPS - 1), path_y), 2)
        if self._step > 0:
            pygame.draw.line(surf, STEP_COLORS[self._step],
                             (sx, path_y), (sx + gap * self._step, path_y), 2)
        for i in range(N_STEPS):
            cx    = sx + i * gap
            color = STEP_COLORS[i]
            if i < self._step:
                pygame.draw.circle(surf, color, (cx, path_y), dot_r)
                pygame.draw.line(surf, BG, (cx - 3, path_y),     (cx - 1, path_y + 2), 1)
                pygame.draw.line(surf, BG, (cx - 1, path_y + 2), (cx + 3, path_y - 2), 1)
            elif i == self._step:
                pygame.draw.circle(surf, SURFACE, (cx, path_y), glow_r)
                pygame.draw.circle(surf, color,   (cx, path_y), glow_r,      2)
                pygame.draw.circle(surf, color,   (cx, path_y), dot_r + 1,   2)
                pygame.draw.circle(surf, TEXT,    (cx, path_y), dot_r - 1)
            else:
                pygame.draw.circle(surf, DIVIDER, (cx, path_y), dot_r, 2)

    def _draw_carved_button(self, surf, rect, active=False, active_color=None, border_radius=6):
        body = tuple(min(255, c + 20) for c in ITEM_SEL) if (active and active_color) else BTN_GRAY
        pygame.draw.rect(surf, body, rect, border_radius=border_radius)
        hi = BTN_GREEN_HI  if (active and active_color == BTN_GREEN) else BTN_GRAY_HI
        sh = BTN_GREEN_SHD if (active and active_color == BTN_GREEN) else BTN_GRAY_SHD
        br = border_radius
        pygame.draw.line(surf, hi, (rect.x + br,    rect.y),          (rect.right - br, rect.y),          2)
        pygame.draw.line(surf, sh, (rect.x + br,    rect.bottom - 1), (rect.right - br, rect.bottom - 1), 2)
        pygame.draw.line(surf, hi, (rect.x,          rect.y + br),    (rect.x,          rect.bottom - br), 1)
        pygame.draw.line(surf, sh, (rect.right,      rect.y + br),    (rect.right,      rect.bottom - br), 1)
        if active and active_color:
            pygame.draw.rect(surf, active_color, rect, 2, border_radius=border_radius)

    def _draw_key(self, surf, rect, bg_color):
        pygame.draw.rect(surf, bg_color, rect, border_radius=3)
        hi = tuple(min(255, c + 30) for c in bg_color)
        sh = tuple(max(0,   c - 20) for c in bg_color)
        pygame.draw.line(surf, hi, (rect.x + 3,     rect.y + 1),      (rect.right - 4, rect.y + 1),      1)
        pygame.draw.line(surf, hi, (rect.x + 1,     rect.y + 3),      (rect.x + 1,     rect.bottom - 4), 1)
        pygame.draw.line(surf, sh, (rect.x + 3,     rect.bottom - 2), (rect.right - 4, rect.bottom - 2), 1)
        pygame.draw.line(surf, sh, (rect.right - 2, rect.y + 3),      (rect.right - 2, rect.bottom - 4), 1)

    def _draw_split_flap(self, surf, hh, mm, cy):
        panel_w = 110
        panel_h = 90
        gap     = 18
        panel_y = cy - panel_h // 2
        panels  = [
            (f"{hh:02d}", self.W // 2 - gap // 2 - panel_w),
            (f"{mm:02d}", self.W // 2 + gap // 2),
        ]
        for digit_str, px in panels:
            pr = pygame.Rect(px, panel_y, panel_w, panel_h)
            pygame.draw.rect(surf, (8, 12, 16), pr)
            pygame.draw.rect(surf, (38, 52, 62), pr, 3)
            pygame.draw.line(surf, (52, 72, 84), (pr.x, pr.y),      (pr.right, pr.y),      1)
            pygame.draw.line(surf, (52, 72, 84), (pr.x, pr.y),      (pr.x,     pr.bottom), 1)
            pygame.draw.line(surf, (4,  6,  8),  (pr.x, pr.bottom), (pr.right, pr.bottom), 1)
            pygame.draw.line(surf, (4,  6,  8),  (pr.right, pr.y),  (pr.right, pr.bottom), 1)
            ds = self._f_big.render(digit_str, True, WARN)
            surf.blit(ds, ds.get_rect(center=pr.center))
            mid_y = pr.centery
            pygame.draw.line(surf, (4,  6,  8),  (pr.x + 3, mid_y),     (pr.right - 3, mid_y),     2)
            pygame.draw.line(surf, (52, 72, 84), (pr.x + 3, mid_y + 2), (pr.right - 3, mid_y + 2), 1)
        col_x = self.W // 2 - gap // 2 + 2
        for dy in (-14, 10):
            pygame.draw.rect(surf, WARN, (col_x, cy + dy, 6, 8))

    def _draw_header(self, surf):
        pygame.draw.rect(surf, SURFACE, (0, 0, self.W, HEADER_H))
        self._draw_star_strip(surf, y=0, h=14)
        pygame.draw.line(surf, DIVIDER, (0, 14), (self.W, 14), 1)
        t = self._f_title.render(STEP_NAMES[self._step], True, TEXT)
        surf.blit(t, t.get_rect(midleft=(16, 28)))
        self._draw_progress_path(surf)
        pygame.draw.line(surf, STEP_COLORS[self._step], (0, HEADER_H), (self.W, HEADER_H), 2)

    def _draw_footer(self, surf):
        fy = self.H - FOOTER_H
        pygame.draw.rect(surf, SURFACE, (0, fy, self.W, FOOTER_H))
        pygame.draw.line(surf, STEP_COLORS[self._step], (0, fy), (self.W, fy), 2)
        bw = self.W // 3
        bh = FOOTER_H - 16
        by = fy + 8
        back_r = pygame.Rect(10, by, bw - 14, bh)
        self._draw_carved_button(surf, back_r, border_radius=4)
        bl = self._f_label.render("Cancel" if self._step == 0 else "Back", True, TEXT)
        surf.blit(bl, bl.get_rect(center=back_r.center))
        next_r = pygame.Rect(self.W - bw + 4, by, bw - 14, bh)
        can_go = self._can_advance()
        self._draw_carved_button(surf, next_r, active=can_go,
                                  active_color=BTN_GREEN if can_go else None, border_radius=4)
        nl = self._f_label.render("Save" if self._step == N_STEPS - 1 else "Next", True, TEXT)
        surf.blit(nl, nl.get_rect(center=next_r.center))
        if self._step < N_STEPS - 1:
            arx, ary = next_r.right - 14, next_r.centery
            pygame.draw.line(surf, TEXT, (arx - 4, ary - 4), (arx, ary), 2)
            pygame.draw.line(surf, TEXT, (arx - 4, ary + 4), (arx, ary), 2)

    # ── Step renderers ─────────────────────────────────────────────────────

    def _draw_dest(self, surf):
        dests  = self.alarm_config.destinations
        starts = self.alarm_config.starting_points
        y = 10
        self._section(surf, y, "DESTINATION")
        y += 24
        for i, d in enumerate(dests):
            sub = d.get("address") or ("Used " + str(d.get("count", 0)) + " times")
            self._item(surf, y, d["name"], sub, selected=(i == self._dest_idx), editable=True)
            y += ITEM_H + ITEM_GAP
        self._item(surf, y, "Other…", "Type a new destination")
        y += ITEM_H + ITEM_GAP
        y += 20
        self._section(surf, y, "STARTING FROM")
        y += 24
        for i, sp in enumerate(starts):
            self._item(surf, y, sp["name"], sp.get("address") or None,
                       selected=(i == self._start_idx), editable=True)
            y += ITEM_H + ITEM_GAP
        self._item(surf, y, "Other…", "Type a new departure")

    def _draw_arrival(self, surf):
        cx = self.W // 2
        self._draw_split_flap(surf, self._arr_h, self._arr_m, self._sy(120))
        for col_x, tag in ((cx - 130, "hour"), (cx + 130, "min")):
            for raw_y, lbl in ((30, "▲"), (175, "▼")):
                r = pygame.Rect(col_x - 45, self._sy(raw_y), 90, 44)
                self._draw_carved_button(surf, r, border_radius=8)
                s = self._f_label.render(lbl, True, STEP_COLORS[1])
                surf.blit(s, s.get_rect(center=r.center))
            tl = self._f_small.render(tag, True, MUTED)
            surf.blit(tl, tl.get_rect(center=(col_x, self._sy(228))))
        self._section(surf, 244, "TRANSPORT MODE")
        modes_cfg = [
            ("drive",            "Drive",   _draw_icon_car),
            ("public_transport", "Transit", _draw_icon_bus),
            ("cycle",            "Cycle",   _draw_icon_cycle),
        ]
        bw = (self.W - 60) // 3
        for i, (mode, name, icon_fn) in enumerate(modes_cfg):
            br  = pygame.Rect(30 + i * bw, self._sy(262), bw - 4, 44)
            sel = self._transport == mode
            self._draw_carved_button(surf, br, active=sel,
                                      active_color=STEP_COLORS[1] if sel else None,
                                      border_radius=4)
            icon_rect = pygame.Rect(br.x + 4, br.y, 36, br.h)
            icon_fn(surf, icon_rect, TEXT if sel else MUTED)
            ns = self._f_small.render(name, True, TEXT if sel else MUTED)
            surf.blit(ns, ns.get_rect(midleft=(br.x + 42, br.centery)))
        self._section(surf, 320, "ESTIMATED JOURNEY TIME")
        self._row_ctrl(surf, 338, f"{self._journey_mins} min")

    def _draw_route(self, surf):
        ptv        = self._ptv()
        has_configs = bool(self.alarm_config.plan.get("route_configs"))

        # ── Case 1: live departures ready ──────────────────────────────────
        if self._routes:
            y = 10
            self._section(surf, y, "SELECT A DEPARTURE")
            y += 24
            for i, r in enumerate(self._routes):
                dep = r["time"].strftime("%H:%M")
                arr = r.get("estimated_arrival",
                            r["time"] + timedelta(minutes=self._journey_mins)).strftime("%H:%M")
                sub = r.get("route_label") or r.get("direction_name", "")
                self._item(surf, y, f"Depart {dep}  →  Arrive {arr}", sub,
                           selected=(i == self._route_idx))
                y += ITEM_H + ITEM_GAP
            return

        # ── Case 2: non-PT transport ───────────────────────────────────────
        if self._transport != "public_transport":
            dep = self._arrival_dt() - timedelta(minutes=self._journey_mins)
            tl = self._f_body.render("Depart by:", True, MUTED)
            surf.blit(tl, tl.get_rect(center=(self.W // 2, self.CH // 2 - 45)))
            dt = self._f_big.render(dep.strftime("%H:%M"), True, WARN)
            surf.blit(dt, dt.get_rect(center=(self.W // 2, self.CH // 2 + 15)))
            return

        # ── Case 3: PTV setup — no credentials ────────────────────────────
        if not ptv:
            cx = self.W // 2
            icon = self._f_big.render("🚌", True, MUTED)
            surf.blit(icon, icon.get_rect(center=(cx, self._sy(50))))
            hl = self._f_label.render("PTV API not configured", True, WARN)
            surf.blit(hl, hl.get_rect(center=(cx, self._sy(110))))
            for i, line in enumerate([
                "Register at ptv.vic.gov.au → Data & Reporting → API",
                "Then add to config/settings.json:",
                '  "ptv": { "devId": "…", "apiKey": "…" }',
            ]):
                ls = self._f_small.render(line, True, MUTED)
                surf.blit(ls, ls.get_rect(center=(cx, self._sy(150 + i * 22))))
            self._section(surf, 210, "SET JOURNEY TIME MANUALLY")
            self._row_ctrl(surf, 220, f"{self._journey_mins} min")
            return

        # ── Case 4: PTV configured, no live departures available ──────────
        self._section(surf, 10, "TRANSPORT TYPE")
        bw = (self.W - 60) // 3
        for i, (rt, name) in enumerate(_ROUTE_TYPES):
            br = pygame.Rect(30 + i * bw, self._sy(30), bw - 4, 44)
            sel = self._route_type_sel == rt
            pygame.draw.rect(surf, ITEM_SEL if sel else ITEM_BG, br, border_radius=8)
            if sel:
                pygame.draw.rect(surf, ACCENT, br, 2, border_radius=8)
            ns = self._f_body.render(name, True, TEXT)
            surf.blit(ns, ns.get_rect(center=br.center))

        self._section(surf, 88, "FIND YOUR NEAREST STOP")
        # Search button
        sr = pygame.Rect(10, self._sy(108), self.W - 20, 52)
        pygame.draw.rect(surf, ITEM_BG, sr, border_radius=10)
        pygame.draw.rect(surf, ACCENT,  sr, 1, border_radius=10)
        hint_txt = "🔍  Tap to search stops…  (results appear above keyboard)"
        hs = self._f_body.render(hint_txt, True, MUTED)
        surf.blit(hs, hs.get_rect(center=sr.center))

        self._section(surf, 174, "JOURNEY TIME")
        self._row_ctrl(surf, 194, f"{self._journey_mins} min")

        # Stopped searching but no configs yet — show a note
        if has_configs:
            note = self._f_small.render("Stop saved — fetching departures…", True, ACCENT)
            surf.blit(note, note.get_rect(center=(self.W // 2, self._sy(256))))

    def _draw_fluffer(self, surf):
        acts = self.alarm_config.fluffer_activities
        y = 10
        if not acts:
            ml = self._f_body.render("No activities configured.", True, MUTED)
            surf.blit(ml, ml.get_rect(center=(self.W // 2, self.CH // 2 - 18)))
            hl = self._f_small.render("Use alarm_config.add_activity(name, minutes) to add tasks.", True, MUTED)
            surf.blit(hl, hl.get_rect(center=(self.W // 2, self.CH // 2 + 14)))
            return
        self._section(surf, y, "SELECT ACTIVITIES")
        y += 24
        for act in acts:
            name = act["name"]
            sel  = name in self._fluffer_sel
            self._item(surf, y, name, str(act.get("minutes", 0)) + " min", selected=sel, checked=sel)
            y += ITEM_H + ITEM_GAP
        total = self.alarm_config.total_fluffer_minutes(list(self._fluffer_sel))
        tl = self._f_label.render("Total prep:  " + str(total) + " min", True, ACCENT)
        surf.blit(tl, tl.get_rect(center=(self.W // 2, self.CH - 20)))

    def _draw_confirm(self, surf):
        if not self._summary:
            self._compute_summary()
        s  = self._summary
        cx = self.W // 2

        # Glow panel behind alarm time
        glow_r = pygame.Rect(cx - 140, self._sy(10), 280, 100)
        pygame.draw.rect(surf, SURFACE_B, glow_r, border_radius=6)
        pygame.draw.rect(surf, STEP_COLORS[4], glow_r, 2, border_radius=6)
        pygame.draw.rect(surf, tuple(min(255, c + 15) for c in SURFACE_B),
                         glow_r.inflate(-4, -4), 1, border_radius=4)

        al = self._f_small.render("ALARM", True, STEP_COLORS[4])
        surf.blit(al, al.get_rect(center=(cx, self._sy(22))))
        at = self._f_big.render(s["alarm_time"].strftime("%H:%M"), True, WARN)
        surf.blit(at, at.get_rect(center=(cx, self._sy(72))))

        # Decorative 6-point stars around the panel
        star_positions = [
            (glow_r.x - 16,     glow_r.y + 10),
            (glow_r.right + 16, glow_r.y + 10),
            (glow_r.x - 20,     glow_r.centery),
            (glow_r.right + 20, glow_r.centery),
            (glow_r.x + 20,     glow_r.bottom + 10),
            (glow_r.right - 20, glow_r.bottom + 10),
        ]
        for sx, sy in star_positions:
            _draw_star(surf, sx, sy, r_outer=8,  r_inner=4, color=STEP_COLORS[4])
        for sx, sy in star_positions:
            _draw_star(surf, sx + 14, sy - 8, r_outer=4, r_inner=2, color=MUTED)

        sl = self._f_label.render(
            str(s["sleep_hours"]) + "h  " + str(s["sleep_minutes"]) + "m of sleep", True, ACCENT)
        surf.blit(sl, sl.get_rect(center=(cx, self._sy(148))))
        dep_str = ("Depart " + s["departure_time"].strftime("%H:%M") +
                   "  ·  " + str(self._journey_mins) + " min journey")
        dl = self._f_small.render(dep_str, True, MUTED)
        surf.blit(dl, dl.get_rect(center=(cx, self._sy(182))))
        sn_lbl = self._f_small.render("PLANNED SNOOZES", True, MUTED)
        surf.blit(sn_lbl, sn_lbl.get_rect(center=(cx, self._sy(214))))
        self._row_ctrl(surf, 230, str(self._snooze_count) + "  snooze(s)")
        self._row_ctrl(surf, 285, str(self._snooze_dur) + " min / snooze")
        if s["fluffer_minutes"] or s["snooze_buffer_minutes"]:
            info = ("Prep: " + str(s["fluffer_minutes"]) +
                    " min  ·  Snooze buffer: " + str(s["snooze_buffer_minutes"]) + " min")
            ils = self._f_small.render(info, True, MUTED)
            surf.blit(ils, ils.get_rect(center=(cx, self._sy(342))))
