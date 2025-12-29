// Premium Background Remover - Clean JavaScript

let currentFiles = [];
let currentProcessedUrl = '';
let currentOriginalFile = '';
let processingSteps = [
    'Analyzing subject…',
    'Refining edges…',
    'Finalizing output…'
];
let currentStep = 0;

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const processingIndicator = document.getElementById('processingIndicator');
const resultsSection = document.getElementById('resultsSection');
const progressFill = document.getElementById('progressFill');
const processingStatus = document.getElementById('processingStatus');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeUpload();
    checkModelHealth();
});

// Initialize upload functionality
function initializeUpload() {
    fileInput.addEventListener('change', handleFileSelect);
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => fileInput.click());
    
    const colorPicker = document.getElementById('customColorPicker');
    if (colorPicker) {
        colorPicker.addEventListener('change', (e) => {
            changeBackground(e.target.value);
        });
    }
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFiles(files);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFiles(files);
    }
}

async function handleFiles(files) {
    currentFiles = Array.from(files);
    
    if (currentFiles.length === 1) {
        await processSingleImage(currentFiles[0]);
    } else if (currentFiles.length > 1) {
        await processBatchImages(currentFiles);
    }
}

async function processSingleImage(file) {
    try {
        uploadArea.style.display = 'none';
        processingIndicator.style.display = 'block';
        resultsSection.style.display = 'none';
        
        animateProgress();
        
        const formData = new FormData();
        formData.append('file', file);
        formData.append('background_color', 'transparent');
        formData.append('output_format', 'png');
        
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

function displayResults(result) {
    processingIndicator.style.display = 'none';
    resultsSection.style.display = 'block';
    
    currentProcessedUrl = result.processed_url;
    currentOriginalFile = result.original_filename;
    
    const originalImage = document.getElementById('originalImage');
    const processedImage = document.getElementById('processedImage');
    
    originalImage.src = result.original_url;
    processedImage.src = result.processed_url;
    
    const originalInfo = document.getElementById('originalInfo');
    const processedInfo = document.getElementById('processedInfo');
    
    originalInfo.textContent = `${formatFileSize(result.original_size)}`;
    processedInfo.textContent = `${formatFileSize(result.processed_size)}`;
    
    resetBackgroundOptions();
}

function animateProgress() {
    let progress = 0;
    currentStep = 0;
    
    const interval = setInterval(() => {
        progress += Math.random() * 12;
        if (progress > 90) {
            clearInterval(interval);
            progress = 90;
        }
        progressFill.style.width = progress + '%';
        
        // Update status text
        if (progress > 30 && currentStep === 0) {
            currentStep = 1;
            processingStatus.textContent = processingSteps[1];
        } else if (progress > 60 && currentStep === 1) {
            currentStep = 2;
            processingStatus.textContent = processingSteps[2];
        }
    }, 200);
}

async function changeBackground(color) {
    try {
        document.querySelectorAll('.bg-option').forEach(opt => {
            opt.classList.remove('active');
        });
        event.target.closest('.bg-option')?.classList.add('active');
        
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
        }
        
    } catch (error) {
        console.error('Error changing background:', error);
    }
}

function openColorPicker() {
    document.getElementById('customColorPicker').click();
}

function resetBackgroundOptions() {
    document.querySelectorAll('.bg-option').forEach(opt => {
        opt.classList.remove('active');
    });
    document.querySelector('.bg-option[data-color="transparent"]')?.classList.add('active');
}

function downloadImage(format = 'png') {
    if (!currentProcessedUrl) return;
    
    const link = document.createElement('a');
    link.href = currentProcessedUrl;
    link.download = `processed_${Date.now()}.${format}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showNotification('Download started');
}

function resetUpload() {
    uploadArea.style.display = 'block';
    processingIndicator.style.display = 'none';
    resultsSection.style.display = 'none';
    fileInput.value = '';
    currentFiles = [];
    currentProcessedUrl = '';
    currentOriginalFile = '';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 10) / 10 + ' ' + sizes[i];
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.2s ease';
        setTimeout(() => notification.remove(), 200);
    }, 3000);
}

function showError(message) {
    processingIndicator.style.display = 'none';
    uploadArea.style.display = 'block';
    showNotification(message, 'error');
}

function copyCode() {
    const code = document.getElementById('apiCode').textContent;
    navigator.clipboard.writeText(code).then(() => {
        showNotification('Copied to clipboard');
    });
}

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

// Prevent default drag behavior
document.addEventListener('dragover', (e) => e.preventDefault());
document.addEventListener('drop', (e) => e.preventDefault());
