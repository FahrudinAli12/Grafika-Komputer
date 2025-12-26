import pygame
import math
import random

# --- KONFIGURASI ---
WIDTH, HEIGHT = 800, 600
BLUE_OCEAN = (30, 80, 150) 
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
RED = (220, 20, 20)
DARK_GREY = (50, 50, 50) 
BUBBLE_COLOR = (173, 216, 230)
ORANGE = (255, 140, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Feeding Frenzy - Fix Victory & Crunch")

# --- LOAD ASSETS ---
try:
    bg_image = pygame.image.load("background1.jpg")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except:
    bg_image = None

font_ui = pygame.font.SysFont("Verdana", 14, bold=True)
font_pop = pygame.font.SysFont("Verdana", 18, bold=True)
font_victory = pygame.font.SysFont("Verdana", 35, bold=True)
font_msg = pygame.font.SysFont("Verdana", 20, bold=True)

# --- 1. ALGORITMA GRAFIKA MANUAL ---
def draw_line_dda(x1, y1, x2, y2, color):
    dx, dy = x2 - x1, y2 - y1
    steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)
    if steps == 0: return
    x_inc, y_inc = dx / (steps or 1), dy / (steps or 1)
    x, y = x1, y1
    for _ in range(int(steps) + 1):
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            screen.set_at((int(x), int(y)), color)
        x += x_inc
        y += y_inc

def draw_circle_midpoint(xc, yc, r, color):
    x, y = 0, r
    p = 1 - r
    def plot_8(xc, yc, x, y):
        pts = [(xc+x, yc+y), (xc-x, yc+y), (xc+x, yc-y), (xc-x, yc-y),
               (xc+y, yc+x), (xc-y, yc+x), (xc+y, yc-x), (xc-y, yc-x)]
        for px, py in pts:
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                screen.set_at((int(px), int(py)), color)
    plot_8(xc, yc, x, y)
    while x < y:
        x += 1
        if p < 0: p += 2*x + 1
        else:
            y -= 1
            p += 2*(x - y) + 1
        plot_8(xc, yc, x, y)

def fill_polygon(points, color):
    if not points: return
    y_coords = [p[1] for p in points]
    y_min, y_max = int(min(y_coords)), int(max(y_coords))
    for y in range(y_min, y_max + 1):
        nodes = []
        for i in range(len(points)):
            p1, p2 = points[i], points[(i + 1) % len(points)]
            if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                x_intersect = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                nodes.append(x_intersect)
        nodes.sort()
        for i in range(0, len(nodes), 2):
            if i + 1 < len(nodes):
                for x in range(int(nodes[i]), int(nodes[i+1]) + 1):
                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                        screen.set_at((x, y), color)

# --- 2. TRANSFORMASI & RENDER OBJEK ---
def transform_all(x, y, tx, ty, scale, angle=0, reflect_x=False):
    x *= scale
    y *= scale
    if reflect_x: x = -x
    rad = math.radians(angle)
    nx = x * math.cos(rad) - y * math.sin(rad)
    ny = x * math.sin(rad) + y * math.cos(rad)
    return int(nx + tx), int(ny + ty)

def draw_fish(tx, ty, scale, color, facing_left=False):
    body = [(30, 0), (0, 18), (-30, 0), (0, -18)]
    tail = [(-25, 0), (-45, 18), (-45, -18)]
    t_body = [transform_all(p[0], p[1], tx, ty, scale, 0, facing_left) for p in body]
    t_tail = [transform_all(p[0], p[1], tx, ty, scale, 0, facing_left) for p in tail]
    fill_polygon(t_body, color)
    fill_polygon(t_tail, color)

def draw_shark(tx, ty, scale, facing_left=False):
    body = [(60, 0), (20, 25), (-60, 10), (-60, -10), (20, -25)]
    fin = [(10, -20), (-10, -45), (-20, -20)] 
    tail = [(-55, 0), (-85, 30), (-85, -30)]
    t_body = [transform_all(p[0], p[1], tx, ty, scale, 0, facing_left) for p in body]
    t_fin = [transform_all(p[0], p[1], tx, ty, scale, 0, facing_left) for p in fin]
    t_tail = [transform_all(p[0], p[1], tx, ty, scale, 0, facing_left) for p in tail]
    fill_polygon(t_body, DARK_GREY)
    fill_polygon(t_fin, DARK_GREY)
    fill_polygon(t_tail, DARK_GREY)
    eye_pos = transform_all(40, -5, tx, ty, scale, 0, facing_left)
    draw_circle_midpoint(eye_pos[0], eye_pos[1], int(3*scale), RED)

def draw_starfish(tx, ty, scale, angle):
    pts = []
    for i in range(10):
        a = math.radians(i * 36)
        r = 20 * scale if i % 2 == 0 else 8 * scale
        px = r * math.cos(a)
        py = r * math.sin(a)
        pts.append(transform_all(px, py, tx, ty, 1, angle))
    fill_polygon(pts, ORANGE)

def draw_ui(xp, score):
    bx, by, bw, bh = 100, 70, 400, 15
    draw_line_dda(bx, by, bx+bw, by, WHITE)
    draw_line_dda(bx, by+bh, bx+bw, by+bh, WHITE)
    draw_line_dda(bx, by, bx, by+bh, WHITE)
    draw_line_dda(bx+bw, by, bx+bw, by+bh, WHITE)
    fill_w = int((min(xp, 600) / 600) * bw)
    for x in range(bx+1, bx+fill_w): draw_line_dda(x, by+1, x, by+bh-1, GOLD)
    thresholds = [200, 400] 
    for t in thresholds:
        tx = bx + int((t / 600) * bw)
        draw_line_dda(tx, by - 5, tx, by + bh + 5, RED)
    draw_fish(bx + 25, by - 25, 0.3, WHITE)           
    draw_fish(bx + bw//3 + 25, by - 25, 0.5, (50, 200, 100)) 
    draw_fish(bx + (2*bw)//3 + 25, by - 25, 0.7, RED)   
    screen.blit(font_ui.render(f"SCORE: {score}", True, WHITE), (650, 20))

# --- 3. GAME ENGINE ---
def reset_game():
    return [WIDTH//2, HEIGHT//2], 0.6, 0, 0, 1, [], [random.randint(50, WIDTH-50), -50, 1.2, 0], \
           [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(2, 5)] for _ in range(20)], \
           [], False, [-200, HEIGHT//2, False, 0]

player_pos, player_scale, player_xp, player_score, player_level, enemies, starfish_data, bubbles, popups, win_state, shark_data = reset_game()
victory_bubbles = [] 

def spawn_en():
    l = random.choice([1, 1, 1, 2, 2, 3])
    side = random.choice([-150, WIDTH+150])
    c = WHITE if l==1 else (50, 200, 100) if l==2 else RED
    return [side, random.randint(100, 550), l, c, 2 if side < 0 else -2]

for _ in range(7): enemies.append(spawn_en())

clock = pygame.time.Clock()
game_over = False
running = True

while running:
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill(BLUE_OCEAN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: 
                player_pos, player_scale, player_xp, player_score, player_level, enemies, starfish_data, bubbles, popups, win_state, shark_data = reset_game()
                enemies = [spawn_en() for _ in range(7)]
                victory_bubbles = []
                game_over = False
            if event.key == pygame.K_q: running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        facing = False
        if keys[pygame.K_LEFT]: player_pos[0] -= 5; facing = True
        if keys[pygame.K_RIGHT]: player_pos[0] += 5; facing = False
        if keys[pygame.K_UP]: player_pos[1] -= 5
        if keys[pygame.K_DOWN]: player_pos[1] += 5

        # Leveling
        if player_level == 1 and player_xp >= 200: 
            player_level, player_scale = 2, 0.8
            popups.append([player_pos[0], player_pos[1], "LEVEL UP!", 40, GOLD])
        elif player_level == 2 and player_xp >= 400: 
            player_level, player_scale = 3, 1.0
            popups.append([player_pos[0], player_pos[1], "MAX LEVEL!", 40, GOLD])
        
        # Shark Logic
        shark_data[3] += 1
        if shark_data[3] >= 1800:
            shark_data[2], shark_data[3], shark_data[0] = True, 0, -150
            shark_data[1] = random.randint(50, HEIGHT - 50)
            popups.append([WIDTH//2 - 100, 50, "DANGER: SHARK!", 120, RED])

        if shark_data[2]: 
            shark_data[0] += 3
            draw_shark(shark_data[0], shark_data[1], 1.2, False)
            if math.sqrt((player_pos[0]-shark_data[0])**2 + (player_pos[1]-shark_data[1])**2) < 60: game_over = True
            for i, en in enumerate(enemies):
                if math.sqrt((en[0]-shark_data[0])**2 + (en[1]-shark_data[1])**2) < 70: 
                    enemies[i] = spawn_en()
                    popups.append([int(shark_data[0]), int(shark_data[1]), "CRUNCH!", 30, WHITE]) # CRUNCH HIU
            if shark_data[0] > WIDTH + 150: shark_data[2] = False

        # Ambient & Starfish
        for b in bubbles:
            b[1] -= 2
            if b[1] < -10: b[1] = HEIGHT + 10; b[0] = random.randint(0, WIDTH)
            draw_circle_midpoint(b[0], b[1], b[2], BUBBLE_COLOR)

        starfish_data[1] += 1.5
        starfish_data[3] = (starfish_data[3] + 2) % 360
        if starfish_data[1] > HEIGHT + 50: starfish_data[1] = -50; starfish_data[0] = random.randint(50, WIDTH-50)
        draw_starfish(starfish_data[0], starfish_data[1], starfish_data[2], starfish_data[3])
        if math.sqrt((player_pos[0]-starfish_data[0])**2 + (player_pos[1]-starfish_data[1])**2) < 35:
            player_score += 40; player_xp += 40; starfish_data[1] = HEIGHT + 100
            popups.append([int(player_pos[0]), int(player_pos[1]), "CRUNCH!", 30, GOLD]) # CRUNCH BINTANG

        # --- LOGIKA RANTAI MAKANAN MUSUH ---
        for i in range(len(enemies)):
            for j in range(len(enemies)):
                if i != j:
                    h, p = enemies[i], enemies[j]
                    if h[2] > p[2]:
                        dist_ai = math.sqrt((h[0]-p[0])**2 + (h[1]-p[1])**2)
                        if dist_ai < (25 * h[2] * 0.4):
                            enemies[j] = spawn_en()
                            popups.append([int(h[0]), int(h[1]), "CRUNCH!", 30, WHITE]) # CRUNCH AI MAKAN AI

        # --- UPDATE MUSUH ---
        for i, en in enumerate(enemies[:]):
            en[0] += en[4]
            if abs(en[0] - WIDTH//2) > WIDTH + 200: enemies[i] = spawn_en(); continue
            dist = math.sqrt((player_pos[0]-en[0])**2 + (player_pos[1]-en[1])**2)
            if dist < (40 * player_scale):
                if player_level >= en[2]:
                    player_score += en[2]*10; player_xp += en[2]*10; enemies[i] = spawn_en()
                    popups.append([en[0], en[1], "SLURP!", 25, WHITE])
                elif dist < (22 * player_scale): game_over = True 
            draw_fish(en[0], en[1], 0.4 * en[2], en[3], en[4] < 0)

        # Trigger Victory
        if player_xp >= 600 and not win_state:
            win_state = True
            for i, char in enumerate("FEEDINGFRENZY"): 
                victory_bubbles.append([random.randint(50, 750), HEIGHT + (i*60), char, random.uniform(1.5, 2.5)])

        draw_fish(player_pos[0], player_pos[1], player_scale, (255, 150, 200), facing)
        draw_ui(player_xp, player_score)

    # --- BAGIAN LUAR (TETAP TAMPIL SAAT MENANG) ---
    if win_state:
        for vb in victory_bubbles:
            vb[1] -= vb[3]
            if vb[1] < -50: vb[1] = HEIGHT + 50
            draw_circle_midpoint(vb[0], vb[1], 30, WHITE)
            screen.blit(font_ui.render(vb[2], True, GOLD), (vb[0]-7, vb[1]-10))

    for p in popups[:]:
        screen.blit(font_pop.render(p[2], True, p[4]), (p[0], p[1]))
        p[1] -= 1; p[3] -= 1
        if p[3] <= 0: popups.remove(p)

    if game_over or win_state:
        msg = "GAME OVER" if game_over else f"VICTORY! SCORE: {player_score}"
        color = RED if game_over else GOLD
        txt_main = font_victory.render(msg, True, color)
        txt_sub = font_msg.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
        screen.blit(txt_main, (WIDTH//2 - txt_main.get_width()//2, HEIGHT//2 - 40))
        screen.blit(txt_sub, (WIDTH//2 - txt_sub.get_width()//2, HEIGHT//2 + 30))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()