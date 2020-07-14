def default() -> str:
    return """
paths:
- path: /hello
  attacks:
    - type: delay
      value: '1'
      probability: '80'
    - type: exception
      value: BaseException
  methods:
    - GET
    - POST
- path: /api
  attacks:
    - type: delay
      value: '1'
    - type: exception
      value: BaseException
"""
