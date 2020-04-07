
from django.contrib import admin
from django.urls import path
from weatherForcast.views import forcast
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', forcast),

]
