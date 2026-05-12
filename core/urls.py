from django.http import HttpResponse
from django.urls import path

def test(request):
    return HttpResponse("APP OK")

urlpatterns = [
    path('', test),
]