from constants import *
from rectangle import Rectangle


class GroundPipe(Rectangle):
    def __init__(self, x_start: int, y_start: int, texture_index: int = 1) -> None:
        super().__init__(x_start, y_start, PIPE_WIDTH, PIPE_HEIGHT)
        self.x_velocity = PIPE_X_VELOCITY
        self.texture_index = texture_index

    def render(self) -> None:
        super().render(f"ground_pipe{self.texture_index}")

    def detect_window_left_edge_bypass(self) -> bool:
        if self.x_end <= Y_ORIGIN:
            return True
        return False

    def detect_bird_edge_bypass(self, bird) -> bool:
        if self.x_end <= bird.x_start:
            return True
        return False


class SkyPipe(Rectangle):
    def __init__(self, x_start: int, y_start: int, texture_index: int = 1) -> None:
        super().__init__(x_start, y_start, PIPE_WIDTH, PIPE_HEIGHT)
        self.x_velocity = PIPE_X_VELOCITY
        self.texture_index = texture_index

    def detect_window_left_edge_bypass(self) -> bool:
        if self.x_end <= Y_ORIGIN:
            return True
        return False

    def detect_bird_edge_bypass(self, bird) -> bool:
        if self.x_end <= bird.x_start:
            return True
        return False

    def render(self) -> None:
        super().render(f"sky_pipe{self.texture_index}")


class PipeCouple:
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
        return self.sky_pipe.detect_collision(
            rectangle
        ) or self.ground_pipe.detect_collision(rectangle)

    def render(self) -> None:
        self.sky_pipe.render()
        self.ground_pipe.render()

    def refresh(self) -> None:
        self.sky_pipe.refresh()
        self.ground_pipe.refresh()

    def detect_window_left_edge_bypass(self) -> bool:
        return (
            self.sky_pipe.detect_window_left_edge_bypass()
            or self.ground_pipe.detect_window_left_edge_bypass()
        )

    def detect_bird_edge_bypass(self, bird) -> bool:
        return self.sky_pipe.detect_bird_edge_bypass(
            bird
        ) or self.ground_pipe.detect_bird_edge_bypass(bird)


class Bird(Rectangle):
    def __init__(self, x_start: int, y_start: int, texture_index: int = 1) -> None:
        super().__init__(x_start, y_start, BIRD_WIDTH, BIRD_HEIGHT)
        self.state_counter = 0
        self.texture_index = texture_index

    def render(self):
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
        self.state_counter = BIRD_MID - 1
        self.y_velocity += BIRD_VELOCITY_INCREMENT_ON_CLICK

    def refresh(self) -> None:
        self.y_velocity += GRAVITY
        super().refresh()


class Base(Rectangle):
    def __init__(self) -> None:
        super().__init__(X_ORIGIN, Y_ORIGIN, BASE_WIDTH, BASE_HEIGHT)
        self.x_velocity = BASE_X_VELOCITY

    def render(self) -> None:
        if self.x_end <= WINDOW_WIDTH:
            self.x_start = X_ORIGIN
        super().render("base")


class Background(Rectangle):
    def __init__(self, texture_index: int = 1) -> None:
        super().__init__(1, 1, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
        self.texture_index = texture_index

    def render(self) -> None:
        super().render(f"background{self.texture_index}")


class GameOver(Rectangle):
    def __init__(self) -> None:
        super().__init__(
            (WINDOW_WIDTH // 2) - (GAME_OVER_WIDTH // 2),
            (WINDOW_HEIGHT // 2) - (GAME_OVER_HEIGHT // 2) + (BASE_HEIGHT // 2),
            GAME_OVER_WIDTH,
            GAME_OVER_HEIGHT,
        )

    def render(self) -> None:
        super().render("game_over")


class StartMessage(Rectangle):
    def __init__(self) -> None:
        super().__init__(
            X_ORIGIN + 25, Y_ORIGIN + 50, WINDOW_WIDTH - 50, WINDOW_HEIGHT - 100
        )

    def render(self) -> None:
        super().render("start_message")


class ScoreDigit(Rectangle):
    def __init__(self, x_start: int, y_start: int) -> None:
        super().__init__(x_start, y_start, SCORE_DIGIT_WIDTH, SCORE_DIGIT_HEIGHT)
        self.digit = "0"

    def render(self) -> None:
        super().render(str(self.digit))

    def set_digit(self, digit: str) -> None:
        self.digit = digit


class Score:
    def __init__(self) -> None:
        self.right_digit = ScoreDigit(
            WINDOW_WIDTH // 2 + SCORE_DIGIT_WIDTH // 2,
            WINDOW_HEIGHT - (SCORE_DIGIT_HEIGHT + 5),
        )
        self.left_digit = ScoreDigit(
            WINDOW_WIDTH // 2 - SCORE_DIGIT_WIDTH // 2,
            WINDOW_HEIGHT - (SCORE_DIGIT_HEIGHT + 5),
        )
        self.digits = 0

    def render(self) -> None:
        self.right_digit.render()
        self.left_digit.render()

    def refresh(self) -> None:
        self.right_digit.refresh()
        self.left_digit.refresh()

    def set_score(self, score: int):
        score_string = str(score) if score > 9 else "0" + str(score)
        self.digits = score_string
        self.right_digit.set_digit(self.digits[1])
        self.left_digit.set_digit(self.digits[0])
