const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const imagePreview = document.getElementById('image-preview');

// Open file manager when drop area is clicked
dropArea.addEventListener('click', () => {
    fileInput.click();
});

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false)
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false)
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false)
});

function highlight(e) {
    dropArea.classList.add('highlight')
}

function unhighlight(e) {
    dropArea.classList.remove('highlight')
}

dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;

    handleFiles(files);
}

fileInput.addEventListener('change', (event) => {
    handleFiles(event.target.files);
});

function handleFiles(files) {
    const file = files[0];
    if (!file) {
        alert('No file selected!');
        return;
    }
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file.');
        return;
    }

    const reader = new FileReader();

    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        imagePreview.style.display = 'block'; // Show the image
    };

    reader.readAsDataURL(file);
}

document.getElementById('convert-btn').addEventListener('click', () => {
    // Add your conversion logic here.
    alert("Conversion logic will be added here.");
});
