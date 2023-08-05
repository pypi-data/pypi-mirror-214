from webob import Response as WebObResponse
import json
class Response:
    def __init__(self) -> None:
        self.json = None
        self.html = None
        self.body = b''
        self.text = None
        self.content_type = None
        self.status_code = 200

    def set_content_and_body_type(self):
        if self.json is not None:
            self.body = json.dumps(self.json).encode("utf-8")
            self.content_type = "application/json"
        if self.html is not None:
            self.body = self.html.encode()
            self.content_type = "text/html"
        if self.text is not None:
            self.body = self.text
            self.content_type = "text/plain"

    def __call__(self, environ, start_response):
        self.set_content_and_body_type()
        response = WebObResponse(
            body=self.body,
            status=self.status_code,
            content_type=self.content_type
        )
        return response(environ, start_response)