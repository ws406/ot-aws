from kafka import KafkaConsumer, KafkaProducer
import json
import sys
from src.ops.bet_placer.fb_betfair import FBBetfair
import datetime


class Main():
    kafka_topic_fb_game_qualified = 'event-game-qualified'
    kafka_topic_bet_placed = 'event-bet-placed'
    kafka_topic_error = 'event-error'

    amount = 2
    mins_before_kickoff = 5
    commission_rate = 0.05
    profit_margin = 0.02 # ensure we win something!

    def execute(self, debug_mode=False):

        print ("Bet_placer starting...")

        # Step 1: Get betfair session and key
        args = len (sys.argv)

        if args < 3:
            print ('Please provide Application key and session token')
            app_key = input ('Enter your application key :')
            session_token = input ('Enter your session Token/SSOID :')
            print ('Thanks for the input provided')
        else:
            app_key = sys.argv [1]
            session_token = sys.argv [2]

        fb_betfair = FBBetfair (app_key, session_token, self.commission_rate, self.profit_margin)

        # Step 2: Get data ready to be processed
        if debug_mode:
            games_to_bet_on = [
                {'gid': 1691209, 'league_id': 358, 'league_name': 'Brazil Serie B', 'kickoff': 1563920100.0, 'home_team_name': 'Figueirense', 'away_team_name': 'Parana PR', 'home_team_id': 355, 'away_team_id': 2449, 'true_odds': {'1': 2.221815605646156, 'x': 3.284223304072542, '2': 4.428231071028553}, 'strategy': 'true_odds'},
                {'gid': 1691210, 'league_id': 358, 'league_name': 'Brazil Serie B', 'kickoff': 1563920100.0, 'home_team_name': 'Sao Bento', 'away_team_name': 'Operario Ferroviario PR', 'home_team_id': 3824, 'away_team_id': 13086, 'true_odds': {'1': 3.1057135132182703, 'x': 3.210221168999228, '2': 2.8826756257463164}, 'strategy': 'true_odds'},
                {'gid': 1691211, 'league_id': 358, 'league_name': 'Brazil Serie B', 'kickoff': 1563920100.0, 'home_team_name': 'Guarani SP', 'away_team_name': 'Cuiaba', 'home_team_id': 367, 'away_team_id': 1973, 'true_odds': {'1': 2.486616361674639, 'x': 3.303340946336411, '2': 3.629560832496613}, 'strategy': 'true_odds'},
                {'gid': 1691215, 'league_id': 358, 'league_name': 'Brazil Serie B', 'kickoff': 1563920100.0, 'home_team_name': 'Coritiba PR', 'away_team_name': 'Vila Nova', 'home_team_id': 350, 'away_team_id': 1972, 'true_odds': {'1': 2.320257284218045, 'x': 3.3457554430714604, '2': 3.991708279258591}, 'strategy': 'true_odds'},
                {'gid': 1691207, 'league_id': 358, 'league_name': 'Brazil Serie B', 'kickoff': 1563924600.0, 'home_team_name': 'Bragantino', 'away_team_name': 'Ponte Preta', 'home_team_id': 3820, 'away_team_id': 381, 'true_odds': {'1': 2.0812978077460564, 'x': 3.4249409262383823, '2': 4.80892056101687}, 'strategy': 'true_odds'},
                {'gid': 1691213, 'league_id': 358, 'league_name': 'Brazil Serie B', 'kickoff': 1563924600.0, 'home_team_name': 'Atletico Clube Goianiense', 'away_team_name': 'Botafogo SP', 'home_team_id': 5156, 'away_team_id': 9814, 'true_odds': {'1': 2.1567839829715627, 'x': 3.423804489948762, '2': 4.451049598494313}, 'strategy': 'true_odds'}
            ]
        else:
            producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            consumer = KafkaConsumer(
                self.kafka_topic_fb_game_qualified,
                bootstrap_servers='localhost:9092',
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest'  # or latest
            )
            games_to_bet_on = []
            for message in consumer:
                games_to_bet_on.append(message.value)

        # Step 3: placing bets

        for game_data in games_to_bet_on:
            actual_kickoff = datetime.datetime.fromtimestamp (game_data ['kickoff'])

            if game_data['league_id'] == 21:
                # Kickoff is always 10 mins after the official kickoff time in game_data.
                actual_kickoff = datetime.datetime.fromtimestamp(game_data['kickoff']) + datetime.timedelta(minutes = 10)

            betfair = fb_betfair

            # If actual_kickoff is more than mins_before_kickoff mins away, do not place bet
            if actual_kickoff - datetime.datetime.now() > datetime.timedelta(minutes = self.mins_before_kickoff):
                print ("Too early to place bet for game " + ' ' + game_data ['home_team_name'] + ' vs ' +
                       game_data ['away_team_name'])
                continue

            result = betfair.place_match_odds_bet(game_data, self.amount, debug_mode)
            if debug_mode:
                print('(debug_mode) - bet_placing_request_pay_load:')
                print(result)

            else:
                print(result)
                status = result['status']
                message = result['message']
                if status == 'error':
                    producer.send(self.kafka_topic_error, message)
                elif status == 'success':
                    producer.send(self.kafka_topic_bet_placed, message)
                elif status == 'ignore':
                    print(message)
                    pass


if __name__ == '__main__':
    debug_mode = False
    while True:
        Main().execute(debug_mode=debug_mode)
        if debug_mode:
            break
