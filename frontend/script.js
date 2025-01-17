// Add event listener to the Convert button
document.getElementById('convert-btn').addEventListener('click', () => {
    // Get the selected conversion type
    const selectedType = document.querySelector('input[name="conversion-type"]:checked').value;

    // Get the image element from the processing section
    const imageElement = document.getElementById("image-preview");

    // Check if an image is uploaded
    if (!imageElement.src || imageElement.src === "") {
        alert("Please upload an image first!");
        return;
    }

    // Apply conversion based on the selected type
    if (selectedType === 'artistic') {
        applyArtisticConversion(imageElement)
            .then((processedImageSrc) => {
                // Display the processed image in the converted section
                const convertedImageElement = document.querySelector("#converted-sec #image-preview");
                convertedImageElement.src = processedImageSrc;
                convertedImageElement.style.display = "block"; // Ensure the image is visible

                // Hide processing section and show converted section
                document.getElementById('processing-sec').style.display = 'none';
                document.getElementById('converted-sec').style.display = 'block';

                // Alert the user about the successful conversion
                alert("Artistic conversion applied successfully!");
            })
            .catch((error) => {
                alert("An error occurred during artistic conversion: " + error.message);
            });
    } else if (selectedType === 'geometric') {
        alert("Geometric converter is not implemented yet."); // Placeholder for geometric conversion
    } else {
        alert("Invalid conversion type selected!");
    }
});

// Ensure converted-sec is hidden initially
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('converted-sec').style.display = 'none';
});

// Artistic conversion logic
function applyArtisticConversion(imageElement) {
    return new Promise((resolve, reject) => {
        try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');

            canvas.width = imageElement.naturalWidth;
            canvas.height = imageElement.naturalHeight;

            ctx.drawImage(imageElement, 0, 0);

            // Get the image data from the canvas
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const data = imageData.data;

            // Apply a Gaussian blur or custom smoothing algorithm
            const kernel = [1, 2, 1, 2, 4, 2, 1, 2, 1]; // Gaussian kernel (3x3 matrix)
            const kernelSum = kernel.reduce((a, b) => a + b, 0);

            const width = canvas.width;
            const height = canvas.height;
            const newImageData = ctx.createImageData(width, height);
            const newData = newImageData.data;

            for (let y = 1; y < height - 1; y++) {
                for (let x = 1; x < width - 1; x++) {
                    for (let c = 0; c < 3; c++) { // RGB channels
                        let sum = 0;

                        for (let ky = -1; ky <= 1; ky++) {
                            for (let kx = -1; kx <= 1; kx++) {
                                const px = x + kx;
                                const py = y + ky;
                                const idx = (py * width + px) * 4 + c;

                                const kernelValue = kernel[(ky + 1) * 3 + (kx + 1)];
                                sum += data[idx] * kernelValue;
                            }
                        }

                        const idx = (y * width + x) * 4 + c;
                        newData[idx] = sum / kernelSum; // Normalize by kernel sum
                    }
                    newData[(y * width + x) * 4 + 3] = 255; // Set alpha to 255
                }
            }

            // Update the canvas with the smoothed image data
            ctx.putImageData(newImageData, 0, 0);

            // Resolve the processed image as a data URL
            resolve(canvas.toDataURL());
        } catch (error) {
            reject(error);
        }
    });
}



function downloadImage() {
    // Get the image source from the img tag
    const imageElement = document.getElementById("image-preview");
    const imageSrc = imageElement.src;

    if (!imageSrc) {
        alert("No image available to download!");
        return;
    }

    // Create an anchor element and trigger the download
    const link = document.createElement("a");
    link.href = imageSrc;
    link.download = "Image.jpg"; // Set the download file name
    link.click();
}
// Select elements
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const imagePreview = document.getElementById('image-preview');

// Prevent default behavior for drag-and-drop events
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

// Highlight drop area on dragover
function highlight(e) {
    dropArea.classList.add('highlight');
}

function unhighlight(e) {
    dropArea.classList.remove('highlight');
}

['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

// Handle file drop
dropArea.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
});

// Handle file input click
dropArea.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

// Process uploaded files
function handleFiles(files) {
    if (files.length === 0) {
        alert('No file selected!');
        return;
    }
    
    const file = files[0];
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file.');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        imagePreview.style.display = 'block'; // Show the preview image
    };
    reader.readAsDataURL(file);
}