from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterprojectapi.models import Category


class CategoryViewSet(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            game_category = Category.objects.get(pk=pk)
            serializer = GameCategorySerializer(game_category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all game types
        Returns:
            Response -- JSON serialized list of game types
        """
        gamecategories = Category.objects.all()

        serializer = GameCategorySerializer(
            gamecategories, many=True, context={'request': request})
        return Response(serializer.data)

class GameCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for game categories
    Arguments:
        serializers
    """
    class Meta:
        model = Category
        fields = ('id', 'label')