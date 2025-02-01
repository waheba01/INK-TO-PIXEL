import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import VGG16
import tensorflow_hub as hub

# Load the CycleGAN pre-trained model
cycle_gan_url = "https://tfhub.dev/google/cyclegan/horse2zebra/1"
cycle_gan_model = hub.load(cycle_gan_url)

# Preprocess the image for CycleGAN
def preprocess_image_cyclegan(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    img = cv2.resize(img, (256, 256))  # Resize for CycleGAN model input
    img = (img / 127.5) - 1  # Normalize to [-1, 1]
    return np.expand_dims(img, axis=0)

# Process the image using CycleGAN
def process_with_cyclegan(input_path, output_path):
    img_array = preprocess_image_cyclegan(input_path)
    output_image = cycle_gan_model(img_array)
    output_image = output_image[0].numpy()  # Convert TensorFlow tensor to NumPy array
    output_image = (output_image + 1) * 127.5  # Revert normalization
    output_image = np.clip(output_image, 0, 255).astype(np.uint8)  # Ensure valid pixel values
    output_image = cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)  # Convert back to BGR for saving
    cv2.imwrite(output_path, output_image)
    print(f"CycleGAN processed image saved at: {output_path}")

# Load the VGG16 model pre-trained on ImageNet
vgg16_model = VGG16(weights='imagenet')

# Display VGG16 model summary (optional)
# vgg16_model.summary()

# Process and enhance the input image
def process_image(input_path, output_path):
    # Step 1: Load the hand-drawn image
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: Unable to load the image.")
        return

    # Step 2: Invert the image to focus on lines (white on black)
    inverted_img = cv2.bitwise_not(img)

    # Step 3: Apply adaptive thresholding for line extraction
    binary_img = cv2.adaptiveThreshold(
        inverted_img, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 
        11, 2
    )

    # Step 4: Apply Gaussian Blur for line smoothing
    smoothed_img = cv2.GaussianBlur(binary_img, (5, 5), 0)

    # Step 5: Perform edge detection using Canny
    edges = cv2.Canny(smoothed_img, 50, 150)

    # Step 6: Invert edges back to white background for a digital look
    digital_img = cv2.bitwise_not(edges)

    # Step 7: Save and display the output
    cv2.imwrite(output_path, digital_img)
    print(f"Processed image (edges) saved at: {output_path}")

    # Optional: Display the images
    cv2.imshow("Original Image", img)
    cv2.imshow("Processed Image", digital_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Input and output paths
input_image_path = "C:\\Users\\Admin\\OneDrive\\Desktop\\INK-TO-PIXEL\\img pro\\inputimages\\3.jpg"  # Path to input image
output_image_path_edges = "C:\\Users\\Admin\\OneDrive\\Desktop\\INK-TO-PIXEL\\img pro\\output_images\\digital_output_edges_3.jpg"
output_image_path_cyclegan = "C:\\Users\\Admin\\OneDrive\\Desktop\\INK-TO-PIXEL\\img pro\\output_images\\digital_output_cyclegan_3.jpg"

# Process the image with edges detection
process_image(input_image_path, output_image_path_edges)

# Process the image with CycleGAN
process_with_cyclegan(input_image_path, output_image_path_cyclegan)
