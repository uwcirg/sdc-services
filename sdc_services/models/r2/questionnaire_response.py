from sdc_services.models.r2.observation import Observation
from sdc_services.models.r3.questionnaire import Questionnaire


class QuestionnaireResponse(object):
    def __init__(self):
        self.group = None
        self.identifier = None
        self.authored = None
        self.questionnaire_ref = None
        self.questionnaire_res = None

    @classmethod
    def from_json(cls, qnr_json):
        qnr = cls()

        qnr.group = qnr_json['group']
        qnr.identifier = qnr_json['identifier']
        qnr.authored = qnr_json['authored']
        qnr.questionnaire_ref = qnr_json['questionnaire']

        if 'contained' in qnr_json:
            contained_questionnaires = []
            for resource in qnr_json['contained']:
                if resource['resourceType'] == 'Questionnaire':
                    contained_questionnaires.append(resource)
            # HACK use FHIR r3 for contained Questionnaire (in r2 QuestionnaireResponse)
            qnr.questionnaire_res = Questionnaire.from_json(contained_questionnaires[0])

        return qnr

    def as_fhir(self):
        fhir_json = {
            'resourceType': self.__class__.__name__,
            'group': self.group,
            'identifier': self.identifier,
        }
        # filter out unset attributes
        filtered_fhir_json = {k: v for k, v in fhir_json.items() if v}
        return filtered_fhir_json

    def walk_answers(self, items=None):
        """Traverse nested groups and answers, yielding individual answers"""

        if items is None:
            items = self.group

        for item in items:
            if item == 'group':
                yield from self.walk_answers(items['group'])
            elif item == 'question':
                for question in items['question']:
                    for answer in question['answer']:
                        yield answer

    def extract(self):
        """Extract coded Observations from individual answers"""

        observations = []
        for answer in self.walk_answers():
            if 'valueCoding' not in answer:
                continue

            codes = []
            if self.questionnaire_res:
                # remove option index to get linkId
                answer_code = answer['valueCoding']['code']
                link_id = ".".join(answer_code.split('.')[0:2])
                question_codes = self.questionnaire_res.question_codes(link_id)
                codes.extend(question_codes)

                # add any attributes (eg extensions) in Questionnaire option
                questionnaire_option = self.questionnaire_res.answered_option(answer_code)
                answer['valueCoding'].update(questionnaire_option)

            obs = Observation(
                derived_from=self.identifier,
                value={'valueCoding': answer['valueCoding']},
                issued=self.authored,
                codes=codes,
            )
            observations.append(obs.as_fhir())

        return observations
