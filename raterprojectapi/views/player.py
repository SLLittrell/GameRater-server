from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from raterprojectapi.models import Player
from django.contrib.auth.models import User
from rest_framework import serializers

class PlayerViewSet(ViewSet):
    def list(self, request):
        players = Player.objects.all()
        res = PlayerSerializer(players, many=True)
        return Response(res.data)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = UserSerializer(many=False)

    class Meta:
        model = Player
        fields = ['id', 'user']

