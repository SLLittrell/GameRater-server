from raterprojectapi.models import categories
from raterprojectapi.models.rating import Rating
from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    release_year = models.IntegerField()
    number_players = models.IntegerField()
    time_to_play = models.IntegerField()
    age = models.IntegerField()
    creator = models.ForeignKey("Player", on_delete=models.CASCADE)
    categories = models.ManyToManyField("Category", related_name="games")



    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = Rating.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating
        
        average = 0 
        if(len(ratings)):
            average = total_rating / len(ratings)

        return average
            

        # Calculate the average and return it.
        # If you don't know how to calculate average, Google it.
