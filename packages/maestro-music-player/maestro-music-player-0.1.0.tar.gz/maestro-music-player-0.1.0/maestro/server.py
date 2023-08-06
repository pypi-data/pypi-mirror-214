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


if __name__ == "__main__":
    import argparse
    from maestro.view.constants import MAESTRO_MOTTO
    from maestro.utils.ressources import USER_CONFIG_FILE
    from maestro.systemutils.instance_control import (
        get_running_instance,
        open_master_instance,
        close_master_instance,
        master_instance_exists,
    )

    parser = argparse.ArgumentParser(
        prog='maestroserver',
        description='Launch the main application',
        epilog='If you want to send commands to the main application, use maestro',
    )
    parser.add_argument(
        '-c', '--config',
        action='store',
        dest='config_file',
        default=USER_CONFIG_FILE,
        help='configuration file path',
    )
    args = parser.parse_args()

    # instance system
    instance = get_running_instance()
    if instance:
        if master_instance_exists(instance):
            print(f'There is already a maestro instance running [pid {instance}] !')
            quit()
        else:
            close_master_instance()
    # start master instance
    print("starting maestro master instance")
    import os
    os.environ['KIVY_NO_ARGS'] = '1'
    # start application
    import trio
    from maestro.control.maincontroller import MainController
    from maestro.view.application import MaestroApp
    from maestro.model.application import Application
    from maestro.sound.songplayer import SongPlayer

    # loop = asyncio.get_event_loop()

    controller = MainController(
        model=Application,
        view=MaestroApp,
        sound=SongPlayer,
        user_config=args.config_file,
    )

    open_master_instance(controller.command_line_event)

    trio.run(controller.async_run)

    close_master_instance()
