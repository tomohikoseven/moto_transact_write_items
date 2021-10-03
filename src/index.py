import boto3


client = boto3.client('dynamodb',  region_name='ap-northeast-1')
def lambda_handler( month:str, date:str ):
  try:
    response = client.transact_write_items(
      TransactItems=[
        {
          'Update' : {
            'Key' : {
              'hKey': { 'S': month },
              'rKey': { 'S': month + '00' }
            },
            'TableName':'ClickCount',
            'UpdateExpression': 'ADD clickCount :increment',
            'ExpressionAttributeValues' : {
              ':increment': { 'N': '1' }
            }
          }
        },
        {
          'Update' : {
            'Key' : {
              'hKey': { 'S': month },
              'rKey': { 'S': date }
            },
            'TableName':'ClickCount',
            'UpdateExpression': 'ADD clickCount :increment',
            'ExpressionAttributeValues' : {
              ':increment': { 'N': '1' }
            }
          }
        }
      ]
    )
  except Exception as e :
    print("===")
    print(e)
    raise e

  return 200