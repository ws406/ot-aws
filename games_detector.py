from src.win007.subject.upcoming_games import Subject as UpcomingGamesProcessor
from src.win007.modules.games_fetcher.football_odds_fetcher.game_info_and_all_odds_sequence import GameInfoAndAllOddsSequence
import json
from kafka import KafkaProducer
import time
import datetime

class Main:
    # These data is used for
    bids = {
        80: "macau_slot",  # Macao Slot
        115: "will_hill",  # WH
        281: "bet365",     # Bet365
        177: "pinnacle",   # Pinnacle
        432: "hkjc",       # HKJC
        104: "interwetten" # Interwetten
    }
    minutes = 15
    league_ids = [
        34,  # IT1
        36,  # EPL
        37,  # ENC
        31,  # ES1
        8,  # GE1
        16,  # HO1
    ]

    gameDetector = None
    producer = None
    consumer = None

    kafka_topic = 'event-new-game'

    def __init__(self):
        self.gameDetector = UpcomingGamesProcessor(GameInfoAndAllOddsSequence(self.bids))

    def execute(self, kafka_producer: KafkaProducer):
        print("Start...")

        # Get required data from process
        msg = "Getting games that will start in the next " + str(self.minutes) + " mins"
        if self.league_ids is not None:
            msg += " and from "+ str(len(self.league_ids)) + " leagues.."
        print(msg)
        games = self.gameDetector.get_games(self.minutes, self.league_ids)    # Get games starting in the next 5 mins.
        file = open('test_data.json', 'w+')
        file.write(json.dumps(games))
        file.close()

        for game in games:
            gid_str = str(game['game_id'])
            kafka_producer.send(self.kafka_topic, game, key=gid_str)
            kafka_producer.send(self.kafka_topic, game)
            print("\tSend game " + gid_str + " to Kafka")

        print(str(len(games)) + " games pushed Kafka under topic " + self.kafka_topic)


if __name__ == '__main__':
    interval_in_mins = 1
    producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    while (True) :
        Main().execute(producer)
        # sleep for 5 mins
        print("Next run at UTC: " + str(datetime.datetime.now() + datetime.timedelta(minutes=interval_in_mins)))
        time.sleep(60 * interval_in_mins)
