import os
import pygame
from PIL import Image

TILE_SIZE = 32
MAX_ROWS = 150
MAX_COLUMNS = 150

WIDTH = 1080
HEIGHT = 720

class SpriteData:
    def __init__(self) -> None:
        self.sprites = []
        self.load_sprites()
        self.sprite_keys = {key+1:val for key, val in enumerate(self.sprites)}
        self.active = 0

    def load_sprites(self, path="assets/imgs"):
        try:
            file_names = os.listdir(path)
            for i, file_name in enumerate(file_names):
                file_path = os.path.join(path, file_name)
                tile = pygame.image.load(file_path)
                self.sprites.append(tile)
        except FileNotFoundError:
            print(f"asset path invalid: '{path}'")

    @staticmethod
    def split_sheets(file_name, assets_path: str = "assets/sheets/") -> None:
        """
        only splits horizontaly for now
        """
        file, ext = os.path.splitext(assets_path+file_name)
        try:
            with Image.open(assets_path+file_name) as im:
                columns = im.width // TILE_SIZE
                for index in range(columns):
                    offset = index*TILE_SIZE
                    cropped_image_name = f"assets/imgs/{file_name}-{index}{ext}"
                    im.crop((offset, 0, offset + TILE_SIZE, im.height)).save(cropped_image_name, 'png')
        except Exception as e:
            print("Error loading spritesheet at: ", assets_path+file_name)
            print(e)


if __name__ == "__main__":
    SpriteData.split_sheets("red-bush.png")


