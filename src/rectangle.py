from OpenGL.GL import *
from OpenGL.GLUT import *
from src.texture import textures_lookup
from src.constants import *
from typing import Type


class Rectangle:
    def __init__(self, x_start: int, y_start: int, width: int, height: int) -> None:
        self.x_start = x_start
        self.width = width
        self.x_end = self.x_start + self.width
        self.y_start = y_start
        self.height = height
        self.y_end = self.y_start + self.height
        self.x_center = (self.x_start + self.x_end) // 2
        self.y_center = (self.y_start + self.y_end) // 2
        self.x_velocity = self.y_velocity = 0

    def draw(self) -> None:
        glBegin(GL_POLYGON)
        glVertex(self.x_start, self.y_start, 0)
        glVertex(self.x_end, self.y_start, 0)
        glVertex(self.x_end, self.y_end, 0)
        glVertex(self.x_start, self.y_end, 0)
        glEnd()

    def render(self, texture_name: str) -> None:
        glColor(1, 1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, textures_lookup[texture_name + ".png"])
        glBegin(GL_POLYGON)
        glTexCoord(0, 0)
        glVertex2d(self.x_start, self.y_start)
        glTexCoord(1, 0)
        glVertex2d(self.x_end, self.y_start)
        glTexCoord(1, 1)
        glVertex2d(self.x_end, self.y_end)
        glTexCoord(0, 1)
        glVertex2d(self.x_start, self.y_end)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, -1)

    def refresh(self) -> None:
        self.x_start += self.x_velocity
        self.y_start += self.y_velocity
        self.x_end = self.x_start + self.width
        self.y_end = self.y_start + self.height
        self.x_center = (self.x_start + self.x_end) // 2
        self.y_center = (self.y_start + self.y_end) // 2

    def detect_collision(self, other: Type["Rectangle"]) -> bool:
        if (
            other.x_start <= self.x_end
            and self.x_start <= other.x_end
            and other.y_start <= self.y_end
            and self.y_start <= other.y_end
        ):
            return True
        return False

    def detect_window_top_edge_collision(self) -> bool:
        if self.y_end >= WINDOW_HEIGHT:
            return True
        return False
