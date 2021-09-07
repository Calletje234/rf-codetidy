from robot.parsing import ModelTransformer
from robot.parsing import Token

from robot.parsing.model import Statement


class ChangeSpacingSettings(ModelTransformer):
    def __init__(self):
        self.changed_lines: int = 0

    def visit_SettingSection(self, node):
        return self.add_space(node)

    def add_space(self, node):
        self.changed_lines += 1
        space = Statement.from_tokens([Token(Token.EOL, '\n')])
        node.body.insert(-1, space)
        print("Inserted Empty Line")
        return self.generic_visit(node)

    def get_changed_lines(self):
        return self.changed_lines


class ChangeSpacingKeyword(ModelTransformer):
    def __init__(self):
        self.changed_lines: int = 0

    def visit_KeywordSection(self, node):
        return self.add_space(node)

    def add_space(self, node):
        self.changed_lines += 1
        space = Statement.from_tokens([Token(Token.EOL, '\n')])
        node.body.insert(-1, space)
        return self.generic_visit(node)

    def get_changed_lines(self):
        return self.changed_lines


class ChangeSpacingTestCase(ModelTransformer):
    def __init__(self):
        self.changed_lines: int = 0

    def visit_TestCaseSection(self, node):
        return self.add_space(node)

    def add_space(self, node):
        self.changed_lines += 1
        space = Statement.from_tokens([Token(Token.EOL, '\n')])
        node.body.insert(-1, space)
        return self.generic_visit(node)

    def get_changed_lines(self):
        return self.changed_lines


class ChangeSpacingVariable(ModelTransformer):
    def __init__(self):
        self.changed_lines: int = 0

    def visit_VariableSection(self, node):
        return self.add_space(node)

    def add_space(self, node):
        self.changed_lines += 1
        space = Statement.from_tokens([Token(Token.EOL, '\n')])
        node.body.insert(-1, space)
        return self.generic_visit(node)

    def get_changed_lines(self):
        return self.changed_lines







