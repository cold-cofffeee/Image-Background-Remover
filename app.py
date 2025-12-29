"""
Premium Image Background Remover Web Application
A modern web app for removing image backgrounds using U2Net deep learning model
"""

from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import json
from pathlib import Path

# Import services with error handling
try:
    from services.background_remover import BackgroundRemoverService
    from services.image_processor import ImageProcessor
    MODEL_AVAILABLE = True
except Exception as e:
    print(f"\n⚠️  Warning: Could not load AI models")
    print(f"❌ Error: {e}")
    print(f"\n📋 To fix this, install Microsoft Visual C++ Redistributable:")
    print(f"📥 Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe\n")
    MODEL_AVAILABLE = False
    BackgroundRemoverService = None
    ImageProcessor = None

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROCESSED_FOLDER'] = 'static/processed'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp'}

# Ensure required directories exist
for folder in ['static/uploads', 'static/processed', 'static/temp']:
    Path(folder).mkdir(parents=True, exist_ok=True)

# Initialize services
if MODEL_AVAILABLE:
    bg_remover = BackgroundRemoverService()
    image_processor = ImageProcessor()
else:
    bg_remover = None
    image_processor = None
    print("⏳ App will start in UI-only mode. Install Visual C++ to enable AI features.\n")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(original_filename):
    """Generate unique filename with timestamp and UUID"""
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'png'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}.{ext}"

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and background removal"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, WEBP'}), 400
        
        # Save uploaded file
        filename = generate_unique_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get processing options
        options = {
            'background_color': request.form.get('background_color', 'transparent'),
            'background_image': request.form.get('background_image'),
            'output_format': request.form.get('output_format', 'png')
        }
        
        # Check if model is available
        if not MODEL_AVAILABLE or bg_remover is None:
            return jsonify({
                'error': 'AI model not available. Please install Microsoft Visual C++ Redistributable.',
                'download_url': 'https://aka.ms/vs/17/release/vc_redist.x64.exe'
            }), 503
        
        # Process image
        processed_filename = bg_remover.remove_background(filepath, options)
        
        # Get file info
        original_size = os.path.getsize(filepath)
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
        processed_size = os.path.getsize(processed_path)
        
        return jsonify({
            'success': True,
            'original_url': url_for('static', filename=f'uploads/{filename}'),
            'processed_url': url_for('static', filename=f'processed/{processed_filename}'),
            'original_filename': filename,
            'processed_filename': processed_filename,
            'original_size': original_size,
            'processed_size': processed_size,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch-upload', methods=['POST'])
def batch_upload():
    """Handle batch file upload"""
    try:
        files = request.files.getlist('files')
        
        if not files or len(files) == 0:
            return jsonify({'error': 'No files provided'}), 400
        
        if len(files) > 10:
            return jsonify({'error': 'Maximum 10 files allowed per batch'}), 400
        
        results = []
        options = {
            'background_color': request.form.get('background_color', 'transparent'),
            'background_image': request.form.get('background_image'),
            'output_format': request.form.get('output_format', 'png')
        }
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = generate_unique_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    processed_filename = bg_remover.remove_background(filepath, options)
                    results.append({
                        'success': True,
                        'original_url': url_for('static', filename=f'uploads/{filename}'),
                        'processed_url': url_for('static', filename=f'processed/{processed_filename}'),
                        'original_filename': file.filename,
                        'processed_filename': processed_filename
                    })
                except Exception as e:
                    results.append({
                        'success': False,
                        'original_filename': file.filename,
                        'error': str(e)
                    })
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(files),
            'processed': len([r for r in results if r.get('success')])
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    """Download processed image"""
    try:
        filepath = os.path.join(app.config['PROCESSED_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/change-background', methods=['POST'])
def change_background():
    """Change background of already processed image"""
    try:
        data = request.json
        original_file = data.get('original_file')
        background_type = data.get('background_type', 'color')
        background_value = data.get('background_value', '#ffffff')
        
        if not original_file:
            return jsonify({'error': 'Original file required'}), 400
        
        # Process with new background
        result = image_processor.change_background(
            original_file,
            background_type,
            background_value
        )
        
        return jsonify({
            'success': True,
            'url': url_for('static', filename=f'processed/{result}')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/gallery')
def gallery():
    """Gallery page showing processed images"""
    return render_template('gallery.html')

@app.route('/api/gallery')
def get_gallery():
    """Get list of processed images"""
    try:
        processed_dir = app.config['PROCESSED_FOLDER']
        images = []
        
        for filename in os.listdir(processed_dir):
            if allowed_file(filename):
                filepath = os.path.join(processed_dir, filename)
                stat = os.stat(filepath)
                images.append({
                    'filename': filename,
                    'url': url_for('static', filename=f'processed/{filename}'),
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
                })
        
        # Sort by creation time, newest first
        images.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({'images': images[:50]})  # Return last 50 images
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete a processed image"""
    try:
        filepath = os.path.join(app.config['PROCESSED_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True})
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': bg_remover.is_model_loaded(),
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Run in development mode
    print("🚀 Starting Premium Background Remover Server...")
    print("📱 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
