"""
Digital 7-segment style font renderer
"""
import pygame
from typing import Tuple


class DigitalFont:
    """Renders digits in 7-segment LED display style"""

    # 7-segment display mapping
    #     _a_
    #   f|   |b
    #     _g_
    #   e|   |c
    #     _d_

    SEGMENTS = {
        '0': ['a', 'b', 'c', 'd', 'e', 'f'],
        '1': ['b', 'c'],
        '2': ['a', 'b', 'g', 'e', 'd'],
        '3': ['a', 'b', 'g', 'c', 'd'],
        '4': ['f', 'g', 'b', 'c'],
        '5': ['a', 'f', 'g', 'c', 'd'],
        '6': ['a', 'f', 'g', 'e', 'd', 'c'],
        '7': ['a', 'b', 'c'],
        '8': ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
        '9': ['a', 'b', 'c', 'd', 'f', 'g'],
        ' ': [],
    }

    @staticmethod
    def draw_digit(surface, digit, x, y, width, height, color, off_color=None, segment_thickness=None):
        """
        Draw a single digit in 7-segment style

        Args:
            surface: Pygame surface to draw on
            digit: Character to draw ('0'-'9' or ' ')
            x, y: Top-left position
            width, height: Size of the digit
            color: Color for active segments
            off_color: Color for inactive segments (None to hide)
            segment_thickness: Thickness of segments (None for auto)
        """
        if digit not in DigitalFont.SEGMENTS:
            return

        # Auto-calculate segment thickness
        if segment_thickness is None:
            segment_thickness = max(height // 15, 3)

        # Padding
        pad = segment_thickness // 2

        # Calculate segment positions
        # Horizontal segments (a, g, d)
        h_length = width - 2 * pad
        h_start_x = x + pad
        h_end_x = x + width - pad

        # Vertical segments (b, c, e, f)
        v_length = (height - 3 * pad) // 2
        v_top_end = y + v_length + pad
        v_bottom_start = y + v_length + 2 * pad

        # Segment coordinates
        segments_coords = {
            'a': [(h_start_x, y + pad), (h_end_x, y + pad)],  # Top horizontal
            'b': [(x + width - pad, y + pad), (x + width - pad, v_top_end)],  # Top right vertical
            'c': [(x + width - pad, v_bottom_start), (x + width - pad, y + height - pad)],  # Bottom right vertical
            'd': [(h_start_x, y + height - pad), (h_end_x, y + height - pad)],  # Bottom horizontal
            'e': [(x + pad, v_bottom_start), (x + pad, y + height - pad)],  # Bottom left vertical
            'f': [(x + pad, y + pad), (x + pad, v_top_end)],  # Top left vertical
            'g': [(h_start_x, y + height // 2), (h_end_x, y + height // 2)],  # Middle horizontal
        }

        active_segments = DigitalFont.SEGMENTS[digit]

        # Draw all segments
        for segment, coords in segments_coords.items():
            is_active = segment in active_segments
            seg_color = color if is_active else off_color

            if seg_color is None and not is_active:
                continue

            # Draw the segment with rounded ends
            pygame.draw.line(surface, seg_color, coords[0], coords[1], segment_thickness)

            # Add rounded ends
            pygame.draw.circle(surface, seg_color, coords[0], segment_thickness // 2)
            pygame.draw.circle(surface, seg_color, coords[1], segment_thickness // 2)

    @staticmethod
    def render_text(surface, text, x, y, digit_width, digit_height, spacing, color, off_color=None):
        """
        Render a string of digits

        Args:
            surface: Pygame surface
            text: String to render
            x, y: Starting position
            digit_width: Width of each digit
            digit_height: Height of each digit
            spacing: Space between digits
            color: Active segment color
            off_color: Inactive segment color
        """
        current_x = x

        for char in text:
            if char == ':':
                # Draw colon as two dots
                dot_radius = digit_height // 15
                dot_y1 = y + digit_height // 3
                dot_y2 = y + 2 * digit_height // 3
                dot_x = current_x + spacing // 2

                pygame.draw.circle(surface, color, (dot_x, dot_y1), dot_radius)
                pygame.draw.circle(surface, color, (dot_x, dot_y2), dot_radius)

                current_x += spacing
            elif char in DigitalFont.SEGMENTS:
                DigitalFont.draw_digit(
                    surface, char, current_x, y,
                    digit_width, digit_height,
                    color, off_color
                )
                current_x += digit_width + spacing
            else:
                # Unknown character, skip
                current_x += spacing

    @staticmethod
    def get_text_width(text, digit_width, spacing):
        """Calculate the width of rendered text"""
        width = 0
        for char in text:
            if char == ':':
                width += spacing
            elif char in DigitalFont.SEGMENTS:
                width += digit_width + spacing
            else:
                width += spacing

        return width - spacing if width > 0 else 0  # Remove last spacing
