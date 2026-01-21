import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# --- 1. KOMPONEN VISUAL ---
def draw_textured_cube(w, h, d, color, is_building=False, is_train=False):
    vertices = [[w,-h,-d], [w,h,-d], [-w,h,-d], [-w,-h,-d], [w,-h,d], [w,h,d], [-w,-h,d], [-w,h,d]]
    surfaces = [(0,1,2,3), (3,2,7,6), (6,7,5,4), (4,5,1,0), (1,5,7,2), (4,0,3,6)]  
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        c = [max(0, x - (i*0.1)) for x in color]
        glColor4f(c[0], c[1], c[2], 1.0)
        for vertex in surface: glVertex3fv(vertices[vertex])
    glEnd()

    if is_building:
        glColor3f(0.9, 0.9, 0.5) 
        for row in range(5):
            for col in range(2):
                glBegin(GL_QUADS)
                v_y, v_x = -h + 2 + (row * 3.5), -w + 1 + (col * 3)
                glVertex3f(v_x, v_y, d+0.01); glVertex3f(v_x+1.5, v_y, d+0.01)
                glVertex3f(v_x+1.5, v_y+2, d+0.01); glVertex3f(v_x, v_y+2, d+0.01); glEnd()

    if is_train:
        glColor3f(0.1, 0.1, 0.1); glBegin(GL_QUADS) 
        glVertex3f(-w+0.5, 0, d+0.01); glVertex3f(w-0.5, 0, d+0.01)
        glVertex3f(w-0.5, h-0.5, d+0.01); glVertex3f(-w+0.5, h-0.5, d+0.01); glEnd()
        glColor3f(1, 1, 0.8) 
        for lx in [-w+0.5, w-1.0]:
            glBegin(GL_QUADS)
            glVertex3f(lx, -h+0.5, d+0.02); glVertex3f(lx+0.5, -h+0.5, d+0.02)
            glVertex3f(lx+0.5, -h+1.0, d+0.02); glVertex3f(lx, -h+1.0, d+0.02); glEnd()

def draw_rail(lane_x, dist):
    for off in [-0.5, 0.5]:
        glPushMatrix()
        glTranslatef(lane_x + off, -1.0, -100)
        draw_textured_cube(0.08, 0.05, 300, (0.7, 0.7, 0.7))
        glPopMatrix()
    offset_z = dist % 6
    for z in range(-150, 100, 6):
        glPushMatrix()
        glTranslatef(lane_x, -1.05, z + offset_z)
        draw_textured_cube(0.8, 0.03, 0.3, (0.3, 0.2, 0.1))
        glPopMatrix()

def draw_clamped_shadow(x, z, w, d, opacity=0.4):
    glPushMatrix()
    glDisable(GL_DEPTH_TEST)
    glTranslatef(x - 3.5, -1.18, z)
    draw_textured_cube(w * 1.2, 0.01, d * 0.7, (0, 0, 0))
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()

def draw_text(text, x, y, font, color=(255, 255, 0)):
    text_surface = font.render(text, True, color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

# --- 2. ENGINE UTAMA ---
def main():
    pygame.init()
    display = (1000, 700)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Subway Surfers - Auto-Speed Difficulty")
    
    font = pygame.font.SysFont('Arial', 32, bold=True)
    glClearColor(0.4, 0.7, 1.0, 1.0)
    glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)

    lanes = [-5, 0, 5]
    curr_lane, py, jumping, jv = 1, 0, False, 0
    score, coins_count = 0, 0
    
    # KONDISI SPEED AWAL
    base_speed = 1.0
    speed, dist = base_speed, 0 
    max_speed = 3.5 # Batas kecepatan maksimal biar tetep playable
    over = False

    trains = [[random.choice(lanes), 1.2, -180 - (i*150)] for i in range(2)]
    buildings = [[side, 10, -i*60] for i in range(15) for side in [-30, 30]]
    coin_list = [[random.choice(lanes), 1.0, -80 - (i*60)] for i in range(5)]

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); quit()
            if event.type == KEYDOWN and not over:
                if event.key == K_LEFT and curr_lane > 0: curr_lane -= 1
                if event.key == K_RIGHT and curr_lane < 2: curr_lane += 1
                if event.key == K_SPACE and not jumping: jumping = True; jv = 0.45
            if event.type == KEYDOWN and over: main()

        if not over:
            score += 1
            
            # LOGIKA MENAMBAH KECEPATAN (Tiap 500 skor, speed naik 0.2)
            speed = min(base_speed + (score / 500.0) * 0.2, max_speed)
            
            dist += speed
            if jumping:
                py += jv; jv -= 0.02
                if py <= 0: py, jumping = 0, False

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            gluPerspective(45, (1000/700), 0.1, 600.0)
            gluLookAt(0, 18, 55, 0, 0, -60, 0, 1, 0)

            glPushMatrix()
            glTranslatef(0, -1.3, -150); draw_textured_cube(200, 0.1, 400, (0.2, 0.6, 0.2))
            glPopMatrix()

            for lp in lanes: draw_rail(lp, dist)

            for b in buildings:
                b[2] += speed
                if b[2] > 100: b[2] = -500
                draw_clamped_shadow(b[0], b[2], 6, 6)
                glPushMatrix()
                glTranslatef(b[0], b[1], b[2])
                draw_textured_cube(6, 18, 6, (0.6, 0.5, 0.4), is_building=True)
                glPopMatrix()

            for t in trains:
                t[2] += speed + 0.3
                if t[2] > 100: t[2], t[0] = -500, random.choice(lanes)
                draw_clamped_shadow(t[0], t[2], 2.5, 12)
                glPushMatrix()
                glTranslatef(t[0], 1.5, t[2])
                draw_textured_cube(2.5, 3, 12, (0.1, 0.2, 0.5), is_train=True)
                glPopMatrix()
                if abs(t[0] - lanes[curr_lane]) < 2.5 and abs(t[2] - 15) < 12 and py < 2.5: over = True

            for c in coin_list:
                c[2] += speed
                if c[2] > 100: c[2], c[0] = -500, random.choice(lanes)
                if abs(c[0] - lanes[curr_lane]) < 2 and abs(c[2] - 15) < 3:
                    coins_count += 1; c[2] = -500
                glPushMatrix()
                glTranslatef(c[0], 1.2, c[2])
                glRotatef(pygame.time.get_ticks() * 0.5, 0, 1, 0)
                draw_textured_cube(0.6, 0.6, 0.1, (1.0, 0.9, 0.0))
                glPopMatrix()

            draw_shadow_fix = True # Dummy for player shadow
            draw_clamped_shadow(lanes[curr_lane], 15, 1.2, 1)
            glPushMatrix()
            glTranslatef(lanes[curr_lane], py + 1.2, 15)
            draw_textured_cube(1.2, 1.8, 0.8, (1, 1, 1))
            glPopMatrix()

            # UI - Nambahin tampilan kecepatan biar lu tau lagi secepat apa
            draw_text(f"SCORE: {score}", 750, 650, font)
            draw_text(f"COINS: {coins_count}", 50, 650, font)
            draw_text(f"SPEED: {speed:.1f}x", 430, 650, font, (100, 255, 100))

            pygame.display.flip()
            clock.tick(60)
        else:
            draw_text("GAME OVER - Press any key", 250, 350, font, (255, 0, 0))
            pygame.display.flip()

if __name__ == "__main__":
    main()
