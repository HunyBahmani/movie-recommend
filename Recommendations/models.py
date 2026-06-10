from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator 
from Movie.models import Movie , Actor 
from Users.models import User

class UserInformationFormovieSuggestions(models.Model): 
      user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='userinformation',primary_key=True)
      favActor = models.ForeignKey(Actor,on_delete=models.SET_NULL,null=True,blank=True,related_name='favactor')
      aveIMDBSc = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)]) 
      interestInAction = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)]) 
      interestInComedy = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)]) 
      interestInDrama = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)]) 
      interestInViolent = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)]) 
      interestInFamilyFriendly = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)])
class MovieWatched(models.Model): 
      userInform = models.ForeignKey(UserInformationFormovieSuggestions,on_delete=models.CASCADE,related_name='userinform') 
      movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='userinform') 
      likeAMovie = models.BooleanField(default=True)
      theDegreeOfInterestOrDisinterest = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)]) 
      isUse = models.BooleanField(default=False)
      class Meta:
         constraints =  [models.UniqueConstraint(fields=["userInform", "movie"], name="unique_movie_watched")]
class MovieFeatur(models.Model): 
      movie = models.OneToOneField(Movie,on_delete=models.CASCADE,related_name='moviefeatur',primary_key=True)
      amountOfAction = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)]) 
      amountOfComedy = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)]) 
      amountOfDrama = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)]) 
      amountOfViolent = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)]) 
      amountOfFamilyFriendly = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)])