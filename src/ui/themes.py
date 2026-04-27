"""
Seasonal theme system for the alarm clock
"""
from datetime import datetime
from typing import Dict, Tuple


class ThemeManager:
    """Manages seasonal themes and color schemes"""

    def __init__(self):
        """Initialize theme manager"""
        self.themes = {
            "summer": {
                "name": "Summer",
                "bg_color": (230, 240, 250),  # Soft sky blue
                "text_color": (80, 100, 140),  # Deep blue-gray
                "accent_color": (255, 200, 100),  # Sunny yellow
                "secondary_color": (100, 180, 220),  # Ocean blue
                # Mushroom colors - DARKER for contrast on light background
                "mushroom_caps": [(200, 60, 80), (220, 120, 40), (40, 140, 200)],  # Deep coral, orange, ocean blue
                "mushroom_stems": (140, 100, 70),  # Dark tan
                "vine_color": (60, 120, 60),  # Dark green
                "flower_petal": (200, 80, 120),  # Deep pink
                "flower_center": (220, 160, 40),  # Golden yellow
            },
            "autumn": {
                "name": "Autumn",
                "bg_color": (245, 235, 220),  # Warm beige
                "text_color": (100, 70, 50),  # Deep brown
                "accent_color": (220, 120, 60),  # Burnt orange
                "secondary_color": (200, 160, 100),  # Golden brown
                # Mushroom colors - DARKER for contrast
                "mushroom_caps": [(150, 50, 40), (140, 90, 30), (120, 60, 60)],  # Deep rust, dark ochre, burgundy
                "mushroom_stems": (120, 90, 70),  # Dark brown
                "vine_color": (100, 130, 60),  # Olive green
                "flower_petal": (180, 70, 50),  # Deep rust
                "flower_center": (200, 140, 60),  # Amber
            },
            "winter": {
                "name": "Winter",
                "bg_color": (235, 240, 245),  # Icy white-blue
                "text_color": (60, 80, 100),  # Cool gray-blue
                "accent_color": (150, 200, 230),  # Ice blue
                "secondary_color": (200, 210, 230),  # Frost
                # Mushroom colors - DARKER for contrast
                "mushroom_caps": [(80, 100, 140), (60, 80, 120), (100, 60, 120)],  # Deep blue, navy, purple-blue
                "mushroom_stems": (100, 110, 130),  # Dark gray-blue
                "vine_color": (70, 100, 90),  # Dark teal
                "flower_petal": (140, 160, 200),  # Medium blue
                "flower_center": (200, 200, 220),  # Light gray
            },
            "spring": {
                "name": "Spring",
                "bg_color": (240, 250, 240),  # Mint green tint
                "text_color": (70, 100, 80),  # Forest green
                "accent_color": (140, 200, 120),  # Fresh green
                "secondary_color": (255, 180, 200),  # Cherry blossom pink
                # Mushroom colors - DARKER for contrast
                "mushroom_caps": [(200, 80, 120), (140, 60, 180), (60, 160, 100)],  # Deep pink, purple, forest green
                "mushroom_stems": (100, 120, 90),  # Dark olive
                "vine_color": (60, 140, 80),  # Rich green
                "flower_petal": (220, 100, 150),  # Vibrant pink
                "flower_center": (240, 200, 80),  # Bright yellow
            }
        }

        self.current_theme = self.get_current_season_theme()

    def get_season_from_date(self, date: datetime = None) -> str:
        """
        Get the current season based on Australian seasons
        Summer: Dec, Jan, Feb
        Autumn: Mar, Apr, May
        Winter: Jun, Jul, Aug
        Spring: Sep, Oct, Nov
        """
        if date is None:
            date = datetime.now()

        month = date.month

        if month in [12, 1, 2]:
            return "summer"
        elif month in [3, 4, 5]:
            return "autumn"
        elif month in [6, 7, 8]:
            return "winter"
        else:  # 9, 10, 11
            return "spring"

    def get_current_season_theme(self) -> Dict:
        """Get the theme for the current season"""
        season = self.get_season_from_date()
        return self.themes[season]

    def get_theme(self, theme_name: str = None) -> Dict:
        """Get a specific theme or current seasonal theme"""
        if theme_name and theme_name in self.themes:
            return self.themes[theme_name]
        return self.current_theme

    def get_color(self, color_name: str) -> Tuple[int, int, int]:
        """Get a specific color from the current theme"""
        return self.current_theme.get(color_name, (255, 255, 255))

    def update_season(self):
        """Update theme based on current season (call this periodically)"""
        self.current_theme = self.get_current_season_theme()
        return self.current_theme
