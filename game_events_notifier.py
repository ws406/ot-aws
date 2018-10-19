from kafka import KafkaConsumer, KafkaProducer
import json
from src.utils.mailer import Mailer
import datetime
import sys

kafka_topic_game_qualified = 'event-game-qualified'
kafka_topic_bb_game_qualified = 'event-bb-game-qualified'
kafka_topic_game_bet = 'event-game-bet'

recipient1 = "wangjia.sun@gmail.com"
recipient2 = "panda0079@gmail.com"

producer = KafkaProducer (value_serializer = lambda v: json.dumps (v).encode ('utf-8'))
consumer = KafkaConsumer (
	kafka_topic_game_qualified,
	kafka_topic_game_bet,
	kafka_topic_bb_game_qualified,
	bootstrap_servers = 'localhost:9092',
	value_deserializer = lambda m: json.loads (m.decode ('utf-8')),
	auto_offset_reset = 'latest'
)
mailer = Mailer ()

while True:
	# Consume message one by one
	for message in consumer:		# Send notification when a game is qualified
		if message.topic == kafka_topic_game_qualified or message.topic == kafka_topic_bb_game_qualified:
			game_data = message.value
			print (game_data)
			subject = str (game_data ['home_team_name']) + ' vs ' + str (game_data ['away_team_name']) + ' at ' + str (
				datetime.datetime.now ())
			mailer.send_email (recipient1, subject, str (game_data))
			mailer.send_email (recipient2, subject, str (game_data))

		# Send notification when a bet is placed
		elif message.topic == kafka_topic_game_bet:
			game_data = message.value
			# Place bet & send results to Kafka
			subject = game_data ['game_title']
			content = ''
			mailer.send_email (recipient1, subject, str (game_data))
			# mailer.send_email (recipient2, subject, str (game_data))
