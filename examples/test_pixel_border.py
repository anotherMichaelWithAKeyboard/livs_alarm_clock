#!/usr/bin/env python3
"""
Test the pixel art border
"""
import pygame
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ui.pixel_border import PixelBorder


def main():
    """Test pixel border"""
    pygame.init()

    # Create display
    width, height = 800, 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pixel Border Test")

    # Create pixel border
    border = PixelBorder(width, height)

    # Colors
    bg_color = (20, 20, 30)

    # Font
    info_font = pygame.font.Font(None, 32)
    title_font = pygame.font.Font(None, 48)

    clock = pygame.time.Clock()
    running = True
    frame_count = 0

    print("Pixel Border Test")
    print("=" * 50)
    print("Watch the mushroom people gently bob!")
    print("Press ESC to quit")
    print()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Draw
        screen.fill(bg_color)

        # Draw animated border
        border.draw_animated(screen, frame_count)

        # Draw title in center
        title_text = "Pixel Art Border"
        title_surface = title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(width // 2, height // 2 - 40))

        # Add shadow
        title_shadow = title_font.render(title_text, True, (0, 0, 0))
        shadow_rect = title_shadow.get_rect(center=(title_rect.centerx + 2, title_rect.centery + 2))
        screen.blit(title_shadow, shadow_rect)
        screen.blit(title_surface, title_rect)

        # Draw info
        info_lines = [
            "🍄 Mushroom People",
            "🌿 Vines & Flowers",
            "⭐ Decorative Stars"
        ]

        y = height // 2 + 20
        for line in info_lines:
            info_surface = info_font.render(line, True, (200, 200, 200))
            info_rect = info_surface.get_rect(center=(width // 2, y))
            screen.blit(info_surface, info_rect)
            y += 35

        # Instructions
        esc_text = "Press ESC to quit"
        esc_surface = info_font.render(esc_text, True, (150, 150, 150))
        esc_rect = esc_surface.get_rect(center=(width // 2, height - 30))
        screen.blit(esc_surface, esc_rect)

        pygame.display.flip()
        clock.tick(30)
        frame_count += 1

    pygame.quit()
    print("\nTest complete!")


if __name__ == "__main__":
    main()
