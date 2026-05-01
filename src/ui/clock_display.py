"""
Main clock display UI
"""
import pygame
from datetime import datetime
import pytz
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.config_loader import ConfigLoader
from ui.themes import ThemeManager
from ui.photo_frame import PhotoFrame
from ui.commute_panel import CommutePanel
from ui.split_flap import SplitFlapDisplay
from ui.pixel_border import PixelBorder
from ui.alarm_panel import AlarmPanel
from ui.seasonal_texture import SeasonalTexture
from services.ptv_api import PTVService
from services.alarm_manager import AlarmManager
from services.alarm_logic import AlarmConfig
from services.journey_planner import JourneyPlanner


class ClockApp:
    """Main application class for the alarm clock"""

    def __init__(self):
        """Initialize the clock application"""
        pygame.init()
        pygame.mixer.init()

        # Load configuration
        self.config = ConfigLoader()

        # Display settings
        self.fullscreen = self.config.get('display.fullscreen', True)

        if self.fullscreen:
            # (0, 0) lets SDL pick the true physical resolution, avoiding any
            # compositor work-area offsets caused by panels or taskbars.
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
            self.width  = self.screen.get_width()
            self.height = self.screen.get_height()
        else:
            self.width  = self.config.get('display.width', 800)
            self.height = self.config.get('display.height', 480)
            self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("Liv's Alarm Clock")

        # Theme manager for seasonal colors
        self.theme_manager = ThemeManager()
        self.theme = self.theme_manager.get_current_season_theme()

        # Colors from theme
        self.bg_color = self.theme['bg_color']
        self.text_color = self.theme['text_color']
        self.accent_color = self.theme['accent_color']
        self.secondary_color = self.theme['secondary_color']

        # Font
        self.clock_font = pygame.font.Font(None, 120)
        self.small_font = pygame.font.Font(None, 36)
        self.tiny_font = pygame.font.Font(None, 24)

        # Timezone
        self.timezone = pytz.timezone(self.config.get('timezone', 'Australia/Melbourne'))

        # Photo frame mode
        idle_timeout = self.config.get('photoFrame.idleTimeout', 60)
        self.photo_frame = PhotoFrame(idle_timeout=idle_timeout)

        # PTV service for commute tracking (optional)
        ptv_dev_id = self.config.get('ptv.devId')
        ptv_api_key = self.config.get('ptv.apiKey')

        if ptv_dev_id and ptv_api_key:
            self.ptv_service = PTVService(ptv_dev_id, ptv_api_key)
            self.commute_panel = CommutePanel(self.ptv_service)

            # Configure commute stops from config
            home_stop = self.config.get('ptv.homeStopId')
            home_route_type = self.config.get('ptv.homeRouteType', 0)
            work_stop = self.config.get('ptv.workStopId')
            work_route_type = self.config.get('ptv.workRouteType', 0)

            if home_stop and work_stop:
                self.commute_panel.configure_commute(
                    home_stop, home_route_type,
                    work_stop, work_route_type
                )
        else:
            self.ptv_service = None
            self.commute_panel = None

        # Alarm manager and full-screen panel
        self.alarm_manager = AlarmManager()
        self.alarm_config = AlarmConfig()
        self.journey_planner = JourneyPlanner(self.ptv_service if hasattr(self, 'ptv_service') else None)
        self.alarm_panel = AlarmPanel(self.width, self.height, self.alarm_manager, self.alarm_config, self.journey_planner)
        self._last_alarm_check = 0

        # Slide-in state:
        #   _panel_x  – current divider position in pixels (0 = closed, width = fully open)
        #   _panel_target – snap destination after a swipe
        #   _panel_was_open – whether the panel was open when the current touch began
        #   _swipe_start – finger-down position, or None when not touching
        #   _swipe_active – True once horizontal motion exceeds the dead-zone
        self._panel_x      = 0.0
        self._panel_target = 0.0
        self._panel_was_open = False
        self._swipe_start  = None
        self._swipe_active = False

        # Clock settings
        self.clock = pygame.time.Clock()
        self.fps = 30  # Reduced from 60 to save CPU

        # Theme update timer
        self.last_theme_update = pygame.time.get_ticks()
        self.theme_update_interval = 3600000  # Check season every hour

        # Split-flap display for clock (30% larger)
        self.split_flap = SplitFlapDisplay(
            num_digits=4,
            digit_width=117,
            digit_height=182,
            spacing=20
        )
        # Snap to current time immediately so display is correct on first frame
        init_time = self.get_current_time().strftime("%I:%M")
        self.split_flap.set_time(init_time)
        for digit in self.split_flap.digits:
            digit.current_value = digit.target_value
            digit.is_flipping = False

        # Pixel art border with theme colors
        self.pixel_border = PixelBorder(self.width, self.height, self.theme)
        self.seasonal_texture = SeasonalTexture(self.width, self.height, self.theme['name'], self.accent_color)

        # Animation frame counter
        self.frame_count = 0

        self.running = True

    def get_current_time(self):
        """Get current time in Melbourne timezone"""
        return datetime.now(self.timezone)

    def draw_clock(self, surf):
        """Draw the digital clock display with split-flap style onto surf."""
        current_time = self.get_current_time()

        time_str   = current_time.strftime("%I:%M")
        period_str = current_time.strftime("%p")

        self.split_flap.set_time(time_str)

        bright_accent = tuple(min(255, c + 55) for c in self.accent_color)
        flap_colors = {
            'bg':        (6, 6, 10),
            'text':      bright_accent,
            'shadow':    (0, 0, 0),
            'highlight': (255, 255, 255),
        }

        center_pos = (self.width // 2, self.height // 2 - 20)
        self.split_flap.draw(surf, center_pos, self.clock_font, flap_colors, show_colon=True)

        clock_right_edge = center_pos[0] + (self.split_flap.total_width // 2)
        period_x = clock_right_edge + int(self.width * 0.03)
        period_y = center_pos[1] + int(self.height * 0.15)
        period_surface = self.small_font.render(period_str, True, self.accent_color)
        surf.blit(period_surface, period_surface.get_rect(midleft=(period_x, period_y)))

        clock_half_height = self.split_flap.total_height // 2
        padding = int(self.height * 0.03)

        season_y = center_pos[1] - clock_half_height - padding - 60
        season_surface = self.tiny_font.render(self.theme['name'], True, self.secondary_color)
        surf.blit(season_surface, season_surface.get_rect(center=(self.width // 2, season_y)))

        weekend_y = center_pos[1] - clock_half_height - padding - 20
        if self.alarm_manager.is_weekend():
            ws = self.small_font.render("✨ Weekend ✨", True, self.accent_color)
            surf.blit(ws, ws.get_rect(center=(self.width // 2, weekend_y)))
        elif self.alarm_manager.is_holiday():
            holiday_name = self.alarm_manager.holiday_service.get_holiday_name(current_time.date())
            hs = self.small_font.render(f"🎉 {holiday_name} 🎉", True, self.accent_color)
            surf.blit(hs, hs.get_rect(center=(self.width // 2, weekend_y)))

        date_str = current_time.strftime("%A, %B %d, %Y")
        date_surface = self.small_font.render(date_str, True, self.text_color)
        date_y = center_pos[1] + clock_half_height + padding
        surf.blit(date_surface, date_surface.get_rect(center=(self.width // 2, date_y)))

        # Subtle left-edge tab hinting that swiping right opens the alarm panel
        pygame.draw.rect(surf, self.accent_color,
                         pygame.Rect(0, self.height // 2 - 40, 6, 80), border_radius=3)

    def draw_commute_info(self, surf):
        """Draw commute information if available."""
        if self.commute_panel and self.commute_panel.departures:
            theme_colors = {
                'text_color':      self.text_color,
                'accent_color':    self.accent_color,
                'secondary_color': self.secondary_color,
            }
            self.commute_panel.draw_compact(surf, (20, self.height - 80), theme_colors)

    def handle_events(self):
        """Handle pygame events with live swipe tracking."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self._panel_target > 0:
                        self._panel_target = 0.0
                        self._swipe_start  = None
                        self._swipe_active = False
                    else:
                        self.running = False
                self.photo_frame.register_activity()
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                self._swipe_start    = event.pos
                self._swipe_active   = False
                self._panel_was_open = (self._panel_target >= self.width)
                if not self._panel_was_open:
                    self.photo_frame.register_activity()

            elif event.type == pygame.MOUSEMOTION and self._swipe_start is not None:
                dx = event.pos[0] - self._swipe_start[0]
                dy = event.pos[1] - self._swipe_start[1]

                if self._panel_was_open and abs(dy) > abs(dx) and abs(dy) > 5:
                    self.alarm_panel.handle_scroll(-event.rel[1])
                elif abs(dx) > abs(dy) and abs(dx) > 15:
                    # Load alarm data as soon as the opening swipe is recognised
                    if not self._swipe_active and not self._panel_was_open and dx > 0:
                        self.alarm_panel.load()
                    self._swipe_active = True

                    if self._panel_was_open:
                        # Dragging to close: slide panel back left
                        self._panel_x = max(0.0, min(self.width + dx, float(self.width)))
                    else:
                        # Dragging to open: slide panel in from left
                        self._panel_x = max(0.0, min(float(dx), float(self.width)))

            elif event.type == pygame.MOUSEBUTTONUP and self._swipe_start is not None:
                dx = event.pos[0] - self._swipe_start[0]
                dy = event.pos[1] - self._swipe_start[1]
                total_move = (dx * dx + dy * dy) ** 0.5
                self._swipe_start = None

                if total_move < 20:
                    # Tap — forward to alarm panel if it is open
                    if self._panel_was_open:
                        if self.alarm_panel.handle_tap(event.pos):
                            self._panel_target = 0.0
                elif self._swipe_active:
                    threshold = self.width * 0.35
                    if self._panel_was_open:
                        self._panel_target = 0.0 if dx < -threshold else float(self.width)
                    else:
                        self._panel_target = float(self.width) if dx > threshold else 0.0

                self._swipe_active = False

    def _update_panel_animation(self):
        """Ease _panel_x towards _panel_target when no active drag."""
        if self._swipe_active:
            return
        diff = self._panel_target - self._panel_x
        if abs(diff) < 1.5:
            self._panel_x = self._panel_target
        else:
            self._panel_x += diff * 0.25

    def update_theme(self):
        """Update theme based on current season"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_theme_update >= self.theme_update_interval:
            self.theme = self.theme_manager.update_season()
            self.bg_color = self.theme['bg_color']
            self.text_color = self.theme['text_color']
            self.accent_color = self.theme['accent_color']
            self.secondary_color = self.theme['secondary_color']
            self.pixel_border = PixelBorder(self.width, self.height, self.theme)
            self.seasonal_texture = SeasonalTexture(self.width, self.height, self.theme['name'], self.accent_color)
            self.last_theme_update = current_time

    def _check_alarm_trigger(self):
        if pygame.time.get_ticks() - self._last_alarm_check < 30000:
            return
        self._last_alarm_check = pygame.time.get_ticks()
        self.alarm_manager.check_alarms()
        if self.alarm_manager.trigger.check_snooze_expired():
            self.alarm_manager.trigger.trigger(self.alarm_manager.trigger.triggered_alarm)

    def run(self):
        """Main application loop"""
        clock_surf = pygame.Surface((self.width, self.height))
        panel_surf = pygame.Surface((self.width, self.height))

        while self.running:
            self.handle_events()
            self._update_panel_animation()

            self.photo_frame.update()
            self.split_flap.update()
            if self.commute_panel:
                self.commute_panel.update()
            self.update_theme()
            self._check_alarm_trigger()
            self.frame_count += 1

            # --- Draw clock to offscreen surface ---
            clock_surf.fill(self.bg_color)
            if not self.photo_frame.draw(clock_surf):
                self.seasonal_texture.draw(clock_surf)
                self.pixel_border.draw_animated(clock_surf, self.frame_count)
                self.draw_clock(clock_surf)
                self.draw_commute_info(clock_surf)

            # --- Composite: slide clock right, panel in from left ---
            px = int(self._panel_x)

            if px <= 0:
                self.screen.blit(clock_surf, (0, 0))
            elif px >= self.width:
                # Panel fully open — draw directly to avoid blitting panel_surf twice
                self.alarm_panel.draw(self.screen)
            else:
                # Mid-swipe: both views visible
                self.alarm_panel.draw(panel_surf)
                self.screen.blit(panel_surf, (px - self.width, 0))
                self.screen.blit(clock_surf,  (px, 0))

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
