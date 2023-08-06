import pytest
from unittest.mock import patch
from art_api_client import client as art

@patch('articolare.ArticolareClient._request')
def test_create(mock_request):
    mock_request.return_value = {"success": True}

    client = art.ArticolareClient(api_key="testkey")
    response = client.create(
        model="testmodel",
        lang="English",
        style="Conversation Formal",
        dialect="Latam",
        prompt="testprompt",
        max_tokens=10
    )

    assert response == {"success": True}
    mock_request.assert_called_once_with("POST", "/create", json={
        "model": "testmodel",
        "lang": "English",
        "style": "Conversation Formal",
        "dialect": "Latam",
        "prompt": "testprompt",
        "max_tokens": 10
    })
