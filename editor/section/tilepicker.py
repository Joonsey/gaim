from section.section import *

class Tilepicker(Section):
    def __init__(self, dimensions, color, **kwargs) -> None:
        super().__init__(dimensions, color, **kwargs)
        self.has_mouse_event = True
        self.buttons = {}
        self.max_buttons = self.surf.get_height() // TILE_SIZE

    def highlight_outline(self, img, position, width=1):
        mask = pygame.mask.from_surface(img)
        mask_surface = mask.to_surface()
        mask_surface.set_colorkey((0,0,0))
        self.surf.blit(mask_surface, (position[0]-width, position[1]))
        self.surf.blit(mask_surface, (position[0]+width, position[1]))
        self.surf.blit(mask_surface, (position[0], position[1]-width))
        self.surf.blit(mask_surface, (position[0], position[1]+width))

    def handle_mouse_event(self, mouse, cursor):
        if mouse[0] and self.surf.get_bounding_rect().collidepoint(cursor):
            for key, sprite in self.buttons.items():
                if sprite.collidepoint(cursor):
                    self.sprite_data.active = key

    def draw(self):
        super().draw()
        x = -1
        for key, sprite in self.sprite_data.sprite_keys.items():
            if key >= 0 and key % self.max_buttons == 0:
                x+=1
            if self.sprite_data.active == key:
                self.highlight_outline(sprite, (x*TILE_SIZE, (key % self.max_buttons)*TILE_SIZE))
            self.buttons[key] = self.surf.blit(sprite, (x*TILE_SIZE, (key % self.max_buttons)*TILE_SIZE))

