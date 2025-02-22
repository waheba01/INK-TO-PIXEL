document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file-input");
    const imagePreview = document.getElementById("image-preview");
    const convertedImage = document.getElementById("converted-image");
    const convertBtn = document.getElementById("convert-btn");
    const dropArea = document.getElementById("drop-area");
    const convertedSec = document.getElementById("converted-sec");

    // File selection preview
    fileInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                imagePreview.src = e.target.result;
                imagePreview.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    });

    // Convert button logic
    convertBtn.addEventListener("click", function () {
        if (fileInput.files.length === 0) {
            alert("Please select an image first.");
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.converted_image) {
                convertedImage.src = data.converted_image;
                convertedSec.style.display = "block";
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => console.error("Error:", error));
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

                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const data = imageData.data;

                const kernel = [1, 2, 1, 2, 4, 2, 1, 2, 1];
                const kernelSum = kernel.reduce((a, b) => a + b, 0);
                const width = canvas.width;
                const height = canvas.height;
                const newImageData = ctx.createImageData(width, height);
                const newData = newImageData.data;

                for (let y = 1; y < height - 1; y++) {
                    for (let x = 1; x < width - 1; x++) {
                        for (let c = 0; c < 3; c++) {
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
                            newData[idx] = sum / kernelSum;
                        }
                        newData[(y * width + x) * 4 + 3] = 255;
                    }
                }

                ctx.putImageData(newImageData, 0, 0);
                resolve(canvas.toDataURL());
            } catch (error) {
                reject(error);
            }
        });
    }

    // Download image
    function downloadImage() {
        const imageSrc = imagePreview.src;
        if (!imageSrc) {
            alert("No image available to download!");
            return;
        }
        const link = document.createElement("a");
        link.href = imageSrc;
        link.download = "Image.jpg";
        link.click();
    }

    // Drag and drop functionality
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function highlight() {
        dropArea.classList.add("highlight");
    }

    function unhighlight() {
        dropArea.classList.remove("highlight");
    }

    ["dragenter", "dragover"].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ["dragleave", "drop"].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    dropArea.addEventListener("drop", (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    });

    dropArea.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", (e) => handleFiles(e.target.files));

    function handleFiles(files) {
        if (files.length === 0) {
            alert("No file selected!");
            return;
        }
        
        const file = files[0];
        if (!file.type.startsWith("image/")) {
            alert("Please select an image file.");
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});
