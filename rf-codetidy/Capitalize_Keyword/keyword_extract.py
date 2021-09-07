import os

from robot.parsing import get_model
from robot.parsing import ModelVisitor


class AllKeywordsFromFile:
    def __init__(self, keyword_file_list, path_to_keyword_dir):
        self.keyword_files_list = keyword_file_list
        self.path_kd = path_to_keyword_dir
        self.all_keywords = []
        self.keyword = KeywordNameVisitor()

    def add_all_keywords_to_list(self):
        nr_files = 0
        nr_kw = 0
        print("-"*50)
        print("Getting Files from Keyword Directory")
        for file in self.keyword_files_list:
            ky_source = self.path_kd + f"\\{file}"
            model = get_model(ky_source)
            self.keyword.visit(model)
            keyword_tokens = self.keyword.return_name_list()
            nr_files += 1
            for keyword in keyword_tokens:
                self.all_keywords.append(keyword)
                nr_kw += 1
        print(f" * Found {nr_files} Files")
        print(f" * Found {nr_kw} Keywords")

    def get_all_keywords_list(self):
        return self.all_keywords


class GetFiles:
    @staticmethod
    def get_dir(dir_name):
        files = os.listdir(dir_name)
        return files


class KeywordNameVisitor(ModelVisitor):
    def __init__(self):
        self.keywordnames = []

    def visit_KeywordName(self, node):
        self.keywordnames.append(node.name)

    def return_name_list(self):
        return self.keywordnames


class KeywordCallVisitor(ModelVisitor):
    @staticmethod
    def visit_KeywordCall(node):
        return node.keyword


class AllKeywordVisitor(ModelVisitor):
    def __init__(self):
        self.all_keywords = []

    def visit_KeywordCall(self, node):
        self.all_keywords.append(node.keyword)

    def visit_KeywordName(self, node):
        self.all_keywords.append(node.name)

    def return_list(self):
        return self.all_keywords

