from robot.parsing import ModelVisitor


class GetOrder(ModelVisitor):
    def __init__(self):
        self.setting_section_start: int = 0
        self.keyword_section_start: int = 0
        self.variable_section_start: int = 0
        self.testcase_section_start: int = 0

        self.setting_section_end: int = 0
        self.keyword_section_end: int = 0
        self.variable_section_end: int = 0
        self.testcase_section_end: int = 0

        self.sections_start: dict = {}
        self.sorted_sections_start: dict = {}

        self.sections_end: dict = {}
        self.sorted_sections_end: dict = {}

    def visit_SettingSection(self, node):
        self.setting_section_start = node.lineno
        self.setting_section_end = node.end_lineno
        self.sections_start["setting_section"] = self.setting_section_start
        self.sections_end["setting_section"] = self.setting_section_end

    def visit_KeywordSection(self, node):
        self.keyword_section_start = node.lineno
        self.keyword_section_end = node.end_lineno
        self.sections_start["keyword_section"] = self.keyword_section_start
        self.sections_end["keyword_section"] = self.keyword_section_end

    def visit_VariableSection(self, node):
        self.variable_section_start = node.lineno
        self.variable_section_end = node.end_lineno
        self.sections_start["variable_section"] = self.variable_section_start
        self.sections_end["variable_section"] = self.variable_section_end

    def visit_TestCaseSection(self, node):
        self.testcase_section_start = node.lineno
        self.testcase_section_end = node.end_lineno
        self.sections_start["testcase_section"] = self.testcase_section_start
        self.sections_end["testcase_section"] = self.testcase_section_end

    def get_order_of_section(self):
        self.sorted_sections_start = dict(sorted(self.sections_start.items(), key=lambda item: item[1]))
        return self.sorted_sections_start

    def get_end_of_sections(self):
        self.sorted_sections_end = dict(sorted(self.sections_end.items(), key=lambda item: item[1]))
        return self.sorted_sections_end
