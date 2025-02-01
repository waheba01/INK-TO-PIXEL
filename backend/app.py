from flask import Flask, request, jsonify
import subprocess  # For running the Python script

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_image():
    try:
        # Run the specific Python script (e.g., demo1.py) that processes the image
        subprocess.run(['python', 'demo1.py'], check=True)
        
        # Here you can add any logic to return the result (like a path to the output image)
        return jsonify({'status': 'success', 'message': 'Image converted successfully', 'output_image': 'path/to/output_image.png'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
