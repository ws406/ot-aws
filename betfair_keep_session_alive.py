from kafka import KafkaConsumer, KafkaProducer
import json
import sys
from src.ops.bet_placer.bb_betfair import BBBetfair
from src.ops.bet_placer.fb_betfair import FBBetfair
import datetime
import time

kafka_topic_error = 'event-error'

producer = KafkaProducer (value_serializer = lambda v: json.dumps (v).encode ('utf-8'))
print ("Betfair keep_session_alive starting...")

args = len (sys.argv)

if args < 3:
    print ('Please provide Application key and session token')
    appKey = input ('Enter your application key :')
    sessionToken = input ('Enter your session Token/SSOID :')
    print ('Thanks for the input provided')
else:
    appKey = sys.argv [1]
    sessionToken = sys.argv [2]

betfair = BBBetfair (appKey, sessionToken)
session_lifespan_in_hours = 7
while True:
    result = betfair.keep_session_alive()
    if result ['status'] == 'error':
        producer.send (kafka_topic_error, result)
    else:
        print ("Session renewed at " + str (datetime.datetime.now ()))
    print ("Next run at UTC: " + str (datetime.datetime.now () + datetime.timedelta (hours = session_lifespan_in_hours)))
    time.sleep (60 * 60 * session_lifespan_in_hours)