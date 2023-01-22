from constants import *
from rectangle import Rectangle


class GroundPipe(Rectangle):
    """
    GroundPipe class that inherits from the Rectangle class. Used to represent the ground pipes in the game.

    Attributes:
        x_velocity (int): the x velocity of the rectangle.
        texture_index (int): the index of the texture to be used.

    Methods:
        render(): renders the ground pipe with the given texture.
        detect_bird_edge_bypass(bird): detects if the pipe has bypassed the bird.
    """

    def __init__(self, x_start: int, y_start: int, texture_index: int = 1) -> None:
        super().__init__(x_start, y_start, PIPE_WIDTH, PIPE_HEIGHT)
        self.x_velocity = -1
        self.texture_index = texture_index

    def render(self) -> None:
        """
        renders the ground pipe with the given texture.
        """
        super().render(f"ground_pipe{self.texture_index}")

    def detect_bird_edge_bypass(self, bird) -> bool:
        """
        detects if the pipe has bypassed the bird. Used to detect if the bird has passed through the pipe.
        args:
            bird (Bird): the bird object.

        returns:
            bool: True if the pipe has bypassed the bird, False otherwise.
        """
        if self.x_end <= bird.x_start:
            return True
        return False


class SkyPipe(Rectangle):
    """
    SkyPipe class that inherits from the Rectangle class. Used to represent the sky pipes in the game.

    Attributes:
        x_velocity (int): the x velocity of the rectangle.
        texture_index (int): the index of the texture to be used.

    Methods:
        render(): renders the sky pipe with the given texture.
        detect_bird_edge_bypass(bird): detects if the pipe has bypassed the bird.

    """

    def __init__(self, x_start: int, y_start: int, texture_index: int = 1) -> None:
        super().__init__(x_start, y_start, PIPE_WIDTH, PIPE_HEIGHT)
        self.texture_index = texture_index

        self.x_velocity = -1

    def detect_bird_edge_bypass(self, bird) -> bool:
        """
        detects if the pipe has bypassed the bird. Used to detect if the bird has passed through the pipe.
        args:
            bird (Bird): the bird object.

        returns:
            bool: True if the pipe has bypassed the bird, False otherwise.
        """
        if self.x_end <= bird.x_start:
            return True
        return False

    def render(self) -> None:
        """
        renders the sky pipe with the given texture.
        """
        super().render(f"sky_pipe{self.texture_index}")


class PipeCouple:
    """
    PipeCouple class that represents a couple of pipes in the game. It consists of a sky pipe and a ground pipe.

    Attributes:
        opening_y_start (int): the y coordinate of the top edge of the opening.
        opening_y_end (int): the y coordinate of the bottom edge of the opening.
        sky_pipe (SkyPipe): the sky pipe object.
        ground_pipe (GroundPipe): the ground pipe object.
        counted (bool): a boolean that indicates if the pipe couple has been counted or not.

    Methods:
        detect_collision(rectangle): detects if the pipe couple has collided with the given rectangle.
        render(): renders the pipe couple.
    """

    def __init__(self, opening_y_start: int, texture_index: int = 1) -> None:
        self.texture_index = texture_index
        self.opening_y_start = opening_y_start
        self.opening_y_end = self.opening_y_start + PIPE_COUPLE_OPENING_HEIGHT
        self.sky_pipe = SkyPipe(
            WINDOW_WIDTH + DELAY_DISTANCE, self.opening_y_end, self.texture_index
        )
        self.ground_pipe = GroundPipe(
            WINDOW_WIDTH + DELAY_DISTANCE,
            self.opening_y_start - PIPE_HEIGHT,
            self.texture_index,
        )
        self.counted = False

    def detect_collision(self, rectangle: Rectangle) -> None:
        """
        detects if the pipe couple has collided with the given rectangle.
        Wrapper for the ground/sky pipe detect_collision
        args:
            rectangle (Rectangle): the rectangle object.

        returns:
            bool: True if the pipe couple has collided with the given rectangle, False otherwise.
        """
        return self.sky_pipe.detect_collision(
            rectangle
        ) or self.ground_pipe.detect_collision(rectangle)

    def render(self) -> None:
        """
        renders the pipe couple.
        Wrapper for the ground/sky pipe render
        """
        self.sky_pipe.render()
        self.ground_pipe.render()

    def refresh(self) -> None:
        """
        refreshes the pipe couple.
        Wrapper for the ground/sky pipe refresh

        """

        self.sky_pipe.refresh()
        self.ground_pipe.refresh()

    def detect_window_left_edge_bypass(self) -> bool:
        """
        detects if the pipe couple has bypassed the left edge of the window.
        Wrapper for the ground/sky pipe detect_window_left_edge_bypass

        returns:
            bool: True if the pipe couple has bypassed the left edge of the window, False otherwise.
        """
        return (
            self.sky_pipe.detect_window_left_edge_bypass()
            or self.ground_pipe.detect_window_left_edge_bypass()
        )

    def detect_bird_edge_bypass(self, bird) -> bool:
        """
        detects if the pipe couple has bypassed the bird.
        Wrapper for the ground/sky pipe detect_bird_edge_bypass

        args:
            bird (Bird): the bird object.

        returns:
            bool: True if the pipe couple has bypassed the bird, False otherwise.
        """
        return self.sky_pipe.detect_bird_edge_bypass(
            bird
        ) or self.ground_pipe.detect_bird_edge_bypass(bird)


class Bird(Rectangle):
    """
    Bird class that represents the bird in the game.

    Attributes:
        state_counter (int): the state counter of the bird.
        texture_index (int): the index of the texture to be used.

    Methods:
        render(): renders the bird with the given texture.
        detect_collision(rectangle): detects if the bird has collided with the given rectangle.
        detect_window_top_edge_bypass(): detects if the bird has bypassed the top edge of the window.
        detect_window_bottom_edge_bypass(): detects if the bird has bypassed the bottom edge of the window.

    """

    def __init__(self, x_start: int, y_start: int, texture_index: int = 1) -> None:
        super().__init__(x_start, y_start, BIRD_WIDTH, BIRD_HEIGHT)
        self.state_counter = 0
        self.texture_index = texture_index

    def render(self):
        """
        renders the bird with the given texture.
        """
        if self.state_counter <= BIRD_DOWN:
            super().render(f"bird_down{self.texture_index}")
        elif self.state_counter <= BIRD_MID:
            super().render(f"bird_mid{self.texture_index}")
        elif self.state_counter <= BIRD_UP:
            super().render(f"bird_up{self.texture_index}")
            if self.state_counter == BIRD_UP:
                self.state_counter = -1
        self.state_counter += 1

    def jump(self) -> None:
        """
        makes the bird jump.
        """
        self.state_counter = BIRD_MID - 1
        self.y_velocity += BIRD_VELOCITY_INCREMENT_ON_CLICK

    def refresh(self) -> None:
        """
        refreshes the bird.
        """
        self.y_velocity += GRAVITY
        super().refresh()


class Base(Rectangle):
    """
    Base class that represents the base in the game.
    attributes:
        x_velocity (int): the x velocity of the base.
    methods:
        render(): renders the base.
    """

    def __init__(self) -> None:
        super().__init__(X_ORIGIN, Y_ORIGIN, BASE_WIDTH, BASE_HEIGHT)
        self.x_velocity = -3

    def render(self) -> None:
        """
        renders the base.
        """
        if self.x_end <= WINDOW_WIDTH:
            self.x_start = X_ORIGIN
        super().render("base")


class Background(Rectangle):
    """
    Background class that represents the background in the game.

    attributes:
        texture_index (int): the index of the texture to be used.

    methods:
        render(): renders the background with the given texture.
    """

    def __init__(self, texture_index: int = 1) -> None:
        super().__init__(1, 1, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
        self.texture_index = texture_index

    def render(self) -> None:
        """
        renders the background with the given texture.
        """
        super().render(f"background{self.texture_index}")


class GameOver(Rectangle):
    """
    GameOver class that represents the game over message in the game.

    methods:
        render(): renders the game over message.
    """

    def __init__(self) -> None:
        super().__init__(
            (WINDOW_WIDTH // 2) - (GAME_OVER_WIDTH // 2),
            (WINDOW_HEIGHT // 2) - (GAME_OVER_HEIGHT // 2) + (BASE_HEIGHT // 2),
            GAME_OVER_WIDTH,
            GAME_OVER_HEIGHT,
        )

    def render(self) -> None:
        """
        renders the game over message.
        """
        super().render("game_over")


class StartMessage(Rectangle):
    """
    StartMessage class that represents the start message in the game.

    methods:
        render(): renders the start message.

    """

    def __init__(self) -> None:
        super().__init__(
            X_ORIGIN + 25, Y_ORIGIN + 50, WINDOW_WIDTH - 50, WINDOW_HEIGHT - 100
        )

    def render(self) -> None:
        """
        renders the start message.
        """
        super().render("start_message")


class ScoreDigit(Rectangle):
    """
    ScoreDigit class that represents a digit in the score in the game.
    """

    def __init__(self, x_start: int, y_start: int) -> None:
        super().__init__(x_start, y_start, SCORE_DIGIT_WIDTH, SCORE_DIGIT_HEIGHT)
        self.digit = "0"

    def render(self) -> None:
        """
        renders the digit.
        """
        super().render(str(self.digit))

    def set_digit(self, digit: str) -> None:
        self.digit = digit


class Score:
    """
    Score class that represents the score in the game.

    methods:
        render(): renders the score.
        refresh(): refreshes the score.
    """

    def __init__(self) -> None:
        self.right_digit = ScoreDigit(
            WINDOW_WIDTH // 2 + SCORE_DIGIT_WIDTH // 2,
            WINDOW_HEIGHT - (SCORE_DIGIT_HEIGHT + SCORE_DIGIT_SPACING // 2),
        )
        self.left_digit = ScoreDigit(
            WINDOW_WIDTH // 2 - SCORE_DIGIT_WIDTH // 2,
            WINDOW_HEIGHT - (SCORE_DIGIT_HEIGHT + SCORE_DIGIT_SPACING // 2),
        )
        self.digits = 0

    def render(self) -> None:
        """
        renders the score.
        """
        self.right_digit.render()
        self.left_digit.render()

    def refresh(self) -> None:
        """
        refreshes the score.
        """
        self.right_digit.refresh()
        self.left_digit.refresh()

    def set_score(self, score: int):
        """
        sets the score for each digit.

        args:
            score (int): the score to be set.
        """
        score_string = str(score) if score > 9 else "0" + str(score)
        self.digits = score_string
        self.right_digit.set_digit(self.digits[1])
        self.left_digit.set_digit(self.digits[0])
