from kafka import KafkaConsumer, KafkaProducer
import json
from src.utils.mailer import Mailer
import datetime
import sys
from src.ops.bet_placer.betfair import Betfair

kafka_topic_input = 'event-game-qualified'
kafka_topic_output = 'event-bet-placed'

producer = KafkaProducer (value_serializer = lambda v: json.dumps (v).encode ('utf-8'))
consumer = KafkaConsumer (
	kafka_topic_input,
	bootstrap_servers = 'localhost:9092',
	value_deserializer = lambda m: json.loads (m.decode ('utf-8')),
	auto_offset_reset = 'latest'  # or earliest
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

betfair = Betfair(appKey, sessionToken)
amount = 2

while True:
	for message in consumer:
		game_data = message.value
		betfair.place_match_odds_bet(game_data, amount)
