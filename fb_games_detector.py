from src.win007.subject.fb_upcoming_games import Subject as UpcomingGamesProcessor
from src.win007.modules.games_fetcher.football_odds_fetcher.game_info_and_all_odds_sequence import \
    GameInfoAndAllOddsSequence
import json
from kafka import KafkaProducer
import time
import datetime


class Main:
    # These data is used for
    bids = {
        281: "bet365",  # Bet365
        177: "pinnacle",  # Pinnacle
        81:  "betvictor",  # Bet Victor
        # 80: "macau_slot",  # Macao Slot
        # 115: "will_hill",  # WH
        # 432: "hkjc",  # HKJC
        # 104: "interwetten"  # Interwetten
    }
    minutes = 15
    league_ids = [
        34,  # IT1
        # 40,  # IT2
        #
        36,  # EPL
        37,  # ENC
        39,  # EFL1
        35,  # EFL2
        #
        31,  # ES1
        33,  # ES2
        #
        8,  # GE1
        9,  # GE2
        #
        11,  # FR1
        12,  # FR2
        #
        # 13, # FIN1
        # 700, # THAI1
        #
        16,  # HO1
        17,  # HO2
        #
        25,  # JAP1
        284,  # JAP2
        #
        4,  # BRA1
        358,  # BRA2
        #
        23,  # POTG1
        29,  # SCOT1
        30,  # TUR1
        5,  # BEL1
        26,  # SWE1
        22,  # NOR1
        # 27,  # SWl1
        10,  # RUS1
        # 2,  # ARG1
        21,  # USA1
        # 415,  # CHILE1
        # 140,  # MEX1

        60,  # CHN1
        15,  # KOR1
        273,  # AUS
    ]

    gameDetector = None
    producer = None
    consumer = None

    kafka_topic = 'event-new-game'
    kafka_producer = None

    def __init__ (self):
        self.gameDetector = UpcomingGamesProcessor (GameInfoAndAllOddsSequence (self.bids))

    def get_kafka_producer (self):
        if self.kafka_producer is None:
            self.kafka_producer = KafkaProducer (value_serializer = lambda v: json.dumps (v).encode ('utf-8'))
        return self.kafka_producer

    def execute (self, debug_mode=True):
        print ("Start...")

        # Get required data from process
        msg = "Getting games that will start in the next " + str (self.minutes) + " mins"
        if self.league_ids is not None:
            msg += " and from " + str (len (self.league_ids)) + " leagues.."
        print (msg)
        games = self.gameDetector.get_games (self.minutes, self.league_ids)  # Get games starting in the next 5 mins.

        # Return false to indicate that this needs to be return
        if games is False:
            print ('Failed to get data from URL. Retrying....')
            return False

        if not debug_mode:
            kafka_producer = self.get_kafka_producer ()

        for game in games:
            gid_str = str (game ['game_id'])
            if not debug_mode:
                kafka_producer.send (self.kafka_topic, game, key = gid_str)
                kafka_producer.send (self.kafka_topic, game)
                print ("\tSend game " + gid_str + " to Kafka")
            else:
                print(game)

        if not debug_mode:
            print(str(len(games)) + " games pushed Kafka under topic " + self.kafka_topic)
        return len(games)


if __name__ == '__main__':
    normal_interval_in_mins = 5
    # wait =

    while (True):
        try:
            num_games = Main().execute(debug_mode=False)

            # Failed to get games from URL, retry
            if num_games is False:
                continue

            if num_games == 0:
                wait = Main().minutes - normal_interval_in_mins
            else:
                wait = normal_interval_in_mins
        except Exception as e:
            print ('Exception happened.... Try again later.')
            raise e
        print ("Next run at UTC: " + str (datetime.datetime.now () + datetime.timedelta (minutes = wait)))
        time.sleep (60 * wait)
