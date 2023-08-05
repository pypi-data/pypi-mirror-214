import cv2
import numpy as np
import sys
import timeit
import time
from tqdm import tqdm
from math import sqrt
from ._util import *

ORIGIN = "\033[0;0H"
ALPHABET = " .:-=+*#%@"
RESET = "\033[39m"
CLEAR = "\033[2J"


class video:
    def __init__(self, file: str):
        self.video = cv2.VideoCapture(file)
        if not self.video.isOpened():
            raise FileNotFoundError("Could not open the video file")

        self.fps = int(self.video.get(cv2.CAP_PROP_FPS))
        self.framecount = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frames = []
        self.ascii_frames = []
        self.converted = False

    def convert(self, alphabet=ALPHABET, progress_bar=True):
        if self.converted:
            ConvertWarning("Video has already been converted")
            return

        wrapper = tqdm if progress_bar else lambda x: x
        video: cv2.VideoCapture = self.video

        while video.isOpened():
            success, frame = video.read()
            if not success:
                break

            self.frames.append(frame)

        if len(self.frames) == 0:
            raise ConvertError("No frames were read from the video")

        if len(self.frames) > 1000:
            ConvertWarning("Video is very long, this may take a while")

        char_width, char_height = get_bounds(self.width, self.height)
        last_color_str = None
        frame: np.ndarray
        for frame in wrapper(self.frames):
            ascii_frame: str = ""
            frame_resized: np.ndarray = cv2.resize(
                frame, (char_width, char_height))
            frame_rgb: np.ndarray = cv2.cvtColor(
                frame_resized, cv2.COLOR_BGR2RGB)

            for row in frame_rgb:
                for pixel in row:
                    r, g, b = pixel

                    lum: float = sqrt(
                        0.299 * r ** 2 + 0.587 * g ** 2 + 0.114 * b ** 2)
                    ascii_char: str = alphabet[int(
                        lum / 255 * (len(alphabet)))]

                    color_str: str = get_color(r, g, b)
                    if color_str != last_color_str:
                        last_color_str = color_str
                        ascii_frame += RESET + color_str + ascii_char
                    else:
                        ascii_frame += ascii_char

                ascii_frame += "\n"

            self.ascii_frames.append(ascii_frame)
        self.converted = True
        return self.ascii_frames

    def play(self, sync=True, progress_bar=True):
        if not self.converted:
            print("Converting video...")
            self.convert(progress_bar=progress_bar)

        print(CLEAR, end="")

        try:
            frame_gap = 1 / self.fps
            for frame in self.ascii_frames:
                sys.stdout.write(ORIGIN + frame)
                delay = timeit.timeit(sys.stdout.flush, number=1)
                if sync:
                    if delay < frame_gap:
                        time.sleep(frame_gap - delay)
                
        except KeyboardInterrupt:
            print(RESET + CLEAR, end="")
            print("Video playback stopped")
            return
