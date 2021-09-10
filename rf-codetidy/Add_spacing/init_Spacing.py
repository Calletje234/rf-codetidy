from Add_spacing.get_section_order import GetOrder

from Add_spacing.start_Spacing import ChangeSpacingSettings
from Add_spacing.start_Spacing import ChangeSpacingKeyword
from Add_spacing.start_Spacing import ChangeSpacingVariable
from Add_spacing.start_Spacing import ChangeSpacingTestCase

from robot.parsing import get_model


class StartSpacing:
    def __init__(self, source):
        self.sorted_sections_start: dict = {}
        self.sorted_sections_end: dict = {}
        self.start_list: list = []
        self.end_list: list = []
        self.source = source

        self.model = get_model(source)
        self.sorter = GetOrder()
        self.setting = ChangeSpacingSettings()
        self.keyword = ChangeSpacingKeyword()
        self.variable = ChangeSpacingVariable()
        self.testcase = ChangeSpacingTestCase()

        print("Adding WhiteLines between Sections")
        self.get_ordered_list_of_sections()
        self.check_for_spacing()
        print("**DONE**")

    def get_ordered_list_of_sections(self):
        self.sorter.visit(self.model)
        self.sorted_sections_start = self.sorter.get_order_of_section()
        self.sorted_sections_end = self.sorter.get_end_of_sections()
        self.convert_start_dict_list()
        self.convert_end_dict_list()

    def check_for_spacing(self):
        start_dic_length = len(self.start_list)
        end_dic_length = len(self.end_list)
        if start_dic_length != end_dic_length:
            raise SystemExit("There is unequal amount of Sections. Therefore the program cant proceed.")
        else:
            print(self.end_list)
            print(self.start_list)
            for i in range(start_dic_length - 1):
                line = self.start_list[i + 1][1] - self.end_list[i][1]
                if line == 1:
                    self.change_spacing(self.end_list[i])

    def change_spacing(self, section_item):
        if section_item == "setting_section":
            self.setting.visit_SettingSection(self.model)
            self.model.save(self.source)
        elif section_item == "testcase_section":
            self.testcase.visit(self.model)
        elif section_item == "keyword_section":
            self.keyword.visit(self.model)
        elif section_item == "variable_section":
            self.variable.visit(self.model)

    def convert_start_dict_list(self):
        for i in self.sorted_sections_start.keys():
            item_list = [i, self.sorted_sections_start.get(i)]
            self.start_list.append(item_list)

    def convert_end_dict_list(self):
        for i in self.sorted_sections_end.keys():
            item_list = [i, self.sorted_sections_end.get(i)]
            self.end_list.append(item_list)

    def get_added_lines(self):
        added_lines = self.setting.get_changed_lines() + self.testcase.get_changed_lines()
        added_lines += self.keyword.get_changed_lines() + self.variable.get_changed_lines()
        return added_lines
