import pytest
import boto3

@pytest.fixture
def set_dynamodb_Count():
  def definition():
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
    dynamodb.create_table(
      TableName='ClickCount',
      KeySchema=[
          {
              'AttributeName': 'hKey',
              'KeyType': 'HASH'
          },
          {
              'AttributeName': 'rKey',
              'KeyType': 'RANGE'
          }
      ],
      AttributeDefinitions=[
          {
              'AttributeName': 'hKey',
              'AttributeType': 'S'
          },
          {
              'AttributeName': 'rKey',
              'AttributeType': 'S'
          }
      ],
    )

    return dynamodb.Table('ClickCount')
  return definition