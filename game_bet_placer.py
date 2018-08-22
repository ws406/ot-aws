from kafka import KafkaConsumer, KafkaProducer
import json
from src.utils.mailer import Mailer
import datetime
import sys

kafka_topic_input = 'event-game-qualified'
kafka_topic_output = 'event-bet-placed'

recipient = "wangjia.sun@gmail.com, panda0079@gmail.com"

producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
consumer = KafkaConsumer(
				kafka_topic_input,
				bootstrap_servers='localhost:9092',
				value_deserializer=lambda m: json.loads(m.decode('utf-8')),
				auto_offset_reset='latest'  # or earliest
			)
mailer = Mailer()

# print("Bet_placer starting...")
#
# args = len(sys.argv)
#
# if args < 3:
# 	print ('Please provide Application key and session token')
# 	appKey  = input('Enter your application key :')
# 	sessionToken = input('Enter your session Token/SSOID :')
# 	print ('Thanks for the input provided')
# else:
# 	appKey = sys.argv[1]
# 	sessionToken = sys.argv[2]
#
# headers = {'X-Application': appKey, 'X-Authentication': sessionToken, 'content-type': 'application/json'}

while True:
	content = ''
	# Consume message one by one
	for message in consumer:
		game_data = message.value
		print(game_data)
		# Place bet & send results to Kafka
		subject = str(game_data['home_team_name']) + ' vs ' + str(game_data['away_team_name']) + ' at ' + str(datetime.datetime.now())
		mailer.send_email("wangjia.sun@gmail.com, panda0079@gmail.com", subject, str(game_data))
	