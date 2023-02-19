import pyglet
import sys

from rendergroup import RenderGroup
from pyglet.gl import *
from pyglet.graphics import Group
from pyglet.graphics.shader import Shader, ShaderProgram

ASSETS = {"textures": {"player" : "pyglet.png"}}

SPEED = 220
BYTEORDER = "little"
POSITION_BYTE_LEN = 4
MAX_POSITION_BYTE_VAL = POSITION_BYTE_LEN **16


_vertex_source = """#version 330 core
    in vec2 position;
    in vec3 tex_coords;
    out vec3 texture_coords;
    uniform float time; 
    uniform WindowBlock 
    {                       // This UBO is defined on Window creation, and available
        mat4 projection;    // in all Shaders. You can modify these matrixes with the
        mat4 view;          // Window.view and Window.projection properties.
    } window;  
    void main()
    {
        gl_Position = window.projection * window.view * vec4(position, 1 * time, 1);
        texture_coords = tex_coords;
    }
"""

_fragment_source = """#version 330 core
    in vec3 texture_coords;
    out vec4 final_colors;
    uniform sampler2D our_texture;
    void main()
    {
        final_colors = texture(our_texture, texture_coords.xy);
    }
"""

vert_shader = Shader(_vertex_source, 'vertex')
frag_shader = Shader(_fragment_source, 'fragment')
shader_program = ShaderProgram(vert_shader, frag_shader)

def create_quad(x, y, texture):
    x2 = x + texture.width
    y2 = y + texture.height
    return x, y, x2, y, x2, y2, x, y2

def position_to_packet(position: tuple[int, int]):
    return position[0].to_bytes(POSITION_BYTE_LEN , BYTEORDER) + position[1].to_bytes(POSITION_BYTE_LEN , BYTEORDER)

class Player():
    def __init__(self, x: int, y: int, batch=None) -> None:
        self.x = x
        self.y = y
        self.batch = batch
        self.position = self.x, self.y
        self.texture = pyglet.resource.texture(ASSETS['textures']['player'])

        indices = (0, 1, 2, 0, 2, 3)
        self.vertex_list = shader_program.vertex_list_indexed(
            4, GL_TRIANGLES, 
            indices, 
            batch,
            position=('f', 
                      create_quad(
                        self.x, 
                        self.y,
                        self.texture)),
            tex_coords=('f', 
                        self.texture.tex_coords),
                        group=RenderGroup(self.texture, shader_program)
        )
        self.direction = [0,0]
        self.dash_cooldown = 2
        self.dash_duration = .2
        self._max_dash_duration = .2
        self._is_dashing = False

    def _update_pos(self, x, y, scroll):
        self.x = x
        self.y = y
        self.position = int(self.x), int(self.y)
        self.vertex_list = create_quad(x - scroll[0], y - scroll[1], self.texture)

    def dash(self, speed: int, direction: list|tuple[float | int, float | int], t :float, scroll: tuple, total_t: float|int = 1) -> float:
        if total_t <= 0:
            return self._max_dash_duration
        x = self.x + speed * direction[0] * t
        y = self.y + speed * direction[1] * t
        self._update_pos(x, y, scroll)
        return total_t-t if total_t-t > 0 else self._max_dash_duration

    def handle_movement(self, keyboard, mousehandler, dt, scroll):
        from pyglet.window import key
        from pyglet.window import mouse

        if self.dash_cooldown > 0: self.dash_cooldown -= dt

        if (mousehandler[mouse.LEFT] and self.dash_cooldown <= 0) or self.dash_duration != self._max_dash_duration:
            self.dash_cooldown = 2
            self.dash_duration = self.dash(SPEED*2, self.direction, dt, scroll, self.dash_duration)
            self._is_dashing = True
        else:
            self._is_dashing = False

        if keyboard[key.W]:
            self.direction[1] = 1

        elif keyboard[key.S]:
            self.direction[1] = -1

        else:
            self.direction[1] = 0

        if keyboard[key.A]:
            self.direction[0] = -1

        elif keyboard[key.D]:
            self.direction[0] = 1

        else:
            self.direction[0] = 0

        if keyboard[key.Q]:
            sys.exit()


        if self.direction[0] and self.direction[1]:
            self.direction = [i/2 for i in self.direction] #TODO ask leon about this lmao
            x = self.x + self.direction[0] * SPEED * dt
            y = self.y + self.direction[1] * SPEED * dt

        else:
            x = self.x + self.direction[0] * SPEED * dt
            y = self.y + self.direction[1] * SPEED * dt


        self._update_pos(x, y, scroll)
