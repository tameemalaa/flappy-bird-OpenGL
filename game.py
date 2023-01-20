from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from constants import *
from game_elements import *
from time import sleep
from random import randint
from audio import Audio


class Game:
    """
    The main game class. encapsulates all the game elements and the game logic.

    Attributes:
        bird(Bird): the bird object.
        background(Background): the background object.
        base(Base): the base object.
        game_over(GameOver): the game over object.
        start_message(StartMessage): the start message object.
        pipe_couples(list): the list of pipe couples.
        state(int): the game state.
        score(Score): the score object.
        score_value(int): the score value.
        pipe_spawn_counter(int): the counter used to spawn pipes.
        pipe_texture_index(int): the index of the pipe texture to be used.

    Methods:
        play(): handles the game logic.
        user_input(): handles the user input.
    """

    def __init__(self) -> None:
        """
        Initializes the Game class.
        """
        self.bird = Bird(127, 200, randint(1, 3))
        self.background = Background(randint(1, 2))
        self.base = Base()
        self.game_over = GameOver()
        self.Start_message = StartMessage()
        self.pipe_couples = []
        self.state = PRE_GAME
        self.score = Score()
        self.score_value = 0
        self.pipe_spawn_counter = 0
        self.pipe_texture_index = randint(1, 2)

    def play(self) -> None:
        """
        Handles the game logic.
        Args:
            None

        Returns:
            None
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.background.render()
        if self.state == PRE_GAME:
            self.Start_message.render()
        elif self.state == PLAYING:
            if self.pipe_spawn_counter == TWO_PIPE_COUPLES_OPENING_SPACING:
                self.pipe_couples.append(
                    PipeCouple(
                        randint(
                            BASE_HEIGHT, WINDOW_HEIGHT - PIPE_COUPLE_OPENING_HEIGHT
                        ),
                        self.pipe_texture_index,
                    )
                )
                self.pipe_spawn_counter = 0
            self.pipe_spawn_counter += 1
            for pipe_couple in self.pipe_couples:
                pipe_couple.render()
                pipe_couple.refresh()
            if self.pipe_couples:
                if self.pipe_couples[0].detect_window_left_edge_bypass():
                    self.pipe_couples.pop(0)
                if not self.pipe_couples[0].counted and self.pipe_couples[
                    0
                ].detect_bird_edge_bypass(self.bird):
                    Audio("point.wav").start()
                    self.score_value += 1
                    self.pipe_couples[0].counted = True
                    self.score.set_score(self.score_value)
                    if self.score_value == 99:
                        self.state = POST_GAME
            self.base.render()
            self.base.refresh()
            self.bird.render()
            self.bird.refresh()
            self.score.render()

            if (
                self.base.detect_collision(self.bird)
                or self.bird.detect_window_top_edge_collision()
                or any(
                    map(
                        lambda pipe_couple: pipe_couple.detect_collision(self.bird),
                        self.pipe_couples,
                    )
                )
            ):
                Audio("hit.wav").start()
                Audio("die.wav").start()
                self.state = POST_GAME
        else:
            for pipe_couple in self.pipe_couples:
                pipe_couple.render()
            self.base.render()
            self.bird.render()
            self.game_over.render()
            self.score.render()
            self.bird.state_counter = 0
            if self.bird.y_start > BASE_HEIGHT:
                self.bird.refresh()
        glutSwapBuffers()
        sleep(1 / FPS)

    def user_input(self, key: bytes, x: int, y: int) -> None:
        """
        Handles the user input. This function is called by the glutKeyboardFunc function.
        Args:
            key(bytes): the key pressed.
            x(int): the x coordinate of the mouse.
            y(int): the y coordinate of the mouse.

        Returns:
            None
        """
        if self.state == PRE_GAME or self.state == POST_GAME:
            if key == b" ":
                self.__init__()
                self.state = PLAYING
        if key == b" ":
            Audio("wing.wav").start()
            self.bird.jump()
