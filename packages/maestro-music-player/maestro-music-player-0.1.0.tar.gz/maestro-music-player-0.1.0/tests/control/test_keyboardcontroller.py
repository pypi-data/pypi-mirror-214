from maestro.control.keyboardcontroller import KeyboardController


class dummy_func:

    def __init__(self):
        self._calls = 0

    def __call__(self, *args, **kwargs):
        self._calls += 1

    @property
    def was_never_called(self):
        return self._calls == 0

    @property
    def was_called_once(self):
        return self._calls == 1

def test_do_not_return_key_name_when_print_keycodes_deactivated():
    a = dummy_func()
    keymap = {'k': a}
    controller = KeyboardController(keymap)
    assert controller.keypress_event((121, 'a'), ['shift']) is None
    assert a.was_never_called

def test_returns_key_name_when_print_keycodes_activated():
    a = dummy_func()
    keymap = {'k': a}
    controller = KeyboardController(keymap)
    controller.print_keycodes = True
    message = controller.keypress_event((121, 'a'), ['shift'])
    assert 'shift-a' in message
    assert 'shift-121' in message
    message = controller.keypress_event((118, ''), ['shift'])
    assert 'shift-118' in message
    assert a.was_never_called

def test_keyboard_controller_keypress_by_name():
    a = dummy_func()
    keymap = {'k': a}
    controller = KeyboardController(keymap)
    assert controller.keypress_event((123, 'k'), []) is None
    assert a.was_called_once

def test_keyboard_controller_keypress_by_code():
    a = dummy_func()
    keymap = {'123': a}
    controller = KeyboardController(keymap)
    controller.keypress_event((123, 'k'), [])
    assert a.was_called_once

def test_keyboard_controller_keypress_with_modifiers():
    a = dummy_func()
    b = dummy_func()
    keymap = {'k': a, 'shift-k': b}
    controller = KeyboardController(keymap)
    controller.keypress_event((123, 'k'), ['shift'])
    assert a.was_never_called
    assert b.was_called_once

def test_keyboard_controller_keypress_no_calls():
    a = dummy_func()
    b = dummy_func()
    keymap = {'k': a, 'shift-k': b}
    controller = KeyboardController(keymap)
    controller.keypress_event((123, 'z'), [])
    assert a.was_never_called
    assert b.was_never_called
