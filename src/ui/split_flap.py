"""
Split-flap display component for retro clock aesthetic
"""
import pygame
from typing import Tuple
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from digital_font import DigitalFont


class SplitFlapDigit:
    """Single digit in split-flap display style"""

    def __init__(self, width=80, height=120):
        """
        Initialize split-flap digit

        Args:
            width: Width of the digit display
            height: Height of the digit display
        """
        self.width = width
        self.height = height
        self.current_value = "0"
        self.target_value = "0"

        # Animation state
        self.flip_progress = 0.0  # 0.0 to 1.0
        self.is_flipping = False
        self.flip_speed = 0.15  # How fast the flap flips

    def set_value(self, value: str):
        """Set target value and trigger flip animation"""
        if value == self.current_value:
            return
        if self.is_flipping and self.target_value == value:
            return  # already animating toward this value
        self.target_value = value
        self.is_flipping = True
        self.flip_progress = 0.0

    def update(self):
        """Update animation state"""
        if self.is_flipping:
            self.flip_progress += self.flip_speed

            if self.flip_progress >= 1.0:
                self.flip_progress = 0.0
                self.is_flipping = False
                self.current_value = self.target_value

    def draw(self, surface, position, font, colors):
        """
        Draw the split-flap digit

        Args:
            surface: Pygame surface to draw on
            position: (x, y) tuple
            font: Font to use
            colors: Dict with 'bg', 'text', 'shadow', 'highlight' keys
        """
        x, y = position

        # Background panel (dark)
        panel_rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(surface, colors['bg'], panel_rect, border_radius=5)

        # Border/frame effect
        pygame.draw.rect(surface, colors['shadow'], panel_rect, 2, border_radius=5)

        # Split line in the middle
        mid_y = y + self.height // 2
        pygame.draw.line(surface, colors['shadow'], (x, mid_y), (x + self.width, mid_y), 2)

        # Draw current digit
        if self.is_flipping:
            # During flip animation
            # Top half shows current, bottom half transitions
            self._draw_flipping_digit(surface, position, font, colors)
        else:
            # Static display
            self._draw_static_digit(surface, position, font, colors, self.current_value)

        # Add shine/reflection effect on top half
        shine_rect = pygame.Rect(x + 5, y + 5, self.width - 10, self.height // 2 - 10)
        shine_surface = pygame.Surface((shine_rect.width, shine_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shine_surface, (*colors['highlight'], 20), shine_surface.get_rect(), border_radius=3)
        surface.blit(shine_surface, shine_rect.topleft)

    def _draw_static_digit(self, surface, position, font, colors, digit):
        """Draw a static digit in 7-segment digital style"""
        x, y = position

        # Calculate digit display area (with padding)
        padding = 15
        digit_width = self.width - 2 * padding
        digit_height = self.height - 2 * padding

        # Center position for the digit
        digit_x = x + padding
        digit_y = y + padding

        # Draw digital 7-segment digit
        # Create dim version for "off" segments
        off_color = tuple(min(c + 15, 255) for c in colors['bg'])

        DigitalFont.draw_digit(
            surface, digit,
            digit_x, digit_y,
            digit_width, digit_height,
            colors['text'],
            off_color=off_color
        )

    def _draw_flipping_digit(self, surface, position, font, colors):
        """Draw digit during flip animation"""
        x, y = position
        mid_y = y + self.height // 2

        # Top half - shows old digit
        top_clip = pygame.Rect(x, y, self.width, self.height // 2)
        surface.set_clip(top_clip)
        self._draw_static_digit(surface, position, font, colors, self.current_value)
        surface.set_clip(None)

        # Bottom half - transitions to new digit
        # Calculate flip perspective
        flip_scale = abs(self.flip_progress - 0.5) * 2  # 1.0 -> 0.0 -> 1.0

        bottom_clip = pygame.Rect(x, mid_y, self.width, self.height // 2)
        surface.set_clip(bottom_clip)

        # Show current digit when flip < 0.5, target when flip > 0.5
        display_digit = self.current_value if self.flip_progress < 0.5 else self.target_value

        # Apply vertical scaling for flip effect
        if flip_scale > 0.1:  # Avoid division by very small numbers
            self._draw_static_digit(surface, position, font, colors, display_digit)

        surface.set_clip(None)


class SplitFlapDisplay:
    """Multi-digit split-flap display"""

    def __init__(self, num_digits=4, digit_width=80, digit_height=120, spacing=10):
        """
        Initialize split-flap display

        Args:
            num_digits: Number of digits
            digit_width: Width of each digit
            digit_height: Height of each digit
            spacing: Space between digits
        """
        self.num_digits = num_digits
        self.digit_width = digit_width
        self.digit_height = digit_height
        self.spacing = spacing

        self.digits = [SplitFlapDigit(digit_width, digit_height) for _ in range(num_digits)]

        # Calculate total width
        self.total_width = (num_digits * digit_width) + ((num_digits - 1) * spacing)
        self.total_height = digit_height

    def set_time(self, time_str: str):
        """
        Set time string (e.g., "12:34")

        Args:
            time_str: Time string, can include ':'
        """
        # Remove colons and other separators
        digits_only = ''.join(c for c in time_str if c.isdigit())

        # Pad with zeros if needed
        while len(digits_only) < self.num_digits:
            digits_only = '0' + digits_only

        # Set each digit
        for i, digit in enumerate(digits_only[:self.num_digits]):
            self.digits[i].set_value(digit)

    def update(self):
        """Update all digit animations"""
        for digit in self.digits:
            digit.update()

    def draw(self, surface, position, font, colors, show_colon=True):
        """
        Draw the complete display

        Args:
            surface: Pygame surface
            position: (x, y) center position
            font: Font to use
            colors: Color dict
            show_colon: Whether to show colon between hours and minutes
        """
        # Calculate starting x position (centered)
        x, y = position
        start_x = x - (self.total_width // 2)
        start_y = y - (self.total_height // 2)

        current_x = start_x

        for i, digit in enumerate(self.digits):
            digit.draw(surface, (current_x, start_y), font, colors)
            current_x += self.digit_width + self.spacing

            # Draw colon after 2nd digit (between hours and minutes)
            if show_colon and i == 1:
                self._draw_colon(surface, (current_x - self.spacing, start_y), colors)

    def _draw_colon(self, surface, position, colors):
        """Draw colon separator"""
        x, y = position
        colon_y_offset = self.digit_height // 3
        colon_radius = 5

        # Top dot
        pygame.draw.circle(surface, colors['text'], (x, y + colon_y_offset), colon_radius)
        # Bottom dot
        pygame.draw.circle(surface, colors['text'], (x, y + self.digit_height - colon_y_offset), colon_radius)

        # Add shadow
        pygame.draw.circle(surface, colors['shadow'], (x + 1, y + colon_y_offset + 1), colon_radius)
        pygame.draw.circle(surface, colors['shadow'], (x + 1, y + self.digit_height - colon_y_offset + 1), colon_radius)
