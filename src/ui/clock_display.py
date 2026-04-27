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
from services.ptv_api import PTVService
from services.alarm_manager import AlarmManager


class ClockApp:
    """Main application class for the alarm clock"""

    def __init__(self):
        """Initialize the clock application"""
        pygame.init()

        # Load configuration
        self.config = ConfigLoader()

        # Display settings
        self.width = self.config.get('display.width', 800)
        self.height = self.config.get('display.height', 480)
        self.fullscreen = self.config.get('display.fullscreen', False)

        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
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

        # Alarm manager
        self.alarm_manager = AlarmManager()

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

        # Pixel art border with theme colors
        self.pixel_border = PixelBorder(self.width, self.height, self.theme)

        # Animation frame counter
        self.frame_count = 0

        self.running = True

    def get_current_time(self):
        """Get current time in Melbourne timezone"""
        return datetime.now(self.timezone)

    def draw_clock(self):
        """Draw the digital clock display with split-flap style"""
        current_time = self.get_current_time()

        # Format time as 12-hour with AM/PM
        time_str = current_time.strftime("%I:%M")
        period_str = current_time.strftime("%p")

        # Update split-flap display
        self.split_flap.set_time(time_str)

        # Define split-flap colors from theme
        flap_colors = {
            'bg': (40, 40, 50),  # Dark background
            'text': self.text_color,
            'shadow': (0, 0, 0),
            'highlight': (255, 255, 255)
        }

        # Draw split-flap clock in center
        center_pos = (self.width // 2, self.height // 2 - 20)
        self.split_flap.draw(self.screen, center_pos, self.clock_font, flap_colors, show_colon=True)

        # Draw AM/PM indicator NEXT TO the clock (to the right)
        # Calculate position to the right of the split-flap display with 3% padding
        clock_right_edge = center_pos[0] + (self.split_flap.total_width // 2)
        period_x = clock_right_edge + int(self.width * 0.03)  # 3% of screen width padding
        # Position 15% of screen height down from clock center
        period_y = center_pos[1] + int(self.height * 0.15)

        period_surface = self.small_font.render(period_str, True, self.accent_color)
        period_rect = period_surface.get_rect(midleft=(period_x, period_y))
        self.screen.blit(period_surface, period_rect)

        # Draw season and weekend/holiday ABOVE the clock (centered)
        # Position based on clock height with 3% padding
        clock_half_height = self.split_flap.total_height // 2
        padding = int(self.height * 0.03)

        # Season goes above clock with padding
        season_y = center_pos[1] - clock_half_height - padding - 60

        # Draw season indicator
        season_name = self.theme['name']
        season_surface = self.tiny_font.render(f"{season_name}", True, self.secondary_color)
        season_rect = season_surface.get_rect(center=(self.width // 2, season_y))
        self.screen.blit(season_surface, season_rect)

        # Draw weekend/holiday indicator (below season, still above clock with padding)
        weekend_y = center_pos[1] - clock_half_height - padding - 20
        if self.alarm_manager.is_weekend():
            weekend_surface = self.small_font.render("✨ Weekend ✨", True, self.accent_color)
            weekend_rect = weekend_surface.get_rect(center=(self.width // 2, weekend_y))
            self.screen.blit(weekend_surface, weekend_rect)
        elif self.alarm_manager.is_holiday():
            holiday_name = self.alarm_manager.holiday_service.get_holiday_name(current_time.date())
            holiday_surface = self.small_font.render(f"🎉 {holiday_name} 🎉", True, self.accent_color)
            holiday_rect = holiday_surface.get_rect(center=(self.width // 2, weekend_y))
            self.screen.blit(holiday_surface, holiday_rect)

        # Draw date below the clock with 3% padding
        date_str = current_time.strftime("%A, %B %d, %Y")
        date_surface = self.small_font.render(date_str, True, self.text_color)
        date_y = center_pos[1] + clock_half_height + padding
        date_rect = date_surface.get_rect(center=(self.width // 2, date_y))
        self.screen.blit(date_surface, date_rect)

    def draw_commute_info(self):
        """Draw commute information if available"""
        if self.commute_panel and self.commute_panel.departures:
            theme_colors = {
                'text_color': self.text_color,
                'accent_color': self.accent_color,
                'secondary_color': self.secondary_color
            }

            # Draw compact version at bottom of screen
            self.commute_panel.draw_compact(
                self.screen,
                (20, self.height - 80),
                theme_colors
            )

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Register activity to reset photo frame timer
                self.photo_frame.register_activity()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Register activity on any mouse/touch interaction
                self.photo_frame.register_activity()

    def update_theme(self):
        """Update theme based on current season"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_theme_update >= self.theme_update_interval:
            self.theme = self.theme_manager.update_season()
            self.bg_color = self.theme['bg_color']
            self.text_color = self.theme['text_color']
            self.accent_color = self.theme['accent_color']
            self.secondary_color = self.theme['secondary_color']

            # Update pixel border with new theme
            self.pixel_border = PixelBorder(self.width, self.height, self.theme)

            self.last_theme_update = current_time

    def run(self):
        """Main application loop"""
        while self.running:
            self.handle_events()

            # Update photo frame state
            self.photo_frame.update()

            # Update split-flap animation
            self.split_flap.update()

            # Update commute info if available
            if self.commute_panel:
                self.commute_panel.update()

            # Update theme periodically
            self.update_theme()

            # Increment frame counter for animations
            self.frame_count += 1

            # Clear screen
            self.screen.fill(self.bg_color)

            # Check if photo frame should display
            if self.photo_frame.draw(self.screen):
                # Photo frame is active, skip clock display
                pass
            else:
                # Draw pixel art border first (background layer)
                self.pixel_border.draw_animated(self.screen, self.frame_count)

                # Draw normal clock interface on top
                self.draw_clock()
                self.draw_commute_info()

            # Update display
            pygame.display.flip()

            # Control frame rate
            self.clock.tick(self.fps)

        pygame.quit()
