"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from raterprojectapi.models import Rating, Game
from raterproject_reports.views import Connection

def game_rating_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT 
                    avg(r.rating) average,
                    g.title, 
                    g.id 
                From raterprojectapi_game g
                JOIN raterprojectapi_rating r ON r.game_id = g.id
                GROUP BY g.title
                ORDER BY average DESC 
                LIMIT 5
            """)

            dataset = db_cursor.fetchall()

            top_5_games = {}

            for row in dataset:

                game =Game()
                game.id = row['id']
                game.title = row['title']
                game.rating = row['average']
                
                top_5_games[game.id]= game

        list_of_top_5_games = list(top_5_games.values())

        template = 'games/game_report.html'
        context = {
            'top_5_games_list': list_of_top_5_games
        }

        return render(request, template, context)