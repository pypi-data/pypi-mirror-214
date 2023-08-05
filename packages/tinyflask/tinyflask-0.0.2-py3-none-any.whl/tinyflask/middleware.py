from webob import Request
class Middleware:
    def __init__(self, app):
        self.app = app
    
    def add(self, other_middleware_cls):
        self.app = other_middleware_cls(self.app)
    
    def process_request(self, request):
        pass

    def process_response(self, request, response):
        pass

    def handle_request(self, request):
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)
        return response
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        # NOTE: here we don't do the line below because self.app is wrapped
        # by the middleware already, so we can call self.app.handle_request
        # response = self.handle_request(request)
        response = self.app.handle_request(request)
        return response(environ, start_response)