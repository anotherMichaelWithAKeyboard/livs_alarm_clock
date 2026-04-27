# Rare Mushroom System 🍄✨

Your alarm clock now features a **rarity system** for mushroom people with different spawn rates!

## Mushroom Rarity Tiers

### Common (64% spawn rate)
**Standard mushroom people** you'll see most often:
- **Standing Mushroom** - Classic pose with spots
- **Arms-Up Mushroom** - Celebratory pose
- **Squat Mushroom** - Short and wide variety

### Uncommon (20% spawn rate) 🌟
**Tall Thin Mushroom** - Elegant and slender
- Narrow cap with spots
- Very tall, thin body
- Graceful appearance

### Rare (10% spawn rate) ⭐⭐
**Crowned Mushroom** - Royal variant
- Crown-like points on cap
- Bright glowing spots
- Wider, more regal stance

### Very Rare (5% spawn rate) ⭐⭐⭐
**Spotted Giant** - Massive mushroom
- Huge cap with multiple spot sizes
- Thick, sturdy body
- Takes up more space

### LEGENDARY (1% spawn rate) 👑✨
**THE MUSHROOM QUEEN** - Ultimate discovery!
- Golden crown on top
- Glowing, multi-colored cap
- Ornate spots that shimmer
- Dress-like flowing bottom
- Largest and most majestic
- Only ~1 chance in 100!

## How It Works

When the border generates, each position that gets a mushroom person (70% of positions) goes through the rarity roll:

```
Roll 0-1%     → MUSHROOM QUEEN 👑
Roll 1-6%     → Spotted Giant ⭐⭐⭐
Roll 6-16%    → Crowned Mushroom ⭐⭐
Roll 16-36%   → Tall Mushroom 🌟
Roll 36-100%  → Common mushrooms
```

## Finding Rare Mushrooms

### Tips for Spotting
1. **Look for size** - Rare mushrooms are often larger
2. **Check the caps** - Rare ones have unique patterns
3. **Golden crown** - Mushroom Queen has distinctive gold
4. **Top and bottom borders** - Mushrooms spawn here most

### What to Look For

**Tall Mushroom (Uncommon)**:
- Noticeably taller than others
- Thin, slender profile
- Narrow cap

**Crowned Mushroom (Rare)**:
- Three point crown on top
- Brighter spot colors
- Wide cap

**Spotted Giant (Very Rare)**:
- HUGE mushroom
- Multiple different-sized spots
- Thick body
- Dominates its space

**Mushroom Queen (LEGENDARY)**:
- Golden crown (unmistakable)
- Glowing effect around cap
- Largest of all
- Dress-like flowing bottom
- Multiple bright spots

## Seasonal Variations

Each rare mushroom changes colors with the seasons:

### Summer
- Deep coral, orange, and ocean blue caps
- Dark tan stems
- Bright, warm palette

### Autumn
- Deep rust, dark ochre, and burgundy caps
- Dark brown stems
- Rich, earthy tones

### Winter
- Deep navy, ice blue, and purple-blue caps
- Dark gray-blue stems
- Cool, frosty colors

### Spring
- Deep pink, purple, and forest green caps
- Dark olive stems
- Vibrant, fresh colors

## Spawn Statistics

With ~20 mushroom positions per screen:
- **Common mushrooms**: ~13 per screen
- **Uncommon (Tall)**: ~4 per screen
- **Rare (Crowned)**: ~2 per screen
- **Very Rare (Giant)**: ~1 per screen
- **Legendary (Queen)**: ~0.2 per screen (1 in 5 screens!)

**Note**: The border is generated once when the app starts (with random seed 42), so it's consistent. Restart the app to get a new roll and potentially find the Queen!

## Achievement Ideas

Try to spot:
- [ ] All 3 common mushroom types
- [ ] At least one Tall mushroom
- [ ] A Crowned mushroom
- [ ] The elusive Spotted Giant
- [ ] **THE MUSHROOM QUEEN** 👑

## Fun Facts

- The Mushroom Queen is ~10 pixels tall (vs 9 for regular mushrooms)
- She has a golden crown that doesn't change color with seasons
- The glowing effect is created by progressively lighter pixels
- Size variations mean even common mushrooms look unique
- With random seed 42, you get the same rare spawns each run

## Easter Egg Hunt

Want to increase your chances of finding the Queen?

The spawn seed is set to `42` in `src/ui/pixel_border.py`. You could:
1. Comment out the `random.seed(42)` line for different spawns each run
2. Change the seed number to try different layouts
3. Temporarily increase the spawn rate for testing

```python
# In _generate_border_elements():
# random.seed(42)  # Comment this out for random each time!
```

Happy mushroom hunting! 🍄✨👑
