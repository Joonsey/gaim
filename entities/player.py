from enum import IntEnum, auto
import pygame
from entities.entity import Entity

class PlayerState(IntEnum):
    IDLE = auto()
    JUMPING = auto()
    WALKING = auto()

class Player(Entity):
    def __init__(self, x, y, w, h) -> None:
        super().__init__(x, y, w, h)
        self.velocity = [0.,.0]
        self.state = PlayerState.IDLE
        self.base_acceleration = .25
        self.acceleration = self.base_acceleration
        self.max_velocity = .5





        #TODO pretty sure velocity acceleration are the opposite terms
        #don't care to fix it now, maybe in the future

    def handle_movement(self, keys, dt):
        normalized_dt = dt/100
        if keys[pygame.K_w]:
            self.velocity[1] = -self.acceleration
        elif keys[pygame.K_s]:
            self.velocity[1] = self.acceleration
        else:
            self.velocity[1] = 0

        if keys[pygame.K_a]:
            self.velocity[0] = -self.acceleration
        elif keys[pygame.K_d]:
            self.velocity[0] = self.acceleration
        else:
            self.velocity[0] = 0

        if self.velocity[0] or self.velocity[1]:
            self.acceleration *= dt / 14
            if self.acceleration >= self.max_velocity:
                self.acceleration = self.max_velocity
        else:
            self.acceleration = self.base_acceleration / 4

        delta_x = self.velocity[0] * self.speed * normalized_dt
        delta_y = self.velocity[1] * self.speed * normalized_dt

        self.update_position(self.x + delta_x, self.y + delta_y)
