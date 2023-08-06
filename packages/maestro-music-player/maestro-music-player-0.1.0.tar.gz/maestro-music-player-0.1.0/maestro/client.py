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
    from maestro.systemutils.instance_control import (
        get_running_instance,
        close_master_instance,
        open_slave_instance,
        slave_send_message,
    )

    parser = argparse.ArgumentParser(
        prog='maestro',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            'Send commands to the main application\n'
            'For a detailed help about available commands, see maestro help'
        ),
        epilog='If you want to launch the main application, use maestroserver',
    )
    parser.add_argument("--silent-missing-server", action='store_true',
                        help="do nothing if the server is not running",
                        dest='silent')
    parser.add_argument("command", nargs="*", help="any valid maestro command")
    args = parser.parse_args()

    if len(args.command) == 0:
        command_line = "help"
    else:
        command_line = " ".join(args.command)
    if command_line.startswith('help'):
        from maestro.control.maincontroller import MainController
        dummy_inst = MainController.dummy()
        dummy_inst.command_line_event(command_line)
    else:
        # instance system
        instance = get_running_instance()
        if instance:
            open_slave_instance()
            try:
                slave_send_message(command_line, instance)
            except ProcessLookupError:
                close_master_instance()
                instance = None
        if instance is None:
            if args.silent:
                print()
            else:
                print("No running maestro instance found. Start maestro first with maestroserver")
