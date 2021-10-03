from importlib import import_module
import boto3
from moto import mock_dynamodb2
from unittest import mock
from botocore.exceptions import ClientError
import pytest


@mock_dynamodb2
def test_success(set_dynamodb_Count):
  # mock dynamodb
  table = set_dynamodb_Count()

  month = '202101'
  date = '20210101'
  from src.index import lambda_handler
  res = lambda_handler( month, date )

  item = table.get_item(Key={'hKey':month, 'rKey': date})
  assert res == 200
  assert item['Item']['clickCount'] == 1

@mock_dynamodb2
def test_count_up(set_dynamodb_Count):
  # mock dynamodb
  table = set_dynamodb_Count()
  month = '202101'
  date = '20210101'
  response = table.put_item(
    Item={
      'hKey' : month,
      'rKey' : date,
      'clickCount' : 2
    }
  )

  from src.index import lambda_handler
  res = lambda_handler(month, date)

  item = table.get_item(Key={'hKey':month, 'rKey':date })
  assert res == 200
  assert item['Item']['clickCount'] == 3

@mock_dynamodb2
def test_next_day(set_dynamodb_Count):
  # mock dynamodb
  table = set_dynamodb_Count()
  month = '202101'
  date = '20210101'
  _ = table.put_item(
    Item={
      'hKey' : month,
      'rKey' : month+'00',
      'clickCount' : 2
    }
  )
  _ = table.put_item(
    Item={
      'hKey' : month,
      'rKey' : date,
      'clickCount' : 2
    }
  )

  next_day = '20210102'
  from src.index import lambda_handler
  res = lambda_handler(month, next_day)

  item = table.get_item(Key={'hKey':month, 'rKey':date })
  item_next_day = table.get_item(Key={'hKey':month, 'rKey':next_day })
  item_month = table.get_item(Key={'hKey':month, 'rKey':month+'00'})
  assert res == 200
  assert item['Item']['clickCount'] == 2
  assert item_next_day['Item']['clickCount'] == 1
  assert item_month['Item']['clickCount'] == 3

@mock_dynamodb2
def test_next_month(set_dynamodb_Count):
  # mock dynamodb
  table = set_dynamodb_Count()
  month = '202101'
  date = '20210131'
  _ = table.put_item(
    Item={
      'hKey' : month,
      'rKey' : month+'00',
      'clickCount' : 2
    }
  )
  _ = table.put_item(
    Item={
      'hKey' : month,
      'rKey' : date,
      'clickCount' : 2
    }
  )

  next_month = '202102'
  next_day = '20210201'
  from src.index import lambda_handler
  res = lambda_handler(next_month, next_day)

  item = table.get_item(Key={'hKey':month, 'rKey':date })
  item_pre_month = table.get_item(Key={'hKey':month, 'rKey':month+'00'})
  item_next_month = table.get_item(Key={'hKey':next_month, 'rKey':next_month+'00' })
  item_next_day = table.get_item(Key={'hKey':next_month, 'rKey':next_day})
  assert res == 200
  assert item['Item']['clickCount'] == 2
  assert item_pre_month['Item']['clickCount'] == 2
  assert item_next_month['Item']['clickCount'] == 1
  assert item_next_day['Item']['clickCount'] == 1


@mock_dynamodb2
@mock.patch('src.index.client')
def test_exception(mock_client, set_dynamodb_Count):
  # mock dynamodb
  table = set_dynamodb_Count()
  month = '202101'
  date = '20210101'
  response = table.put_item(
    Item={
      'hKey' : month,
      'rKey' : date,
      'clickCount' : 2
    }
  )
  mock_client.transact_write_items.side_effect = Exception()

  with pytest.raises(Exception) as e:
    from src.index import lambda_handler
    res = lambda_handler(month, date)
    item = table.get_item(Key={'hKey':month, 'rKey':date})
    assert item['Item']['clickCount'] == 2

