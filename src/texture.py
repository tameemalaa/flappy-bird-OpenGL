from OpenGL.GL import *
from OpenGL.GLUT import *
from constants import *
import pygame
import os

textures_paths = [x for x in os.listdir(os.path.dirname(TEXTURES_DIRECTORY))]
textures_lookup = {x: y for y, x in enumerate(textures_paths)}


def texture_setup(
    texture_image_binary: list[bytes], texture_number: int, width: int, height: int
) -> None:
    """
    Sets up a texture for OpenGL and map it to a texture_number.

    Args:
        texture_image_binary (list[bytes]): The texture image in binary format.
        texture_number (int): The texture number.
        width (int): The width of the texture.
        height (int): The height of the texture.

    Returns:
        None
    """
    glBindTexture(GL_TEXTURE_2D, texture_number)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        width,
        height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        texture_image_binary,
    )
    glBindTexture(GL_TEXTURE_2D, -1)


def texture_init():
    """
    Initializes the textures for OpenGL.
    """
    glEnable(GL_TEXTURE_2D)
    texture_pygame = [
        pygame.image.load(TEXTURES_DIRECTORY + texture)
        for texture in textures_lookup.keys()
    ]
    textures_opengl = [
        pygame.image.tostring(texture, "RGBA", True) for texture in texture_pygame
    ]
    glGenTextures(len(texture_pygame), [*textures_lookup.values()])
    for i in range(len(texture_pygame)):
        texture_setup(
            textures_opengl[i],
            i,
            texture_pygame[i].get_width(),
            texture_pygame[i].get_height(),
        )
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
