def default():
    return [
        {"name": "delay", "value": "1", "probability": "100", "route": "/hello"},
        {"name": "delay", "value": "1", "route": "/api"}
    ]


def invalid():
    return [
        {"xxx": "aaa"}
    ]
