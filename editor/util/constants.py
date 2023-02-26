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
        self.sprite_keys = {key:val for key, val in enumerate(self.sprites)}
        self.active = -1
        self.flipped = False
        self.bg = None
        self.load_background()

    def load_sprites(self, path="assets/imgs"):
        try:
            file_names = os.listdir(path)
            file_names.sort()
            for i, file_name in enumerate(file_names):
                file_path = os.path.join(path, file_name)
                tile = pygame.image.load(file_path)
                tile = pygame.transform.scale(tile, (TILE_SIZE,TILE_SIZE))
                #tile_but_rotated = pygame.transform.flip(tile, True, False)
                self.sprites.append(tile)
        except FileNotFoundError:
            print(f"asset path invalid: '{path}'")

    def load_background(self, path="assets/bg/bg.png"):
        try:
            self.bg = pygame.image.load(path)
        except:
            print("unable to load background image")

    @staticmethod
    def split_sheets(file_name, assets_path: str = "assets/sheets/", tile_size=TILE_SIZE) -> None:
        file, ext = os.path.splitext(assets_path+file_name)
        try:
            with Image.open(assets_path+file_name) as im:
                columns = im.width // tile_size
                rows = im.height // tile_size
                for column in range(columns):
                    for row in range(rows):
                        x_offset = column*tile_size
                        y_offset = row*tile_size
                        cropped_image_name = f"assets/imgs/{file_name}-{column}-{row}{ext}"
                        im.crop((x_offset, y_offset, x_offset + tile_size, y_offset+tile_size)).save(cropped_image_name, 'png')
        except Exception as e:
            print("Error loading spritesheet at: ", assets_path+file_name)
            print(e)


if __name__ == "__main__":
    SpriteData.split_sheets(input(), tile_size=16)
