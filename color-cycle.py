#!/usr/bin/env python3


import argparse
import math
import signal
import sys
import time



from PIL import Image
from subprocess import Popen, PIPE


RUNNING = True


def handler(signum, frame):
    global RUNNING
    RUNNING = False
    PROC.terminate()


def solid_color_image(col):
    return Image.new("RGB", (640, 360), col)


START = time.time()
def elapsed():
    return time.time() - START


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True)
    parser.add_argument("--fps", type=float, default=30.0)
    args = parser.parse_args()

    signal.signal(signal.SIGINT, handler)

    URL = f"rtmp://a.rtmp.youtube.com/live2/{args.key}"

    CMD = [
        "ffmpeg",
        "-loglevel", "error",
        "-re",
        "-f", "image2pipe", "-i", "-",
        "-f", "lavfi", "-i", "anullsrc", \
        "-vcodec", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-r", "30", "-g", "60", "-b:v", "1000k",
        "-acodec", "libmp3lame", "-ar", "44100", "-b:a", "128k",
        "-bufsize", "300k",
    ]

    CMD += ["-f", "flv", URL]

    global PROC
    PROC = Popen(CMD, stdin=PIPE)


    colors = {
        "magenta": (255, 0, 255),
        "pink": (255, 182, 193),
        "grey": (105, 105, 105),
        "gold": (218, 165, 32),
        "black": (0, 0, 0),
    }


    images = {
        name: solid_color_image(c)
        for name, c in colors.items()
    }


    i = 0
    prev = ""

    while RUNNING:

        index = int(elapsed()) % len(images)
        color = list(images.keys())[index]

        if prev != color:
            print(color)
            prev = color

        images[color].save(PROC.stdin, "JPEG")
        time.sleep(1.0/args.fps)
        i += 1


    PROC.stdin.close()
    PROC.wait()

    print("(>o_O)> Finishing normally")
