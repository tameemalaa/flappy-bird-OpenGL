from OpenGL.GL import *
from OpenGL.GLUT import *
from src.constants import *
import pygame
import os

textures_paths = [x for x in os.listdir(os.path.dirname(TEXTURES_DIRECTORY))]
textures_lookup = {x: y for y, x in enumerate(textures_paths)}


def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
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
