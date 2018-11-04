from kafka import KafkaConsumer, KafkaProducer
import json
import sys
from src.ops.bet_placer.bb_betfair import BBBetfair
from src.ops.bet_placer.fb_betfair import FBBetfair
import datetime
import time

kafka_topic__bb_game_qualified = 'event-bb-game-qualified'
kafka_topic__fb_game_qualified = 'event-game-qualified'
kafka_topic_bet_placed = 'event-bet-placed'
kafka_topic_error = 'event-error'

producer = KafkaProducer (value_serializer = lambda v: json.dumps (v).encode ('utf-8'))
consumer = KafkaConsumer (
    kafka_topic__bb_game_qualified,
    kafka_topic__fb_game_qualified,
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

bb_betfair = BBBetfair (appKey, sessionToken)
fb_betfair = FBBetfair (appKey, sessionToken)
amount = 1000
mins_before_kickoff = 5

now_ts = time.time()
eight_hours_ts = 60*60*8

# TODO: this only bet on NBA now
while True:

    if time.time() - now_ts >= eight_hours_ts:
        result = fb_betfair.keep_session_alive()
        if result['status'] == 'error':
            producer.send (kafka_topic_error, result)
        else:
            print("Session renewed at " + str(datetime.datetime.now()))

    for message in consumer:
        game_data = message.value
        print(game_data)
        if message.topic == kafka_topic__bb_game_qualified:
            # Actual kickoff is kickoff + 10 mins for NBA
            actual_kickoff = datetime.datetime.fromtimestamp(game_data['kickoff']) + datetime.timedelta(minutes = 10)
            betfair = bb_betfair
        elif message.topic == kafka_topic__fb_game_qualified:
            actual_kickoff = datetime.datetime.fromtimestamp (game_data ['kickoff'])
            betfair = fb_betfair
        else:
            print('Can not handle topic - ' + message.topic)

        # If actual_kickoff is more than mins_before_kickoff mins away, do not place bet
        if actual_kickoff - datetime.datetime.now () > datetime.timedelta (minutes = mins_before_kickoff):
            print ("Too early to place bet for game " + ' ' + game_data ['home_team_name'] + ' vs ' +
                   game_data ['away_team_name'])
            continue
        result = betfair.place_match_odds_bet (game_data, amount)
        if result['status'] == 'error':
            producer.send (kafka_topic_error, result)
        else:
            producer.send (kafka_topic_bet_placed, result)
