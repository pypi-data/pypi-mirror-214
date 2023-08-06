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

def simple_cache(root_cls):
    root_cls._cache = {}
    root_cls._modified = False

    @classmethod
    def set_cache(cls, cache):
        if not isinstance(cache, dict):
            raise TypeError('cache should be a dict')
        cls._cache = cache
        cls._modified = False

    @classmethod
    def get_cache(cls):
        return cls._cache

    @classmethod
    def is_modified(cls):
        return cls._modified

    def get_from_cache(self, key):
        return self._cache.get(key)

    def write_to_cache(self, key, value):
        self._cache[key] = value
        root_cls._modified = True

    root_cls.set_cache = set_cache
    root_cls.get_cache = get_cache
    root_cls.get_from_cache = get_from_cache
    root_cls.write_to_cache = write_to_cache
    root_cls.is_modified = is_modified
    return root_cls


def cached_attr(attr_name: str, keyfunc: Callable):
    def wrap(compute_attr):
        def _compute_attr(self):
            key = keyfunc(self)
            value = self.get_from_cache(key)
            if value is None:
                value = compute_attr(self)
                self.write_to_cache(key, value)
            setattr(self, attr_name, value)
            return value
        return _compute_attr
    return wrap


