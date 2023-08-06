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
from enum import Enum

from maestro.model.documentation import (
    Text,
    Section,
    Table,
    TableLine
)

from maestro.utils.parsing import (
    parse_color,
    make_description,
)


class UndefinedKey:

    @classmethod
    def get(cls, *args):
        return cls

    @classmethod
    def __repr__(cls):
        return 'UndefinedKey'


class ConfigType(Enum):
    STR = 1
    INT = 2
    BOOL = 3
    COLOR = 4
    MAPPING = 5

    @classmethod
    def from_standard_type(cls, std_type: type):
        if std_type is str:
            return cls.STR
        if std_type is int:
            return cls.INT
        if std_type is bool:
            return cls.BOOL
        if std_type is dict:
            return cls.MAPPING

    @classmethod
    def from_type_name(cls, type_name: str):
        match type_name:
            case 'str': return cls.STR
            case 'int': return cls.INT
            case 'bool': return cls.BOOL
            case 'color': return cls.COLOR
            case 'mapping': return cls.MAPPING

    @classmethod
    def read_value(cls, value, expected_type: 'ConfigType'):
        assert isinstance(expected_type, ConfigType)
        if expected_type is ConfigType.COLOR:
            return parse_color(value)
        user_value_type = ConfigType.from_standard_type(type(value))
        if user_value_type != expected_type:
            raise ValueError(
                f'Expected a value of type {expected_type.name} '
                f'but got "{value}" of type {user_value_type.name}'
            )
        if ( expected_type is ConfigType.MAPPING
             and not all(v is not None for v in value.values())):
            raise ValueError(
                f'a key in the mapping has an undefined value'
            )
        return value


class InvalidConfig(Exception):
    pass


class ErrorCollector:

    def __init__(self):
        self._errors = []

    def log(self, message):
        self._errors.append(message)

    @property
    def has_errors(self):
        return len(self._errors) > 0

    @property
    def error(self):
        return InvalidConfig('\n'.join(self._errors))


class ConfigNode:

    def __init__(self, description=None):
        self.summary, self.description = make_description(description)

    def _show_key_path(self, *key_path: str) -> str:
        return ".".join(key_path)


class ConfigBlock(ConfigNode):

    FIELDS = ['description']

    def __init__(self, **specifications):
        kwargs = {}
        for key in ConfigBlock.FIELDS:
            if key in specifications:
                kwargs[key] = specifications.pop(key)
        super().__init__(**kwargs)
        self._keys = {}
        for config_key, value in specifications.items():
            if 'type' in value:
                constructor = ConfigOption
                args = [value.pop('type')]
            else:
                constructor = ConfigBlock
                args = []
            self._keys[config_key] = constructor(*args, **value)

    @property
    def documentation(self):
        return Section(*self.documentation_blocks)

    @property
    def documentation_blocks(self):
        sections = [Section(Text(key), *config_obj.documentation_blocks)
                    for key, config_obj in self._keys.items()]
        if self.summary:
            return [Text(self.summary), Text(*self.description), *sections]
        return sections

    def set_user_config(self,
                        user_config: dict,
                        keypath: list[str],
                        error_collector: ErrorCollector):
        key_path = self._show_key_path(*keypath)
        if user_config is None:
            error_collector.log(
                f'Key "{key_path}" was specified without any value'
            )
            user_config = UndefinedKey
        self._errors = []
        # check for invalid keys in user config
        if user_config is not UndefinedKey:
            for key in user_config:
                if key not in self._keys:
                    key_path = self._show_key_path(*keypath, key)
                    error_collector.log(f'"{key_path}" is not a valid key')
        # merge user config with default config
        final_config = {}
        for key, config_node in self._keys.items():
            user_value = user_config.get(key, UndefinedKey)
            config_node.set_user_config(user_value, [*keypath, key], error_collector)

    def ask_key(self, keypath: list[str], force_default: bool):
        if keypath == []:
            raise KeyError('Empty keypath')
        key_path = self._show_key_path(*keypath)
        first_key, *remain = keypath
        try:
            config_obj = self._keys[first_key]
        except KeyError:
            raise KeyError(f'Invalid keypath: {key_path}')
        if remain == [] and isinstance(config_obj, ConfigOption):
            if force_default:
                return config_obj.default
            else:
                return config_obj.value
        try:
            return config_obj.ask_key(remain, force_default)
        except KeyError:
            pass
        raise KeyError(f'Incomplete keypath: {key_path}')

    def __repr__(self):
        return repr(self._keys)


class ConfigOption(ConfigNode):

    def __init__(self, type_name, default=None, **kwargs):
        super().__init__(**kwargs)
        self.config_type = ConfigType.from_type_name(type_name)
        if default is None:
            self.is_mandatory = True
        else:
            self.is_mandatory = False
            self.default = ConfigType.read_value(default, self.config_type)
            self.value = self.default
            self.default_txt = repr(default)

    @property
    def documentation_blocks(self):
        table = Table(
            TableLine(Text('type'), Text(self.config_type.name.lower())),
            TableLine(Text('required'), Text('YES' if self.is_mandatory else 'no')),
        )
        if not self.is_mandatory:
            table.add(TableLine(Text('default'), Text(self.default_txt)))
        if self.summary != '':
            return [Text(self.summary), table, Text(*self.description)]
        return [table]

    def set_user_config(self,
                        raw_user_value,
                        keypath: list[str],
                        error_collector: ErrorCollector):
        key_path = self._show_key_path(*keypath)
        if raw_user_value is None:
            error_collector.log(
                f'Key "{key_path}" was specified without any value'
            )
            raw_user_value = UndefinedKey
        try:
            if self.is_mandatory:
                if raw_user_value is UndefinedKey:
                    error_collector.log(
                        f'Key {key_path} is required in config file'
                    )
                else:
                    self.value = ConfigType.read_value(raw_user_value, self.config_type)
            else:
                if raw_user_value is UndefinedKey:
                    self.value = self.default
                else:
                    user_value = ConfigType.read_value(raw_user_value, self.config_type)
                    if self.config_type is ConfigType.MAPPING:
                        self.value = {**self.default, **user_value}
                    else:
                        self.value = user_value
        except ValueError as error:
            error_collector.log(f'Invalid key "{key_path}": {error}')

    def __repr__(self):
        return self.config_type.name

    def ask_key(self, keys: list[str], force_default: bool):
        key, *_ = keys
        if self.config_type is ConfigType.MAPPING:
            if force_default:
                return self.default[key]
            else:
                return self.value[key]
        else:
            raise KeyError('ConfigOption of type {self.config_type.name} has no keys')


class ConfigManager:

    def __init__(self, specifications: dict):
        """
        Build a ConfigManager from a dict of specifications.

        The specifications are a nested dict that represent a tree.
        The leaves of the tree correspond to configurable options.

        Each configurable option has the following keys:
            type: the type of the config value
            default: a default value (for optional keys)
                     if this key is missing, this option is considered mandatory

        Each node can also have the following keys:
            description: a useful description used to generate the documentation
        """
        self._config_tree = ConfigBlock(**specifications)

    def set_user_config(self, user_config):
        """
        Set the user config

        user_config is a nested dict which must comply to the specifications
        that where passed to the constructor of the ConfigManager.

        The user config must have the same keys as the specification.
        Optional keys may be omited, all other keys are mandatory and must be
        defined.
        Keys should have the same type as in the specification.

        If the provided user_config does not respect the specification,
        an InvalidConfig exception is raised.
        """
        if user_config is None:
            raise InvalidConfig('The config file is empty')
        error_collector = ErrorCollector()
        self._config_tree.set_user_config(user_config, [], error_collector)
        if error_collector.has_errors:
            raise error_collector.error

    def ask_key(self, raw_key_path: str, force_default=False):
        """
        Ask for a key in the config file

        The key is searched first in the user config.
        If it’s found there, the value is returned.
        Otherwise, the default value from the specification is returned.
        """
        return self._config_tree.ask_key(self._extract_key_path(raw_key_path),
                                         force_default)

    def _extract_key_path(self, raw_key_path: str) -> list[str]:
        return raw_key_path.split('.')

    def get_config_help(self, raw_key_path: str):
        return self._config_tree.documentation

