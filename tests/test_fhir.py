from sdc_services.models.r2.questionnaire_response import QuestionnaireResponse


def test_r2_bundle(r2_questionnaire_response):
    qnr = QuestionnaireResponse.from_json(r2_questionnaire_response)
    assert len(qnr.group['question']) == 26


def test_extract_observation(empro_r2_questionnaire_response):
    qnr = QuestionnaireResponse.from_json(empro_r2_questionnaire_response)
    observations = qnr.extract()
    assert len(observations) == 2

    obs = observations[0]

    assert obs['code']['coding'][0]['code'] == 'ironman_ss'
    assert obs['code']['coding'][0]['system'] == 'http://us.truenth.org/questionnaire'

    assert obs['issued'] == empro_r2_questionnaire_response['authored']

    assert obs['related'][0] == {
        "target": f"QuestionnaireResponse/{empro_r2_questionnaire_response['identifier']['value']}",
        "type": "derived-from",
    }

    assert obs['valueCoding'] == empro_r2_questionnaire_response['group']['question'][0]['answer'][1]['valueCoding']


def test_extract_api(client, r2_questionnaire_response):
    result = client.post('/v/r2/fhir/$extract', json=r2_questionnaire_response)
    assert result.status_code == 200

    obs_bundle = result.json
    assert len(obs_bundle['entry']) == 26
