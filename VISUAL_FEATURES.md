# Visual Design Features

This document describes the visual styling enhancements to the alarm clock.

## Split-Flap Display Clock

The main clock display uses a **split-flap display** aesthetic, inspired by vintage airport and train station departure boards.

### Features
- **Mechanical flip animation** - Digits animate when the time changes
- **Realistic split-line** - Horizontal line through middle of each digit panel
- **3D depth effects** - Shadows and highlights create depth
- **Dark panels** - Classic black background with light text
- **Smooth transitions** - Animated flipping between numbers

### Implementation Details
- Located in: `src/ui/split_flap.py`
- Each digit is independently animated
- Flip animation progress: 0.0 to 1.0
- Configurable digit size and spacing
- Includes colon separator with matching style

### How It Works
```python
# The split-flap display automatically updates
self.split_flap.set_time("12:34")  # Set new time
self.split_flap.update()           # Update animation
self.split_flap.draw(surface, pos, font, colors)  # Draw
```

---

## Pixelated Border Art

A decorative pixel art border featuring **vines and mushroom people** surrounds the clock display.

### Elements

#### Mushroom People 🍄
Two types of mushroom characters:
- **Standing mushroom person** - Red cap with white spots, cream body
- **Arms-up mushroom person** - Purple cap, celebratory pose
- **Size**: 8x9 pixels (scaled 4x for visibility)

#### Vegetation 🌿
- **Vine segments** - Green climbing vines with leaves
- **Small mushrooms** - Orange decorative mushrooms
- **Flowers** - Pink petals with yellow centers
- **Stars** - Twinkling decorative elements

### Border Layout
- **Top**: Mushroom people and vines
- **Bottom**: Mushroom people and vines
- **Left/Right**: Climbing vines and flowers
- **Corners**: Scattered stars

### Animation
- **Subtle bobbing** - Mushroom people gently bob up and down
- **Consistent seed** - Border layout stays consistent (not random each frame)
- **Pixel size**: 4x4 pixels for retro aesthetic

### Implementation Details
- Located in: `src/ui/pixel_border.py`
- All art is procedurally defined (no image files needed)
- Colors match seasonal themes
- ~50 border elements distributed around screen

### Pixel Art Patterns
Each element is defined as a list of `(x, y, color)` tuples:

```python
# Example: Small mushroom
pattern = [
    (1, 0, cap), (2, 0, cap),                    # Cap top
    (0, 1, cap), (1, 1, cap), (2, 1, cap), (3, 1, cap),  # Cap
    (1, 2, stem), (2, 2, stem),                  # Stem
    (1, 3, stem), (2, 3, stem),
]
```

---

## Visual Hierarchy

The complete visual stack (back to front):

1. **Background color** - Seasonal theme color
2. **Pixel art border** - Vines and mushroom people
3. **Split-flap clock** - Main time display
4. **Text overlays** - Date, AM/PM, season, holiday info
5. **Commute panel** - Transport info (if configured)

---

## Color Coordination

All visual elements respect the seasonal theme colors:

### Split-Flap Colors
- **Panel background**: Dark gray `(40, 40, 50)`
- **Text**: Theme's primary text color
- **Shadow**: Pure black for depth
- **Highlight**: White for reflections

### Pixel Art Colors
- **Mushroom caps**: Red, purple, orange (vary by type)
- **Mushroom bodies**: Cream `(240, 220, 200)`
- **Vines**: Green tones `(80, 150, 80)` to `(100, 200, 100)`
- **Flowers**: Pink petals `(255, 180, 200)`, yellow centers
- **Stars**: Soft yellow `(255, 255, 200)`

---

## Customization

### Adjust Split-Flap Size
Edit `src/ui/clock_display.py`:

```python
self.split_flap = SplitFlapDisplay(
    num_digits=4,
    digit_width=90,      # Increase for larger digits
    digit_height=140,    # Increase for taller digits
    spacing=15           # Space between digits
)
```

### Modify Border Density
Edit `src/ui/pixel_border.py`:

```python
# In _generate_border_elements()
x += random.randint(40, 80)  # Change spacing between elements
```

### Change Pixel Size
Edit `src/ui/pixel_border.py`:

```python
# In PixelArt class
PIXEL_SIZE = 4  # Change to 3 for smaller, 5 for larger
```

### Add New Pixel Art
Add new patterns to the `PixelArt` class:

```python
@staticmethod
def my_custom_sprite():
    """Your custom pixel art"""
    pattern = [
        (0, 0, (255, 0, 0)),  # Red pixel at 0,0
        (1, 0, (0, 255, 0)),  # Green pixel at 1,0
        # ... more pixels
    ]
    return pattern
```

Then add to border generation:
```python
element_type = random.choice(['mushroom1', 'my_custom_sprite', ...])
```

---

## Performance

### Optimizations
- **Static border**: Border elements are positioned once at init
- **Minimal redraws**: Only animated elements update
- **Simple animation**: Basic sine wave for bobbing (low CPU)
- **30 FPS**: Reduced from 60 FPS for efficiency

### Resource Usage
- **No image files**: All graphics procedurally generated
- **Low memory**: ~50 border elements × 10 pixels = ~500 pixels
- **Fast rendering**: Direct pixel drawing to surface

---

## Future Enhancements

Potential visual additions:
- [ ] Flip sound effects when digits change
- [ ] More mushroom person varieties
- [ ] Seasonal border themes (snowflakes in winter, flowers in spring)
- [ ] Parallax scrolling vines
- [ ] Particle effects (fireflies, leaves)
- [ ] Day/night cycle for border colors
- [ ] Interactive mushroom people (wave when touched)
