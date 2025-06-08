from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import boto3
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize boto3 Lambda client
lambda_client = boto3.client('lambda', region_name='eu-north-1')  

s3 = boto3.client('s3')
bucket_name = 'platform-eng-hdo4'
object_key = 'wiki_summaries.txt'
local_path = '/tmp/wiki_summaries.txt'  # /tmp is writable in Lambda/Flask

@app.route('/download')
def download_file():
    # Download from S3
    s3.download_file(bucket_name, object_key, local_path)
    return send_file(local_path, as_attachment=True, download_name='wiki_summaries.txt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    return "✅ User created (placeholder)"

@app.route('/csv_to_excel', methods=['POST'])
def csv_to_excel():
    file = request.files['csv_file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f"📁 File '{filename}' uploaded for CSV to Excel conversion"
    return "❌ No file selected"

#@app.route('/get_info', methods=['POST'])
#def get_info():
#    topic = request.form.get('topic')
#    return f"📖 Getting Wikipedia info for topic: {topic}"

@app.route('/get_info', methods=['POST'])
def get_info():
    print("Raw request data:", request.data)
    topic = request.form.get('topic')
    print(f"topic is {topic}") 
    # Invoke the Lambda function
    try:
        response = lambda_client.invoke(
            FunctionName='hello',
            InvocationType='RequestResponse',  # Use 'Event' for async
            Payload=json.dumps({'topic': topic})
        )
        print("Lambda Response:", response) 
        # Read the Lambda response
        payload = json.loads(response['Payload'].read().decode('utf-8'))
        return f"📖 Lambda response: {payload}"
    except Exception as e:
        return f"❌ Error invoking Lambda: {str(e)}"


@app.route('/backup', methods=['POST'])
def backup():
    file = request.files['backup_file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f"💾 Backup file '{filename}' uploaded"
    return "❌ No file selected"

@app.route('/new_project', methods=['POST'])
def new_project():
    name = request.form.get('project_name')
    return f"🚀 New project created: {name}"

@app.route('/send_whatsapp', methods=['POST'])
def send_whatsapp():
    return "📨 WhatsApp message sent (placeholder)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

