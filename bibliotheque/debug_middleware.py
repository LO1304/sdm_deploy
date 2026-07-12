import traceback
from django.http import HttpResponse

class GlobalDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            error_msg = traceback.format_exc()
            return HttpResponse(f"<pre>Global Catch-All: {str(e)}\n\n{error_msg}</pre>", status=500)

    def process_exception(self, request, exception):
        error_msg = traceback.format_exc()
        return HttpResponse(f"<pre>Global Error: {str(exception)}\n\n{error_msg}</pre>", status=500)
