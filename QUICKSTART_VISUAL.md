# Quick Start - Visual Edition

## What You'll See

When you run the alarm clock, you'll see a beautiful retro-futuristic display:

```
┌─────────────────────────────────────────────────────────────┐
│  🍄  🌿  ⭐  🍄  🌿  🌺  🍄  🌿  ⭐  🍄  🌿  🌺  🍄  🌿  │  ← Pixel border
│🌿                                                        🌿│
│🌺              Autumn (Season name)                     🍄│
│⭐          ✨ Weekend ✨ (if applicable)                🌿│
│🍄                                                        🌺│
│🌿         ┌────┐ ┌────┐   ┌────┐ ┌────┐                ⭐│
│🌺         │    │ │    │ : │    │ │    │                🍄│  ← Split-flap
│⭐         │ 12 │ │ 34 │   │ 56 │ │ 78 │                🌿│    display
│🍄         │────│ │────│   │────│ │────│                🌺│
│🌿         └────┘ └────┘   └────┘ └────┘                ⭐│
│🌺                                                        🍄│
│⭐                    PM                                  🌿│
│🍄           Friday, April 26, 2024                      🌺│
│🌿                                                        ⭐│
│🌺     Next train: 5 min (if configured)                 🍄│
│⭐                                                        🌿│
│  🍄  🌿  🌺  🍄  🌿  ⭐  🍄  🌿  🌺  🍄  🌿  ⭐  🍄  🌿  │
└─────────────────────────────────────────────────────────────┘
```

## Visual Features Breakdown

### 1. Split-Flap Clock
The time displays in a **retro split-flap style** like old airport departure boards:
- Dark panels with light text
- Horizontal split line through middle
- Smooth flip animation when digits change
- 3D depth with shadows and highlights
- Classic colon separator

### 2. Pixel Art Border
**Mushroom people** and **vines** create a whimsical frame:
- 🍄 **Red mushroom people** - Standing, with white spots on caps
- 🍄 **Purple mushroom people** - Arms raised in celebration
- 🌿 **Green vines** - Climbing up the sides with leaves
- 🌺 **Pink flowers** - Small decorative blooms
- 🍄 **Orange mushrooms** - Tiny decorative caps
- ⭐ **Yellow stars** - Twinkling accents

**Animation**: Mushroom people gently bob up and down!

### 3. Seasonal Colors
The whole display changes colors with the seasons:

- **Summer** ☀️ - Deep blue background, warm yellow text, orange accents
- **Autumn** 🍂 - Dark brown background, cream text, burnt orange accents
- **Winter** ❄️ - Blue-gray background, cool white text, icy blue accents
- **Spring** 🌸 - Dark green-gray background, soft white text, fresh green/pink accents

## Running the Clock

### Full Experience
```bash
python src/main.py
```

You'll see:
- ✅ Split-flap clock with flip animations
- ✅ Pixel art border with mushroom people
- ✅ Seasonal theme colors
- ✅ Weekend/holiday indicators
- ✅ Commute info (if configured)

### Test Components Individually

**Test just the split-flap display:**
```bash
python examples/test_split_flap.py
```
- Press SPACE to see the flip animation
- Watch the mechanical-style transitions

**Test just the pixel border:**
```bash
python examples/test_pixel_border.py
```
- Watch the mushroom people bob gently
- See the variety of pixel art elements

## First Time Setup

### 1. Install Dependencies
```bash
# Using Nix (recommended)
nix develop

# Or using pip
pip install pygame requests pytz
```

### 2. Run the Clock
```bash
python src/main.py
```

### 3. Add Your Photos (Optional)
```bash
# Copy some photos for photo frame mode
cp ~/Pictures/*.jpg assets/photos/

# Clock will show them after 60 seconds idle
```

## What You Can Customize

### Change Clock Size
Edit `src/ui/clock_display.py`:
```python
self.split_flap = SplitFlapDisplay(
    digit_width=120,    # Bigger digits
    digit_height=180,   # Taller digits
)
```

### Change Pixel Size
Edit `src/ui/pixel_border.py`:
```python
PIXEL_SIZE = 5  # Larger pixels (default is 4)
```

### Disable Border (Keep Clock Only)
Comment out in `src/ui/clock_display.py`:
```python
# self.pixel_border.draw_animated(self.screen, self.frame_count)
```

## Tips

**Too bright at night?**
- Dim mode activates automatically (22:00-06:00 by default)
- Adjust in `config/settings.json`

**Want more mushrooms?**
- Edit `src/ui/pixel_border.py`
- Adjust spacing in `_generate_border_elements()`

**Different colors?**
- Edit `src/ui/themes.py`
- Modify the seasonal color palettes

## Performance

- **30 FPS** - Smooth animations without CPU waste
- **No image files** - All graphics are procedurally generated
- **Low memory** - Tiny pixel patterns
- **Fast startup** - Renders in milliseconds

## Troubleshooting

**Clock digits not showing?**
- Make sure pygame font can render digits
- Try increasing `digit_width` and `digit_height`

**Border looks pixelated (too much)?**
- That's intentional! It's pixel art 🎨
- Reduce `PIXEL_SIZE` for smaller pixels

**No animation?**
- Check that the main loop is running at 30 FPS
- Look for errors in console

**Colors look wrong?**
- Check current season matches your expectation
- Verify `src/ui/themes.py` color definitions

## Next Steps

Once you're happy with the basic look:

1. ✅ Set up weekday alarms → `python examples/setup_weekday_alarm.py`
2. ✅ Configure PTV for train times → `python examples/find_ptv_stops.py`
3. ✅ Add your favorite photos → Copy to `assets/photos/`
4. ✅ Deploy to Raspberry Pi → See `DEVELOPMENT.md`

Enjoy your beautiful retro alarm clock! 🎨⏰✨
