from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import cv2  # For image processing
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER

# Load models
artistic_model = load_model('models/line_smoothing_generator.h5')
geometric_model = load_model('models/shape_detector.h5')

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_image():
    file = request.files.get('file')
    conversion_type = request.form.get('conversionType')

    if not file:
        return jsonify({'success': False, 'error': 'No file uploaded'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Process the image
    img = cv2.imread(filepath)

    if conversion_type == 'artistic':
        processed_img = artistic_model.predict(np.expand_dims(img, axis=0))[0]
    elif conversion_type == 'geometric':
        processed_img = geometric_model.predict(np.expand_dims(img, axis=0))[0]
    else:
        return jsonify({'success': False, 'error': 'Invalid conversion type'})

    converted_path = os.path.join(app.config['CONVERTED_FOLDER'], f'converted_{filename}')
    cv2.imwrite(converted_path, processed_img)
    return jsonify({'success': True, 'path': converted_path})

@app.route('/download', methods=['GET'])
def download_image():
    file_path = os.path.join(app.config['CONVERTED_FOLDER'], 'converted_image.jpg')
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
