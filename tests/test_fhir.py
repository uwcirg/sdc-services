from sdc_services.models.r2.questionnaire_response import QuestionnaireResponse


def test_r2_bundle(r2_questionnaire_response):
    qnr = QuestionnaireResponse.from_json(r2_questionnaire_response)
    assert len(qnr.group['question']) == 26

def test_extract_api(client, r2_questionnaire_response):
    result = client.post('/v/r2/fhir/$extract', json=r2_questionnaire_response)
    assert result.status_code == 200

    obs_bundle = result.json
    assert len(obs_bundle['entry']) == 26
