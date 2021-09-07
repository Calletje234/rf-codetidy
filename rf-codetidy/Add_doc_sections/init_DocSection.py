from robot.parsing import get_model
from Add_doc_sections.Add_docsection import AddDocSection


class StartDocCheck:
    def __init__(self, source):
        self.added_docs = 0
        self.model = get_model(source)
        print("Adding Documentation Section to file")
        self.changer = AddDocSection()
        self.changer.visit(self.model)
        self.model.save()
        print("**Done**")

    def get_amount_doc_added(self):
        return self.changer.get_added_docs()


