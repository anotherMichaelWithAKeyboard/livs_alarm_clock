"""
Commute planner UI panel
"""
import pygame
from datetime import datetime
from typing import Optional
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from services.ptv_api import PTVService, CommuteTracker


class CommutePanel:
    """Display train/tram schedule for commute planning"""

    def __init__(self, ptv_service: Optional[PTVService] = None):
        """
        Initialize commute panel

        Args:
            ptv_service: PTV service instance (optional)
        """
        self.ptv = ptv_service
        self.commute_tracker = CommuteTracker(ptv_service) if ptv_service else None
        self.last_update = 0
        self.update_interval = 30000  # Update every 30 seconds
        self.departures = []
        self.is_morning_commute = True

    def configure_commute(self, home_stop_id: int, home_route_type: int,
                         work_stop_id: int, work_route_type: int):
        """Configure commute stops"""
        if self.commute_tracker:
            self.commute_tracker.configure_commute(
                home_stop_id, home_route_type,
                work_stop_id, work_route_type
            )

    def should_show_morning_commute(self) -> bool:
        """
        Determine if we should show morning or evening commute
        Morning: 5am - 12pm
        Evening: 12pm - 10pm
        """
        hour = datetime.now().hour
        return 5 <= hour < 12

    def update(self):
        """Update departure information"""
        if not self.commute_tracker:
            return

        current_time = pygame.time.get_ticks()

        if current_time - self.last_update >= self.update_interval or not self.departures:
            self.is_morning_commute = self.should_show_morning_commute()

            try:
                if self.is_morning_commute:
                    self.departures = self.commute_tracker.get_morning_departures(max_results=3)
                else:
                    self.departures = self.commute_tracker.get_evening_departures(max_results=3)

                self.last_update = current_time
            except Exception as e:
                print(f"Error updating departures: {e}")
                self.departures = []

    def draw(self, screen, position, theme_colors=None):
        """
        Draw the commute panel

        Args:
            screen: Pygame screen
            position: (x, y) tuple for panel position
            theme_colors: Optional dict with color keys (text_color, accent_color, etc.)
        """
        if not self.departures:
            return

        # Default colors if theme not provided
        if theme_colors is None:
            theme_colors = {
                'text_color': (255, 255, 255),
                'accent_color': (100, 150, 255),
                'secondary_color': (180, 180, 180)
            }

        x, y = position

        # Fonts
        title_font = pygame.font.Font(None, 32)
        time_font = pygame.font.Font(None, 48)
        detail_font = pygame.font.Font(None, 24)

        # Draw title
        title = "To Work" if self.is_morning_commute else "To Home"
        title_surface = title_font.render(title, True, theme_colors['accent_color'])
        screen.blit(title_surface, (x, y))
        y += 40

        # Draw departures
        for i, departure in enumerate(self.departures[:3]):
            minutes = departure['minutes_until']
            direction = departure['direction_name']
            route = departure.get('route_number', '')
            platform = departure.get('platform_number', '')

            # Time until departure
            if minutes <= 0:
                time_text = "NOW"
                time_color = (255, 100, 100)  # Red for imminent
            elif minutes <= 5:
                time_text = f"{minutes} min"
                time_color = (255, 200, 100)  # Orange for soon
            else:
                time_text = f"{minutes} min"
                time_color = theme_colors['text_color']

            time_surface = time_font.render(time_text, True, time_color)
            screen.blit(time_surface, (x, y))

            # Direction and details
            details = direction
            if route:
                details = f"{route} - {details}"
            if platform:
                details += f" (Platform {platform})"

            detail_surface = detail_font.render(details, True, theme_colors['secondary_color'])
            screen.blit(detail_surface, (x + 150, y + 10))

            y += 60

    def draw_compact(self, screen, position, theme_colors=None):
        """
        Draw a compact version showing just next departure

        Args:
            screen: Pygame screen
            position: (x, y) tuple for panel position
            theme_colors: Optional dict with color keys
        """
        if not self.departures:
            return

        # Default colors if theme not provided
        if theme_colors is None:
            theme_colors = {
                'text_color': (255, 255, 255),
                'accent_color': (100, 150, 255),
                'secondary_color': (180, 180, 180)
            }

        x, y = position

        # Fonts
        label_font = pygame.font.Font(None, 24)
        time_font = pygame.font.Font(None, 36)

        next_dep = self.departures[0]
        minutes = next_dep['minutes_until']
        route = next_dep.get('route_number', '')

        # Label
        label = f"Next {'train' if route else 'tram'}"
        if route:
            label += f" ({route})"
        label += ":"

        label_surface = label_font.render(label, True, theme_colors['secondary_color'])
        screen.blit(label_surface, (x, y))

        # Time
        if minutes <= 0:
            time_text = "NOW"
            time_color = (255, 100, 100)
        elif minutes <= 5:
            time_text = f"{minutes} min"
            time_color = (255, 200, 100)
        else:
            time_text = f"{minutes} min"
            time_color = theme_colors['text_color']

        time_surface = time_font.render(time_text, True, time_color)
        time_rect = time_surface.get_rect(left=x, top=y + 25)
        screen.blit(time_surface, time_rect)
