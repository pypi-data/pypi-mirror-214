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
from typing import Callable
import itertools
from collections import defaultdict

from maestro.model.documentation import (
    DocPart,
    Section,
    Table,
    TableLine,
    Text,
)
from maestro.utils.parsing import make_description


class CommandError(Exception):
    pass


class CommandInterface:
    COMMAND_DATA_FIELD = '_command_data'

    def __init__(self, name="<root>"):
        self.root_group = CommandGroup(name)
        for elem in dir(self):
            field = getattr(self, elem)
            if callable(field) and hasattr(field, self.COMMAND_DATA_FIELD):
                cmd_data = getattr(field, self.COMMAND_DATA_FIELD)
                top_cmd = cmd_data.get_top_command()
                self.root_group.register_command(top_cmd)

    def interprete_command(self, command_line: str):
        return self.prepare_command(command_line)()

    def prepare_command(self, command_line: str):
        callback, args = self.root_group.parse(command_line)
        return lambda : callback(self, *args)

    def get_command_help(self, command_line: str):
        help_text = self.root_group.get_help(command_line)
        return help_text


class BaseCommand:

    def __init__(self, name: str, description=None):
        self.name = name
        self.summary, self.description = make_description(description)
        self.parent = CommandGroup._current_group
        self.thematicgroup = ThematicGroup.get_current()
        if self.parent is not None:
            self.parent.register_command(self)
        if self.thematicgroup is not None:
            self.thematicgroup.register_command(self)

    def get_top_command(self):
        if self.parent is None:
            return self
        return self.parent.get_top_command()

    @property
    def full_name(self):
        names = []
        cmd = self
        while cmd is not None:
            names.append(cmd.name)
            cmd = cmd.parent
        return ' '.join(reversed(names))

    def __repr__(self):
        return f'/{self.full_name}>'


class ThematicGroup:
    __count = 0
    _current_group = None
    _lock = False

    @classmethod
    def new_count(cls):
        count = cls.__count
        cls.__count += 1
        return count

    @classmethod
    def unlock(cls):
        cls._lock = False

    @classmethod
    def lock(cls):
        cls._lock = True

    @classmethod
    def get_current(cls):
        if not cls._lock:
            return cls._current_group

    def __init__(self, name: str, description=None):
        self.name = name
        self.index = ThematicGroup.new_count()
        self.description = description
        self.parent = ThematicGroup._current_group
        self.commands = []

    def __enter__(self):
        ThematicGroup._current_group = self
        ThematicGroup.unlock()

    def __exit__(self, *args):
        ThematicGroup._current_group = self.parent

    def register_command(self, command: BaseCommand):
        if command not in self.commands:
            self.commands.append(command)

    def __lt__(self, other):
        if isinstance(other, ThematicGroup):
            return self.index < other.index
        return NotImplemented # pragma: no cover


class CommandGroup(BaseCommand):
    _current_group = None

    def __init__(self, *args, fallback_path: str|None=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = {}
        self.fallback_path = fallback_path

    def __enter__(self):
        CommandGroup._current_group = self
        ThematicGroup.lock()

    def __exit__(self, *args):
        CommandGroup._current_group = self.parent
        ThematicGroup.unlock()

    def parse(self, command_line: str=""):
        subcommand_name, *args = command_line.strip().split(' ', 1)
        if subcommand_name == '':
            if self.fallback_path is None:
                raise CommandError(f'Command "{self.full_name}" expects a subcommand')
            subcommand_name, *args = self.fallback_path.strip().split(' ', 1)
        try:
            subcommand = self.commands[subcommand_name]
        except KeyError:
            if self.parent is None:
                message = f'Command {subcommand_name} does not exist'
            else:
                message = (f'Command "{self.full_name}" '
                           f'has no subcommand {subcommand_name}')
            raise CommandError(message)
        if len(args) == 0:
            return subcommand.parse()
        return subcommand.parse(args[0])

    @property
    def documentation(self) -> DocPart:
        doc = Section(Text(f'List of commands for {self.full_name}:'))
        all_commands = set(self.commands.values())
        thematic_groups = set()
        other_commands = set()
        for command in all_commands:
            if command.thematicgroup is None:
                other_commands.add(command)
            else:
                thematic_groups.add(command.thematicgroup)
        if len(thematic_groups) == 0:
            table = Table(columns=2)
            for cmd in self.commands.values():
                table.add(TableLine(Text(cmd.name), Text(cmd.summary)))
            doc.add(table)
        else:
            if other_commands:
                other_group = ThematicGroup('Other')
                for cmd in other_commands:
                    other_group.register_command(cmd)
                thematic_groups.add(other_group)
            for thematicgroup in sorted(thematic_groups):
                table = Table(columns=2)
                thematic = Section(Text(thematicgroup.name), table)
                for cmd in thematicgroup.commands:
                    table.add(TableLine(Text(cmd.name), Text(cmd.summary)))
                doc.add(thematic)
        return doc

    def get_help(self, command_line: str=""):
        subcommand_name, *args = command_line.strip().split(' ', 1)
        if subcommand_name in self.commands:
            return self.commands[subcommand_name].get_help(*args)
        return self.documentation

    def register_command(self, command: BaseCommand):
        previous = self.commands.get(command.name)
        if previous is command:
            return
        if previous is not None:
            raise ValueError(f'Multiple definition of command {command.name} '
                             f'in group {self.full_name}')
        self.commands[command.name] = command


class Argument:

    def __init__(self, description: str,
                       validator: Callable,
                       convertor: Callable,
                       default=None,
                       name=None,
                       greedy=False):
        self._name = name
        if default is not None:
            self.description = f'{description}, default: {default}'
        else:
            self.description = description
        self.validator = validator
        self.convertor = convertor
        self.default = default
        self.greedy = greedy

    @property
    def name(self):
        if self._name is None:
            return '_'
        return self._name

    @property
    def usage(self):
        if self.default is None:
            return self.name
        return f'[{self.name}]'

    def parse(self, text: str | None):
        if text is None:
            if self.default is None:
                raise CommandError('Missing mandatory argument')
            return self.default
        if self.validator(text):
            return self.convertor(text)
        raise CommandError(f'Invalid argument "{text}"')


class Command(BaseCommand):

    def __init__(self,
                 name: str,
                 callback: Callable,
                 args_specs: list[Argument],
                 **kwargs):
        super().__init__(name, **kwargs)
        self.callback = callback
        self.args_specs = args_specs

    def parse(self, command_line: str | None = None):
        arg_str = ('' if command_line is None else command_line).strip()
        arg_list = []
        for arg_spec in self.args_specs:
            # read one argument
            if arg_str == '':
                arg = None
            elif ' ' in arg_str and not arg_spec.greedy:
                arg, remain = arg_str.split(' ', 1)
                arg_str = remain.strip()
            else:
                arg = arg_str
                arg_str = ''
            # process argument
            try:
                arg_value = arg_spec.parse(arg)
            except CommandError as error:
                raise CommandError(f'{str(error)} for command "{self.name}"')
            arg_list.append(arg_value)
        if arg_str != '':
            raise CommandError(f'Too many arguments for command "{self.name}"')
        return (self.callback, arg_list)

    @property
    def documentation(self) -> DocPart:
        args_usage = ' '.join(a.usage for a in self.args_specs)
        usage_line = f'Usage: {self.full_name} {args_usage}'
        args_descs = [
            TableLine(
                Text(a.name),
                Text(a.description)
            ) for a in self.args_specs
        ]
        args_table = [Table(*args_descs)] if len(args_descs) > 0 else []
        description_texts = [Text(part) for part in self.description]
        doc = Section(Text(f'Command {self.full_name}:'),
                      Text(self.summary),
                      Section(Text(usage_line),
                              *args_table,
                      ),
                      *description_texts,
        )
        return doc

    def get_help(self, command_line: str=""):
        return self.documentation



def command(name: str, *argument_specifications,
            description=None):
    def decorate(method):
        cmd_obj = Command(name,
                          method,
                          argument_specifications,
                          description=description,
                          )
        setattr(method, CommandInterface.COMMAND_DATA_FIELD, cmd_obj)
        return method
    return decorate

def str_arg(description: str, default=None, name=None):
    return Argument(description, lambda x: True, lambda x:x,
                    default=default,
                    name='<string>' if name is None else name)

def greedy_str_arg(description: str, default=None, name=None):
    return Argument(description, lambda x: True, lambda x:x,
                    default=default,
                    name='<string>' if name is None else name,
                    greedy=True)

def flag_arg(*flag_values, default=None, name=None):
    values = ', '.join(f"'{value}'" for value in flag_values)
    description = f'one of {values}'
    validator = lambda x: x in flag_values
    return Argument(description, validator, lambda x:x,
                    default=default,
                    name=name)

def bool_arg(default=None, name=None):
    description = f'"on" or "off"'
    validator = lambda x: x in ['on', 'off']
    transform = lambda x: {"on": True, "off": False}[x]
    return Argument(description, validator, transform,
                    default=default,
                    name='<state>' if name is None else name)

def int_arg(default=None, name=None):
    description = f'an integer'
    validator = lambda x: x.isdigit()
    return Argument(description, validator, lambda x:int(x),
                    default=default,
                    name='<int>' if name is None else name)

