"""
This file creates the main loop of the visualization of Christmas movies based on imported csv data.
christmas_movies.csv and visual_objects.py are required to run this code.
"""

# ====================================================
# AI Documentation: 
# ====================================================
# AI Tool Used: Claude.
# AI Guidance Used:
# 1. Advised moving the slider bar lower to avoid overlapping with the title.
# 2. Provided guidance on drawing trees in a windowed, scrollable layout.
# 3. Suggested references to pygame library documentation for methods like:
#    pygame.font.SysFont(): to create fonts, arguments include font name and size.
#    pygame.draw.rect(), pygame.draw.circle(): to draw shapes on surfaces, arguments include surface, color, rect/position, radius, and optional parameters.
#    pygame.image.load(), pygame.transform.scale(): load and resize images.
#    pygame.Surface.blit(): render images or text surfaces onto another surface.


import csv
import pygame

from visual_objects import (
    Tree,
    compute_tree_height,
)

DATA_PATH = "christmas_movies.csv"
WINDOW_SIZE = 10
TREE_WIDTH = 110  
BULB_UPDATE_PERIOD = 30  # Frames between bulb position updates.

# ====================================================
# LOAD DATA FROM FILE 
# ====================================================

def load_trees(path):
    """
    Load Christmas movies from csv and group them by release year.
    Returns a list of tree objects sorted by year.
    """
    years = {}
    
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Skip rows without a release year.
            if not row.get("release_year"):
                continue
            try:
                year = int(float(row["release_year"]))
            except ValueError:
                continue

            # Read the IMDb rating and store it to visualize the tree's height.
            imdb = None
            if row.get("imdb_rating"):
                try:
                    imdb = float(row["imdb_rating"])
                except ValueError:
                    imdb = None

            # Content rating category(G/PG/PG-13/etc) for the Christmas bulb's color.
            rating_cat = row.get("rating")

            # Store the IMDb rating and content rating category for each movie in a dictionary.
            years.setdefault(year, {"ratings": [], "movies": []})

            if imdb is not None:
                years[year]["ratings"].append(imdb)

            years[year]["movies"].append(
                {
                    "title": row.get("title", "").strip(),
                    "imdb_rating": imdb,
                    "rating_cat": rating_cat,
                }
            )
    
    # Build visual tree objects from the data.
    trees = []
    for year, d in sorted(years.items()):
        ratings = d["ratings"]
        avg_rating = sum(ratings) / len(ratings) if ratings else None
        trees.append(Tree(year, avg_rating, d["movies"]))
    
    return trees

# ====================================================
# INTERACTIVE SLIDER
# ==================================================== 

def draw_slider(screen, font, trees, start_idx, window_size,
                slider_rect, handle_radius):
    bar_color = (155, 191, 130)
    handle_color = (165, 42, 42)
    label_color = (230, 230, 230)

    x, y, w, h = slider_rect
    # Draw the slider bar.
    pygame.draw.rect(screen, bar_color, slider_rect, border_radius=h // 2)

    # Calculate the maximum starting index for the slider.
    max_start = max(0, len(trees) - window_size)
    t = 0 if max_start == 0 else start_idx / max_start
    handle_x = int(x + t * w)
    handle_y = y + h // 2
    pygame.draw.circle(screen, handle_color, (handle_x, handle_y), handle_radius)

    # Draw the slider label.
    if trees:
        start_year = trees[start_idx].year
        end_idx = min(start_idx + window_size - 1, len(trees) - 1)
        end_year = trees[end_idx].year
        label = f"Slide to Change Year Range: {start_year} - {end_year}"
        text = font.render(label, True, label_color)
        screen.blit(text, (x, y - 32))


def slider_value_from_mouse(x_pos, trees, window_size, slider_rect):
    x, y, w, h = slider_rect
    max_start = max(0, len(trees) - window_size)
    if max_start == 0:
        return 0
    t = (x_pos - x) / w
    t = max(0.0, min(1.0, t))
    return int(round(t * max_start))

# ====================================================
# CREATE LEGEND ON THE SIDE
# ====================================================

def draw_legend(surface, legend_font, x, y):
    # Legend items = left label + right explanation.
    legend_items = [
        ("Tree Hight", "Average IMDb rating per year"),
        ("Each Christmas Bulb", "One movie"),
        ("Christmas Bulb Color", "Content rating"),
    ]
    color = (255, 255, 255)
    for i, (left, right) in enumerate(legend_items):
        text = legend_font.render(f"{left} : {right}", True, color)
        surface.blit(text, (x, y + i*20))


# ====================================================
# VISUALIZATION OF CHRISTMAS MOVIES
# ====================================================

def draw_visualization(screen, trees, font, title_font, legend_font, window_start, window_size,
                       frame, slider_rect, handle_radius, background_img):
    W, H = screen.get_size()
    screen.blit(background_img, (0, 0))

    # Create the title of this visualization. 
    title_surf = title_font.render("Christmas Movies Visualization (1934-2023)", True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(W // 2, 40))
    screen.blit(title_surf, title_rect)

    if not trees:
        return

    # Clamp visible window.
    window_start = max(0, min(window_start, len(trees) - 1))
    visible = trees[window_start: window_start + window_size]
    if not visible:
        visible = trees[-window_size:]

    ratings = [t.avg_rating for t in trees if t.avg_rating is not None]
    rating_min = min(ratings) if ratings else 0
    rating_max = max(ratings) if ratings else 10

    # Layout.
    margin_x = 100
    base_y = H - 90
    area_width = W - 2 * margin_x
    n = len(visible)
    spacing = area_width / max(1, (n - 1))

    # Consistent colors.
    tree_color = (0, 50, 20)
    trunk_color = (10, 20, 10)
    text_color = (240, 240, 240)

    # Draw slider.
    draw_slider(screen, font, trees, window_start, window_size,
                slider_rect, handle_radius)

    # Draw legend (left-top).
    legend_y = slider_rect.y + slider_rect.height + 45
    draw_legend(screen, legend_font, x=40, y=legend_y)

    # Draw all trees in this window.
    for idx, tree in enumerate(visible):
        x = int(margin_x + idx * spacing)
        h = compute_tree_height(tree.avg_rating, rating_min, rating_max)

        tree.draw(
            surface=screen,
            font=font,
            x_center=x,
            base_y=base_y,
            tree_width=TREE_WIDTH,
            height=h,
            frame=frame,
            update_period=BULB_UPDATE_PERIOD,
            tree_color=tree_color,
            trunk_color=trunk_color,
            text_color=text_color,
        )


# ====================================================
# MAIN LOOP
# ====================================================

def main():
    pygame.init()
    W, H = 1400, 800
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Christmas Movies")

    # Title font.
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    # Normal font.
    font = pygame.font.SysFont("Arial", 20)
    # Legend font.
    legend_font = pygame.font.SysFont("Arial", 15, bold=True)

    trees = load_trees(DATA_PATH)

    # Load background image.
    background_img = pygame.image.load("background.jpg").convert()
    background_img = pygame.transform.scale(background_img, (W, H))

    # Slider.
    slider_width = W - 240
    slider_rect = pygame.Rect(120, 120, slider_width, 14)
    handle_radius = 10

    window_start = 0
    dragging_slider = False

    clock = pygame.time.Clock()
    frame = 0
    running = True

    while running:

        # ----------------------------------------
        # 1. EVENT HANDLING
        # ----------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Mouse controls slider.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if slider_rect.inflate(0, 20).collidepoint(mx, my):
                    dragging_slider = True
                    window_start = slider_value_from_mouse(
                        mx, trees, WINDOW_SIZE, slider_rect
                    )

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_slider = False

            elif event.type == pygame.MOUSEMOTION and dragging_slider:
                mx, my = event.pos
                window_start = slider_value_from_mouse(
                    mx, trees, WINDOW_SIZE, slider_rect
                )

        # ----------------------------------------
        # 2. DRAWING
        # ----------------------------------------        
        draw_visualization(
            screen, trees, font, title_font, legend_font, window_start, WINDOW_SIZE,
            frame, slider_rect, handle_radius, background_img
        )

        pygame.display.flip()
        clock.tick(25)
        frame += 1

    pygame.quit()


if __name__ == "__main__":
    main()
