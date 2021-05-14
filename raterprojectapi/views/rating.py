from raterprojectapi.models.rating import Rating
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterprojectapi.models import Game, Player, Rating


class RatingViewSet(ViewSet):
    
    def create(self, request):

        player = Player.objects.get(user= request.auth.user)

        rating = Rating()
        rating.rating = request.data['rating']
        rating.player = player
        game = Game.objects.get(pk=request.data['gameId'])
        rating.game = game
    
        try:
            rating.save()
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class RatingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Rating
        fields = ('id', 'player','rating', 'game')
        depth = 1