from kafka import KafkaProducer
import time
import datetime
from src.win007.subject.bb_upcoming_games import Subject as UpcomingGamesProcessor
from src.win007.modules.games_fetcher.basketball_odds_fetcher.game_info_and_all_odds_sequence \
    import GameInfoAndAllOddsSequence
import json


class Main:
    # These data is used for
    bids = {
        26: "will_hill",  # WH
        # 214: "bet365",  # Bet365
        17: "pinnacle",  # Pinnacle
        82: "vcbet",  # VcBet
        6: "easybet",
        83: "ladbroke",
        381: "marathon",
        457: "marathonbet",
        446: "skybet",
    }
    minutes = 30
    league_names = {
        'NBA': 1  # NBA
    }

    gameDetector = None
    producer = None
    consumer = None

    kafka_topic = 'event-new-bb-game'
    kafka_producer = None

    def __init__ (self):
        self.gameDetector = UpcomingGamesProcessor (GameInfoAndAllOddsSequence (self.bids))

    def get_kafka_producer (self):
        if self.kafka_producer is None:
            self.kafka_producer = KafkaProducer (value_serializer = lambda v: json.dumps (v).encode ('utf-8'))
        return self.kafka_producer

    def execute (self):
        print ("Start...")

        # Get required data from process
        msg = "Getting basketball games that will start in the next " + str (self.minutes) + " mins"
        if self.league_names is not None:
            msg += " and from " + str (len (self.league_names)) + " leagues.."
        print (msg)
        games = self.gameDetector.get_games (self.minutes, self.league_names)

        kafka_producer = self.get_kafka_producer ()
        for game in games:
            gid_str = str (game ['game_id'])
            kafka_producer.send (self.kafka_topic, game, key = gid_str)
            kafka_producer.send (self.kafka_topic, game)
            print ("\tSend game " + gid_str + " to Kafka")
        print (str (len (games)) + " games pushed Kafka under topic " + self.kafka_topic)
        return len(games)


if __name__ == '__main__':
    normal_interval_in_mins = 5

    while (True):
        try:
            num_games = Main ().execute ()
            if num_games == 0:
                wait = Main().minutes - 5
            else:
                wait = normal_interval_in_mins
        except Exception as e:
            print ('Exception happened.... Try again later.')
        print ("Next run at UTC: " + str (datetime.datetime.now () + datetime.timedelta (minutes = wait)))
        time.sleep (60 * wait)
