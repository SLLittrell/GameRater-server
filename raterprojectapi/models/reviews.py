from django.db import models

class Review(models.Model):
    title =(models.CharField(max_length=50))
    review =(models.TextField())
    rating =(models.IntegerField())
    game =(models.ForeignKey("Game", on_delete= models.CASCADE))
    reviewer = (models.ForeignKey("Player", on_delete =models.CASCADE))
    