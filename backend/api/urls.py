from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('learning-paths/', include('apps.learning_paths.urls')),
    path('recommendations/', include('apps.recommendations.urls')),
    path('progress/', include('apps.progresstracker.urls'))
]
