import boto3
import wikipedia

s3 = boto3.client('s3')
bucket_name = 'platform-eng-hdo4'
object_key = 'wiki_summaries.txt'

def lambda_handler(event, context):
    topic = event.get('topic', 'Python (programming language)')
    print(f"Searching Wikipedia for: {topic}")
    
    try:
        summary = wikipedia.summary(topic, sentences=3)
        entry = f"\n\n{topic}:\n{summary}"

        # Download existing file content (if exists)
        try:
            response = s3.get_object(Bucket=bucket_name, Key=object_key)
            existing = response['Body'].read().decode('utf-8')
        except s3.exceptions.NoSuchKey:
            existing = ''
        
        # Append new content and upload back
        updated_content = existing + entry
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=updated_content.encode('utf-8'))

        return {
            'statusCode': 200,
            'body': f"Updated S3 object with summary for {topic}"
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }

