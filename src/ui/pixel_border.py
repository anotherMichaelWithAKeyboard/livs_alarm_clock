"""
Pixelated decorative border with vines and mushroom people
"""
import pygame
import random
from typing import List, Tuple


class PixelArt:
    """Pixel art patterns for decorative elements"""

    # Pixel size for all art
    PIXEL_SIZE = 4

    @staticmethod
    def mushroom_person_1(cap_color, stem_color):
        """
        Mushroom person sprite (standing)
        Returns list of (x, y, color) tuples
        """
        spots = tuple(min(255, c + 50) for c in cap_color)  # Lighter spots
        face = tuple(max(0, c - 30) for c in stem_color)    # Darker face
        feet = tuple(max(0, c - 50) for c in stem_color)    # Even darker feet

        pattern = [
            # Mushroom cap (top)
            (2, 0, cap_color), (3, 0, cap_color), (4, 0, cap_color), (5, 0, cap_color),
            (1, 1, cap_color), (2, 1, cap_color), (3, 1, cap_color), (4, 1, cap_color), (5, 1, cap_color), (6, 1, cap_color),
            (1, 2, cap_color), (2, 2, spots), (3, 2, cap_color), (4, 2, cap_color), (5, 2, spots), (6, 2, cap_color),
            (2, 3, cap_color), (3, 3, cap_color), (4, 3, cap_color), (5, 3, cap_color),

            # Face/body
            (3, 4, stem_color), (4, 4, stem_color),
            (2, 5, stem_color), (3, 5, face), (4, 5, face), (5, 5, stem_color),
            (2, 6, stem_color), (3, 6, stem_color), (4, 6, stem_color), (5, 6, stem_color),
            (2, 7, stem_color), (3, 7, stem_color), (4, 7, stem_color), (5, 7, stem_color),

            # Feet
            (1, 8, feet), (2, 8, feet), (5, 8, feet), (6, 8, feet),
        ]
        return pattern

    @staticmethod
    def mushroom_person_2(cap_color, stem_color):
        """Mushroom person sprite (arms up)"""
        spots = tuple(min(255, c + 50) for c in cap_color)
        face = tuple(max(0, c - 30) for c in stem_color)

        pattern = [
            # Cap
            (2, 0, cap_color), (3, 0, cap_color), (4, 0, cap_color), (5, 0, cap_color),
            (1, 1, cap_color), (2, 1, spots), (3, 1, cap_color), (4, 1, cap_color), (5, 1, spots), (6, 1, cap_color),
            (1, 2, cap_color), (2, 2, cap_color), (3, 2, cap_color), (4, 2, cap_color), (5, 2, cap_color), (6, 2, cap_color),

            # Arms up
            (0, 3, stem_color), (7, 3, stem_color),
            (1, 4, stem_color), (6, 4, stem_color),

            # Body
            (3, 4, stem_color), (4, 4, stem_color),
            (2, 5, stem_color), (3, 5, face), (4, 5, face), (5, 5, stem_color),
            (2, 6, stem_color), (3, 6, stem_color), (4, 6, stem_color), (5, 6, stem_color),
            (3, 7, stem_color), (4, 7, stem_color),
        ]
        return pattern

    @staticmethod
    def mushroom_person_3(cap_color, stem_color):
        """Mushroom person sprite (small/squat)"""
        spots = tuple(min(255, c + 50) for c in cap_color)
        face = tuple(max(0, c - 30) for c in stem_color)

        pattern = [
            # Wide cap
            (1, 0, cap_color), (2, 0, cap_color), (3, 0, cap_color), (4, 0, cap_color), (5, 0, cap_color),
            (0, 1, cap_color), (1, 1, spots), (2, 1, cap_color), (3, 1, cap_color), (4, 1, spots), (5, 1, cap_color), (6, 1, cap_color),
            (1, 2, cap_color), (2, 2, cap_color), (3, 2, cap_color), (4, 2, cap_color), (5, 2, cap_color),

            # Short body
            (2, 3, stem_color), (3, 3, face), (4, 3, face), (5, 3, stem_color),
            (2, 4, stem_color), (3, 4, stem_color), (4, 4, stem_color), (5, 4, stem_color),
        ]
        return pattern

    @staticmethod
    def vine_segment(vine_color):
        """Vine/plant segment with theme color"""
        leaf = tuple(min(255, c + 40) for c in vine_color)  # Lighter leaf

        pattern = [
            (1, 0, vine_color),
            (1, 1, vine_color), (2, 1, leaf),
            (1, 2, vine_color),
            (0, 3, leaf), (1, 3, vine_color),
            (1, 4, vine_color),
            (1, 5, vine_color), (2, 5, leaf),
        ]
        return pattern

    @staticmethod
    def small_mushroom(cap_color, stem_color):
        """Small decorative mushroom with theme colors"""
        pattern = [
            (1, 0, cap_color), (2, 0, cap_color),
            (0, 1, cap_color), (1, 1, cap_color), (2, 1, cap_color), (3, 1, cap_color),
            (1, 2, stem_color), (2, 2, stem_color),
            (1, 3, stem_color), (2, 3, stem_color),
        ]
        return pattern

    @staticmethod
    def flower(petal_color, center_color, stem_color):
        """Small pixel flower with theme colors"""
        pattern = [
            (1, 0, petal_color), (3, 0, petal_color),
            (0, 1, petal_color), (2, 1, center_color), (4, 1, petal_color),
            (1, 2, petal_color), (3, 2, petal_color),
            (2, 3, stem_color),
            (2, 4, stem_color),
        ]
        return pattern

    # RARE MUSHROOM VARIANTS

    @staticmethod
    def mushroom_tall(cap_color, stem_color):
        """Uncommon: Tall thin mushroom (20% spawn rate)"""
        spots = tuple(min(255, c + 50) for c in cap_color)
        face = tuple(max(0, c - 30) for c in stem_color)

        pattern = [
            # Narrow cap
            (2, 0, cap_color), (3, 0, cap_color), (4, 0, cap_color),
            (1, 1, cap_color), (2, 1, spots), (3, 1, cap_color), (4, 1, spots), (5, 1, cap_color),
            (2, 2, cap_color), (3, 2, cap_color), (4, 2, cap_color),

            # Tall thin body
            (3, 3, stem_color),
            (3, 4, stem_color),
            (2, 5, stem_color), (3, 5, face), (4, 5, stem_color),
            (2, 6, stem_color), (3, 6, stem_color), (4, 6, stem_color),
            (3, 7, stem_color),
            (3, 8, stem_color),
            (3, 9, stem_color),
        ]
        return pattern

    @staticmethod
    def mushroom_crowned(cap_color, stem_color):
        """Rare: Mushroom with crown-like cap (10% spawn rate)"""
        spots = tuple(min(255, c + 60) for c in cap_color)
        face = tuple(max(0, c - 30) for c in stem_color)
        crown = tuple(min(255, c + 80) for c in cap_color)  # Bright crown

        pattern = [
            # Crown points
            (1, 0, crown), (3, 0, crown), (5, 0, crown),
            # Cap
            (0, 1, cap_color), (1, 1, cap_color), (2, 1, cap_color), (3, 1, cap_color), (4, 1, cap_color), (5, 1, cap_color), (6, 1, cap_color),
            (1, 2, cap_color), (2, 2, spots), (3, 2, cap_color), (4, 2, spots), (5, 2, cap_color),
            (2, 3, cap_color), (3, 3, cap_color), (4, 3, cap_color),

            # Body
            (2, 4, stem_color), (3, 4, face), (4, 4, face), (5, 4, stem_color),
            (2, 5, stem_color), (3, 5, stem_color), (4, 5, stem_color), (5, 5, stem_color),
            (3, 6, stem_color), (4, 6, stem_color),
        ]
        return pattern

    @staticmethod
    def mushroom_spotted_giant(cap_color, stem_color):
        """Very Rare: Giant mushroom with many spots (5% spawn rate)"""
        spots1 = tuple(min(255, c + 50) for c in cap_color)
        spots2 = tuple(min(255, c + 70) for c in cap_color)
        face = tuple(max(0, c - 30) for c in stem_color)

        pattern = [
            # Large cap with multiple spot sizes
            (3, 0, cap_color), (4, 0, cap_color), (5, 0, cap_color), (6, 0, cap_color),
            (2, 1, cap_color), (3, 1, spots2), (4, 1, cap_color), (5, 1, cap_color), (6, 1, spots2), (7, 1, cap_color),
            (1, 2, cap_color), (2, 2, cap_color), (3, 2, cap_color), (4, 2, spots1), (5, 2, cap_color), (6, 2, cap_color), (7, 2, cap_color), (8, 2, cap_color),
            (1, 3, cap_color), (2, 3, spots1), (3, 3, cap_color), (4, 3, cap_color), (5, 3, cap_color), (6, 3, spots1), (7, 3, cap_color), (8, 3, cap_color),
            (2, 4, cap_color), (3, 4, cap_color), (4, 4, cap_color), (5, 4, cap_color), (6, 4, cap_color), (7, 4, cap_color),

            # Thick body
            (3, 5, stem_color), (4, 5, stem_color), (5, 5, stem_color), (6, 5, stem_color),
            (3, 6, stem_color), (4, 6, face), (5, 6, face), (6, 6, stem_color),
            (3, 7, stem_color), (4, 7, stem_color), (5, 7, stem_color), (6, 7, stem_color),
            (3, 8, stem_color), (4, 8, stem_color), (5, 8, stem_color), (6, 8, stem_color),
        ]
        return pattern

    @staticmethod
    def mushroom_queen(cap_color, stem_color):
        """LEGENDARY: Mushroom Queen (1% spawn rate) - Glowing, majestic!"""
        # Create rainbow/glowing effect
        glow1 = tuple(min(255, c + 100) for c in cap_color)
        glow2 = tuple(min(255, c + 80) for c in cap_color)
        spots = tuple(min(255, c + 120) for c in cap_color)
        face = tuple(max(0, c - 20) for c in stem_color)
        crown = (255, 220, 100)  # Golden crown

        pattern = [
            # Royal crown
            (4, 0, crown), (5, 0, crown), (6, 0, crown),
            (3, 1, crown), (4, 1, crown), (5, 1, crown), (6, 1, crown), (7, 1, crown),

            # Glowing cap with ornate spots
            (2, 2, glow1), (3, 2, glow2), (4, 2, cap_color), (5, 2, cap_color), (6, 2, glow2), (7, 2, glow1),
            (1, 3, glow1), (2, 3, cap_color), (3, 3, spots), (4, 3, cap_color), (5, 3, cap_color), (6, 3, spots), (7, 3, cap_color), (8, 3, glow1),
            (0, 4, cap_color), (1, 4, cap_color), (2, 4, cap_color), (3, 4, cap_color), (4, 4, spots), (5, 4, cap_color), (6, 4, cap_color), (7, 4, cap_color), (8, 4, cap_color), (9, 4, cap_color),
            (1, 5, cap_color), (2, 5, spots), (3, 5, cap_color), (4, 5, cap_color), (5, 5, cap_color), (6, 5, cap_color), (7, 5, spots), (8, 5, cap_color),
            (2, 6, cap_color), (3, 6, cap_color), (4, 6, cap_color), (5, 6, cap_color), (6, 6, cap_color), (7, 6, cap_color),

            # Regal body with dress-like bottom
            (3, 7, stem_color), (4, 7, stem_color), (5, 7, stem_color), (6, 7, stem_color),
            (3, 8, stem_color), (4, 8, face), (5, 8, face), (6, 8, stem_color),
            (2, 9, stem_color), (3, 9, stem_color), (4, 9, stem_color), (5, 9, stem_color), (6, 9, stem_color), (7, 9, stem_color),
            (2, 10, stem_color), (3, 10, stem_color), (4, 10, stem_color), (5, 10, stem_color), (6, 10, stem_color), (7, 10, stem_color),
            (1, 11, stem_color), (2, 11, stem_color), (3, 11, stem_color), (4, 11, stem_color), (5, 11, stem_color), (6, 11, stem_color), (7, 11, stem_color), (8, 11, stem_color),
        ]
        return pattern

    @staticmethod
    def tiny_star():
        """Tiny decorative star"""
        star = (255, 255, 200)   # Yellow star

        pattern = [
            (1, 0, star),
            (0, 1, star), (1, 1, star), (2, 1, star),
            (1, 2, star),
        ]
        return pattern


class PixelBorder:
    """Decorative pixelated border renderer"""

    def __init__(self, screen_width, screen_height, theme=None):
        """Initialize pixel border"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pixel_size = PixelArt.PIXEL_SIZE
        self.border_thickness = 50  # Pixels from edge

        # Store theme for mushroom colors
        self.theme = theme

        # Generate border elements with size variations
        self.elements = self._generate_border_elements()

    def _roll_for_mushroom_type(self):
        """
        Roll for mushroom type based on rarity
        Returns: mushroom type string

        Rarity rates:
        - Common (mushroom1, mushroom2, mushroom3): 64%
        - Uncommon (mushroom_tall): 20%
        - Rare (mushroom_crowned): 10%
        - Very Rare (mushroom_spotted_giant): 5%
        - Legendary (mushroom_queen): 1%
        """
        roll = random.random() * 100

        if roll < 1:  # 1%
            return 'mushroom_queen'
        elif roll < 6:  # 5%
            return 'mushroom_spotted_giant'
        elif roll < 16:  # 10%
            return 'mushroom_crowned'
        elif roll < 36:  # 20%
            return 'mushroom_tall'
        else:  # 64%
            return random.choice(['mushroom1', 'mushroom2', 'mushroom3'])

    def _generate_border_elements(self) -> List[Tuple]:
        """Generate random placement of border elements with size/color variations"""
        elements = []
        random.seed(42)  # Consistent layout

        # Get colors from theme
        cap_colors = self.theme.get('mushroom_caps', [(200, 50, 50), (150, 100, 200), (255, 150, 100)]) if self.theme else [(200, 50, 50), (150, 100, 200)]
        stem_color = self.theme.get('mushroom_stems', (240, 220, 200)) if self.theme else (240, 220, 200)
        vine_color = self.theme.get('vine_color', (60, 120, 60)) if self.theme else (60, 120, 60)
        flower_petal = self.theme.get('flower_petal', (200, 80, 120)) if self.theme else (200, 80, 120)
        flower_center = self.theme.get('flower_center', (220, 160, 40)) if self.theme else (220, 160, 40)

        # Top border - mushroom people and decorations
        x = 20
        while x < self.screen_width - 100:
            # Decide if this position gets a mushroom or decoration
            if random.random() < 0.7:  # 70% chance of mushroom
                element_type = self._roll_for_mushroom_type()
                size_variation = random.uniform(0.9, 1.1)
            else:  # 30% chance of vine/flower/small mushroom
                element_type = random.choice(['vine', 'small_mushroom', 'flower'])
                size_variation = 1.0

            cap_color = random.choice(cap_colors)
            elements.append((element_type, x, 10, size_variation, cap_color, stem_color, vine_color, flower_petal, flower_center))
            x += random.randint(40, 80)

        # Bottom border - mushroom people and decorations
        x = 20
        while x < self.screen_width - 100:
            if random.random() < 0.7:  # 70% chance of mushroom
                element_type = self._roll_for_mushroom_type()
                size_variation = random.uniform(0.9, 1.1)
            else:
                element_type = random.choice(['vine', 'small_mushroom', 'flower'])
                size_variation = 1.0

            cap_color = random.choice(cap_colors)
            elements.append((element_type, x, self.screen_height - 40, size_variation, cap_color, stem_color, vine_color, flower_petal, flower_center))
            x += random.randint(40, 80)

        # Left border - vines growing up
        y = 80
        while y < self.screen_height - 100:
            element_type = random.choice(['vine', 'flower', 'tiny_star', 'small_mushroom'])
            cap_color = random.choice(cap_colors)
            elements.append((element_type, 10, y, 1.0, cap_color, stem_color, vine_color, flower_petal, flower_center))
            y += random.randint(30, 60)

        # Right border - vines growing up
        y = 80
        while y < self.screen_height - 100:
            element_type = random.choice(['vine', 'flower', 'tiny_star', 'small_mushroom'])
            cap_color = random.choice(cap_colors)
            elements.append((element_type, self.screen_width - 30, y, 1.0, cap_color, stem_color, vine_color, flower_petal, flower_center))
            y += random.randint(30, 60)

        # Add some scattered stars in corners
        for _ in range(5):
            elements.append(('tiny_star', random.randint(10, 60), random.randint(50, 80), 1.0, cap_colors[0], stem_color, vine_color, flower_petal, flower_center))
            elements.append(('tiny_star', random.randint(self.screen_width - 60, self.screen_width - 10),
                           random.randint(50, 80), 1.0, cap_colors[0], stem_color, vine_color, flower_petal, flower_center))

        return elements

    def _get_pattern(self, element_type, cap_color, stem_color, vine_color, flower_petal, flower_center):
        """Get pixel pattern for element type with seasonal colors"""
        patterns = {
            # Common mushrooms
            'mushroom1': PixelArt.mushroom_person_1(cap_color, stem_color),
            'mushroom2': PixelArt.mushroom_person_2(cap_color, stem_color),
            'mushroom3': PixelArt.mushroom_person_3(cap_color, stem_color),
            # Rare mushrooms
            'mushroom_tall': PixelArt.mushroom_tall(cap_color, stem_color),
            'mushroom_crowned': PixelArt.mushroom_crowned(cap_color, stem_color),
            'mushroom_spotted_giant': PixelArt.mushroom_spotted_giant(cap_color, stem_color),
            'mushroom_queen': PixelArt.mushroom_queen(cap_color, stem_color),
            # Decorations
            'vine': PixelArt.vine_segment(vine_color),
            'small_mushroom': PixelArt.small_mushroom(cap_color, stem_color),
            'flower': PixelArt.flower(flower_petal, flower_center, vine_color),
            'tiny_star': PixelArt.tiny_star(),
        }
        return patterns.get(element_type, [])

    def draw_pixel(self, surface, x, y, color, size_scale=1.0):
        """Draw a single pixel (scaled square) with size variation"""
        pixel_size = int(self.pixel_size * size_scale)
        rect = pygame.Rect(int(x * self.pixel_size * size_scale), int(y * self.pixel_size * size_scale),
                          pixel_size, pixel_size)
        pygame.draw.rect(surface, color, rect)

    def draw_pattern(self, surface, pattern, base_x, base_y, size_scale=1.0):
        """Draw a pixel art pattern at position with size variation"""
        for px, py, color in pattern:
            pixel_x = base_x + int(px * size_scale)
            pixel_y = base_y + int(py * size_scale)
            # Calculate screen position
            screen_x = int(pixel_x * self.pixel_size)
            screen_y = int(pixel_y * self.pixel_size)
            pixel_size = int(self.pixel_size * size_scale)
            rect = pygame.Rect(screen_x, screen_y, pixel_size, pixel_size)
            pygame.draw.rect(surface, color, rect)

    def draw(self, surface):
        """Draw the complete border"""
        for element_data in self.elements:
            element_type, x, y, size_var, cap_color, stem_color, vine_color, flower_petal, flower_center = element_data
            pattern = self._get_pattern(element_type, cap_color, stem_color, vine_color, flower_petal, flower_center)
            # Convert screen coordinates to pixel grid coordinates
            grid_x = x // self.pixel_size
            grid_y = y // self.pixel_size
            self.draw_pattern(surface, pattern, grid_x, grid_y, size_var)

    def draw_animated(self, surface, frame_count):
        """
        Draw border with subtle animation

        Args:
            surface: Pygame surface
            frame_count: Current frame number for animation
        """
        for i, element_data in enumerate(self.elements):
            element_type, x, y, size_var, cap_color, stem_color, vine_color, flower_petal, flower_center = element_data
            pattern = self._get_pattern(element_type, cap_color, stem_color, vine_color, flower_petal, flower_center)

            # Convert screen coordinates to pixel grid coordinates
            grid_x = x // self.pixel_size
            grid_y = y // self.pixel_size

            # Subtle bobbing animation for mushroom people
            if 'mushroom' in element_type:
                offset_y = int(2 * pygame.math.Vector2(0, 1).rotate(frame_count * 2 + i * 30).y)
                grid_y += offset_y // self.pixel_size

            self.draw_pattern(surface, pattern, grid_x, grid_y, size_var)
