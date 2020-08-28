import json
import botocore
import boto3

SUPPORTED_LANGUAGES = [
    'ar', 'zh', 'fr', 'de', 'it',
    'ja', 'ko', 'es', 'es-MX', 'en'
]


def main(event, context):

    translate_client = boto3.client('translate')
    status = 200
    body = json.loads(event['body'])
    try:
        if body is not None and 'text' in body:
            message = body['text']
            if body.get('lang', '') in SUPPORTED_LANGUAGES:
                language = body['lang']
            else:
                language = 'en'
            # Assumes the source language is ES
            translate_response = translate_client.translate_text(
                Text=message,
                SourceLanguageCode='es',
                TargetLanguageCode=language
            )
            response = translate_response['TranslatedText']
        else:
            print('No message was passed')
            response = 'No message was passed to translate'
    except botocore.exceptions.ClientError as e:
        print(f'Problem translating text: {e}')
        response = str(e)
        status = 502

    response = {
        "statusCode": status,
        "body": json.dumps(response)
    }

    return response
