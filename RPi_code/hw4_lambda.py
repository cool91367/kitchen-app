import json
import boto3


def detect_faces(photo, bucket):

    client=boto3.client('rekognition')

    response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':photo}},Attributes=['ALL'])

    print('Detected faces for ' + photo)
    return len(response['FaceDetails'])
    
    
def lambda_handler(event, context):
    # TODO implement
    client_iot = boto3.client('iot-data')
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        tmpkey = key.replace('/', '')
        print(tmpkey)
    
    face = detect_faces(tmpkey, bucket)
    if face > 0:
        payload_json = json.dumps({'state': { 'desired': { 'light': 1 }}})
    else:
        payload_json = json.dumps({'state': { 'desired': { 'light': 0 }}})
    response = client_iot.update_thing_shadow(
        thingName = "hw4", 
        payload =  payload_json
        )
    
    
    print(response)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
