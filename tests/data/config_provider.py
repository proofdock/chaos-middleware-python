def default() -> str:
    return """
    [ 
     { "action":"delay","value":"1","probability":"80","target":{"route":"/hello"} },
     { "action":"delay","value":"1","target":{"route":"/api"} }
    ]
    """


def invalid() -> str:
    return """[ { "xxx":"aaa" } ]"""
