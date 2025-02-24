import cv2
import numpy as np

def enhance_sketch(image_path, output_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image.")
        return
    image = cv2.resize(image, (image.shape[1] * 2, image.shape[0] * 2))

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    smoothed_image = cv2.bilateralFilter(gray_image, 7, 50, 50)

    thresholded_image = cv2.adaptiveThreshold(
        smoothed_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 9, 2
    )
    inverted_image = cv2.bitwise_not(thresholded_image)
    kernel = np.ones((3, 3), np.uint8)
    cleaned_image = cv2.morphologyEx(inverted_image, cv2.MORPH_OPEN, kernel, iterations=1)
    cleaned_image = cv2.morphologyEx(cleaned_image, cv2.MORPH_CLOSE, kernel, iterations=1)

    # Stronger Denoising (Combined Gaussian and Median)
    cleaned_image = cv2.GaussianBlur(cleaned_image, (7, 7), 0)
    cleaned_image = cv2.medianBlur(cleaned_image, 7)

    sobel_x = cv2.Sobel(cleaned_image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(cleaned_image, cv2.CV_64F, 0, 1, ksize=3)
    edges = cv2.magnitude(sobel_x, sobel_y)
    edges = np.uint8(np.clip(edges, 0, 255))
    enhanced_edges = cv2.addWeighted(cleaned_image, 0.9, edges, 0.1, 0)

    thickening_kernel = np.ones((3, 3), np.uint8)
    thickened_image = cv2.dilate(enhanced_edges, thickening_kernel, iterations=3)

    kernel_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    final_image = cv2.filter2D(thickened_image, -1, kernel_sharpen)

    final_image = cv2.convertScaleAbs(final_image, alpha=1.1, beta=10)

    # Final Denoising (Stronger Median)
    final_image = cv2.medianBlur(final_image, 7)

    final_image = cv2.bitwise_not(final_image)

    cv2.imwrite(output_path, final_image)
    print(f"Enhanced digital sketch saved to {output_path}")

# Example usage
input_image_path = (f"C:\\Users\\Admin\\OneDrive\\Desktop\\INK-TO-PIXEL\\frontend\\img5.jpeg")
output_image_path = (f"C:\\Users\\Admin\\OneDrive\\Desktop\\INK-TO-PIXEL\\frontend\\digital-img4-smooth.png")
enhance_sketch(input_image_path, output_image_path)



# // bhai code 
# import cv2

# import numpy as np



# def enhance_sketch(image_path, output_path):

#    

#     # Load the image

#     image = cv2.imread(image_path)

#     if image is None:

#         print("Error: Could not load image.")

#         return

#     image = cv2.resize(image, (image.shape[1] * 2, image.shape[0] * 2))  # Double the resolution



#    

#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)



#    

#     smoothed_image = cv2.bilateralFilter(gray_image, 9, 75, 75)



#    

#     thresholded_image = cv2.adaptiveThreshold(

#         smoothed_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,

#         cv2.THRESH_BINARY, 11, 2

#     )



#    

#     inverted_image = cv2.bitwise_not(thresholded_image)



#     kernel = np.ones((3, 3), np.uint8)  # Kernel for morphological operations

#     cleaned_image = cv2.morphologyEx(inverted_image, cv2.MORPH_OPEN, kernel, iterations=2)  # Remove small dots

#     cleaned_image = cv2.morphologyEx(cleaned_image, cv2.MORPH_CLOSE, kernel, iterations=2)  # Close gaps in lines



#    

#     cleaned_image = cv2.medianBlur(cleaned_image, 13)



#    

#     sobel_x = cv2.Sobel(cleaned_image, cv2.CV_64F, 1, 0, ksize=3)

#     sobel_y = cv2.Sobel(cleaned_image, cv2.CV_64F, 0, 1, ksize=3)

#     edges = cv2.magnitude(sobel_x, sobel_y)

#     edges = np.uint8(np.clip(edges, 0, 255))



#    

#     enhanced_edges = cv2.addWeighted(cleaned_image, 0.8, edges, 0.2, 0)



#    

#     thickening_kernel = np.ones((3, 3), np.uint8)

#     thickened_image = cv2.dilate(enhanced_edges, thickening_kernel, iterations=4)



#  kernel_sharpen = np.array([[0, -1, 0], [-1, 6, -1], [0, -1, 0]])

#     final_image = cv2.filter2D(thickened_image, -1, kernel_sharpen)



#     final_image = cv2.bitwise_not(final_image)



#     cv2.imwrite(output_path, final_image)

#     print(f"Enhanced digital sketch saved to {output_path}")



# # Example usage

# input_image_path = (f"C:\\Users\\Admin\\OneDrive\\Desktop\\INK-TO-PIXEL\\frontend\\img4.jpeg") # Replace with your input image path

# output_image_path =(f"C:\\Users\\Admin\\OneDrive\\Desktop\\INK-TO-PIXEL\\frontend\\digital-img4.png")  # Replace with your desired output path

# enhance_sketch(input_image_path, output_image_path)







