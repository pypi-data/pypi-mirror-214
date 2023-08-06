from maestro.control.configmanager import ConfigManager, InvalidConfig
from maestro.model.documentation import (
    Section,
    Text,
    Table,
    TableLine,
)

import pytest

def test_undefined_mapping_key_raises_invalid_config():
    specs = {'option': {'type': 'mapping', 'default': {}}}
    cm = ConfigManager(specs)
    with pytest.raises(InvalidConfig):
        cm.set_user_config({'option': {'a': None}})

def test_setting_key_to_none_raises_invalid_config():
    # simple
    specs = {'default': {'type': 'int', 'default': 3}}
    cm = ConfigManager(specs)
    with pytest.raises(InvalidConfig):
        cm.set_user_config({'default': None})
    # mapping key
    specs = {'food': {'fruits': {'apple': {'type': 'color', 'default': '#000000'}, 'orange': {'type': 'int', 'default': 3}}},
            }
    cm = ConfigManager(specs)
    user2 = {'food': {'fruits': None}}
    with pytest.raises(InvalidConfig):
        cm.set_user_config(user2)

def test_init_with_none_raises_invalid_config():
    specs = {'default': {'type': 'int', 'default': 3}}
    cm = ConfigManager(specs)
    with pytest.raises(InvalidConfig):
        cm.set_user_config(None)

def test_init_with_default():
    specs = {'default': {'type': 'int', 'default': 3}}
    cm = ConfigManager(specs)
    cm.set_user_config({})
    assert cm.ask_key('default') == 3

def test_colors():
    specs = {'background': {'type': 'color', 'default': '#ff0000'}}
    cm = ConfigManager(specs)
    cm.set_user_config({})
    assert cm.ask_key('background') == (1, 0, 0)

def test_invalid_color_in_config():
    specs = {'background': {'type': 'color', 'default': '#ff0000'}}
    cm = ConfigManager(specs)
    with pytest.raises(InvalidConfig):
        cm.set_user_config({'background': {'color': '#fg0000'}})

def test_user_can_define_optional_keys():
    specs = {'apple': {'type': 'int', 'default': 3}, 'banana': {'type': 'int'}}
    cm = ConfigManager(specs)
    user = {'banana': 4}
    cm.set_user_config(user)
    assert cm.ask_key('banana') == 4

def test_user_cannot_define_new_keys():
    specs = {'apple': {'type': 'int', 'default': 3}, 'banana': {'type': 'int', 'default': 4}}
    cm = ConfigManager(specs)
    user = {'chocolate': 4}
    with pytest.raises(InvalidConfig):
        cm.set_user_config(user)

def test_user_can_override_default_keys():
    specs = {'apple': {'type': 'int', 'default': 3}, 'banana': {'type': 'int', 'default': 4}}
    cm = ConfigManager(specs)
    user = {'apple': 6}
    cm.set_user_config(user)
    assert cm.ask_key('apple') == 6

def test_force_default_bypasses_user_key():
    specs = {'apple': {'type': 'int', 'default': 3}, 'banana': {'type': 'int', 'default': 4}}
    cm = ConfigManager(specs)
    user = {'apple': 6}
    cm.set_user_config(user)
    assert cm.ask_key('apple', force_default=True) == 3

def test_undefined_mandatory_key_raises_error():
    specs = {'apple': {'type': 'int', 'default': 3}, 'banana': {'type': 'int'}}
    cm = ConfigManager(specs)
    user = {'apple': 6}
    with pytest.raises(InvalidConfig):
        cm.set_user_config(user)

def test_defining_key_with_wrong_type_raises_error():
    specs = {'apple': {'type': 'int', 'default': 3}, 'banana': {'type': 'int'}}
    cm = ConfigManager(specs)
    user = {'apple': 'test', 'banana': 3}
    with pytest.raises(InvalidConfig):
        cm.set_user_config(user)
    user2 = {'banana': 'test', 'apple': 3}
    with pytest.raises(InvalidConfig):
        cm.set_user_config(user2)

def test_ask_incomplete_key_path_raises_error():
    specs = {'food': {'fruits': {'apple': {'type': 'int', 'default': 3}, 'banana': {'type': 'int'}}}}
    cm = ConfigManager(specs)
    user = {'food': {'fruits': {'apple': 6, 'banana': 2}}}
    cm.set_user_config(user)
    with pytest.raises(KeyError):
        cm.ask_key('food')
    with pytest.raises(KeyError):
        cm.ask_key('food.fruits')

def test_ask_too_long_key_path_raises_error():
    specs = {'food': {'fruits': {'apple': {'type': 'int', 'default': 3}, 'banana': {'type': 'int'}}}}
    cm = ConfigManager(specs)
    user = {'food': {'fruits': {'apple': 6, 'banana': 2}}}
    cm.set_user_config(user)
    with pytest.raises(KeyError):
        cm.ask_key('food.fruits.apple.what')
    with pytest.raises(KeyError):
        cm.ask_key('food.fruits.banana.2')

def test_ask_invalid_key_path_raises_error():
    specs = {'food': {'fruits': {'apple': {'type': 'int', 'default': 3}, 'banana': {'type': 'int'}}}}
    cm = ConfigManager(specs)
    user = {'food': {'fruits': {'apple': 6, 'banana': 2}}}
    cm.set_user_config(user)
    with pytest.raises(KeyError):
        cm.ask_key('food.fruits.tomato')
    with pytest.raises(KeyError):
        cm.ask_key('food.meat.chicken')

def test_access_to_nested_keys():
    specs = {'food': {'fruits': {'apple': {'type': 'int', 'default': 3}, 'banana': {'type': 'int'}},
                      'chocolate': {'type': 'int', 'default': 20}}
            }
    cm = ConfigManager(specs)
    user = {'food': {'fruits': {'banana': 6}}}
    cm.set_user_config(user)
    assert cm.ask_key('food.fruits.banana') == 6
    assert cm.ask_key('food.fruits.apple') == 3
    assert cm.ask_key('food.chocolate') == 20

def test_change_user_config():
    specs = {'food': {'fruits': {'apple': {'type': 'int', 'default': 3}, 'banana': {'type': 'int'}},
                      'chocolate': {'wonkamagic': {'type': 'int', 'default': 20}}
                     }
            }
    cm = ConfigManager(specs)
    user = {'food': {'fruits': {'banana': 6}}}
    cm.set_user_config(user)
    assert cm.ask_key('food.fruits.apple') == 3
    assert cm.ask_key('food.fruits.banana') == 6
    assert cm.ask_key('food.chocolate.wonkamagic') == 20
    new_user = {'food': {'fruits': {'banana': 2, 'apple': 6}}}
    cm.set_user_config(new_user)
    assert cm.ask_key('food.fruits.apple') == 6
    assert cm.ask_key('food.fruits.banana') == 2
    assert cm.ask_key('food.chocolate.wonkamagic') == 20

def test_infinite_keys():
    specs = {'food': {'fruits': {'type': 'mapping', 'default': {'apple': 3}},
                      'chocolate': {'type': 'int', 'default': 20}}
            }
    cm = ConfigManager(specs)
    user0 = {}
    cm.set_user_config(user0)
    assert cm.ask_key('food.fruits.apple') == 3
    assert cm.ask_key('food.chocolate') == 20
    user1 = {'food': {'fruits': {'orange': 1, 'banana': 6, 'lemon': 24}}}
    cm.set_user_config(user1)
    data = cm.ask_key('food.fruits')
    assert data['orange'] == 1
    assert data['banana'] == 6
    assert data['lemon'] == 24
    assert data['apple'] == 3
    assert cm.ask_key('food.chocolate') == 20
    user3 = {'food': {'fruits': 12}}
    with pytest.raises(InvalidConfig):
        cm.set_user_config(user3)

def test_force_default_bypasses_user_mapping_keys():
    specs = {'food': {'fruits': {'type': 'mapping', 'default': {'apple': 3}},
                     }
            }
    cm = ConfigManager(specs)
    user1 = {'food': {'fruits': {'apple': 1, 'banana': 6, 'lemon': 24}}}
    cm.set_user_config(user1)
    data = cm.ask_key('food.fruits', force_default=True)
    assert data == {'apple': 3}
    data = cm.ask_key('food.fruits.apple', force_default=True)
    assert data == 3

def test_documentation_generation():
    specs = {
        'app': {
            'user': {'type': 'str', 'description': 'The username'},
            'decoration': {'type': 'bool', 'default': True, 'description': 'Show decorations'},
            'magic': {'type': 'color'},
        },
        'description': 'An awesome app',
    }
    cm = ConfigManager(specs)
    doc = Section(
        Text('An awesome app'),
        Section(Text('user'),
            Text('The username'),
            Table(
                TableLine(Text('type'), Text('str')),
                TableLine(Text('required'), Text('YES')),
            )
        ),
        Section(Text('decoration'),
            Text('Show decorations'),
            Table(
                TableLine(Text('type'), Text('bool')),
                TableLine(Text('required'), Text('no')),
                TableLine(Text('default'), Text('True')),
            )
        ),
        Section(Text('magic'),
            Table(
                TableLine(Text('type'), Text('color')),
                TableLine(Text('required'), Text('YES')),
            )
        ),
    )
    assert cm.get_config_help('')

