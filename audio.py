import os
from threading import Thread
from playsound import playsound
from constants import AUDIO_DIRECTORY


PARENT_DIR = os.path.dirname(os.path.abspath(__file__)).replace(":", ":\\")


class Audio(Thread):
    def __init__(self, audio_file: str) -> None:
        super().__init__()
        self.audio = os.path.join(PARENT_DIR, AUDIO_DIRECTORY, audio_file)

    def run(self):
        playsound(self.audio)
