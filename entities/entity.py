import pygame

class Physics_object:
    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def update_position(self, x, y):
        self.x, self.y = self.x, self.y

    def check_collision(self, obj):
        if self.x < obj.x + obj.w and self.x + self.w > obj.x and self.y < obj.y + obj.h and self.h + self.y > obj.y:
            return True
        else:
            return False

class Entity(Physics_object):
    def __init__(self, x, y, w, h) -> None:
        super().__init__(x, y, w, h)
        self.position = (x,y)
        self.acceleration = 1
        self.speed = 60
        self.surf = pygame.surface.Surface((w, h))

    def update_position(self, x, y):
        self.x, self.y = x, y
        self.position = (x,y)
