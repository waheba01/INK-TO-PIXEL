// document.getElementById('convert-btn').addEventListener('click', async () => {
//     const fileInput = document.getElementById('file-input');
//     const file = fileInput.files[0];

//     if (!file) {
//         alert("Please upload an image first!");
//         return;
//     }

//     let formData = new FormData();
//     formData.append("image", file);

//     try {
//         let response = await fetch("http://127.0.0.1:5000/convert", {
//             method: "POST",
//             body: formData
//         });

//         if (!response.ok) {
//             throw new Error("Failed to convert image");
//         }

//         let data = await response.json();
//         document.getElementById("converted-image").src = data.converted_image;

//     } catch (error) {
//         console.error("Error:", error);
//         alert("An error occurred. Please try again.");
//     }
// });

document.getElementById("file-input").addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById("image-preview").src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

// document.getElementById("convert-btn").addEventListener("click", function () {
//     const fileInput = document.getElementById("file-input");
//     if (fileInput.files.length === 0) {
//         alert("Please select an image first.");
//         return;
//     }

//     const formData = new FormData();
//     formData.append("file", fileInput.files[0]);

//     fetch("/upload", {
//         method: "POST",
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.converted_image) {
//             document.getElementById("converted-image").src = data.converted_image;
//         } else {
//             alert("Error: " + data.error);
//         }
//     })
//     .catch(error => console.error("Error:", error));
// });



document.getElementById("convert-btn").addEventListener("click", async () => {
    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload an image first!");
        return;
    }

    let formData = new FormData();
    formData.append("image", file);

    try {
        let response = await fetch("http://127.0.0.1:5000/convert", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Failed to convert image");
        }

        let data = await response.json();
        let convertedImage = document.getElementById("converted-image");

        // Set the source of the converted image
        convertedImage.src = "http://127.0.0.1:5000" + data.converted_image;
        
        // Make the converted image section visible
        document.getElementById("converted-sec").style.display = "block";

    } catch (error) {
        console.error("Error:", error);
        alert("Error processing image");
    }
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