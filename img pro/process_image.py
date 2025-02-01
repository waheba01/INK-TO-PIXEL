import cv2
import numpy as np
import os

def process_image(input_path, output_path, block_size=11, c_constant=2, canny_threshold1=50, canny_threshold2=150):
    try:
        # Step 1: Load the hand-drawn image
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print("Error: Unable to load the image. Check the file path.")
            return

        # Step 2: Denoise the image using Median Blur
        denoised_img = cv2.medianBlur(img, 5)

        # Step 3: Adaptive Thresholding for better line segmentation
        binary_img = cv2.adaptiveThreshold(
            denoised_img, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            block_size, c_constant
        )

        # Step 4: Apply Morphological Operations (Opening for line cleaning)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        morph_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel, iterations=2)

        # Step 5: Perform Gaussian Blur for smooth edges
        blurred_img = cv2.GaussianBlur(morph_img, (5, 5), 0)

        # Step 6: Edge Detection using Canny
        edges = cv2.Canny(blurred_img, canny_threshold1, canny_threshold2)

        # Step 7: Resize for Anti-aliasing
        resized_img = cv2.resize(edges, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        smoothed_img = cv2.GaussianBlur(resized_img, (5, 5), 0)
        final_img = cv2.resize(smoothed_img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)

        # Step 8: Invert the image to digital look
        digital_img = cv2.bitwise_not(final_img)

        # Step 9: Save and display the output
        cv2.imwrite(output_path, digital_img)
        print(f"Processed image saved at: {output_path}")

        # Optional: Display the images
        cv2.imshow("Original Image", img)
        cv2.imshow("Smooth Output Image", digital_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"An error occurred: {e}")

# Input and output paths
input_image_path =  "C:\\Users\\Admin\\OneDrive\\Desktop\\INK-TO-PIXEL\\img pro\\input_images\\1.jpg"  # Replace with the path to your input image
output_image_path = "C:\\Users\\Admin\\OneDrive\\Desktop\\INK-TO-PIXEL\\img pro\\output_images\\digital_output_1.jpg"  # Output file path

# Check if input file exists
if not os.path.exists(input_image_path):
    print(f"Error: Input file does not exist at {input_image_path}")
else:
    # Process the image
    process_image(input_image_path, output_image_path)
