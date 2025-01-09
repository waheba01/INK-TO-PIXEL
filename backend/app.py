from flask import Flask, request, send_file, make_response
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_image():
    if 'image' not in request.files:
        return "No image provided", 400

    image_file = request.files['image']
    format = request.form.get('format', 'jpg').lower() # Get the desired format

    try:
        img = Image.open(image_file.stream)

        if format == 'jpg':
            img_io = BytesIO()
            img.convert("RGB").save(img_io, 'JPEG', quality=85) # Convert to RGB for JPEG
            img_io.seek(0)
            return send_file(img_io, mimetype='image/jpeg', download_name='converted.jpg')
        elif format == 'png':
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            return send_file(img_io, mimetype='image/png', download_name='converted.png')
        elif format == 'pdf':
            img_io = BytesIO()
            c = canvas.Canvas(img_io, pagesize=letter)
            img_width, img_height = img.size
            c.drawImage(image_file, 50, 50, width=img_width/3, height=img_height/3) # Adjust size as needed
            c.save()
            img_io.seek(0)
            response = make_response(img_io.getvalue())
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=converted.pdf'
            return response
        else:
            return "Invalid format specified", 400

    except Exception as e:
        return f"Error during conversion: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)