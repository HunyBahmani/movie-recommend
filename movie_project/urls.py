"""
Definition of urls for movie_project.
"""

from django.urls import path , include , re_path
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.conf import settings 
from django.conf.urls.static import static 
from Movie.views import HomePage

urlpatterns = [
    path('', HomePage.as_view(),name='home'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls), 
    re_path(r'^Movie/',include('Movie.urls')),
    re_path(r'^Users/',include('Users.urls')),
    re_path(r'^Recommendations/',include('Recommendations.urls')) 
] 
if settings.DEBUG:
            urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
