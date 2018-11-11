from kafka import KafkaConsumer, KafkaProducer
import json

kafka_topic_input = 'event-new-game'

producer = KafkaProducer (value_serializer = lambda v: json.dumps (v).encode ('utf-8'))
consumer = KafkaConsumer (
    kafka_topic_input,
    bootstrap_servers = 'localhost:9092',
    value_deserializer = lambda m: json.loads (m.decode ('utf-8')),
    auto_offset_reset = 'latest'  # or earliest
)

print ("GCP Kafka tester starting...")

while True:
    # Consume message one by one
    for message in consumer:
        print (message)
# producer.send(kafka_topic_output, game_qualification_info)
