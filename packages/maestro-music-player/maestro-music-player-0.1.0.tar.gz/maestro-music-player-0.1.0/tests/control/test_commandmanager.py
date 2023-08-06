from maestro.control.commandmanager import (
    CommandInterface,
    command,
    CommandGroup,
    ThematicGroup,
    CommandError,
    str_arg,
    flag_arg,
    int_arg,
)

import pytest

@pytest.fixture
def stupid():
    class Stupid(CommandInterface):
        pass

    return Stupid()

@pytest.fixture
def counter():
    class Counter(CommandInterface):

        def __init__(self):
            super().__init__()
            self.reset()

        @command('increment')
        def increment_counter(self):
            self.counter += 1

        @command('reset')
        def reset(self):
            self.counter = 0

        def dummy(self):
            pass

    return Counter()


@pytest.fixture
def cake_maker():
    class CakeMaker(CommandInterface):

        def __init__(self):
            super().__init__()
            self.ingredients = {}
            self.message = None

        @command('add',
                 flag_arg('sugar', 'flour', 'lemon', 'eggs'),
                 int_arg(default=1),
        )
        def add(self, ingredient: str, quantity: int):
            self.ingredients[ingredient] = quantity

        def _show_ingredient(self, ingredient, quantity):
            if quantity == 1:
                return ingredient
            else:
                return f'{quantity} {ingredient}'

        @command('bake')
        def bake(self):
            content = ', '.join(self._show_ingredient(i, n)
                                for i, n in self.ingredients.items())
            return f'A cake with {content}'

        @command('decorate',
                 str_arg('message'),
        )
        def decorate(self, message):
            self.message = message

    return CakeMaker()


@pytest.fixture
def house():
    class House(CommandInterface):

        def __init__(self):
            self.actions = []
            super().__init__()

        with ThematicGroup('security'):
            @command('unlock')
            def unlock_house(self):
                self.log_action('unlock')

            @command('lock')
            def lock_house(self):
                self.log_action('lock')

        with CommandGroup('kitchen'):

            with CommandGroup('cook'):

                @command('meal', str_arg('meal name'))
                def meal(self, meal: str):
                    self.log_action(f'cook a {meal}')

                @command('tea')
                def tea(self):
                    self.log_action(f'make some tea')

                @command('pasta')
                def pasta(self):
                    self.log_action(f'have some pasta')

            @command('wash')
            def wash_kitchen(self):
                self.log_action('wash')

        with CommandGroup('bathroom'):

            @command('wash')
            def wash_bathroom(self):
                self.log_action('wash')

        def log_action(self, action):
            self.actions.append(action)

        @property
        def present(self):
            return ' '.join(self.actions)

        with CommandGroup('bedroom'):

            @command('wash')
            def wash_bedroom(self):
                self.log_action('wash')

            @command('sleep')
            def sleep(self):
                self.log_action('sleep')


    return House()


def test_help_simple_command(counter):
    doc = counter.get_command_help('increment')
    assert 'increment' in ''.join(doc.header.lines)

def test_help_command_with_arguments(cake_maker):
    doc = cake_maker.get_command_help('add')
    args = doc[1][0]
    assert 'add' in ''.join(doc.header.lines)
    assert 'sugar' in ''.join(args[0][1].lines)
    assert '1' in ''.join(args[1][1].lines)

def test_help_on_command_group(house):
    doc = house.get_command_help('kitchen')
    assert 'kitchen' in ''.join(doc.header.lines)
    cmds = doc[0]
    assert 'cook' in ''.join(cmds[0][0].lines)
    assert 'wash' in ''.join(cmds[1][0].lines)

def test_help_on_command_inside_group(house):
    doc = house.get_command_help('kitchen cook meal')
    assert 'kitchen cook meal' in ''.join(doc.header.lines)
    args = doc[1][0]
    assert 'meal name' in ''.join(args[0][1].lines)

def test_stupid_class_with_no_commands(stupid):
    with pytest.raises(CommandError):
        stupid.interprete_command('test')

def test_simple_increment_counter(counter):
    assert counter.counter == 0
    counter.interprete_command('increment')
    assert counter.counter == 1

def test_other_counter(counter):
    assert counter.counter == 0
    for x in range(10):
        counter.interprete_command('increment')
    assert counter.counter == 10
    counter.interprete_command('reset')
    assert counter.counter == 0
    with pytest.raises(CommandError):
        counter.interprete_command('dummy')

def test_commands_with_arguments(cake_maker):
    cake_maker.interprete_command('add sugar 1')
    assert cake_maker.interprete_command('bake') == 'A cake with sugar'
    cake_maker.interprete_command('add flour')
    assert cake_maker.interprete_command('bake') == 'A cake with sugar, flour'
    cake_maker.interprete_command('add eggs 3')
    assert cake_maker.interprete_command('bake') == 'A cake with sugar, flour, 3 eggs'
    cake_maker.interprete_command('add lemon')
    assert cake_maker.interprete_command('bake') == 'A cake with sugar, flour, 3 eggs, lemon'
    cake_maker.interprete_command('decorate wow!')
    assert cake_maker.message == 'wow!'

def test_too_many_arguments(cake_maker):
    with pytest.raises(CommandError):
        cake_maker.interprete_command('add lemon 3 big red apples')

def test_not_enough_arguments(cake_maker):
    with pytest.raises(CommandError):
        cake_maker.interprete_command('add')

def test_invalid_argument(cake_maker):
    with pytest.raises(CommandError):
        cake_maker.interprete_command('add trash')

def test_command_inside_a_group(house):
    house.interprete_command('unlock')
    house.interprete_command('bathroom wash')
    house.interprete_command('bedroom sleep')
    house.interprete_command('lock')
    assert house.present == 'unlock wash sleep lock'

def test_command_inside_a_nested_group(house):
    house.interprete_command('kitchen cook tea')
    house.interprete_command('bedroom wash')
    house.interprete_command('kitchen cook pasta')
    assert house.present == 'make some tea wash have some pasta'

def test_command_inside_a_nested_group_with_arguments(house):
    house.interprete_command('kitchen cook meal chicken')
    house.interprete_command('bathroom wash')
    house.interprete_command('kitchen cook tea')
    house.interprete_command('bedroom sleep')
    assert house.present == 'cook a chicken wash make some tea sleep'

def test_invalid_command_in_group_raises_exception(house):
    with pytest.raises(CommandError):
        house.interprete_command('kitchen cook coffee')

def test_calling_a_group_raises_command_error(house):
    with pytest.raises(CommandError):
        house.interprete_command('bathroom')
    with pytest.raises(CommandError):
        house.interprete_command('kitchen cook')
    with pytest.raises(CommandError):
        house.interprete_command('kitchen sleep')

def test_thematic_group(house):
    doc = house.get_command_help('')
    thematic = doc[0]
    assert 'security' == ''.join(thematic.header.lines)

def test_multiple_commands_with_same_name_in_group_raises_value_error():
    with pytest.raises(ValueError):
        class House(CommandInterface):

            def __init__(self):
                self.actions = []
                super().__init__()

            with CommandGroup('kitchen'):

                with CommandGroup('cook'):

                    @command('meal', str_arg('meal name'))
                    def meal(self, meal: str):
                        self.log_action(f'cook a {meal}')

                    @command('tea')
                    def tea(self):
                        self.log_action(f'make some tea')

                    @command('meal')
                    def pasta(self):
                        self.log_action(f'have some pasta')

