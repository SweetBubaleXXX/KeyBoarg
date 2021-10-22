import os
import sys
from threading import Thread

import simpleaudio as sa
from pynput import keyboard
from pynput.keyboard import Key

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


def play_audio(file):
    wave_obj = sa.WaveObject.from_wave_file(file)
    play_obj = wave_obj.play()
    play_obj.wait_done()


def get_filename(key):
    if key == Key.space or key == Key.backspace:
        return "_space.wav"
    elif key == Key.enter:
        return "_enter.wav"
    else:
        return ".wav"


def on_press(key):
    global pressed_key
    try:
        if (pressed_key == key and pressed_key.released == True) or pressed_key != key:
            pressed_key = key
            pressed_key.released = False
            play_audio(f"sounds/press{get_filename(key)}")
    except NameError:
        pressed_key = key


def on_release(key):
    global pressed_key
    try:
        pressed_key.released = True
    except NameError:
        pass
    play_audio(f"sounds/release{get_filename(key)}")


with keyboard.Listener(
        on_press=lambda key: Thread(
            target=on_press, args=(key,)).start(),
        on_release=lambda key: Thread(
            target=on_release, args=(key,)).start()) as listener:
    listener.join()
