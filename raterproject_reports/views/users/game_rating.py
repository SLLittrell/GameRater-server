"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from raterprojectapi.models import Game
from raterproject_reports.views import Connection

def userevents_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    e.id,
                    e.date,
                    e.description,
                    e.time,
                    e.game_id,
                    g.title,
                    u.id user_id,
                    u.first_name || ' ' || u.last_name AS full_name
                FROM
                    levelupapi_event e
                JOIN
                    levelupapi_game g ON g.id = e.game_id
                JOIN
                    levelupapi_gamer gr ON gr.id = e.organizer_id 
                JOIN
                    auth_user u ON gr.user_id = u.id
            """)

            dataset = db_cursor.fetchall()

            events_by_user = {}

            for row in dataset:

                event = Event()
                event.time = row["time"]
                event.date = row["date"]
                event.description = row["description"]
                event.game_id = row["game_id"]
                event.game_name = event.game.title

                uid = row["user_id"]

                if uid in events_by_user:

                   events_by_user[uid]['events'].append(event)

                else:
                   events_by_user[uid] = {}
                   events_by_user[uid]["id"] = uid
                   events_by_user[uid]["full_name"] = row["full_name"]
                   events_by_user[uid]["events"] = [event]

        list_of_users_with_events = events_by_user.values()

        template = 'users/list_with_events.html'
        context = {
            'userevent_list': list_of_users_with_events
        }

        return render(request, template, context)