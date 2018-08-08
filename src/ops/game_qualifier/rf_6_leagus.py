from kafka import KafkaConsumer
from src.ops.game_qualifier.interface import GameQualifierInterface
import json
from kafka import KafkaProducer
import time
import datetime


class RF6Leagus(GameQualifierInterface):

    kafka_topic = 'event-new-game'

    def __init__(self):
        pass

    def is_game_qualified(self, game_data):
        # TODO: this needs to be filled.
        # Input date format is the one single game (only ONE game) in json

        # If not qualified, return
        return False

        # If qualified, return the following, pay attention to "preferred_team", "bet_on_market" an "min_odds_to_bet_on"
        return {
            "game_id": 996135,
            "rounds": "1",
            "league_id": 273,
            "season": "2014-2015",
            "league_name": "Australia A-League",
            "kickoff": 1412930400.0,
            "home_team_name": "Melbourne Victory",
            "away_team_name": "Western Sydney",
            "home_team_id": 2901,
            "away_team_id": 20394,
            "preferred_team": 'home or away',
            "bet_on_market": "dnb, +0.5 or win",
            "min_odds_to_bet_on": 3.21
        }
        pass

