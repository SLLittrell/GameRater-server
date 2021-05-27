import json
from rest_framework import status
from rest_framework.test import APITestCase
from raterprojectapi.models import Category, Game, Player


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

        self.game = Game()
        self.game.title = "Monopoly"
        self.game.description = "I got all the Money"
        self.game.release_year = 1935
        self.game.number_players = 8
        self.game.time_to_play = 180
        self.game.age = 8
        self.game.creator_id =1

        self.game.save()
        self.game.categories.set([1])

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
    
    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """
       

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.get(f"/games/{self.game.id}")

        json_response = json.loads(response.content)
      
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["title"], "Monopoly")
        self.assertEqual(json_response["description"], "I got all the Money")
        self.assertEqual(json_response["release_year"], 1935)
        self.assertEqual(json_response["number_players"], 8)
        self.assertEqual(json_response["time_to_play"], 180)
        self.assertEqual(json_response["age"], 8)

    def test_get_all_games(self):
        """
        Ensure we can get an existing game.
        """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.get(f"/games")

        json_response = json.loads(response.content)
      
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(json_response), 1)

    def test_update_game(self):
        """ Ensure we can update a game.
        """
        url= "/games/1"
        data = {
        "title": "Monopoly",
        "description": "I got all the Money",
        "releaseYear": 1935,
        "numberPlayers": 8,
        "timeToPlay": 180,
        "age": 8,
        "creator": 1,
        "categories":[1]
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # self.game.categories.set([1])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'/games/{self.game.id}')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["title"], data["title"] )
        self.assertEqual(json_response["description"], data["description"] )
        self.assertEqual(json_response["release_year"], data["releaseYear"])
        self.assertEqual(json_response["number_players"], data["numberPlayers"])
        self.assertEqual(json_response["time_to_play"], data["timeToPlay"])
        self.assertEqual(json_response["age"], data["age"])
    
    
    def test_delete_game(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f'/games/{self.game.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'/games/{self.game.id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
