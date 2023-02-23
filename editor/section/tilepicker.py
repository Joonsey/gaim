from section.section import *

class Tilepicker(Section):
    def __init__(self, dimensions, color, **kwargs) -> None:
        super().__init__(dimensions, color, **kwargs)
        self.has_mouse_event = True
        self.active_sprite = None
        self.buttons = {}


    def handle_mouse_event(self, mouse, cursor):
        if mouse[0] and self.surf.get_bounding_rect().collidepoint(cursor):
            for key, sprite in self.buttons.items():
                if sprite.collidepoint(cursor):
                    self.sprite_data.active = key

    def draw(self):
        super().draw()
        for key, sprite in self.sprite_data.sprite_keys.items():
            self.buttons[key] = self.surf.blit(sprite, (0, key*TILE_SIZE))

