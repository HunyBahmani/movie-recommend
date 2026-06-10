from Movie.models import Movie , Actor  
from Users.models import FavouriteMovies 
from .models import MovieWatched , UserInformationFormovieSuggestions , MovieFeatur 
import numpy as np 

def update_user_interests(user_info:UserInformationFormovieSuggestions):
    watched_movies = MovieWatched.objects.filter(userInform=user_info)
    sum_action = sum_comedy = sum_drama = sum_violent = sum_family = 0
    total_weight = 0
    for wm in watched_movies:
        try:
            features = wm.movie.moviefeatur
        except MovieFeatur.DoesNotExist:
            continue  # اگر فیلم ویژگی نداشت، رد کن
        degree = wm.theDegreeOfInterestOrDisinterest - 5  # تبدیل به بازه -5 تا +5
        sum_action += features.amountOfAction * degree
        sum_comedy += features.amountOfComedy * degree
        sum_drama += features.amountOfDrama * degree
        sum_violent += features.amountOfViolent * degree
        sum_family += features.amountOfFamilyFriendly * degree
        total_weight += abs(degree)
    if total_weight > 0:
        user_info.interestInAction = max(0, min(10, sum_action / total_weight))
        user_info.interestInComedy = max(0, min(10, sum_comedy / total_weight))
        user_info.interestInDrama = max(0, min(10, sum_drama / total_weight))
        user_info.interestInViolent = max(0, min(10, sum_violent / total_weight))
        user_info.interestInFamilyFriendly = max(0, min(10, sum_family / total_weight))
        user_info.save()
def cosine_similarity(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    dot = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0
    return dot / (norm1 * norm2) 
def recommend_by_user_similarity(target_user_info:UserInformationFormovieSuggestions, top_n_users=3, top_n_movies=10): 
    #Collaborative-Filtering
    # پروفایل کاربر هدف
    target_profile = [
        target_user_info.interestInAction,
        target_user_info.interestInComedy,
        target_user_info.interestInDrama,
        target_user_info.interestInViolent,
        target_user_info.interestInFamilyFriendly,
    ]
    # پروفایل سایر کاربران
    other_users = UserInformationFormovieSuggestions.objects.exclude(user=target_user_info.user)
    similarities = []
    for other in other_users:
        other_profile = [
            other.interestInAction,
            other.interestInComedy,
            other.interestInDrama,
            other.interestInViolent,
            other.interestInFamilyFriendly,
        ]
        sim = cosine_similarity(target_profile, other_profile)
        similarities.append((other, sim))
    # مرتب‌سازی براساس شباهت
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_users = [u for u, s in similarities[:top_n_users]]
    # جمع‌آوری فیلم‌های مورد علاقه کاربران مشابه
    recommended_movies = set()
    for u in top_users:
        liked_movies = MovieWatched.objects.filter(userInform=u, likeAMovie=True, theDegreeOfInterestOrDisinterest__gte=5).order_by("-theDegreeOfInterestOrDisinterest")
        for lm in liked_movies:
            recommended_movies.add(lm.movie)
    # حذف فیلم‌هایی که کاربر هدف دیده
    watched_movies = set(mw.movie for mw in MovieWatched.objects.filter(userInform=target_user_info))
    final_movies = recommended_movies - watched_movies
    return list(final_movies)[:top_n_movies]
def recommend_movies_by_content(user_info:UserInformationFormovieSuggestions, top_n=10): 
    # پروفایل کاربر
    #Content-Based-Filtering
    user_vector = [
        user_info.interestInAction,
        user_info.interestInComedy,
        user_info.interestInDrama,
        user_info.interestInViolent,
        user_info.interestInFamilyFriendly,
    ]
    similarities = []
    for movie in Movie.objects.all():
        try:
            features = movie.moviefeatur
        except MovieFeatur.DoesNotExist:
            continue  # اگر فیلم ویژگی نداشت، رد کن
        movie_vector = [
            features.amountOfAction,
            features.amountOfComedy,
            features.amountOfDrama,
            features.amountOfViolent,
            features.amountOfFamilyFriendly,
        ]
        sim = cosine_similarity(user_vector, movie_vector)
        similarities.append((movie, sim))
    # مرتب‌سازی براساس شباهت
    similarities.sort(key=lambda x: x[1], reverse=True)
    # انتخاب N فیلم برتر
    recommended_movies = set()
    for m, s in similarities[:top_n]:
        recommended_movies.add(m)
    watched_movies = set(mw.movie for mw in MovieWatched.objects.filter(userInform=user_info))
    final_movies = recommended_movies - watched_movies
    # مرتب‌سازی براساس امتیاز IMDB
    final_movies = sorted(final_movies, key=lambda m: m.IMDBscore, reverse=True)
    return final_movies
def detect_favorite_actor(user_info:UserInformationFormovieSuggestions): 
    #Actor-Preference-Mining
    watched_movies = MovieWatched.objects.filter(userInform=user_info, likeAMovie=True)
    actor_scores = {}
    for wm in watched_movies:
        try:
            actors = wm.movie.MovieActor.all()
        except Exception:
            continue
        degree = wm.theDegreeOfInterestOrDisinterest
        for actor in actors:
            if actor not in actor_scores:
                actor_scores[actor] = 0
            actor_scores[actor] += degree
    if not actor_scores:
        return None
    # مرتب‌سازی براساس امتیاز
    favorite_actor = max(actor_scores.items(), key=lambda x: x[1])[0]
    # ذخیره در پروفایل کاربر
    user_info.favActor = favorite_actor
    user_info.save()
    return favorite_actor
def calculate_suitability(user_info, movie):
    # پروفایل کاربر
    user_vector = [
        user_info.interestInAction,
        user_info.interestInComedy,
        user_info.interestInDrama,
        user_info.interestInViolent,
        user_info.interestInFamilyFriendly,
    ]
    try:
        features = movie.moviefeatur
    except Exception:
        return 0  # اگر فیلم ویژگی نداشت

    movie_vector = [
        features.amountOfAction,
        features.amountOfComedy,
        features.amountOfDrama,
        features.amountOfViolent,
        features.amountOfFamilyFriendly,
    ]
    # شباهت بین کاربر و فیلم
    similarity = cosine_similarity(user_vector, movie_vector)
    # بررسی بازیگر محبوب
    actor_bonus = 0
    if user_info.favActor and user_info.favActor in movie.MovieActor.all():
        actor_bonus = 0.2  # 20 درصد امتیاز اضافه
    # امتیاز نهایی
    suitability_score = similarity + actor_bonus
    # تبدیل به درصد
    suitability_percent = min(100, suitability_score * 100)
    return suitability_percent