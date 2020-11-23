from sdc_services.models.r2.questionnaire_response import QuestionnaireResponse


def test_r2_bundle(r2_questionnaire_response):
    qnr = QuestionnaireResponse.from_json(r2_questionnaire_response)
    assert len(qnr.group['question']) == 26


def test_extract_observation(empro_r2_questionnaire_response):
    qnr = QuestionnaireResponse.from_json(empro_r2_questionnaire_response)
    observations = qnr.extract()
    assert len(observations) == 2

    obs = observations[0]

    assert obs['issued'] == empro_r2_questionnaire_response['authored']

    assert obs['derivedFrom'] == [{
        'reference': 'https://ae-eproms-test.cirg.washington.edu/QuestionnaireResponse/2085.0'
    }]


    assert obs['valueCoding'] == empro_r2_questionnaire_response['group']['question'][0]['answer'][1]['valueCoding']


def test_extract_observation_contained_questionnaire(ironman_ss_r2_qnr_contained_questionnaire):
    """Test Questionnaire contained in QuestionnaireResponse"""
    qnr = QuestionnaireResponse.from_json(ironman_ss_r2_qnr_contained_questionnaire)
    observations = qnr.extract()

    assert observations[2]['code']['coding'][0]['code'] == 'general_pain'

    assert qnr.questionnaire_res.item[3]['code'][0] == observations[3]['code']['coding'][0]
    assert observations[3]['code']['coding'][0]['code'] == 'joint_pain'


def test_extract_api(client, r2_questionnaire_response):
    result = client.post('/v/r2/fhir/$extract', json=r2_questionnaire_response)
    assert result.status_code == 200

    obs_bundle = result.json
    assert len(obs_bundle['entry']) == 26
