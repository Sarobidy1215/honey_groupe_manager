from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def test(request):
    return HttpResponse("OK WORKING")

urlpatterns = [
    path('', test),
    path('admin/', admin.site.urls),
]