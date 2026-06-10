from django.http.response import HttpResponse
from django.shortcuts import render 
from django.views.generic import ListView , TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import UserInformationFormovieSuggestions
from .function import recommend_by_user_similarity, recommend_movies_by_content,detect_favorite_actor
from Movie.models import Movie 
import random

class CombinedRecommendationView(LoginRequiredMixin,ListView):
    model = Movie
    template_name = "recommendations.html"
    context_object_name = "movies"
    login_url = "/Users/login/"          # مسیر صفحه‌ی لاگین
    redirect_field_name = "next"   # بعد از لاگین کاربر به این صفحه برمی‌گردد

    def get_queryset(self):
        user = self.request.user
        try:
            user_info = user.userinformation
        except UserInformationFormovieSuggestions.DoesNotExist:
            return Movie.objects.none()
        # 1. Collaborative Filtering
        collab_movies = recommend_by_user_similarity(user_info, top_n_users=3, top_n_movies=5) #15
        # 2. Content-Based Filtering
        content_movies = recommend_movies_by_content(user_info, top_n=10) #20
        # 3. Detect Favorite Actor (و استفاده از آن برای فیلتر)
        fav_actor = detect_favorite_actor(user_info)
        actor_movies = Movie.objects.filter(MovieActor=fav_actor).order_by("-IMDBscore")[5:0] if fav_actor else Movie.objects.none() #5
        # 4. ترکیب نتایج و حذف تکراری‌ها
        combined = set(collab_movies) | set(content_movies) | set(actor_movies)

        combined_list = list(combined)
        # 6. انتخاب تصادفی 15 فیلم
        final_selection = random.sample(combined_list, min(10, len(combined_list)))
        return final_selection 
class StartRecommendView(TemplateView):
    template_name = "start_recommend.html"
