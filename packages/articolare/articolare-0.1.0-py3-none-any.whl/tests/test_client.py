import pytest
from unittest.mock import patch
from articolare import translate as art

@patch('articolare.ArticolareClient._request')
def test_create(mock_request):
    mock_request.return_value = {"success": True}

    client = art.ArticolareClient(api_key="testkey")
    response = client.create(
        model="testmodel",
        lang="english",
        style="conversation formal",
        dialect="latam",
        prompt="testprompt",
        max_tokens=10
    )

    assert response == {"success": True}
    mock_request.assert_called_once_with("POST", "/create", json={
        "model": "testmodel",
        "lang": "english",
        "style": "Conversation Formal",
        "dialect": "latam",
        "prompt": "testprompt",
        "max_tokens": 10
    })
