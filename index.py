import json
import datetime
from lib.win007.main import Main


def handler(event, context):
    data = {
        'output': 'Hello World',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    executor = Main()
    executor.execute()
    print('test')

    # return {'statusCode': 200,
    #         'body': json.dumps(data),
    #         'headers': {'Content-Type': 'application/json'}}
