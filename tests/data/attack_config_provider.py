def default():
    return [
        {"action": "delay", "value": "1", "probability": "80", "target": {"route": "/hello"}},
        {"action": "delay", "value": "1", "target": {"route": "/api"}}
    ]


def invalid():
    return [
        {"xxx": "aaa"}
    ]
