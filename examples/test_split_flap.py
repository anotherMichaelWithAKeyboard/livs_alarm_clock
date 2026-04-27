#!/usr/bin/env python3
"""
Test the split-flap display component
"""
import pygame
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ui.split_flap import SplitFlapDisplay


def main():
    """Test split-flap display"""
    pygame.init()

    # Create display
    width, height = 800, 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Split-Flap Display Test")

    # Create split-flap display
    split_flap = SplitFlapDisplay(
        num_digits=4,
        digit_width=90,
        digit_height=140,
        spacing=15
    )

    # Colors
    bg_color = (20, 20, 30)
    flap_colors = {
        'bg': (40, 40, 50),
        'text': (255, 255, 255),
        'shadow': (0, 0, 0),
        'highlight': (255, 255, 255)
    }

    # Font
    font = pygame.font.Font(None, 120)
    info_font = pygame.font.Font(None, 32)

    # Test sequence
    test_times = ["12:00", "12:01", "12:59", "01:00", "11:59"]
    current_time_idx = 0
    split_flap.set_time(test_times[current_time_idx])

    clock = pygame.time.Clock()
    running = True

    print("Split-Flap Display Test")
    print("=" * 50)
    print("Controls:")
    print("  SPACE - Next time in sequence")
    print("  ESC   - Quit")
    print()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Next time in sequence
                    current_time_idx = (current_time_idx + 1) % len(test_times)
                    new_time = test_times[current_time_idx]
                    split_flap.set_time(new_time)
                    print(f"Setting time to: {new_time}")

        # Update animation
        split_flap.update()

        # Draw
        screen.fill(bg_color)

        # Draw split-flap in center
        center_pos = (width // 2, height // 2)
        split_flap.draw(screen, center_pos, font, flap_colors, show_colon=True)

        # Draw instructions
        info_text = "Press SPACE to advance time | ESC to quit"
        info_surface = info_font.render(info_text, True, (180, 180, 180))
        info_rect = info_surface.get_rect(center=(width // 2, height - 40))
        screen.blit(info_surface, info_rect)

        # Draw current test time
        current_text = f"Showing: {test_times[current_time_idx]}"
        current_surface = info_font.render(current_text, True, (255, 200, 100))
        current_rect = current_surface.get_rect(center=(width // 2, 40))
        screen.blit(current_surface, current_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("\nTest complete!")


if __name__ == "__main__":
    main()
