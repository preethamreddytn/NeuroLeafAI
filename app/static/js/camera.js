// Camera functionality
let stream = null;
const video = document.getElementById('camera-video');
const canvas = document.getElementById('camera-canvas');
const cameraModal = document.getElementById('camera-modal');
const cameraBtn = document.getElementById('camera-btn');
const captureBtn = document.getElementById('capture-photo-btn');
const cancelBtn = document.getElementById('cancel-camera-btn');
const closeBtn = document.querySelector('.close-camera');
const capturedImageInput = document.getElementById('captured-image');
const uploadForm = document.getElementById('upload-form');
const fileInput = document.getElementById('file-upload');
const selectionStatus = document.getElementById('selection-status');
const selectionCount = document.getElementById('selection-count');

// Maintain a DataTransfer to append captured images and keep multiple files
let dt = new DataTransfer();

// Show selection status
function showSelectionStatus() {
    selectionStatus.style.display = 'flex';
    updateSelectionCount();
}

// Hide selection status
function hideSelectionStatus() {
    selectionStatus.style.display = 'none';
    updateSelectionCount();
}

function updateSelectionCount() {
    const count = dt.files.length || 0;
    if (selectionCount) selectionCount.textContent = `${count} ${count === 1 ? 'item' : 'items'} selected`;
}

// File input change event
fileInput.addEventListener('change', (e) => {
    // Replace dt with files selected by user
    dt = new DataTransfer();
    for (const f of e.target.files) {
        dt.items.add(f);
    }
    // assign combined files back to input
    fileInput.files = dt.files;

    if (dt.files.length > 0) {
        showSelectionStatus();
    } else {
        hideSelectionStatus();
    }
});

// Open camera
cameraBtn.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'environment',
                width: { ideal: 1920 },
                height: { ideal: 1080 }
            } 
        });
        video.srcObject = stream;
        cameraModal.style.display = 'flex';
    } catch (error) {
        alert('Unable to access camera. Please make sure you have granted camera permissions.');
        console.error('Camera error:', error);
    }
});

// Close camera
function closeCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    cameraModal.style.display = 'none';
    video.srcObject = null;
}

closeBtn.addEventListener('click', closeCamera);
cancelBtn.addEventListener('click', closeCamera);

// Capture photo
captureBtn.addEventListener('click', () => {
    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw video frame to canvas
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert canvas to blob and create file
    canvas.toBlob((blob) => {
        const file = new File([blob], `captured-image-${Date.now()}.jpg`, { type: 'image/jpeg' });

        // Append to existing DataTransfer so multiple captures accumulate
        dt.items.add(file);

        // Assign updated files back to input
        fileInput.files = dt.files;

        // Show selection status
        showSelectionStatus();

        // Close camera
        closeCamera();
    }, 'image/jpeg', 0.95);
});

// Close modal when clicking outside
cameraModal.addEventListener('click', (e) => {
    if (e.target === cameraModal) {
        closeCamera();
    }
});

// ========== ERROR NOTIFICATION SYSTEM ==========
function showErrorNotification(message) {
    // Remove any existing error notifications
    removeErrorNotification();
    
    const errorDiv = document.createElement('div');
    errorDiv.id = 'error-notification';
    errorDiv.className = 'error-notification';
    errorDiv.innerHTML = `
        <div class="error-content">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <span>${message}</span>
        </div>
        <button type="button" class="close-error" onclick="removeErrorNotification()">&times;</button>
    `;
    document.body.appendChild(errorDiv);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        removeErrorNotification();
    }, 5000);
}

function removeErrorNotification() {
    const errorDiv = document.getElementById('error-notification');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// ========== FORM VALIDATION ==========
uploadForm.addEventListener('submit', function(e) {
    // Check if any files are selected
    if (!fileInput.files || fileInput.files.length === 0) {
        e.preventDefault();
        showErrorNotification('⚠️ Please select an image or take a photo before uploading.');
        return false;
    }
});

// Hide error notification when user selects files
fileInput.addEventListener('change', function() {
    removeErrorNotification();
});
