from botocore.config import Config
from sklearn.ensemble import RandomForestClassifier

import io
import json
import boto3
import joblib
import librosa
import numpy as np

s3_resource = boto3.resource("s3", region_name="ap-southeast-2", config=Config(signature_version='s3v4'))
s3_object = s3_resource.Object("chorisma-app", 'models/model-latest')

with io.BytesIO() as f:
    s3_object.download_fileobj(f)
    f.seek(0)
    latest_model = joblib.load(f)

def get_chromagram(file_obj):
    '''Extracts chromagram from time series audio signal'''
    raw_audio_ts, sr = librosa.load(file_obj)
    chromagram = np.array(librosa.feature.chroma_stft(y=raw_audio_ts, sr=sr, center=True), dtype=object)
    chromagram = np.mean(chromagram, axis=1)
    return chromagram

def lambda_handler(event, context):
    '''Lambda handler for chord recognition'''

    try:
        key = json.loads(event["body"])["resourceLocation"]
        s3_user_audio_obj = s3_resource.Object("chorisma-app", key)
        s3_user_audio_obj.download_file(f"/tmp/temp.wav")

        # Extract chromagram of recorded audio
        extracted_chromagram = get_chromagram(f"/tmp/temp.wav").reshape(1, -1)

        # Model Inference
        predicted_chord = latest_model.predict(extracted_chromagram)[0]
        
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*", 
                "Access-Control-Allow-Methods": "POST"
            },
            "body": json.dumps({
                "message": "Success",
                "chord": predicted_chord[0]
            }),
        }
        
    except Exception as error:
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*", 
                "Access-Control-Allow-Methods": "POST"
            },
            "body": json.dumps({
                "message": "Error!"
            }),
        }


