import cv2
import numpy as np
import os

def demo(input_path, output_path):
    try:
        # Load the image
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print("Error: Unable to load the image.")
            return

        # Invert image
        inverted_img = cv2.bitwise_not(img)

        # Adaptive thresholding
        binary_img = cv2.adaptiveThreshold(
            inverted_img, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 15, 10
        )

        # Median blur for noise removal
        noise_removed = cv2.medianBlur(binary_img, 5)

        # Morphological closing
        kernel = np.ones((3, 3), np.uint8)
        morphed_img = cv2.morphologyEx(noise_removed, cv2.MORPH_CLOSE, kernel)

        # Edge detection
        edges = cv2.Canny(morphed_img, 30, 200)
        edges = cv2.dilate(edges, kernel, iterations=1)

        # Contour filtering
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]

        # Draw contours
        final_img = np.zeros_like(edges)
        cv2.drawContours(final_img, filtered_contours, -1, (255, 255, 255), thickness=cv2.FILLED)

        # Invert for digital look
        digital_img = cv2.bitwise_not(final_img)

        # Save and display
        cv2.imwrite(output_path, digital_img)
        print(f"Processed image saved at: {output_path}")
        cv2.imshow("Original Image", img)
        cv2.imshow("Processed Image", digital_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"An error occurred: {e}")

# Input and output paths
input_image_path = "C:\\Users\\Admin\\OneDrive\\Desktop\\INK-TO-PIXEL\\img pro\\input_images\\1.jpg"
output_image_path = "C:\\Users\\Admin\\OneDrive\\Desktop\\INK-TO-PIXEL\\img pro\\output_images\\digital_output_1.jpg"

# Check if input file exists
if os.path.exists(input_image_path):
    demo(input_image_path, output_image_path)
else:
    print(f"Error: Input file does not exist at {input_image_path}")