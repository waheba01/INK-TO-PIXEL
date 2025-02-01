import cv2
import pytesseract
from PIL import Image, ImageDraw

# Load the image
image_path = 'flow1.jpg'  # Path to your hand-drawn flowchart image
image = cv2.imread(image_path)

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use thresholding to get a binary image
_, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

# Use OCR to extract text
custom_config = r'--oem 3 --psm 6'
text_data = pytesseract.image_to_string(binary_image, config=custom_config)

# Print extracted text
print("Extracted Text:")
print(text_data)

# Draw a new flowchart (this is a placeholder, modify as needed)
def draw_flowchart(text_data, output_file):
    # Create a new blank image
    flowchart_image = Image.new('RGB', (800, 600), 'white')
    draw = ImageDraw.Draw(flowchart_image)

    # Example: storing text lines for drawing; modify based on flowchart structures
    lines = text_data.strip().split('\n')
    y_offset = 50

    # Drawing boxes for text
    for line in lines:
        if line.strip():
            draw.rectangle([50, y_offset, 750, y_offset + 40], outline='black', fill='lightgrey')
            draw.text((60, y_offset + 10), line, fill='black')
            y_offset += 60  # Move down for the next line

    flowchart_image.save(output_file)

# Save the newly created flowchart
draw_flowchart(text_data, 'digital_output_flow1.png')

print("Digital flowchart has been saved as 'digital_flowchart.png'.")