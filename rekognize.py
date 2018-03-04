def upload_image(image_file, filename):    
    import boto3
    from botocore.client import Config

    ACCESS_KEY_ID = 'AKIAJCQD7IY3XXCKDVGQ'
    ACCESS_SECRET_KEY = '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'
    BUCKET_NAME = 'myrecoknitionimages'

    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3')
    )
    s3.Bucket(BUCKET_NAME).put_object(Key=filename, Body=image_file)

def text_read(filename):
    '''
    input the name of the file in the 
    S3 bucket that you want to analyze
    output: list of strings of the recognized words/numbers
    '''
    import requests
    import boto3
    import json
    from PIL import Image
    
    
    fileName=filename
    bucket='myrecoknitionimages'
    
    client=boto3.client('rekognition','us-east-1')

    response = client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':fileName}})

    #print json.dumps(response)
    print('Detected Text for ' + fileName)   
    
    #print json.dumps(response)
    
    data = []
    
    for label in response['TextDetections']:
        #print (label['DetectedText'] + ' : ' + str(label['Confidence']))
        output = str(label['DetectedText'])
        output = output.split()
    
        for item in output:
            if len(item) > 1 and item not in data:
                data.append(item)
            
                
    return data

def csv_write(data):
    import csv
    
    RESULTS = [data]
    
    with open("output.csv",'wb') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerows(RESULTS)

def analyze(image_file, filename):
    upload_image(image_file, filename)
    return text_read(filename)

    
    