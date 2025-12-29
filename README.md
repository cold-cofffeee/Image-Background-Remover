# 🎨 Premium Background Remover - AI-Powered Web Application

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Professional-grade background removal powered by U2Net deep learning**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api-documentation) • [Deploy](#-deployment)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

Premium Background Remover is a state-of-the-art web application that uses the U2Net deep learning model to automatically remove backgrounds from images. Unlike expensive services like Remove.bg ($0.20/image), this is a self-hosted, free, and unlimited solution with a beautiful, modern interface.

### Why This Project?

After discovering Remove.bg's high pricing, I took on the challenge to build a professional alternative that:
- ✅ Works completely offline (no API dependencies)
- ✅ Processes unlimited images for free
- ✅ Provides a premium, user-friendly interface
- ✅ Offers batch processing capabilities
- ✅ Supports custom backgrounds and colors
- ✅ Includes a RESTful API for integration

---

## ✨ Features

### 🖼️ Image Processing
- **AI-Powered Removal**: Advanced U2Net model ensures accurate background removal
- **Batch Processing**: Upload and process up to 10 images simultaneously
- **High Quality Output**: Maintains image quality with lossless PNG export
- **Multiple Formats**: Supports PNG, JPG, JPEG, WEBP, and BMP

### 🎨 Background Customization
- **Transparent Background**: Perfect for design work
- **Solid Colors**: Choose from presets or custom colors
- **Color Picker**: Full RGB color selection
- **Background Images**: Replace with your own images (coming soon)
- **Gradient Backgrounds**: Beautiful gradient options (coming soon)

### 🚀 User Experience
- **Drag & Drop**: Intuitive drag-and-drop interface
- **Real-time Processing**: See results in seconds
- **Before/After Comparison**: Side-by-side image comparison
- **Download Options**: PNG or JPG format downloads
- **Gallery View**: Browse all processed images
- **Responsive Design**: Works on desktop, tablet, and mobile

### 🔧 Developer Features
- **RESTful API**: Easy integration into your applications
- **Batch API Endpoint**: Process multiple images via API
- **JSON Responses**: Clean, structured API responses
- **Rate Limiting**: Built-in API protection
- **Health Check**: Monitor service status

### 🏗️ Technical Features
- **GPU Acceleration**: Automatic GPU detection and usage
- **Optimized Performance**: Fast processing with caching
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed logging for debugging
- **Configuration**: Environment-based configuration

---

## 📸 Demo

### Web Interface
```
🏠 Home Page: http://localhost:5000
📁 Gallery: http://localhost:5000/gallery
🔗 API Docs: http://localhost:5000/api/health
```

### Features Showcase
- **Upload Interface**: Modern drag-and-drop with progress indicator
- **Background Options**: 6+ preset colors + custom color picker
- **Comparison View**: Side-by-side original and processed images
- **Gallery Management**: View, download, and delete processed images

---

## 🚀 Installation

### Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager
- **Virtual Environment**: Recommended
- **GPU** (Optional): CUDA-capable GPU for faster processing

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Image-Background-Remover.git
cd Image-Background-Remover
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download U2Net Model

Download the pre-trained U2Net model and place it in the appropriate directory:

**Option 1**: Download from Official Repository
```bash
# Create model directory
mkdir -p saved_models/u2net

# Download model (Linux/Mac)
wget -O saved_models/u2net/u2net.pth https://drive.google.com/uc?id=1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ

# For Windows, download manually from:
# https://drive.google.com/file/d/1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ/view
# Save as: saved_models/u2net/u2net.pth
```

**Option 2**: Use Pretrained Model
- Visit: [U2Net GitHub Repository](https://github.com/xuebinqin/U-2-Net)
- Download `u2net.pth` (176 MB)
- Place in `saved_models/u2net/` directory

### Step 5: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your preferred settings
# On Windows: notepad .env
# On Linux/Mac: nano .env
```

---

## ⚡ Quick Start

### Start the Application

```bash
python app.py
```

The server will start at: **http://localhost:5000**

### First Use

1. **Open Browser**: Navigate to `http://localhost:5000`
2. **Upload Image**: Drag & drop or click to select an image
3. **Wait for Processing**: AI processes your image (typically 2-5 seconds)
4. **View Results**: See before/after comparison
5. **Customize**: Change background color if desired
6. **Download**: Save your processed image

---

## 📖 Usage Guide

### Web Interface

#### Single Image Processing
1. Go to the home page
2. Drag and drop an image or click "Choose Image"
3. Wait for processing to complete
4. View the result with side-by-side comparison
5. Change background color using preset buttons or color picker
6. Download in PNG or JPG format

#### Batch Processing
1. Select multiple images (up to 10)
2. All images will be processed automatically
3. View results in the gallery
4. Download individual images or all at once

#### Gallery Management
1. Navigate to `/gallery`
2. View all processed images
3. Download or delete images as needed
4. Images are sorted by most recent first

### API Usage

#### Upload Single Image

```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@/path/to/image.jpg" \
  -F "background_color=transparent" \
  -F "output_format=png"
```

**Response:**
```json
{
  "success": true,
  "original_url": "/static/uploads/20241229_123456_abc123.jpg",
  "processed_url": "/static/processed/20241229_123456_abc123_processed.png",
  "original_filename": "20241229_123456_abc123.jpg",
  "processed_filename": "20241229_123456_abc123_processed.png",
  "original_size": 524288,
  "processed_size": 389120,
  "timestamp": "2024-12-29T12:34:56.789"
}
```

#### Batch Upload

```bash
curl -X POST http://localhost:5000/api/batch-upload \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  -F "files=@image3.jpg" \
  -F "background_color=white"
```

#### Health Check

```bash
curl http://localhost:5000/api/health
```

---

## 🔌 API Documentation

### Endpoints

#### POST `/api/upload`
Upload and process a single image.

**Parameters:**
- `file` (required): Image file
- `background_color` (optional): `transparent`, `white`, `black`, `#RRGGBB`
- `output_format` (optional): `png` or `jpg`

**Returns:** JSON with processed image URLs and metadata

#### POST `/api/batch-upload`
Process multiple images at once.

**Parameters:**
- `files` (required): Multiple image files (max 10)
- `background_color` (optional): Background color for all images
- `output_format` (optional): Output format for all images

**Returns:** JSON with array of results

#### GET `/api/download/<filename>`
Download a processed image.

#### GET `/api/gallery`
Get list of all processed images.

**Returns:** JSON array of image objects with URLs and metadata

#### DELETE `/api/delete/<filename>`
Delete a processed image.

#### GET `/api/health`
Check API health and model status.

**Returns:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-12-29T12:34:56.789"
}
```

### Rate Limiting
- Default: 100 requests per hour per IP
- Configurable in `.env` file

---

## ⚙️ Configuration

### Environment Variables

Edit `.env` file to customize settings:

```env
# Server
FLASK_ENV=development
PORT=5000
DEBUG=True

# Model
MODEL_PATH=saved_models/u2net/u2net.pth
USE_GPU=True

# Upload
MAX_CONTENT_LENGTH=16777216  # 16MB
MAX_BATCH_SIZE=10

# Storage
MAX_STORED_IMAGES=100
CLEANUP_AFTER_DAYS=7
```

### Advanced Configuration

See [config.py](config.py) for all available options.

---

## 🌐 Deployment

### Development Server

```bash
python app.py
```

### Production with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment

```dockerfile
# Dockerfile included in project
docker build -t bg-remover .
docker run -p 5000:5000 bg-remover
```

### Cloud Deployment

#### Heroku
```bash
heroku create your-app-name
git push heroku main
```

#### AWS/DigitalOcean
- Use provided Nginx configuration
- Setup SSL with Let's Encrypt
- Configure environment variables

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 🐛 Troubleshooting

### Common Issues

**Model not loading:**
- Ensure `u2net.pth` is in `saved_models/u2net/`
- Check file size: should be ~176 MB
- Verify file isn't corrupted

**Out of memory:**
- Reduce image size before processing
- Disable GPU: set `USE_GPU=False` in `.env`
- Process images one at a time

**Slow processing:**
- Enable GPU if available
- Reduce `MAX_BATCH_SIZE`
- Use smaller images

**Upload fails:**
- Check file size < 16MB
- Verify file format is supported
- Ensure `static/uploads/` directory exists and is writable

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

### U2Net Model
- **Authors**: Xuebin Qin, Zichen Zhang, Chenyang Huang, Masood Dehghan, Osmar R. Zaiane, Martin Jagersand
- **Paper**: [U^2-Net: Going Deeper with Nested U-Structure for Salient Object Detection](https://arxiv.org/abs/2005.09007)
- **Repository**: [https://github.com/xuebinqin/U-2-Net](https://github.com/xuebinqin/U-2-Net)

### Inspiration
- Remove.bg - for inspiration on UI/UX design
- Flask community - for excellent web framework
- PyTorch team - for deep learning tools

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/Image-Background-Remover/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Image-Background-Remover/discussions)
- **Email**: your.email@example.com

---

## 🎬 Video Tutorial

Watch the full tutorial on how to use and deploy this application:
[YouTube Video](https://youtu.be/KkhPN7Z4Fy8)

---

## 🚀 Roadmap

- [ ] Background image upload support
- [ ] Gradient backgrounds
- [ ] Image editing tools (crop, resize, rotate)
- [ ] AI-powered image enhancement
- [ ] Bulk download as ZIP
- [ ] User authentication system
- [ ] Cloud storage integration
- [ ] Mobile app (iOS/Android)
- [ ] Browser extension

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with ❤️ by [Your Name]

</div>
