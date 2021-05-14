from django.db import models

class GamedImage(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    title = models.CharField(max_length=50)