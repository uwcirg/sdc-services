"""
Observations modeled after SDC $extract operation

See http://build.fhir.org/ig/HL7/sdc/extraction.html#observation-based-extraction
"""


class Observation(object):
    def __init__(self, derived_from=None, value=None, issued=None, code=None):
        # FHIR reference to other resource
        self.derived_from = derived_from
        self.value = value
        self.issued = issued
        # list of codes
        self.code = code

    def as_fhir(self):
        fhir_json = {
            'resourceType': self.__class__.__name__,
            'issued': self.issued,
        }
        # filter out unset attributes
        fhir_json = {k: v for k, v in fhir_json.items() if v}

        if self.derived_from:
            fhir_json.update({
                'derivedFrom': [{
                    'reference': f'{self.derived_from['system']}/{self.derived_from['value']}',
                }]
            })

        if self.code:
            code = self.code.copy()
            text = code.pop('text', None)
            if text:
                code['display'] = text
            fhir_json.update({
                'code': {'coding': code},
            })

        if self.value:
            fhir_json.update(self.value)

        return fhir_json
