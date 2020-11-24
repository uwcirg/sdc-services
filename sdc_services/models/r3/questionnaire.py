
class Questionnaire(object):
    def __init__(self):
        self.item = None
        self._question_code_map = None
        self._answer_option_map = None

    @classmethod
    def from_json(cls, qnr_json):
        qnr = cls()
        qnr.item = qnr_json['item']

        return qnr

    def walk_questions(self, items=None):
        """Traverse nested items, yielding individual questions"""

        if items is None:
            items = self.item

        for item in items:
            if 'item' in item:
                yield from self.walk_answers(items['item'])
            else:
                yield item

    def question_codes(self, link_id):
        """Lookup codes associated with question given a linkId"""
        if not self._question_code_map:
            question_code_map = {}
            for item in self.walk_questions():
                question_code_map[item['linkId']] = item['code']
            self._question_code_map = question_code_map

        return self._question_code_map[link_id]

    def answered_option(self, answer_code):
        """Lookup option associated with given answer"""
        if not self._answer_option_map:
            answer_option_map = {}
            for item in self.walk_questions():
                for option in item['option']:
                    coding_option = option.get('valueCoding')
                    if not coding_option:
                        continue
                    answer_option_map[coding_option['code']] = coding_option
            self._answer_option_map = answer_option_map

        return self._answer_option_map[answer_code]
