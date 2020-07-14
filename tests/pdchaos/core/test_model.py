import pytest
from marshmallow import ValidationError
from pdchaos.middleware.core import model


def test_valid_paths_schema():
    _input = {
        "paths": [
            {
                "path": "/hello",
                "attacks": [
                    {
                        "type": "delay",
                        "value": "30",
                        "probability": "80"
                    },
                    {
                        "type": "exception",
                        "value": "BaseException"
                    }
                ],
                "methods": [
                    "GET",
                    "POST"
                ]
            },
            {
                "path": "/api",
                "attacks": [
                    {
                        "type": "delay",
                        "value": "30"
                    }
                ]
            }
        ]
    }

    result = model.parse_paths(_input)
    paths = result.get('paths')
    hello_path = result.get('paths')[0]
    api_path = result.get('paths')[1]

    assert len(paths) == 2
    assert len(hello_path['methods']) == 2
    assert len(hello_path['attacks']) == 2
    assert len(api_path['attacks']) == 1


def test_invalid_paths_schema():
    _input = {"xxx": []}

    result = model.parse_paths(_input)
    assert not result


def test_valid_attacks_schema():
    _input = '[{"type": "delay", "value": "3", "probability": "80"}]'
    result = model.parse_attack(_input)

    assert result[0]['type'] == 'delay'
    assert result[0]['value'] == '3'
    assert result[0]['probability'] == '80'


def test_invalid_attacks_schema():
    _input = '[{"xxx": "80"}]'
    result = model.parse_attack(_input)

    assert not result
