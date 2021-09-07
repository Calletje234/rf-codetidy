from robot.parsing.model import Statement

from robot.parsing.model.statements import Documentation

from robot.parsing import ModelTransformer
from robot.parsing import Token


class AddDocSection(ModelTransformer):
    def __init__(self):
        self.added_docs = 0

    def visit_Keyword(self, node):
        if node.name.lstrip().startswith("#"):
            return
        return self.check_for_doc_presence(node)

    def visit_SettingSection(self, node):
        return self.check_for_doc_presence(node, True)

    def check_for_doc_presence(self, node, setting=False):
        for statements in node.body:
            if isinstance(statements, Documentation):
                break
        else:
            return self.generic_visit(self.add_doc(node, setting))

    def add_doc(self, node, setting):
        self.added_docs += 1
        if not setting:
            documentation = Statement.from_tokens([Token(Token.SEPARATOR, '    '),
                                                   Token(Token.DOCUMENTATION, '[Documentation]'),
                                                   Token(Token.SEPARATOR, '    '),
                                                   Token(Token.ARGUMENT, "Please fill in your own Documentation"),
                                                   Token(Token.EOL, '\n')])
            node.body.insert(0, documentation)
        else:
            documentation = Statement.from_tokens([Token(Token.DOCUMENTATION, 'Documentation'),
                                                   Token(Token.SEPARATOR, '    '),
                                                   Token(Token.ARGUMENT, "Please fill in your own Documentation"),
                                                   Token(Token.EOL, '\n')])
            node.body.insert(0, documentation)
        return self.generic_visit(node)

    def get_added_docs(self):
        return self.added_docs
