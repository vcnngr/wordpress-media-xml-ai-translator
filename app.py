from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import tempfile
import uuid
from werkzeug.utils import secure_filename
from xml_translator import XMLTranslator

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

UPLOAD_FOLDER = '/tmp/uploads'
OUTPUT_FOLDER = '/tmp/outputs'
ALLOWED_EXTENSIONS = {'xml'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_file():
    try:
        # Check if all required fields are present
        if 'api_key' not in request.form or not request.form['api_key']:
            flash('API Key is required')
            return redirect(url_for('index'))
        
        if 'language' not in request.form or not request.form['language']:
            flash('Target language is required')
            return redirect(url_for('index'))
        
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            flash('Only XML files are allowed')
            return redirect(url_for('index'))
        
        # Save uploaded file
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)
        
        # Prepare output file
        output_filename = f"translated_{filename}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        # Initialize translator and process file
        api_key = request.form['api_key']
        target_language = request.form['language']
        
        translator = XMLTranslator(api_key)
        translator.translate_xml_file(input_path, output_path, target_language)
        
        # Clean up input file
        os.remove(input_path)
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=f"translated_{file.filename}",
            mimetype='application/xml'
        )
        
    except Exception as e:
        flash(f'Error processing file: {str(e)}')
        return redirect(url_for('index'))

@app.route('/cleanup/<filename>')
def cleanup(filename):
    """Clean up output files after download"""
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    except:
        pass
    return '', 204

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
