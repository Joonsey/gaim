from section.section import *

class Tilepicker(Section):
    def __init__(self, dimensions, color, **kwargs) -> None:
        super().__init__(dimensions, color, **kwargs)
        self.has_mouse_event = True
        self.active_sprite = None
        self.buttons = {}

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
        for key, sprite in self.sprite_data.sprite_keys.items():
            if self.sprite_data.active == key:
                self.highlight_outline(sprite, (0, key*TILE_SIZE))
            self.buttons[key] = self.surf.blit(sprite, (0, key*TILE_SIZE))

