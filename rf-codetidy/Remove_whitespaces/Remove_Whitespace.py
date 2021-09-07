from robot.parsing import ModelTransformer

from robot.api import Token


class RemoveWhiteSpace(ModelTransformer):
    def __init__(self):
        self.whitespace_lines = 0
        self.whitespaces = 0

    def visit_Statement(self, node):
        for token in node.get_tokens(Token.EOL):
            if self.change_token(token) != token.value:
                self.whitespace_lines += 1
                token.value = self.change_token(token)
        return node

    def get_amount_lines_edited(self):
        return self.whitespace_lines

    def get_amount_ws_removed(self):
        return self.whitespaces

    def change_token(self, token):
        updated_items: list = []
        for i in token.value.split(" "):
            self.whitespaces += 1
            updated_items.append(i.replace(" ", ""))
        return ''.join(updated_items)
