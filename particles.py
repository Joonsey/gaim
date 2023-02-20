from constants import *
from random import randint
import pyglet

def update_particles(particles: list, dt, scroll):
    for particle in particles:
        particle.update(dt, scroll)
        if particle.lifetime == None or particle.lifetime < 0:
            particles.remove(particle)


def from_bytes_to_int(numbers):
    return int.from_bytes(numbers, BYTEORDER)

def position_to_packet(position: tuple[int, int]):
    return position[0].to_bytes(POSITION_BYTE_LEN , BYTEORDER) + position[1].to_bytes(POSITION_BYTE_LEN , BYTEORDER)

class Particle:
    def __init__(self, x: int, y: int, lifetime:float | None, batch=None) -> None:
        self.x = x
        self.y = y
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.absolute_position = self.x, self.y
        self.batch = batch

    def update(self, dt):
        if self.lifetime != None:
            self.lifetime -= dt
            if self.lifetime < 0:
                self.lifetime == None

class Dash_particle(Particle):
    def __init__(self,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 lifetime: float,
                 direction: tuple,
                 batch=None) -> None:
        super().__init__(x, y, lifetime, batch)
        self.rect = pyglet.shapes.Rectangle(x, y, w, h, batch=batch)
        self.direction = direction
        self.speed = 2
        self.base_error = 2
        self.erro_modifier = 5

    def calc_error(self):
        if self.lifetime != None and self.max_lifetime != None:
            return randint(-self.base_error, self.base_error) / (self.max_lifetime +1 - self.lifetime)
        else:
            return 0

    def update(self, dt, scroll):
        super().update(dt)
        if self.lifetime != None and self.max_lifetime != None:
            error = self.calc_error()
            self.x += self.direction[0] * self.speed + error
            self.y += self.direction[1] * self.speed + error
            self.rect.x = int(self.x - scroll[0])
            self.rect.y = int(self.y - scroll[1])

            self.rect.width = self.rect.width * (self.lifetime / self.max_lifetime)
            self.rect.height = self.rect.height * (self.lifetime / self.max_lifetime)
            #print((self.x, self.y), self.direction)
