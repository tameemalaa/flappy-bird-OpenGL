import os
from threading import Thread
from playsound import playsound
from src.constants import AUDIO_DIRECTORY


PARENT_DIR = os.path.dirname(os.path.abspath(__file__)).replace(":", ":\\")[:-4]


class Audio(Thread):
    """
    Thread class that plays a sound file in the background.

    Attributes:
        audio_file (str): The path of the audio file to be played.

    Methods:
        run(): plays the audio file using the playsound function from playsound library.
    """

    def __init__(self, audio_file: str) -> None:
        super().__init__()
        self.audio_file = os.path.join(PARENT_DIR, AUDIO_DIRECTORY, audio_file)

    def run(self):
        """
        plays the audio file using the playsound function from playsound library.

        Args:
            None

        Returns:
            None
        """
        playsound(self.audio_file)
