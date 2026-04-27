"""
Photo frame mode - displays photos when idle
"""
import pygame
import os
import random
from pathlib import Path
from typing import List, Optional


class PhotoFrame:
    """Photo frame mode for displaying images when idle"""

    def __init__(self, photo_dir="assets/photos", idle_timeout=60):
        """
        Initialize photo frame

        Args:
            photo_dir: Directory containing photos
            idle_timeout: Seconds of inactivity before entering photo mode
        """
        self.photo_dir = Path(photo_dir)
        self.photo_dir.mkdir(parents=True, exist_ok=True)

        self.idle_timeout = idle_timeout
        self.last_activity = pygame.time.get_ticks()
        self.is_active = False

        self.photos: List[Path] = []
        self.current_photo_index = 0
        self.current_surface: Optional[pygame.Surface] = None

        self.photo_change_interval = 10000  # 10 seconds per photo
        self.last_photo_change = 0

        self.load_photos()

    def load_photos(self):
        """Load all photos from the photo directory"""
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

        self.photos = [
            f for f in self.photo_dir.iterdir()
            if f.is_file() and f.suffix.lower() in supported_formats
        ]

        if self.photos:
            random.shuffle(self.photos)

    def reload_photos(self):
        """Reload photos from directory (call when adding new photos)"""
        self.load_photos()
        self.current_photo_index = 0

    def register_activity(self):
        """Register user activity to reset idle timer"""
        self.last_activity = pygame.time.get_ticks()
        if self.is_active:
            self.is_active = False
            self.current_surface = None

    def should_activate(self) -> bool:
        """Check if photo frame mode should activate"""
        if not self.photos:
            return False

        current_time = pygame.time.get_ticks()
        idle_time = (current_time - self.last_activity) / 1000  # Convert to seconds

        return idle_time >= self.idle_timeout

    def update(self):
        """Update photo frame state"""
        if self.should_activate() and not self.is_active:
            self.is_active = True
            self.last_photo_change = pygame.time.get_ticks()

        if self.is_active and self.photos:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_photo_change >= self.photo_change_interval:
                self.next_photo()
                self.last_photo_change = current_time

    def load_current_photo(self, screen_size):
        """Load and scale the current photo to fit screen"""
        if not self.photos:
            return None

        photo_path = self.photos[self.current_photo_index]

        try:
            image = pygame.image.load(str(photo_path))

            # Scale image to fit screen while maintaining aspect ratio
            screen_width, screen_height = screen_size
            img_width, img_height = image.get_size()

            # Calculate scaling factor
            scale_x = screen_width / img_width
            scale_y = screen_height / img_height
            scale = min(scale_x, scale_y)

            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))

            return scaled_image

        except Exception as e:
            print(f"Error loading photo {photo_path}: {e}")
            # Remove problematic photo and try next one
            self.photos.pop(self.current_photo_index)
            if self.photos:
                self.current_photo_index = self.current_photo_index % len(self.photos)
            return None

    def next_photo(self):
        """Move to the next photo"""
        if not self.photos:
            return

        self.current_photo_index = (self.current_photo_index + 1) % len(self.photos)
        self.current_surface = None

    def previous_photo(self):
        """Move to the previous photo"""
        if not self.photos:
            return

        self.current_photo_index = (self.current_photo_index - 1) % len(self.photos)
        self.current_surface = None

    def draw(self, screen):
        """Draw the current photo on the screen"""
        if not self.is_active or not self.photos:
            return False

        if self.current_surface is None:
            self.current_surface = self.load_current_photo(screen.get_size())

        if self.current_surface:
            # Center the image
            screen_rect = screen.get_rect()
            image_rect = self.current_surface.get_rect(center=screen_rect.center)

            # Fill background with black
            screen.fill((0, 0, 0))

            # Draw the image
            screen.blit(self.current_surface, image_rect)

            # Draw photo info (optional)
            font = pygame.font.Font(None, 24)
            info_text = f"{self.current_photo_index + 1} / {len(self.photos)}"
            info_surface = font.render(info_text, True, (200, 200, 200))
            info_rect = info_surface.get_rect(bottomright=(screen_rect.width - 10, screen_rect.height - 10))
            screen.blit(info_surface, info_rect)

            return True

        return False
