import pygame
import json
from util.constants import *
from section import *

pygame.init()
sprite_data = SpriteData()

class Editor:
    def __init__(self, width, height, sections = []) -> None:
        self.surface = pygame.display.set_mode((width, height))
        self.sprite_data = sprite_data
        self.sections = sections
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            for section in self.sections:
                if section.active:
                    section.draw()
                    self.surface.blit(section.surf, section.offset)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        for sec in self.sections:
                            if type(sec) == Grid:
                                sec.toggle_grid()

                    if event.key == pygame.K_s:
                        for sec in self.sections:
                            if type(sec) == Grid:
                                sec.save_world()


            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                self.running = False

            if keys[pygame.K_d]:
                self.sprite_data.active = -1

            mouse = pygame.mouse.get_pressed()
            cursor = pygame.mouse.get_pos()

            for section in self.sections:
                if section.has_mouse_event and section.active:
                    section.handle_mouse_event(mouse, cursor)

    @staticmethod
    def parse_from_json(path: str = "config.json") -> list[Section]:
        sections = []
        with open(path, "r") as f:
            config = json.load(f)

        for s in config["sections"]:
            offset = [0,0]
            if "offset" in s.keys():
                offset = s["offset"]
            offset[0] *= WIDTH
            offset[1] *= HEIGHT
            rel_dim = s["relative_dimension"]
            eval_string = f'{s["type"]}((WIDTH*{rel_dim[0]},HEIGHT*{rel_dim[1]}), {s["color"]}, offset={offset}, sprite_data=sprite_data)'
            sec = eval(eval_string)
            sections.append(sec)
        return sections

if __name__ == "__main__":
    sections = Editor.parse_from_json()
    editor = Editor(WIDTH, HEIGHT, sections)
    #sprite_data.split_sheets("green-bush.png")
    editor.run()
