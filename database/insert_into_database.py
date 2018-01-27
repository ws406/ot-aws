from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table = dynamodb.Table('SingleMatch')

with open("moviedata.json") as json_file:
    matches = json.load(json_file, parse_float = decimal.Decimal)
    for match in matches:
        leagueId = int(match['LeagueId'])
        gameId = match['GameId']
        info = match['Info']

        print("Adding match:", leagueId, gameId)

        table.put_item(
           Item={
               'LeagueId': leagueId,
               'GameId': gameId,
               'info': info,
            }
        )
