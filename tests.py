from api.main import web_app


def test_user_get_by_id_success():
    request, response = web_app.test_client.get('/users/3')
    assert response.status == 200


def test_user_get_by_incorrect_url_fails():
    request, response = web_app.test_client.get('/unknown')
    assert response.status == 404
