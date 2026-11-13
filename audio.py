"""pygame.mixerを使ったゲーム音声。"""

import math
import struct

import pygame


class AudioManager:
    """効果音を生成して再生する管理クラス。"""

    SAMPLE_RATE = 44100

    def __init__(self):
        pygame.mixer.init(frequency=self.SAMPLE_RATE, size=-16, channels=1)
        self.sounds = {
            "select": self._make_sound(660, 0.08),
            "correct": self._make_sound(880, 0.12),
            "wrong": self._make_sound(180, 0.18),
            "hint": self._make_sound(520, 0.1),
            "give_up": self._make_sound(240, 0.18),
            "finish": self._make_sound(1046, 0.2),
        }

    def _make_sound(self, frequency, duration):
        sample_count = int(self.SAMPLE_RATE * duration)
        frames = bytearray()
        for index in range(sample_count):
            envelope = 1 - index / sample_count
            value = int(
                10000
                * envelope
                * math.sin(2 * math.pi * frequency * index / self.SAMPLE_RATE)
            )
            frames.extend(struct.pack("<h", value))
        return pygame.mixer.Sound(buffer=bytes(frames))

    def play(self, sound_name):
        self.sounds[sound_name].play()

    def close(self):
        pygame.mixer.quit()
