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

        # Step 2: Apply Gaussian Blur to reduce noise before processing
        blurred_img = cv2.GaussianBlur(img, (7, 7), 0)

        # Step 3: Use adaptive thresholding for better binarization
        binary_img = cv2.adaptiveThreshold(
            blurred_img, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            block_size, c_constant
        )

        # Step 4: Use morphological operations to refine edges
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        morphed_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

        # Step 5: Apply edge detection using Canny
        edges = cv2.Canny(morphed_img, canny_threshold1, canny_threshold2)

        # Step 6: Remove small artifacts and noise
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        clean_img = np.zeros_like(edges)  # Start with a blank canvas
        for contour in contours:
            if cv2.contourArea(contour) > 50:  # Keep only significant contours
                cv2.drawContours(clean_img, [contour], -1, 255, thickness=1)

        # Step 7: Invert edges back to white background for a digital look
        digital_img = cv2.bitwise_not(clean_img)

        # Step 8: Save and display the output
        cv2.imwrite(output_path, digital_img)
        print(f"Processed image saved at: {output_path}")

        # Optional: Display the images
        cv2.imshow("Original Image", img)
        cv2.imshow("Processed Image", digital_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"An error occurred: {e}")

# Input and output paths
input_image_path = "C:\\Users\\Admin\\OneDrive\\Desktop\\INK-TO-PIXEL\\img pro\\input_images\\3.jpg"
output_image_path = "C:\\Users\\Admin\\OneDrive\\Desktop\\INK-TO-PIXEL\\img pro\\output_images\\digital_output_3.jpg"

# Check if input file exists
if not os.path.exists(input_image_path):
    print(f"Error: Input file does not exist at {input_image_path}")
else:
    # Process the image
    process_image(input_image_path, output_image_path)