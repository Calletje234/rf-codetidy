from Capitalize_Keyword.init_Capitilizer import StartCapitilizer
from Remove_whitespaces.init_Whitespace import StartWhiteSpace
from Present_results.init_results import GetResults
from Add_doc_sections.init_DocSection import StartDocCheck
from Add_spacing.init_Spacing import StartSpacing

import shutil
import argparse


class ArgParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.add_arguments_parse()
        self.args = self.parse_arguments()
        self.run_program()

    def add_arguments_parse(self):
        self.parser.add_argument("file", help="This needs the path to .robot file that it needs to change",
                                 type=str)
        self.parser.add_argument("-c", "--copy",
                                 help="The path after this command is where the copy of the given file is "
                                      "stored. This needs to be a Directory",
                                 default="Default")
        self.parser.add_argument("-k", "--keyword",
                                 help="This needs the path to where all the keyword resource files are stored."
                                      " This needs to be a Directory",
                                 type=str,
                                 default="Default")

    def parse_arguments(self):
        args = self.parser.parse_args()
        return args

    def run_program(self):
        if self.args.copy or self.args.copy == str:
            if self.args.copy != str:
                self.create_backup(self.args.file)
            else:
                self.create_backup(self.args.file, self.args.copy)
            if self.args.keyword != "Default":
                caps = StartCapitilizer(self.args.file, self.args.keyword)
                white = StartWhiteSpace(self.args.file)
                doc = StartDocCheck(self.args.file)
                # TODO spacing = StartSpacing(self.args.file)
                GetResults(caps, doc, white)

            else:
                caps = StartCapitilizer(self.args.file)
                white = StartWhiteSpace(self.args.file)
                doc = StartDocCheck(self.args.file)
                # TODO spacing = StartSpacing(self.args.file)
                GetResults(caps, doc, white)
        else:
            if self.args.keyword != "Default":
                caps = StartCapitilizer(self.args.file, self.args.keyword)
                white = StartWhiteSpace(self.args.file)
                doc = StartDocCheck(self.args.file)
                # TODO spacing = StartSpacing(self.args.file)
                GetResults(caps, doc, white)
            else:
                caps = StartCapitilizer(self.args.file)
                white = StartWhiteSpace(self.args.file)
                doc = StartDocCheck(self.args.file)
                # TODO spacing = StartSpacing(self.args.file)
                GetResults(caps, doc, white)

    @staticmethod
    def create_backup(file, output_copy="DEFAULT"):
        try:
            words = file.split("\\")
            file_name = words[-1].split(".")
            file_name.remove(file_name[-1])
            words.remove(words[-1])
            file_name[0] += "-Copy.robot"
            if output_copy == "DEFAULT":
                words.append(file_name[0])
                name = "\\".join(words)
                shutil.copyfile(file, name)
            else:
                if output_copy.endswith("\\"):
                    output_copy += file_name[0]
                    shutil.copyfile(file, output_copy)
                else:
                    output_copy += "\\" + file_name
                    shutil.copyfile(file, output_copy)
        except Exception as e:
            print(f"While creating a Back-up of you file the following error occurred: '{e}'")


if __name__ == '__main__':
    ArgParse()
