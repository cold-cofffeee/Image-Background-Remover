// Premium Background Remover - Main JavaScript

let currentFiles = [];
let currentProcessedUrl = '';
let currentOriginalFile = '';

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const processingIndicator = document.getElementById('processingIndicator');
const resultsSection = document.getElementById('resultsSection');
const progressFill = document.getElementById('progressFill');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeUpload();
    checkModelHealth();
});

// Initialize upload functionality
function initializeUpload() {
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // Custom color picker
    const colorPicker = document.getElementById('customColorPicker');
    if (colorPicker) {
        colorPicker.addEventListener('change', (e) => {
            changeBackground(e.target.value);
        });
    }
}

// Handle drag over
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.add('drag-over');
}

// Handle drag leave
function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('drag-over');
}

// Handle drop
function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFiles(files);
    }
}

// Handle file select
function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFiles(files);
    }
}

// Handle files
async function handleFiles(files) {
    currentFiles = Array.from(files);
    
    if (currentFiles.length === 1) {
        await processSingleImage(currentFiles[0]);
    } else if (currentFiles.length > 1) {
        await processBatchImages(currentFiles);
    }
}

// Process single image
async function processSingleImage(file) {
    try {
        // Show processing indicator
        uploadArea.style.display = 'none';
        processingIndicator.style.display = 'block';
        resultsSection.style.display = 'none';
        
        // Simulate progress
        animateProgress();
        
        // Create form data
        const formData = new FormData();
        formData.append('file', file);
        formData.append('background_color', 'transparent');
        formData.append('output_format', 'png');
        
        // Upload and process
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Upload failed');
        }
        
        const result = await response.json();
        
        if (result.success) {
            displayResults(result);
        } else {
            showError(result.error || 'Processing failed');
        }
        
    } catch (error) {
        showError(error.message);
    }
}

// Process batch images
async function processBatchImages(files) {
    try {
        uploadArea.style.display = 'none';
        processingIndicator.style.display = 'block';
        resultsSection.style.display = 'none';
        
        const formData = new FormData();
        files.forEach(file => {
            formData.append('files', file);
        });
        formData.append('background_color', 'transparent');
        formData.append('output_format', 'png');
        
        const response = await fetch('/api/batch-upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Batch upload failed');
        }
        
        const result = await response.json();
        
        if (result.success) {
            showNotification(`Processed ${result.processed} of ${result.total} images`);
            // Show first image result
            if (result.results.length > 0 && result.results[0].success) {
                displayResults(result.results[0]);
            }
        } else {
            showError(result.error || 'Batch processing failed');
        }
        
    } catch (error) {
        showError(error.message);
    }
}

// Display results
function displayResults(result) {
    processingIndicator.style.display = 'none';
    resultsSection.style.display = 'block';
    
    // Store current data
    currentProcessedUrl = result.processed_url;
    currentOriginalFile = result.original_filename;
    
    // Display images
    const originalImage = document.getElementById('originalImage');
    const processedImage = document.getElementById('processedImage');
    
    originalImage.src = result.original_url;
    processedImage.src = result.processed_url;
    
    // Display file info
    const originalInfo = document.getElementById('originalInfo');
    const processedInfo = document.getElementById('processedInfo');
    
    originalInfo.textContent = `Size: ${formatFileSize(result.original_size)}`;
    processedInfo.textContent = `Size: ${formatFileSize(result.processed_size)}`;
    
    // Reset background options
    resetBackgroundOptions();
}

// Animate progress
function animateProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) {
            clearInterval(interval);
            progress = 90;
        }
        progressFill.style.width = progress + '%';
    }, 200);
}

// Change background
async function changeBackground(color) {
    try {
        // Update active state
        document.querySelectorAll('.bg-option').forEach(opt => {
            opt.classList.remove('active');
        });
        event.target.closest('.bg-option')?.classList.add('active');
        
        // Re-process with new background
        const formData = new FormData();
        const response = await fetch(currentProcessedUrl);
        const blob = await response.blob();
        formData.append('file', blob);
        formData.append('background_color', color);
        formData.append('output_format', 'png');
        
        const uploadResponse = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await uploadResponse.json();
        
        if (result.success) {
            document.getElementById('processedImage').src = result.processed_url;
            currentProcessedUrl = result.processed_url;
            showNotification('Background changed successfully');
        }
        
    } catch (error) {
        console.error('Error changing background:', error);
        showError('Failed to change background');
    }
}

// Open color picker
function openColorPicker() {
    document.getElementById('customColorPicker').click();
}

// Reset background options
function resetBackgroundOptions() {
    document.querySelectorAll('.bg-option').forEach(opt => {
        opt.classList.remove('active');
    });
    document.querySelector('.bg-option[data-color="transparent"]')?.classList.add('active');
}

// Download image
function downloadImage(format = 'png') {
    if (!currentProcessedUrl) return;
    
    // Create download link
    const link = document.createElement('a');
    link.href = currentProcessedUrl;
    link.download = `processed_image_${Date.now()}.${format}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showNotification('Download started');
}

// Reset upload
function resetUpload() {
    uploadArea.style.display = 'block';
    processingIndicator.style.display = 'none';
    resultsSection.style.display = 'none';
    fileInput.value = '';
    currentFiles = [];
    currentProcessedUrl = '';
    currentOriginalFile = '';
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#2ecc71' : '#e74c3c'};
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Show error
function showError(message) {
    processingIndicator.style.display = 'none';
    uploadArea.style.display = 'block';
    showNotification(message, 'error');
}

// Copy API code
function copyCode() {
    const code = document.getElementById('apiCode').textContent;
    navigator.clipboard.writeText(code).then(() => {
        showNotification('Code copied to clipboard!');
    });
}

// Check model health
async function checkModelHealth() {
    try {
        const response = await fetch('/api/health');
        const health = await response.json();
        
        if (!health.model_loaded) {
            console.warn('Model not fully loaded');
        }
    } catch (error) {
        console.error('Health check failed:', error);
    }
}

// Add slide animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Handle window resize
window.addEventListener('resize', () => {
    // Adjust layout if needed
});

// Prevent default drag behavior on document
document.addEventListener('dragover', (e) => {
    e.preventDefault();
});

document.addEventListener('drop', (e) => {
    e.preventDefault();
});
