import math  
import stdio 
import stdarray
import random 
import stddraw
import picture
import sys
from Interface import start_menu,LoseOrLevelUp, exiting
from player import Player
from bullet import Bullet
from enemy import Enemy

# claude AI coding was used for optimization and debugging 

def make_enemies():
    enemies = []
    for row in range(4):
        for col in range(7):
            x = 200 + col * 100
            y = 900 - row * 75
            enemies.append(Enemy(x, y, 20, 25))
    return enemies


#had problems with flashing screen, needed seperate function to take space and esc
def wait_for_space_or_exit():
    while stddraw.hasNextKeyTyped():
        stddraw.nextKeyTyped()
    while True:
        stddraw.show(20)
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == " ":
                return True
            elif key == "\x1b":
                exiting()
                stddraw.show(1000)
                sys.exit()

def main() -> None:
    idle = True
    playing = True
    level = 1
    score = 0

    stddraw.setCanvasSize(1000, 1000)
    stddraw.setYscale(0, 1000)
    stddraw.setXscale(0, 1000)

    p = Player(500, 45, 35, math.pi / 2, 10)
    current_direction = "right"
    bullets = []
    enemy_timer = 0
    enemy_move_every = 15
    enemies = make_enemies()

    # title screen loop
    while idle:
        start_menu()
        stddraw.show(20)
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == "\x1b":
                exiting()
                stddraw.show(1000)
                sys.exit()
            else:
                idle = False

    # main game loop
    while playing:
        stddraw.clear(stddraw.BLACK)
        stddraw.setFontSize(15)
        stddraw.setPenColor(stddraw.BLUE)
        stddraw.text(30, 20, "score: " + str(score))

        keys = stddraw.getKeysPressed()

        # exit key
        if keys[stddraw.K_ESCAPE]:
            exiting()
            stddraw.show(1000)
            playing = False

        # shooting/Bullet creation
        if keys[stddraw.K_SPACE] and p.Reload == 0:
            bullets.append(Bullet(p.x, p.y, p.angle, 3))
            p.Reload = 15


        # enemy movement timer direction check/change and edge check
        enemy_timer += 1
        if enemy_timer >= enemy_move_every:
            for enemy in enemies:
                if current_direction == "right":
                    enemy.move_right()
                elif current_direction == "left":
                    enemy.move_left()
            if any(e.x + e.radius >= 1000 for e in enemies):
                current_direction = "left"
                for enemy in enemies:
                    enemy.move_down()
            if any(e.x - e.radius <= 0 for e in enemies):
                current_direction = "right"
                for enemy in enemies:
                    enemy.move_down()
            enemy_timer = 0

        # bullet update, draw and collision
        for bullet in bullets[:]:
            bullet.update()
            bullet.draw()
            if bullet.live == True:
                for enemy in enemies[:]:
                    distance = math.sqrt((bullet.x - enemy.x)**2 + (bullet.y - enemy.y)**2)
                    if distance < bullet.radius + enemy.radius:
                        bullet.live = False
                        enemy.alive = False
                        score += 5

        # remove dead bullets outside the loop
        bullets = [b for b in bullets if b.live == True]
        # remove dead enemies
        enemies = [e for e in enemies if e.alive == True]

        # enemy reaches player - lose condition
        if any(math.sqrt((e.x - p.x)**2 + (e.y - p.y)**2) <= e.radius + p.radius for e in enemies):
            LoseOrLevelUp(level, score, True)
            stddraw.show(20)
            wait_for_space_or_exit()
            level = 1
            score = 0
            enemies = make_enemies()
            bullets = []
            p.x = 500
            p.angle = math.pi / 2
            current_direction = "right"
            

        # all enemies cleared - level up
        if len(enemies) == 0:
            level += 1
            enemies = make_enemies()
            bullets = []
            LoseOrLevelUp(level, score, False)
            stddraw.show(20)
            wait_for_space_or_exit()

        # draw enemies and player
        for enemy in enemies:
            enemy.draw()

        p.update(keys)
        p.draw()
        stddraw.show(20)

    sys.exit()

if __name__ == "__main__":
    main()
