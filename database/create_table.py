from __future__ import print_function
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2') # remote
#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000") # local

table = dynamodb.create_table(
    TableName='SingleMatch',
    KeySchema=[
        {
            'AttributeName': 'LeagueId',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'GameId',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'LeagueId',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'GameId',
            'AttributeType': 'N'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 100,
        'WriteCapacityUnits': 100
    }
)

print("Table status:", table.table_status)
