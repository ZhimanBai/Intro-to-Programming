"""
This file defines the Tree and Bulb classes, functions for positioning bulbs,
mapping ratings to colors, and computing tree height.
"""

# ====================================================
# AI Documentation: 
# ====================================================
# AI Tool Used: Claude.
# AI Guidance Used:
# 1. Recommended keeping the tree draw logic organized, including trunk, tree shape, bulbs, star, and year label.
# 2. Clarified how to compute random bulb positions while avoiding overlaps.
# 3. Suggested scaling tree height based on average IMDb rating using compute_tree_height().
# 4. Provided guidance on consulting pygame documentation for:
#    random.uniform(a, b): to generate random positions for bulbs, arguments define range.
#    pygame.draw.polygon(): to draw tree triangles, arguments include surface, color, and point list.
#    pygame.draw.rect(), pygame.draw.circle(): for tree trunk and bulbs, arguments include surface, color, position, and optional parameters like radius.


import random
import pygame
import math

# ====================================================
# COLOR MAPPING
# ====================================================

def rating_to_color(rating_cat: str):
    """
    Map rating categories (G, PG, PG-13, R, Not Rated, etc.) to bulb colors.
    Used to differentiate types of movies visually.
    """
    if not rating_cat:
        return (180, 180, 180)

    r = rating_cat.strip().upper()

    if r in ("G", "TV-G"):
        return (140, 220, 140) 
    if r in ("PG", "TV-PG"):
        return (80, 200, 120)
    if r in ("PG-13", "TV-14"):
        return (230, 200, 80)
    if r in ("R", "TV-MA"):
        return (200, 70, 70)

    # Not rated or other categories.
    return (180, 180, 180)


# ====================================================
# CREATE TREE HEIGHT
# ====================================================

def compute_tree_height(value, v_min, v_max,
                        min_h=120, max_h=420):
    """Scale an average each year's IMDb rating to tree height."""
    if value is None or v_max == v_min:
        return min_h

    t = (value - v_min) / (v_max - v_min)
    t = max(0, min(1, t))
    return min_h + t * (max_h - min_h)


# ====================================================
# CREATE BULB PLACEMENT
# ====================================================

def position_bulbs_in_tree_random(num_bulbs, x_center, base_y,
                                  tree_width, tree_height,
                                  max_tries_per_bulb=50,
                                  min_dist=6):
    """Randomly place bulbs inside a triangular tree."""
    positions = []
    if num_bulbs <= 0:
        return positions

    top_y = base_y - tree_height

    for _ in range(num_bulbs):
        tries = 0
        while True:
            tries += 1

            if tries > max_tries_per_bulb:
                # Fallback placement roughly in the middle.
                positions.append((x_center, int((top_y + base_y) / 2)))
                break

            # Pick a random vertical location along the tree.
            y = random.uniform(top_y, base_y)

            # At higher points the tree width narrows.
            frac_from_top = (y - top_y) / tree_height  # 0 at top, 1 at base.
            half_width = (tree_width / 2) * frac_from_top

            # Pick a matching horizontal spot.
            x = random.uniform(x_center - half_width, x_center + half_width)

            # Check distance to existing bulbs to avoid overlapping bulbs.
            ok = True
            for px, py in positions:
                if (px - x) ** 2 + (py - y) ** 2 < min_dist ** 2:
                    ok = False
                    break
            if ok:
                positions.append((int(x), int(y)))
                break

    return positions


# ====================================================
# CREATE CLASSES
# ====================================================

class Bulb:
    def __init__(self, x, y, rating_cat):
        self.x = x                    
        self.y = y                    
        self.rating_cat = rating_cat  # For picking color.
        self.base_radius = 5  # Base radius of the bulb, which can increase temporarily when sparkling.

    def sparkle(self):
        """
        Return True occasionally (2% chance) to create a sparkling effect.
        """
        # random. random() generates a float between 0 and 1. 
        # If the number is less than 0.02, the bulb sparkles.
        return random.random() < 0.02
        
    def draw(self, surface):
        """
        Draw the bulb onto the surface.
        """
        r = self.base_radius
        if self.sparkle():
            r += 3 

        pygame.draw.circle(
            surface,
            rating_to_color(self.rating_cat),
            (int(self.x), int(self.y)),
            int(r)
        )

class Tree:
    def __init__(self, year, avg_rating, movies):
        """
        movies: list of dicts with keys "title", "imdb_rating", "rating_cat".
        years: the year represented by this tree. 
        avg_rating: average IMDb rating for this year.
        """
        self.year = year
        self.avg_rating = avg_rating # For computing tree height.
        self.movies = movies
        self.bulbs = []  # List of bulb objects.

    def update_bulbs(self, x_center, base_y, tree_width, tree_height,
                     frame, update_period):
        """
        Update bulb positions every update_period frames to animate them.
        """
        if (not self.bulbs) or (frame % update_period == 0):
            positions = position_bulbs_in_tree_random(
                len(self.movies), x_center, base_y,
                tree_width * 0.9, tree_height * 0.9
            )
            self.bulbs = [
                Bulb(px, py, movie["rating_cat"])
                for (px, py), movie in zip(positions, self.movies)
            ]

    def draw_star(self, surface, center_x, center_y, radius, color):
        points = []
        # Loop through the 5 outer points of the star.
        for i in range(5):
            
            angle = math.radians(i*72 - 90)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))

            # Calculate the angle for the inner point between two outer points.
            angle = math.radians(i*72 + 36 - 90)
            x = center_x + radius*0.5 * math.cos(angle)
            y = center_y + radius*0.5 * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(surface, color, points)


    def draw(self, surface, font, x_center, base_y, tree_width,
             height, frame, update_period,
             tree_color, trunk_color, text_color):
        """
        Draw trunk, tree triangle, bulb animation, star, and year label.
        """
        # Update bulb locations for animation.
        self.update_bulbs(x_center, base_y, tree_width, height,
                          frame, update_period)

        # Draw trunk.
        trunk_w = 16
        trunk_h = 26
        pygame.draw.rect(
            surface,
            trunk_color,
            (x_center - trunk_w // 2, base_y, trunk_w, trunk_h),
        )

        # Draw tree shape (triangle).
        pts = [
            (x_center, base_y - height),
            (x_center - tree_width // 2, base_y),
            (x_center + tree_width // 2, base_y),
        ]
        pygame.draw.polygon(surface, tree_color, pts)

        # Draw bulbs.
        for bulb in self.bulbs:
            # bulb.draw(surface, radius=5)
            bulb.draw(surface)

        # Draw star at top.
        self.draw_star(surface, x_center, base_y - height, radius=12, color=(255, 255, 0))


        # Draw year label.
        year_text = font.render(str(self.year), True, text_color)
        rect = year_text.get_rect(center=(x_center, base_y + trunk_h + 20))
        surface.blit(year_text, rect)
