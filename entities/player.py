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
        self.velocity = [0,0]
        self.state = PlayerState.IDLE

    def handle_movement(self, keys, dt):
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

        delta_x = self.velocity[0] * self.speed * (dt / 100)
        delta_y = self.velocity[1] * self.speed * (dt / 100)

        self.update_position(self.x + delta_x, self.y + delta_y)
