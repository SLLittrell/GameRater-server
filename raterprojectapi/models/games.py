from raterprojectapi.models import categories
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
