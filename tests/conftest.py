import os
import json
from pytest import fixture


@fixture
def app():
    from sdc_services.app import create_app
    return create_app(testing=True)


@fixture
def client(app):
    with app.test_client() as c:
        yield c


def json_from_file(request, filename):
    data_dir, _ = os.path.splitext(request.module.__file__)
    data_dir = f"{data_dir}_data"
    with open(os.path.join(data_dir, filename), 'r') as json_file:
        data = json.load(json_file)
    return data


@fixture
def r2_questionnaire_response(request):
    return json_from_file(request, "epic26.QuestionnaireResponse.r2.json")


@fixture
def empro_r2_questionnaire_response(request):
    return json_from_file(request, "empro.min.QuestionnaireResponse.r2.json")


@fixture
def ironman_ss_r2_qnr_contained_questionnaire(request):
    return json_from_file(request, "ironman_ss.QuestionnaireResponse.r2.json")
