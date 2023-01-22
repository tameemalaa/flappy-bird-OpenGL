from OpenGL.GL import *
from OpenGL.GLUT import *
from texture import textures_lookup
from constants import *
from typing import Type


class Rectangle:
    """
    rectangle class. Used to create a rectangle object. Used to create the ground, sky, pipes, bird and more.
    Attributes:
        x_start (int): the x coordinate of the left edge of the rectangle.
        y_start (int): the y coordinate of the bottom edge of the rectangle.
        width (int): the width of the rectangle.
        height (int): the height of the rectangle.
        x_end (int): the x coordinate of the right edge of the rectangle.
        y_end (int): the y coordinate of the top edge of the rectangle.
        x_center (int): the x coordinate of the center of the rectangle.
        y_center (int): the y coordinate of the center of the rectangle.
        x_velocity (int): the x velocity of the rectangle.
    Methods:
        draw(): draws the rectangle.
        render(texture_name): renders the rectangle with the given texture.
        refresh(): refreshes the rectangle's position.
    """

    def __init__(self, x_start: int, y_start: int, width: int, height: int) -> None:
        """
        initializes the rectangle class.
        """
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
        """
        draws the rectangle. Used for debugging. Not used in the final product. Use render instead.
        """
        glBegin(GL_POLYGON)
        glVertex(self.x_start, self.y_start, 0)
        glVertex(self.x_end, self.y_start, 0)
        glVertex(self.x_end, self.y_end, 0)
        glVertex(self.x_start, self.y_end, 0)
        glEnd()

    def render(self, texture_name: str) -> None:
        """
        draws the rectangle with the given texture.
        args:
            texture_name (str): the name of the texture to be used.
        """
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
        """
        refreshes the rectangle's position.
        """
        self.x_start += self.x_velocity
        self.y_start += self.y_velocity
        self.x_end = self.x_start + self.width
        self.y_end = self.y_start + self.height
        self.x_center = (self.x_start + self.x_end) // 2
        self.y_center = (self.y_start + self.y_end) // 2

    def detect_collision(self, other: Type["Rectangle"]) -> bool:
        """
        detects collision between two rectangles. Used to detect collision between the bird and other objects mainly.
        Args:
            other (Rectangle): the other rectangle to be checked for collision.

        Returns:
            bool: True if collision detected, False otherwise.
        """
        if (
            other.x_start <= self.x_end
            and self.x_start <= other.x_end
            and other.y_start <= self.y_end
            and self.y_start <= other.y_end
        ):
            return True
        return False

    def detect_window_top_edge_collision(self) -> bool:
        """
        detects collision with the top edge of the window. Used to detect collision between the bird and the top edge of the window mainly.

        Returns:
            bool: True if collision detected, False otherwise.
        """
        if self.y_end >= WINDOW_HEIGHT:
            return True
        return False

    def detect_window_left_edge_bypass(self) -> bool:
        """
        detects if the rectangle has bypassed the left edge of the window. Used to detect if the bird has bypassed the left edge of the window mainly.
        
        Returns:
            bool: True if bypass detected, False otherwise.
        """
        if self.x_end <= Y_ORIGIN:
            return True
        return False
