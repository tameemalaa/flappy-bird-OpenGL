from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from src.constants import *
from src.game import Game
from src.texture import texture_init


def initialize_world():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glClearColor(0, 0, 0, 0)
    glOrtho(X_ORIGIN, WINDOW_WIDTH, Y_ORIGIN, WINDOW_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


def main():
    game = Game()
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow("Flappy Bird")
    initialize_world()
    glutDisplayFunc(game.play)
    glutIdleFunc(game.play)
    glutKeyboardFunc(game.user_input)
    glutReshapeFunc(lambda x, y: glutReshapeWindow(WINDOW_WIDTH, WINDOW_HEIGHT))
    texture_init()
    glutMainLoop()


if __name__ == "__main__":
    main()
