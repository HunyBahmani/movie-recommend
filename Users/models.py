from django.db import models
from django.db.models.base import Model
from django.utils import timezone
from django.db import models
from django.db.models.fields import TextField 
from django.core.validators import MinValueValidator, MaxValueValidator 
from django.contrib.auth.models import AbstractUser 
from Movie.models import Movie
import uuid 
#F_id = models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True,editable=True)

class User(AbstractUser): 
      CITY_CHOICES = [("Ke","kerman"),("Te","tehran"),("Sh","shiraz"),("Ar","ardabil"),("Ta","tabriz")] 
      GENDER_CHOICES = [("M", "Male"),("F", "Female"),] 
      GENRE_CHOICES = [("Ac","Action"),("Ad","Adventure"),("An","Animation"),("Co","Comedy"),("Cr","Crime"),("Do","Documentary"),("Dr","Drama"),("Fa","Fantasy"),("Hi","Historical / Biopic"),("Ho","Horror"),("Mu","Musical"),("My","Mystery"),("Ro","Romance"),("Sc","Science Fiction (Sci-Fi)"),("Th","Thriller"),("Wa","War")]
      BirthDate = models.DateField(blank=True, null=True)
      City = models.CharField(max_length=3,choices=CITY_CHOICES,blank=True)
      Gender = models.CharField(max_length=1,choices=GENDER_CHOICES,blank=True)
      Fmovies = models.ManyToManyField(Movie,through='FavouriteMovies') 
      Fgenre = models.CharField(max_length=2,choices=GENRE_CHOICES,blank=True) 
      def __str__(self):
          return self.username
class FavouriteMovies(Model): 
     Favouritemovie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="favmov") 
     User = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user") 
     theDegreeOfInterest = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)]) 
     isUse = models.BooleanField(default=False)
     class Meta:
         constraints =  [models.UniqueConstraint(fields=["User", "Favouritemovie"], name="unique_user_movie_favourite")] 
class Profile(Model): 
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    Bio = models.TextField(blank=True, null=True) 
    Avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    def __str__(self):
        return f"Profile of {self.user.username}"