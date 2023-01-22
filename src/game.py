from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from src.constants import *
from src.game_elements import *
from time import sleep
from random import randint
from src.audio import Audio


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
        
        Detailed description:
        the game state is an integer that represents the current state of the game.
        the game state can be one of the following:
            PRE_GAME: the game is in the pre game state. => -1
            PLAYING: the game is in the playing state. => 0
            POST_GAME: the game is in the post game state. => 1
        when the game is in the pre game state, the start message is rendered.
        when the game is in the playing state, the following happens:
            when the pipe spawn counter reaches the pipe couples spacing, a new pipe couple is added to the pipe couples list.
            when the pipe spawn counter reaches the pipe couples spacing, the pipe spawn counter is reset.
            when the pipe spawn counter is less than the pipe couples spacing, the pipe spawn counter is incremented.
                if the first pipe couple in the pipe couples list has bypassed the window left edge:
                    the first pipe couple in the pipe couples list is removed from the pipe couples list.
                if the first pipe couple in the pipe couples list has not been counted and the first pipe couple in the pipe couples list has bypassed the bird edge:
                    a point sound is played and the score value is incremented and mark the first pipe couple in the pipe couples list is marked as counted.
                    if the score value is 99: the game state is set to post game.
        when the game is in the post game state, the game over message is rendered.
        note that The sleep function is used to achieve the required FPS.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.background.render()
        if self.state == PRE_GAME:
            self.Start_message.render()
        elif self.state == PLAYING:
            if self.pipe_spawn_counter == TWO_PIPE_COUPLES_SPACING:
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
