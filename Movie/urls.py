from django.urls import path , re_path
from .views import HomePage, MovieDetailPage, JournalList, MovieListView, JournalListView, JournalDetailView, rate_movie, MovieWatchedListView

apps_name = 'Movie' 

urlpatterns = [ 
       re_path(r'home/',HomePage.as_view(),name='home'), 
       path('moviedetail/<uuid:pk>/',MovieDetailPage.as_view(),name='movie_detail'),
       path('journals/',JournalList.as_view(), name='journal_list'),
       path('movies/', MovieListView.as_view(), name='movie_list'), 
       path('movies/watched', MovieWatchedListView.as_view(), name='movie_watched'), 
       path('journals/', JournalListView.as_view(), name='journal_list'), 
       path('journals/<int:pk>/', JournalDetailView.as_view(), name='journal_detail'), 
       path('home/',HomePage.as_view() , name='index'), 
       path("movie/<uuid:movie_id>/rate/", rate_movie, name="rate_movie"), 
    ]
