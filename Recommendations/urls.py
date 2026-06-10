from django.urls import path , re_path
from .views import CombinedRecommendationView , StartRecommendView

apps_name = 'Recommendations' 

urlpatterns = [
       path('recommendations/', CombinedRecommendationView.as_view(), name='start_recommend'), 
       path("start-recommend/", StartRecommendView.as_view(), name="recommend"),
          ]
