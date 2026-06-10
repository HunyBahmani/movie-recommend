from django.contrib import admin
from .models import UserInformationFormovieSuggestions, MovieWatched, MovieFeatur

@admin.register(UserInformationFormovieSuggestions)
class UserInformationFormovieSuggestionsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "favActor",
        "aveIMDBSc",
        "interestInAction",
        "interestInComedy",
        "interestInDrama",
        "interestInViolent",
        "interestInFamilyFriendly",
    )
    search_fields = ("user__username", "favActor__name")
    list_filter = ("favActor",)
    ordering = ("user",)


@admin.register(MovieWatched)
class MovieWatchedAdmin(admin.ModelAdmin):
    list_display = (
        "userInform",
        "movie",
        "likeAMovie",
        "theDegreeOfInterestOrDisinterest",
        "isUse",
    )
    search_fields = ("userInform__user__username", "movie__Title")
    list_filter = ("likeAMovie", "isUse")
    ordering = ("userInform", "movie")


@admin.register(MovieFeatur)
class MovieFeaturAdmin(admin.ModelAdmin):
    list_display = (
        "movie",
        "amountOfAction",
        "amountOfComedy",
        "amountOfDrama",
        "amountOfViolent",
        "amountOfFamilyFriendly",
    )
    search_fields = ("movie__Title",)
    ordering = ("movie",)



