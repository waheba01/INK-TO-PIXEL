
// document.addEventListener('DOMContentLoaded', () => {
//     const fileInput = document.getElementById('file-input');
//     const dropArea = document.getElementById('drop-area');
//     const imagePreview = document.getElementById('image-preview');
//     const uploadText = document.querySelector('#drop-area p');
//     const convertedImage = document.getElementById('converted-image');

//     // Image Preview
//     fileInput.addEventListener('change', (event) => {
//         const file = event.target.files[0];
//         if (file) {
//             const reader = new FileReader();
//             reader.onload = (e) => {
//                 imagePreview.src = e.target.result;
//                 imagePreview.style.display = 'block';
//                 uploadText.style.display = 'none';
//             };
//             reader.readAsDataURL(file);
//         } else {
//             imagePreview.src = '';
//             imagePreview.style.display = 'none';
//             uploadText.style.display = 'block';
//         }
//     });

//     // Drag and Drop
//     ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
//         dropArea.addEventListener(eventName, preventDefaults, false);
//     });

//     function preventDefaults(e) {
//         e.preventDefault();
//         e.stopPropagation();
//     }

//     ['dragenter', 'dragover'].forEach(eventName => {
//         dropArea.addEventListener(eventName, highlight, false);
//     });

//     ['dragleave', 'drop'].forEach(eventName => {
//         dropArea.addEventListener(eventName, unhighlight, false);
//     });

//     function highlight() {
//         dropArea.classList.add('highlight');
//     }

//     function unhighlight() {
//         dropArea.classList.remove('highlight');
//     }

//     dropArea.addEventListener('drop', (e) => {
//         const dt = e.dataTransfer;
//         fileInput.files = dt.files;
//         fileInput.dispatchEvent(new Event('change'));
//     });

//     dropArea.addEventListener('click', () => {
//         fileInput.click();
//     });

//     let data; // Declare data outside the artistic-btn event listener

//     // Artistic Conversion
//     document.getElementById('artistic-btn').addEventListener('click', async () => {
//         const file = fileInput.files[0];

//         if (!file) {
//             alert('Please upload an image first!');
//             return;
//         }

//         let formData = new FormData();
//         formData.append('image', file);

//         try {
//             const response = await fetch('http://127.0.0.1:5000/convert', {
//                 method: 'POST',
//                 body: formData,
//             });

//             if (!response.ok) {
//                 throw new Error('Failed to convert image');
//             }

//             data = await response.json(); // Assign the response to the data variable
//             console.log('data:', data);
//             console.log('data.converted_image:', data.converted_image);

//             const imageUrl = 'http://127.0.0.1:5000' + data.converted_image;
//             console.log('imageUrl:', imageUrl);
//             convertedImage.src = imageUrl;

//             const img = new Image();
//             img.onload = () => {
//                 convertedImage.style.width = img.width + 'px';
//                 alert('Image converted successfully!');
//                 document.getElementById('processing-sec').style.display = 'none';
//                 document.getElementById('converted-sec').style.display = 'block';
//                 document.getElementById('converted-container').style.display = 'block';
//             };
//             img.src = URL.createObjectURL(file);

//             // Edit Button Click
//             document.getElementById('edit-btn').addEventListener('click', () => {
//                 console.log("Edit button clicked!");
//                 try {
//                     window.open('C:\Users\Admin\OneDrive\Desktop\INK-TO-PIXEL\CanvasPaint\public\index.html', '_blank');
//                     let convertedFilename = data.converted_image.split('/').pop();
//                     console.log("convertedFilename:", convertedFilename);

//                     fetch('/edit-image', {
//                         method: 'POST',
//                         headers: {
//                             'Content-Type': 'application/json',
//                         },
//                         body: JSON.stringify({ filename: convertedFilename }),
//                     })
//                     .then(response => {
//                         if (response.ok) {
//                             console.log('Edit request sent successfully.');
//                         } else {
//                             console.error('Error sending edit request:', response.status);
//                         }
//                     })
//                     .catch(error => {
//                         console.error('Fetch Error:', error);
//                     });
//                 } catch (error) {
//                     console.error("Edit button error:", error);
//                 }
//             });

//         } catch (error) {
//             console.error('Error:', error);
//             alert('Error processing image');
//         }
//     });

//     // Download Image
//     window.downloadImage = () => {
//         const imageSrc = convertedImage.src;

//         if (!imageSrc) {
//             alert('No image available to download!');
//             return;
//         }

//         const link = document.createElement('a');
//         link.href = imageSrc;
//         link.download = 'Converted_Image.jpg';
//         link.click();
//     };
// });

// inktopixel/frontend/script.js
document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const dropArea = document.getElementById('drop-area');
    const imagePreview = document.getElementById('image-preview');
    const uploadText = document.querySelector('#drop-area p');
    const convertedImage = document.getElementById('converted-image');

    // Image Preview
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
                uploadText.style.display = 'none';
            };
            reader.readAsDataURL(file);
        } else {
            imagePreview.src = '';
            imagePreview.style.display = 'none';
            uploadText.style.display = 'block';
        }
    });

    // Drag and Drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.classList.add('highlight');
    }

    function unhighlight() {
        dropArea.classList.remove('highlight');
    }

    dropArea.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        fileInput.files = dt.files;
        fileInput.dispatchEvent(new Event('change'));
    });

    dropArea.addEventListener('click', () => {
        fileInput.click();
    });

    let data;

    document.getElementById('artistic-btn').addEventListener('click', async () => {
        const file = fileInput.files[0];

        if (!file) {
            alert('Please upload an image first!');
            return;
        }

        let formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('http://127.0.0.1:5000/convert', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Failed to convert image');
            }

            data = await response.json();
            console.log('data:', data);
            console.log('data.converted_image:', data.converted_image);

            const imageUrl = 'http://127.0.0.1:5000' + data.converted_image;
            console.log('imageUrl:', imageUrl);
            convertedImage.src = imageUrl;

            const img = new Image();
            img.onload = () => {
                convertedImage.style.width = img.width + 'px';
                alert('Image converted successfully!');
                document.getElementById('processing-sec').style.display = 'none';
                document.getElementById('converted-sec').style.display = 'block';
                document.getElementById('converted-container').style.display = 'block';
            };
            img.src = URL.createObjectURL(file);

            document.getElementById('edit-btn').addEventListener('click', () => {
                console.log("Edit button clicked!");
                try {
                    // Construct the full URL to the CanvasPaint application
                    const canvasPaintUrl = 'C:/Users/Admin/OneDrive/Desktop/INK-TO-PIXEL/CanvasPaint/public/index.html'; // Local path (adjust for deployment)
    
                    const canvasPaintWindow = window.open(canvasPaintUrl, '_blank');
    
                    if (canvasPaintWindow) {
                        const imageUrl = 'http://127.0.0.1:5000' + data.converted_image;
    
                        canvasPaintWindow.onload = () => {
                            // Send the converted image URL to CanvasPaint
                            canvasPaintWindow.postMessage({ imageUrl: imageUrl }, '*');
                        };
                    } else {
                        alert("Could not open the CanvasPaint application.");
                    }
    
                } catch (error) {
                    console.error("Edit button error:", error);
                    alert("An error occurred while opening the editor.");
                }
            });

        } catch (error) {
            console.error('Error:', error);
            alert('Error processing image');
        }
    });

    window.downloadImage = () => {
        const imageSrc = convertedImage.src;

        if (!imageSrc) {
            alert('No image available to download!');
            return;
        }

        const link = document.createElement('a');
        link.href = imageSrc;
        link.download = 'Converted_Image.jpg';
        link.click();
    };
});