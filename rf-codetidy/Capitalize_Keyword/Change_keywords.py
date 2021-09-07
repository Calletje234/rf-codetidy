from robot.parsing import Token
from robot.parsing import ModelVisitor

from fuzzywuzzy import fuzz


class KeywordTestCaseUpper(ModelVisitor):
    def __init__(self, all_keywords_list):
        self.all_keywords_list = all_keywords_list
        self.call_count = 0
        self.name_count = 0

    def visit_KeywordCall(self, node):
        if self.update_case(node.keyword) != node.keyword:
            self.call_count += 1
            token = node.get_token(Token.KEYWORD)
            token.value = self.update_case(node.keyword)

    def visit_KeywordName(self, node):
        if self.update_case(node.name) != node.name:
            self.name_count += 1
            token = node.get_token(Token.KEYWORD_NAME)
            token.value = self.update_case(node.name)

    def return_changed_call(self):
        return self.call_count

    def return_changed_name(self):
        return self.name_count

    def get_skip_list(self, name):
        skip_pos = []
        matcher = KeywordMatcher(self.all_keywords_list)
        best_match = matcher.get_all_ratios(name)
        best_match_word_list = best_match.split()
        match_list_length = len(best_match_word_list)
        for i in range(match_list_length):
            for first in best_match_word_list[i].split():
                if first[0] == "$":
                    skip_pos.append(i)
                else:
                    break
        return skip_pos

    def update_case(self, name):
        skip_pos = self.get_skip_list(name)
        words_change_list = name.split()
        word_list_length = len(words_change_list)
        update_list = []
        for i in range(word_list_length):
            if i not in skip_pos:
                if words_change_list[i].isupper():
                    update_list.append(words_change_list[i])
                else:
                    word = words_change_list[i].capitalize()
                    update_list.append(word)
            else:
                update_list.append(words_change_list[i])
        name = ' '.join(update_list)
        return name


class KeywordMatcher:
    def __init__(self, all_keywords_list):
        self.all_keywords_list = all_keywords_list

    def get_all_ratios(self, name):
        all_ratio = {}
        for i in range(len(self.all_keywords_list)):
            ratio = fuzz.ratio(name, self.all_keywords_list[i])
            all_ratio[i] = ratio
        highest_ratio = max(all_ratio, key=all_ratio.get)
        return self.all_keywords_list[highest_ratio]