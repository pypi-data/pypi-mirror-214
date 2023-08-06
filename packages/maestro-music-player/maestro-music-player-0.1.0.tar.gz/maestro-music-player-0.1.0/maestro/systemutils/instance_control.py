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

from typing import Callable, Any, Tuple

import os
import signal
import sys
import time

from pathlib import Path

ROOT = Path("~/.cache/maestro").expanduser()


# instance file
INSTANCE_FILE = ROOT / ".instance"
MESSAGE_FILE = ROOT / ".message"
MASTER_INSTANCE_TIMEOUT = 5


def get_running_instance() -> int | None:
    if INSTANCE_FILE.exists():
        with open(INSTANCE_FILE, "r") as file:
            pid = int(file.read())
        return pid
    return None


# ================================ MASTER ================================


def make_master_handler(command_handler: Callable) -> Callable:
    def _handler(*args: Any) -> None:
        slave_instance, command_line = master_read_message()
        message = command_handler(command_line)
        if message is None:
            message = ''
        master_send_message(message, slave_instance)
    return _handler


def open_master_instance(command_handler: Callable) -> None:
    if not INSTANCE_FILE.exists():
        INSTANCE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(INSTANCE_FILE, "w") as file:
            pid = str(os.getpid())
            file.write(pid)
        signal.signal(signal.SIGUSR1, make_master_handler(command_handler))
    else:
        raise Exception("Cannot open multiple instances")


def close_master_instance() -> None:
    INSTANCE_FILE.unlink()


def master_send_message(message: str, slave_instance: int) -> None:
    MESSAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MESSAGE_FILE, "w") as file:
        file.write(message)
    os.kill(slave_instance, signal.SIGUSR1)


def master_read_message() -> Tuple[int, str]:
    with open(MESSAGE_FILE, "r") as file:
        data = file.read()
    slave, command_line = data.split("\n")
    slave_instance = int(slave)
    return slave_instance, command_line


# ================================ SLAVE ================================


def make_slave_handler(command_handler: Callable) -> Callable:
    def _handler(*args: Any) -> None:
        message = slave_read_message()
        command_handler(message)
    return _handler


def slave_print_and_exit(message: str) -> None:
    if message:
        print(message)
    sys.exit()

def slave_wait_for_response() -> None:
    time.sleep(MASTER_INSTANCE_TIMEOUT)
    slave_print_and_exit("Master instance is not responding")

def open_slave_instance() -> None:
    signal.signal(signal.SIGUSR1, make_slave_handler(slave_print_and_exit))

def slave_send_message(message: str, master_instance: int) -> None:
    MESSAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MESSAGE_FILE, "w") as file:
        pid = str(os.getpid())
        file.write(pid)
        file.write("\n")
        file.write(message)
    os.kill(master_instance, signal.SIGUSR1)
    slave_wait_for_response()

def master_instance_exists(master_instance: int) -> None:
    """ Check For the existence of a unix pid. """
    try:
        os.kill(master_instance, 0)
    except OSError:
        return False
    else:
        return True

def slave_read_message() -> str:
    with open(MESSAGE_FILE, "r") as file:
        message = file.read()
    return message
