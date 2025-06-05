from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

@app.route('/get_info', methods=['POST'])
def get_info():
    topic = request.form.get('topic')
    return f"📖 Getting Wikipedia info for topic: {topic}"

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

