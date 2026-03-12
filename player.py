import sys 
import math
import stddraw
import math

class Player:
    def __init__(self,x,y,radius,angle,speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = angle
        self.Reload = 0


    def update(self, keys):
        if self.Reload > 0:
            self.Reload -= 1
        if keys[stddraw.K_a] and self.x >= 35:
            self.x -= self.speed
        if keys[stddraw.K_d] and self.x <= 965:
            self.x += self.speed 
        if keys[stddraw.K_q] and self.angle <= math.pi:
            self.angle += 0.075
        if keys[stddraw.K_e] and self. angle >= 0:
            self.angle -= 0.075


    def draw(self):
        stddraw.setPenColor(stddraw.YELLOW)
        stddraw.filledCircle(self.x,self.y,self.radius)
        stddraw.setPenColor(stddraw.RED)
        stddraw.setPenRadius(3)
        stddraw.line(self.x,self.y,self.x + math.cos(self.angle) * self.radius, self.y + math.sin(self.angle) * self.radius)
        stddraw.setPenRadius(1)

