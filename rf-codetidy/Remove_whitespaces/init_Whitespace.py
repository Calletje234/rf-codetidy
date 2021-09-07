from robot.parsing import get_model
from Remove_whitespaces.Remove_Whitespace import RemoveWhiteSpace


class StartWhiteSpace:
    def __init__(self, source):
        self.source = source
        self.model = get_model(source)
        self.visitor = RemoveWhiteSpace()
        self.run_remover()

    def run_remover(self):
        print("Removing all trailing Whitespaces")
        self.visitor.visit(self.model)
        print("**DONE**")
        self.model.save(output=self.source)

    def get_lines_edited(self):
        return self.visitor.get_amount_lines_edited()

    def get_ws_removed(self):
        return self.visitor.get_amount_ws_removed()
