import sys
from src.ops.bet_placer.fb_betfair import FBBetfair
import datetime
import time
from src.utils.logger import OtLogger

logger = OtLogger('./logs/bf_session.log')

logger.log("Betfair keep_session_alive starting...")

args = len (sys.argv)

if args < 3:
    print ('Please provide Application key and session token')
    appKey = input ('Enter your application key :')
    sessionToken = input ('Enter your session Token/SSOID :')
    print ('Thanks for the input provided')
else:
    appKey = sys.argv [1]
    sessionToken = sys.argv [2]

betfair = FBBetfair (appKey, sessionToken, 0, logger)
session_lifespan_in_hours = 7
while True:
    result = betfair.keep_session_alive()
    if result ['status'] == 'error':
        # producer.send (kafka_topic_error, result)
        logger.log(result)
    else:
        logger.log("Session renewed at " + str (datetime.datetime.now ()))
    logger.log("Next run at UTC: " + str (datetime.datetime.now () + datetime.timedelta (hours = session_lifespan_in_hours)))
    time.sleep (60 * 60 * session_lifespan_in_hours)
