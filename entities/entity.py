import pygame

class Physics_object:
    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.collideable_objects: list = []
        self.collision = {
            "top" :False,
            "bottom" :False,
            "left" :False,
            "right" :False,
        }

    def __update_collision(self):
        """
        THIS NEEDS A REWORK FOR SURE
        """
        original_x = self.x
        original_y = self.y
        self.x += 1
        if self.__check_all_collisions():
            self.collision["right"] = True
        else:
            self.collision["right"] = False
        self.x = original_x
        self.x -= 1
        if self.__check_all_collisions():
            self.collision["left"] = True
        else:
            self.collision["left"] = False

        self.y += 1
        if self.__check_all_collisions():
            self.collision["bottom"] = True
        else:
            self.collision["bottom"] = False

        self.y = original_y
        self.y -= 1
        if self.__check_all_collisions():
            self.collision["top"] = True
        else:
            self.collision["top"] = False

        self.x = original_x
        self.y = original_y

    def __check_all_collisions(self):
        return any([self.check_collision(collider) for collider in self.collideable_objects])


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
        self.speed = 45
        self.surf = pygame.surface.Surface((w, h))

    def update_position(self, x, y):
        self.x, self.y = x, y
        self.position = (x,y)
