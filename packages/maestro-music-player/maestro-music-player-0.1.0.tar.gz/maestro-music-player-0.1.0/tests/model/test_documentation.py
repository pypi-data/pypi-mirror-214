from maestro.model.documentation import (
    Section,
    Text,
    Table,
    TableLine,
)

import pytest


@pytest.fixture
def render_engine():
    class RenderEngine:

        def __init__(self):
            self.content = []
            self.headerMode = False
            self.tableMode = False
            self.depth = 0

        def render_content(self, content_item):
            headtag = '# ' if self.headerMode else ''
            line = ','.join(content_item.lines)
            item = f'{headtag}{line}'
            if self.tableMode:
                self.buffer.append(item)
            else:
                self.content.append(self.with_indent(item))

        def with_indent(self, text: str):
            indent = ' '*self.depth*2
            return f'{indent}{text}'

        def start_section(self):
            self.depth += 1

        def end_section(self):
            self.depth -= 1

        def start_header(self):
            self.headerMode = True

        def end_header(self):
            self.headerMode = False

        def start_table(self, columns):
            self.content.append(self.with_indent('---'))
            self.tableMode = True

        def end_table(self):
            self.content.append(self.with_indent('---'))
            self.tableMode = False

        def start_table_line(self):
            self.buffer = [self.with_indent('')]

        def end_table_line(self):
            self.buffer.append('')
            self.content.append('|'.join(self.buffer))

        @property
        def result(self):
            return '\n'.join(self.content)

    return RenderEngine()

def test_doc_compare():
    section = Section(Text('a', style='fancy'))
    section.add(Text('b'))
    assert Section(Text('a'), Text('b')) == section
    table = Table(columns=2)
    table.add(TableLine(Text('a'), Text('b')))
    table.add(TableLine(Text('c'), Text('d')))
    table2 = Table(TableLine(Text('a'), Text('b')),
                   TableLine(Text('c'), Text('d')))
    assert table == table2

def test_documentation_builder_nested_structure(render_engine):
    doc = Section(Text("Hello world"),
                  Section(Text("Part 1"),
                          Text("cool"),
                          Text("fun"),
                  ),
                  Section(Text("Part 2"),
                          Text("awesome"),
                  ),
                  Text("wow")
          )
    doc.render(render_engine)
    assert render_engine.result == '''
# Hello world
  # Part 1
    cool
    fun
  # Part 2
    awesome
  wow
'''.strip()

def test_documentation_add_items_to_section(render_engine):
    doc = Section(Text("Section 1"))
    for letter in 'abcde':
        doc.add(Text(letter))
    doc.render(render_engine)
    assert render_engine.result == '''
# Section 1
  a
  b
  c
  d
  e
'''.strip()

def test_documantation_with_table(render_engine):
    doc = Section(Text("The plan"),
                  Table(TableLine(Text("intro"), Text("what")),
                        TableLine(Text("then"), Text("who")),
                        TableLine(Text("finally"), Text("how"))
                  )
    )
    doc.render(render_engine)
    assert render_engine.result == '''
# The plan
  ---
  |intro|what|
  |then|who|
  |finally|how|
  ---
'''.strip()

def test_invalid_table_raises_exception(render_engine):
    with pytest.raises(ValueError):
        Table()
    with pytest.raises(ValueError):
        Table(TableLine(Text('one')), columns=2)
    with pytest.raises(ValueError):
        Table(TableLine(Text('one')), TableLine(Text('one'), Text('two')))
    table = Table(TableLine(Text('one')))
    with pytest.raises(ValueError):
        table.add(TableLine(Text('one'), Text('two')))
