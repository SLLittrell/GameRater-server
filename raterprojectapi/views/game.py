from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterprojectapi.models import Game, GameCategory, Player


class GameViewSet(ViewSet):
    

    def create(self, request):

        creator = Player.objects.get(user=request.auth.user)

        game = Game()
        game.title = request.data['title']
        game.description = request.data['description']
        game.release_year = request.data['releaseYear']
        game.number_players = request.data['numberPlayers']
        game.time_to_play = request.data['timeToPlay']
        game.age = request.data['age']
        game.creator = creator
    
        category = GameCategory.objects.get(pk=request.data["categoryId"])
        game.game_category = category

    
        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
     
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
  
        creator = Player.objects.get(user=request.auth.user)

        game.title = request.data['title']
        game.description = request.data['description']
        game.release_year = request.data['releaseYear']
        game.number_players = request.data['numberPlayers']
        game.time_to_play = request.data['timeToPlay']
        game.age = request.data['age']
        game.creator = creator

        category = GameCategory.objects.get(pk=request.data["categoryId"])
        game.game_category = category
        game.save()


        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
      
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
     
        games = Game.objects.all()

        game_type = self.request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(gametype__id=game_type)

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)

class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'release_year', 'number_players', 'time_to_play', 'age', 'creator')
        depth = 1
