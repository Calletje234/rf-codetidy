from robot.parsing import get_model

from Capitalize_Keyword.keyword_extract import GetFiles
from Capitalize_Keyword.keyword_extract import AllKeywordsFromFile
from Capitalize_Keyword.keyword_extract import KeywordNameVisitor
from Capitalize_Keyword.keyword_extract import KeywordCallVisitor

from Capitalize_Keyword.Change_keywords import KeywordTestCaseUpper


class StartCapitilizer:
    def __init__(self, robot_file, keyword_dir="DEFAULT"):
        self.files_list = []
        self.all_keywords = []
        self.model = get_model(robot_file)
        self.robot_file = robot_file
        self.keyword_dir = keyword_dir
        self.files = GetFiles()
        self.name_visitor = KeywordNameVisitor()
        self.call_visitor = KeywordCallVisitor()
        self.get_keywords_from_resourceFile()
        self.get_keywords_from_test_file()
        self.change_keywords()

    def get_keywords_from_resourceFile(self):
        if self.keyword_dir != "DEFAULT":
            self.files_list = self.files.get_dir(self.keyword_dir)
            extractor = AllKeywordsFromFile(self.files_list, self.keyword_dir)
            extractor.add_all_keywords_to_list()
            for keyword in extractor.get_all_keywords_list():
                self.all_keywords.append(keyword)

    def get_keywords_from_test_file(self):
        self.name_visitor.visit(self.model)
        keyword_names = self.name_visitor.return_name_list()
        for keyword_name in keyword_names:
            self.all_keywords.append(keyword_name)

    def change_keywords(self):
        self.changer = KeywordTestCaseUpper(self.all_keywords)
        print("Updating All Keywords With Uppercase")
        self.changer.visit(self.model)
        print("**DONE**")
        self.model.save(output=self.robot_file)

    def get_changed_KC(self):
        return self.changer.return_changed_call()

    def get_changed_KN(self):
        return self.changer.return_changed_name()