import json
from rest_framework import status
from rest_framework.test import APITestCase
from raterprojectapi.models import Category, Game


class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types
        category = Category()
        category.label = "Board game"
        category.save()

    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        url = "/games"
        data = {
             "title": "Clue",
        "description": "Guess who's the murderer",
        "releaseYear": 1943,
        "numberPlayers": 6,
        "timeToPlay": 30,
        "age": 8,
        "categories":[1]
        }

        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.token)
        response = self.client.post(url, data, format ='json')
        json_response =json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["title"], "Clue")
        self.assertEqual(json_response["description"], "Guess who's the murderer")
        self.assertEqual(json_response["release_year"], 1943)
        self.assertEqual(json_response["number_players"], 6)
        self.assertEqual(json_response["time_to_play"], 30)
        self.assertEqual(json_response["age"], 8)
    