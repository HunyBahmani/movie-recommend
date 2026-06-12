from django.shortcuts import render 
from django.views.generic import TemplateView , ListView , DetailView
from .models import Movie , Actor , Journal
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404 , redirect
from random import sample
from django.db.models import Q
from django.contrib import messages
from Recommendations.models import MovieWatched

class HomePage(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # داده‌های اصلی برای صفحه
        context["movies"] = sample(list(Movie.objects.all()), 10)
        context["journals"] = Journal.objects.all()[:10]
        context["movieactor"] = Movie.objects.all()

        # 🔎 داده‌های اتو کامپلیت (فقط عنوان و سال فیلم‌ها)
        context["movies_for_search"] = Movie.objects.values("Movie_id", "Title")[:100]

        return context

    def render_to_response(self, context, **response_kwargs):
        return render(self.request, self.template_name, context, **response_kwargs)

class MovieDetailPage(DetailView):
    model = Movie
    template_name = "moviedetail.html"
    context_object_name = "movie"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # لیست ۰ تا ۱۰ برای دکمه‌های امتیازدهی
        context["rating_range"] = range(0, 11)
        context["moviewatched"] = None
        if (self.request.user.is_authenticated):
            context["moviewatched"] = MovieWatched.objects.filter(movie=self.get_object(), userInform=self.request.user.userinformation).first()
        return context
class JournalList(ListView):
    model = Journal
    template_name = "all-journals.html"   # قالبی که لیست رو نشون میده
    context_object_name = "journals"      # اسم متغیر در قالب
    ordering = ["-created_at"]            # مرتب‌سازی بر اساس تاریخ ایجاد (جدیدترین اول) 
class MovieListView(ListView):
    model = Movie
    template_name = "movie_list.html"   # مسیر قالب
    context_object_name = "movies"             # اسم کانتکست در قالب
    paginate_by = 15                           # صفحه‌بندی (اختیاری)

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        if not query:
            return Movie.objects.all().order_by('-IMDBscore')
        terms = query.split()
        filters = Q(Title__icontains=query)
        for term in terms:
            filters |= Q(MovieActor__FirstName__icontains=term)
            filters |= Q(MovieActor__LastName__icontains=term)
            filters |= Q(MovieDirector__FirstName__icontains=term)
            filters |= Q(MovieDirector__LastName__icontains=term)
        return Movie.objects.filter(filters).distinct().order_by('-IMDBscore')
class MovieWatchedListView(ListView):
    model = MovieWatched
    template_name = "movie_watched.html"   # مسیر قالب
    context_object_name = "movieWatched"             # اسم کانتکست در قالب
    paginate_by = 15                           # صفحه‌بندی (اختیاری)

    def get_queryset(self):
        return MovieWatched.objects.filter(userInform=self.request.user.userinformation).select_related("movie").order_by("-theDegreeOfInterestOrDisinterest")
class JournalListView(ListView):
    model = Journal
    template_name = "all-journals.html"   # مسیر قالب
    context_object_name = "journals"
    paginate_by = 10   # اختیاری: صفحه‌بندی

    def get_queryset(self):
        # مثلا مرتب‌سازی بر اساس تاریخ ایجاد
        return Journal.objects.order_by('-created_at') 
class JournalDetailView(DetailView):
    model = Journal
    template_name = "journal-detail.html"
    context_object_name = "journal" 
# movies/views.py
from django.contrib.auth.decorators import login_required
from Recommendations.models import  MovieWatched, UserInformationFormovieSuggestions
from Recommendations.function import update_user_interests

@login_required
def rate_movie(request, movie_id):
    movie = get_object_or_404(Movie, Movie_id=movie_id)
    if request.method == "POST":
        score = float(request.POST.get("score"))

        # گرفتن پروفایل کاربر (فرض می‌کنیم UserInformationFormovieSuggestions به User وصل است)
        user_info = get_object_or_404(UserInformationFormovieSuggestions, user=request.user)

        # چون constraint داری (هر کاربر برای هر فیلم فقط یک رکورد)، بهتره update_or_create استفاده کنیم
        obj, created = MovieWatched.objects.update_or_create(
            userInform=user_info,
            movie=movie,
            defaults={
                "theDegreeOfInterestOrDisinterest": score,
                "likeAMovie": True,
                "isUse": True,
            }
        )

        update_user_interests(user_info)
        messages.success(request, "امتیاز شما با موفقیت ثبت شد!")

    return redirect("movie_detail", pk=movie.Movie_id) 





