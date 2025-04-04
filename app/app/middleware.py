from django.http import HttpResponseForbidden
from django.utils import timezone

class OfficeHoursMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = timezone.now().hour

        if current_hour < 8 or current_hour >= 16:
            return HttpResponseForbidden("Chỉ được truy cập từ 8h đến 17h!")

        response = self.get_response(request)
        return response