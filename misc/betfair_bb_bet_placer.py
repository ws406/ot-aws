from kafka import KafkaConsumer, KafkaProducer
import json
import sys
from src.ops.bet_placer.bb_betfair import BBBetfair
from src.ops.bet_placer.fb_betfair import FBBetfair
import datetime

kafka_topic_bb_game_qualified = 'event-bb-game-qualified'
kafka_topic_bet_placed = 'event-bet-placed'
kafka_topic_error = 'event-error'

producer = KafkaProducer (value_serializer = lambda v: json.dumps (v).encode ('utf-8'))
consumer = KafkaConsumer (
    kafka_topic_bb_game_qualified,
    bootstrap_servers = 'localhost:9092',
    value_deserializer = lambda m: json.loads (m.decode ('utf-8')),
    auto_offset_reset = 'latest'  # or latest
)
print ("Bet_placer starting...")

args = len (sys.argv)

if args < 3:
    print ('Please provide Application key and session token')
    appKey = input ('Enter your application key :')
    sessionToken = input ('Enter your session Token/SSOID :')
    print ('Thanks for the input provided')
else:
    appKey = sys.argv [1]
    sessionToken = sys.argv [2]

amount = 1000
mins_before_kickoff = 5
commission_rate = 0.05

bb_betfair = BBBetfair (appKey, sessionToken, commission_rate)


def keep_session_alive():
    result = bb_betfair.keep_session_alive ()
    if result ['status'] == 'error':
        producer.send (kafka_topic_error, result)
    else:
        print ("Session renewed at " + str (datetime.datetime.now ()))

# This only bet on NBA now
while True:

    for message in consumer:
        game_data = message.value
        print(game_data)

        # Kickoff in game_data is 30 mins more than the kickoff from website. To place a bet, we assume the kickoff is
        # website_kickoff + 10. Thus we do kickoff-20 here.
        actual_kickoff = datetime.datetime.fromtimestamp(game_data['kickoff']) - datetime.timedelta(minutes = 20)
        betfair = bb_betfair

        # If actual_kickoff is more than mins_before_kickoff mins away, do not place bet
        if actual_kickoff - datetime.datetime.now () > datetime.timedelta (minutes = mins_before_kickoff):
            print ("Too early to place bet for game " + ' ' + game_data ['home_team_name'] + ' vs ' +
                   game_data ['away_team_name'])
            continue
        result = betfair.place_match_odds_bet (game_data, amount)
        print(result)
        status = result['status']
        message = result['message']
        if status == 'error':
            producer.send (kafka_topic_error, message)
        elif status == 'success':
            producer.send (kafka_topic_bet_placed, message)
        elif status == 'ignore':
            print(message)
            pass
