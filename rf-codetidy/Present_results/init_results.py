class GetResults:
    def __init__(self, cap_obj, doc_obj, ws_obj):
        self.changed_keyword_calls = cap_obj.get_changed_KC()
        self.changed_keyword_names = cap_obj.get_changed_KN()
        self.changed_ws_lines = ws_obj.get_lines_edited()
        self.removed_ws = ws_obj.get_ws_removed()
        self.added_docs = doc_obj.get_amount_doc_added()
        # TODO self.added_white_lines = sp_obj.get_added_lines()
        # Also don't forgot to add spacing object to init arguments
        self.print_output()

    def print_output(self):
        print("-" * 50)
        print(f"Amount of Documentation Sections added: {self.added_docs}")
        print(f"Amount of Changed Keyword Calls: {self.changed_keyword_calls}")
        print(f"Amount of Changed Keyword Names: {self.changed_keyword_names}")
        print(f"Amount of Lines where WhiteSpaces are removed: {self.changed_ws_lines}")
        print(f"Amount of WhiteSpaces Removed: {self.removed_ws}")
        print(f"Amount of Lines added between Sections: {self.added_white_lines}")
        print("-" * 50)
