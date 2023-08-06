#!/usr/bin/env python3

# This file is part of maestro, a keyboard-driven configurable music player.
# Copyright (C) 2022  Baptiste Lambert (Blaireau) rabbitstemplate@disroot.org
#
# Maestro is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path

from maestro.utils.math import clamp, none_to_default


class SongPlayerBase:
    def __init__(self):
        self._is_idle = True  # True if the player has nothing to play (finished playing)
        self._is_paused = False  # True if pausing
        self.time = 0  # playing time in ms
        self.duration = 0  # duration time in ms
        self.volume = 100  # volume in range [0; 100]

    @property
    def is_idle(self):
        return self._is_idle

    @property
    def is_paused(self):
        return self._is_paused

    def set_song(self, path: Path):
        pass

    def ping(self):
        pass

    def set_volume(self, new_volume: int):
        pass

    def increment_volume(self, increment: int):
        pass

    def toggle_play_pause(self):
        pass

    def pause(self):
        pass

    def play(self):
        pass

    def stop(self):
        pass


class SongPlayerVLC(SongPlayerBase):
    def __init__(self, vlc):
        super().__init__()
        self._vlc = vlc
        self.instance = vlc.Instance()
        self.media = None
        self.player = self.instance.media_player_new()

    def set_song(self, path: Path):
        self.media = self.instance.media_new(path.as_posix())
        self.player.set_media(self.media)

    def ping(self):
        state = self.player.get_state()
        if self.media:
            self.time = self.player.get_time()
            self.duration = self.media.get_duration()
        self.volume = self.player.audio_get_volume()
        if state == self._vlc.State.Ended or state == self._vlc.State.Stopped:
            self._is_idle = True
        self._is_paused = state == self._vlc.State.Paused

    def set_volume(self, new_volume: int):
        volume = clamp(0, 100, new_volume)
        self.player.audio_set_volume(volume)

    def increment_volume(self, increment: int):
        volume = self.player.audio_get_volume()
        volume = clamp(0, 100, volume + increment)
        self.set_volume(volume)

    def toggle_play_pause(self):
        self.player.pause()

    def pause(self):
        if not self._is_paused:
            self.player.pause()

    def play(self):
        if self.media is None:
            return
        self._is_idle = False
        self.player.play()

    def stop(self):
        self.player.stop()


class SongPlayerMPV(SongPlayerBase):
    def __init__(self, mpv):
        super().__init__()
        self.player = mpv.MPV()
        self.player.pause = True
        self.player.keep_open = True
        self.media = None

    def set_song(self, path: Path):
        self.media = path.as_posix()
        self.player.play(self.media)

    def ping(self):
        if not self._is_idle and self.player.eof_reached:
            self._is_idle = True
        self.time = none_to_default(self.player.playback_time, 0) * 1000
        self.duration = none_to_default(self.player.duration, 0) * 1000
        self.volume = round(self.player.volume)
        self._is_paused = self.player.pause

    def set_volume(self, new_volume: int):
        volume = clamp(0, 100, new_volume)
        self.player.volume = volume

    def increment_volume(self, increment: int):
        volume = self.player.volume
        volume = clamp(0, 100, volume + increment)
        self.set_volume(volume)

    def toggle_play_pause(self):
        self.player.pause = not self.player.pause

    def pause(self):
        self.player.pause = True

    def play(self):
        if self.media is None:
            return
        self._is_idle = False
        self.player.pause = False

    def stop(self):
        self.player.stop()
        self._is_idle = True


def SongPlayer(backend: str):
    match backend:
        case "mpv":
            import mpv  # type: ignore

            return SongPlayerMPV(mpv)
        case "vlc":
            import vlc  # type: ignore

            return SongPlayerVLC(vlc)
        case _:
            raise ValueError("audio backend should be 'mpv' or 'vlc'")
