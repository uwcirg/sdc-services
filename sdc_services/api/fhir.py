
from flask import Blueprint, request

from sdc_services.models.r2.questionnaire_response import QuestionnaireResponse
from sdc_services.models.r2.bundle import as_bundle

R2_PREFIX = '/v/r2/fhir'
blueprint = Blueprint('fhir', __name__)


# http://build.fhir.org/ig/HL7/sdc/StructureDefinition-sdc-questionnaire-extr-obsn.html#tabs-diff
@blueprint.route(f'/{R2_PREFIX}/$extract', methods=('GET', 'POST'))
def r2_extract():
    """
    Modeled after SDC $extract operation

    http://build.fhir.org/ig/HL7/sdc/OperationDefinition-QuestionnaireResponse-extract.html
    """
    qnr = QuestionnaireResponse.from_json(request.json)
    observations = qnr.extract()

    return as_bundle(observations)
