from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid 

class Director(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    Director_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    FirstName = models.CharField(max_length=200,blank=True,null=True) 
    LastName = models.CharField(max_length=200,blank=True,null=True) 
    Biography = models.TextField(blank=True,null=True) 
    Picture = models.BinaryField(blank=True,null=True) 
    Birth_date = models.DateField(null=True, blank=True) 
    Gender = models.CharField(max_length=1,choices=GENDER_CHOICES,blank=True) 
    def __str__(self):
        return self.FirstName + ' ' + self.LastName 
class Actor(models.Model): 
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    Actor_id = models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True,editable=False)
    FirstName = models.CharField(max_length=200,null=True, blank=True) 
    LastName = models.CharField(max_length=200,null=True, blank=True) 
    Biography = models.TextField(blank=True) 
    Picture = models.ImageField(upload_to='Actoravatars/',blank=True,null=True) 
    Birth_date = models.DateField(null=True, blank=True) 
    Gender = models.CharField(max_length=1,choices=GENDER_CHOICES,blank=True) 
    def __str__(self):
        return self.FirstName + ' ' + self.LastName
class Movie(models.Model): 
    GENRE_CHOICES = [("Ac","Action"),("Ad","Adventure"),("An","Animation"),("Co","Comedy"),("Cr","Crime"),("Do","Documentary"),("Dr","Drama"),("Fa","Fantasy"),("Hi","Historical / Biopic"),("Ho","Horror"),("Mu","Musical"),("My","Mystery"),("Ro","Romance"),("Sc","Science Fiction (Sci-Fi)"),("Th","Thriller"),("Wa","War")]
    Movie_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    Title = models.CharField(max_length=200,null=True, blank=True) 
    Genre = models.CharField(max_length=2,choices=GENRE_CHOICES,blank=True)
    Description = models.TextField(blank=True) 
    IMDBscore = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)])
    Poster = models.ImageField(upload_to='Movieavatars/',blank=True,null=True) 
    Trailer = models.FileField(upload_to="trailers/", null=True, blank=True)
    MovieActor = models.ManyToManyField(Actor,through='MovieActor') 
    MovieDirector = models.ForeignKey(Director,on_delete=models.CASCADE,related_name='Movies')
    def __str__(self):
        return self.Title 
class MovieActor(models.Model): 
    MovieActor_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,related_name='Movies')
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE,related_name='Actors') 
    Description = models.TextField(blank=True,default="Unknown")
    role = models.CharField(max_length=100,default="Unknown") 
    class Meta:
        unique_together = ('movie', 'actor')
    def __str__(self):
        return self.Description
class Journal(models.Model):
    title = models.CharField(max_length=200)  # عنوان ژورنال
    excerpt = models.TextField(blank=True)    # خلاصه یا چکیده
    content = models.TextField()              # متن کامل مقاله
    image = models.ImageField(upload_to="journals/", blank=True, null=True)  # تصویر کاور
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد
    updated_at = models.DateTimeField(auto_now=True)      # تاریخ آخرین ویرایش

    def __str__(self):
        return self.title
