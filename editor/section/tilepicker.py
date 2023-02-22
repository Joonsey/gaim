from section.section import *

class Tilepicker(Section):
    def __init__(self, dimensions, color) -> None:
        super().__init__(dimensions, color)
        self.sprites = []
        self.load_sprites()

    def load_sprites(self, path="assets/imgs"):
        try:
            file_names = os.listdir(path)
            for file_name in file_names:
                file_path = os.path.join(path, file_name)
                self.sprites.append(pygame.image.load(file_path))
        except FileNotFoundError:
            print(f"asset path invalid: '{path}'")

    def draw(self):
        super().draw()
        for i, sprite in enumerate(self.sprites):
            self.surf.blit(sprite, (0,i*TILE_SIZE))

