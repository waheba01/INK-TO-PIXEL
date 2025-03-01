# from flask import Flask, request, jsonify, send_file
# import cv2
# import numpy as np
# import os
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# OUTPUT_FOLDER = 'converted'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # Ensure output folder exists

# def enhance_sketch(image_path, output_path):
#     image = cv2.imread(image_path)
#     if image is None:
#         print("Error: Could not load image.")
#         return
#     image = cv2.resize(image, (image.shape[1] * 2, image.shape[0] * 2))  

#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     smoothed_image = cv2.bilateralFilter(gray_image, 9, 75, 75)
#     thresholded_image = cv2.adaptiveThreshold(
#         smoothed_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C_,
#         cv2.THRESH_BINARY, 11, 2
#     )

#     inverted_image = cv2.bitwise_not(thresholded_image)
#     kernel = np.ones((3, 3), np.uint8)
#     cleaned_image = cv2.morphologyEx(inverted_image, cv2.MORPH_OPEN, kernel, iterations=2)
#     cleaned_image = cv2.morphologyEx(cleaned_image, cv2.MORPH_CLOSE, kernel, iterations=2)
#     cleaned_image = cv2.medianBlur(cleaned_image, 13)

#     sobel_x = cv2.Sobel(cleaned_image, cv2.CV_64F, 1, 0, ksize=3)
#     sobel_y = cv2.Sobel(cleaned_image, cv2.CV_64F, 0, 1, ksize=3)
#     edges = cv2.magnitude(sobel_x, sobel_y)
#     edges = np.uint8(np.clip(edges, 0, 255))

#     enhanced_edges = cv2.addWeighted(cleaned_image, 0.8, edges, 0.2, 0)
#     thickening_kernel = np.ones((3, 3), np.uint8)
#     thickened_image = cv2.dilate(enhanced_edges, thickening_kernel, iterations=4)

#     kernel_sharpen = np.array([[0, -1, 0], [-1, 6, -1], [0, -1, 0]])
#     final_image = cv2.filter2D(thickened_image, -1, kernel_sharpen)
#     final_image = cv2.bitwise_not(final_image)

#     cv2.imwrite(output_path, final_image)
#     print(f"Enhanced digital sketch saved to {output_path}")

# @app.route('/upload', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     filename = secure_filename(file.filename)
#     input_path = os.path.join(UPLOAD_FOLDER, filename)
#     output_path = os.path.join(OUTPUT_FOLDER, f"enhanced_{filename}")

#     file.save(input_path)
#     enhance_sketch(input_path, output_path)

#     return jsonify({"converted_image": f"/get_image/enhanced_{filename}"})

# @app.route('/get_image/<filename>')
# def get_image(filename):
#     filepath = os.path.join(OUTPUT_FOLDER, filename)
#     if not os.path.exists(filepath):
#         return jsonify({"error": "File not found"}), 404
#     return send_file(filepath, mimetype='image/png')

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5001, debug=True)
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
from flask_cors import CORS
import subprocess

app = Flask(__name__, static_folder='frontend') #Added Static folder.
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def enhance_sketch(input_path, output_path):
    try:
        print(f"Input path: {input_path}")
        print(f"Output path: {output_path}")

        image = cv2.imread(input_path)
        if image is None:
            print(f"Error: Could not load image from {input_path}")
            return False

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        inverted = 255 - gray
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        final_image = cv2.divide(gray, 255 - blurred, scale=256)

        cv2.imwrite(output_path, final_image)
        print(f"Enhanced digital sketch saved to {output_path}")
        return True

    except Exception as e:
        print(f"Error processing image: {e}")
        return False

@app.route('/convert', methods=['POST'])
def convert():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(f"Uploaded filename: {filename}")

        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_filename = 'converted_' + filename
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        print(f"Input path: {input_path}")
        print(f"Output path: {output_path}")

        file.save(input_path)
        try:
            if enhance_sketch(input_path, output_path):
                output_path_relative = output_path.replace('\\', '/')
                image_url = 'http://127.0.0.1:5000/' + output_path_relative
                return jsonify({
                    'converted_image': '/' + output_path_relative,
                    'image_url': image_url
                })
            else:
                return jsonify({'error': 'Image processing failed'}), 500
        except Exception as e:
            print(f"Error during image enhancement: {e}")
            return jsonify({'error': 'Image enhancement failed'}), 500
        finally:
            if os.path.exists(input_path):
                os.remove(input_path)
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/outputs/<filename>')
def serve_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route('/edit-image', methods=['POST'])
def edit_image():
    filename = request.json.get('filename')
    if not filename:
        return jsonify({'error': 'Filename not provided'}), 400

    image_path = os.path.join(OUTPUT_FOLDER, filename)

    if os.name == 'nt':
        command = ['mspaint', image_path]
    elif os.name == 'posix':
        command = ['open', '-a', 'Preview', image_path]
    else:
        return jsonify({'error': 'Unsupported operating system'}), 500

    try:
        subprocess.Popen(command)
        return jsonify({'message': 'Image editor opened successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)