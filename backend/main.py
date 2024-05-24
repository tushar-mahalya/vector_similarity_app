from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import csv
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../backend/files'

CORS(app, origins=['http://localhost:8080/*'])

UPLOAD_FOLDER = '../backend/files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return 'No file uploaded', 400

#     file = request.files['file']
#     if file.filename == '':
#         return 'No file selected', 400
#     if file.filename is None:
#         return 'Filename is None', 400
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     if os.path.isfile(file_path):
#         return 'File already exists', 409 
#     file.save(file_path)

#     return 'File uploaded successfully', 200

@app.route('/files', methods=['GET'])
def get_files():
    if not os.path.exists(UPLOAD_FOLDER):
        return 'No files found', 404
    files = [f.name for f in os.scandir(UPLOAD_FOLDER) if f.is_file()]
    return jsonify(files)

@app.route('/files/<filename>', methods=['GET'])
def get_file_content(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.isfile(file_path):
        return 'File not found', 404
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        return str(e), 500
    
@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.isfile(file_path):
        return 'File not found', 404
    try:
        os.remove(file_path)
        return 'File deleted successfully', 200
    except Exception as e:
        return str(e), 500
    
def allowed_file(filename):
    # Add your logic to determine if the file is allowed or not
    # For example, you can check the file extension
    ALLOWED_EXTENSIONS = {'csv'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def csv_to_json(file_path):
    # Add your logic to convert the CSV file to JSON
    # For example, you can use the csv module to read the CSV file and convert it to a list of dictionaries
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        json_data = [dict(row) for row in reader]
    return json_data


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Convert the CSV file to JSON and return it
        csv_data = csv_to_json(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify(csv_data)
    else:
        return jsonify({'error': 'File not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)