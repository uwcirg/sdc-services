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

            questionnaire_code = {
                'system': 'http://us.truenth.org/questionnaire',
                'code': self.questionnaire_ref['reference'].split('/')[-1],
                'display': self.questionnaire_ref['display'],
            }

            obs = Observation(
                derived_from=f"QuestionnaireResponse/{self.identifier['value']}",
                value={'valueCoding': answer['valueCoding']},
                issued=self.authored,
                # TODO add codes from Questionnaire questions (Questionnaire.item.code)
                code=questionnaire_code,
            )
            observations.append(obs.as_fhir())

        return observations
