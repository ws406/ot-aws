from kafka import KafkaConsumer, KafkaProducer
from src.ops.game_predictor.rf_6_leagues import RF6Leagus
import json

kafka_topic_input = 'event-new-game'
kafka_topic_output = 'event-game-qualified'

producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
consumer = KafkaConsumer(
				kafka_topic_input,
				bootstrap_servers='localhost:9092',
				value_deserializer=lambda m: json.loads(m.decode('utf-8')),
				auto_offset_reset='latest'  # or earliest
			)

game_qualifier = RF6Leagus()

print("Consumer / Game_qualifier (RandomForest with 6 leagues) starting...")

while True:
	# Consume message one by one
	for message in consumer:
		game_data = message.value
		game_qualification_info = game_qualifier.get_prediction(game_data)
		# Produce new message on Kafka if game is qualified
		if game_qualification_info is False:
			print ("--- Game " + str(game_data['game_id']) + " is not qualified ---")
		else:
			print("+++ Game " + str(game_data['game_id']) + " is qualified. Send message to Kafka under topic - "
				+ kafka_topic_output + " +++")
			producer.send(kafka_topic_output, game_qualification_info)
