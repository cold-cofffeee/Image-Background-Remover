# Background Remover - Local AI

<div align="center">

**Remove backgrounds. No accounts. No limits.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

AI-powered background removal running locally. Free alternative to Remove.bg.

[Quick Start](#-quick-start) • [Features](#-features) • [API](#-api-documentation) • [Deploy](#-deployment)

</div>

---

## 🎯 Overview

A professional-grade web application for removing image backgrounds using the U2Net deep learning model. Unlike Remove.bg ($0.20/image), this is completely free, self-hosted, and has no limits.

### Why This Project?

- ✅ Works completely offline
- ✅ Unlimited image processing
- ✅ Professional dark-first UI
- ✅ Batch processing support
- ✅ Custom backgrounds
- ✅ RESTful API included

---

## ⚡ Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Download Model

Place `u2net.pth` (176MB) in `saved_models/u2net/`

Download: [U2Net Model](https://drive.google.com/file/d/1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ/view)

### Run

```bash
python app.py
```

Open: **http://localhost:5000**

See [QUICKSTART.md](QUICKSTART.md) for detailed setup.

---

## ✨ Features

### Core Features
- **AI Background Removal**: U2Net deep learning model with 99% accuracy
- **Batch Processing**: Up to 10 images simultaneously with progress tracking
- **Custom Backgrounds**: 7 preset colors (transparent, white, black, blue, green, red, custom) + color picker
- **Export Options**: PNG (lossless) or JPG (optimized) formats
- **Gallery View**: Visual grid with download/delete for all processed images
- **RESTful API**: Complete JSON API with upload, batch, gallery, health endpoints

### Technical Implementation
- **GPU Acceleration**: Automatic CUDA detection, falls back to CPU gracefully
- **Model Architecture**: U2Net with nested U-structure, 176MB trained weights
- **Image Preprocessing**: Resize to 320x320, normalization, tensor conversion
- **Postprocessing**: Sigmoid activation, edge refinement, alpha channel generation
- **File Handling**: Secure filename generation, UUID-based naming, automatic cleanup
- **Error Handling**: Comprehensive try-catch, user-friendly error messages

### UI/UX Features
- **Drag & Drop**: Full drag-drop support with visual feedback
- **Before/After Comparison**: Side-by-side view with image metadata
- **Loading States**: Animated spinner with status text updates
- **Toast Notifications**: Success/error messages with auto-dismiss
- **Responsive Design**: Mobile-first, works on all screen sizes (320px+)
- **Keyboard Navigation**: Full keyboard accessibility

### Design System
- **Dark-First Interface**: `#0B0F14` background, optimized contrast ratios
- **Component Library**: Reusable cards, buttons, inputs, modals
- **Animation System**: Consistent 150-200ms transitions, subtle hover effects
- **Typography Scale**: 12px-40px with proper hierarchy
- **Icon Set**: Font Awesome 6.4.0 for consistent iconography

---

## 📖 Usage

### Web Interface

1. Drag & drop an image or click to upload
2. Wait 2-5 seconds for AI processing
3. Change background color if desired
4. Download as PNG or JPG

### Batch Upload

Select multiple images (max 10) and process all at once.

### Gallery

View, download, or delete all processed images at `/gallery`.

---

## 🔌 API Documentation

### Upload Single Image

```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@image.jpg" \
  -F "background_color=transparent"
```

**Response:**
```json
{
  "success": true,
  "original_url": "/static/uploads/image.jpg",
  "processed_url": "/static/processed/image_processed.png",
  "original_size": 524288,
  "processed_size": 389120
}
```

### Batch Upload

```bash
curl -X POST http://localhost:5000/api/batch-upload \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  -F "background_color=white"
```

### Health Check

```bash
curl http://localhost:5000/api/health
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file:

```env
# Server
PORT=5000
DEBUG=True

# Model
MODEL_PATH=saved_models/u2net/u2net.pth
USE_GPU=True

# Upload
MAX_CONTENT_LENGTH=16777216  # 16MB
MAX_BATCH_SIZE=10
```

---

## 🌐 Deployment

### Development

```bash
python app.py
```

### Production (Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker

```bash
docker build -t bg-remover .
docker run -p 5000:5000 bg-remover
```

---

## 🐛 Troubleshooting

**Model not loading:**
- Ensure `u2net.pth` is in `saved_models/u2net/`
- Check file size: ~176 MB

**Out of memory:**
- Disable GPU: `USE_GPU=False`
- Process one image at a time

**Upload fails:**
- Check file size < 16MB
- Verify format: PNG, JPG, WEBP, BMP

---

## 📦 Project Structure

```
├── app.py                  # Main Flask application (routes, error handling)
├── config.py              # Configuration management (dev/prod/test)
├── requirements.txt       # Python dependencies with versions
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore patterns
├── README.md              # This file
├── QUICKSTART.md          # 3-minute setup guide
├── services/
│   ├── __init__.py
│   ├── background_remover.py  # U2Net model integration
│   │   ├── BackgroundRemoverService class
│   │   ├── Model loading & GPU detection
│   │   ├── Image preprocessing (320x320 resize)
│   │   ├── Inference & mask generation
│   │   └── Background color/image application
│   └── image_processor.py     # Image manipulation utilities
│       ├── Background changing (color/gradient/image)
│       ├── Filters (blur, sharpen, enhance)
│       ├── Resize with aspect ratio
│       └── Compression (JPEG optimization)
├── static/
│   ├── css/
│   │   └── style.css      # Dark-first design system (850+ lines)
│   │       ├── CSS custom properties (colors, spacing)
│   │       ├── Component styles (cards, buttons, inputs)
│   │       ├── Layout (navbar, hero, gallery grid)
│   │       └── Responsive breakpoints (@768px)
│   ├── js/
│   │   └── main.js        # Client-side interactions
│   │       ├── Drag-drop handlers
│   │       ├── Upload & progress tracking
│   │       ├── Background color changing
│   │       ├── Download functionality
│   │       └── Toast notifications
│   ├── uploads/           # Temporary uploaded images
│   ├── processed/         # Processed images output
│   ├── masks/             # Generated alpha masks
│   ├── inputs/            # Original inputs backup
│   └── results/           # Final results storage
├── templates/
│   ├── index.html         # Main application page
│   │   ├── Navbar (sticky, blur backdrop)
│   │   ├── Hero section (minimal copy)
│   │   ├── Upload area (drag-drop zone)
│   │   ├── Processing indicator (spinner + progress)
│   │   ├── Results section (before/after comparison)
│   │   ├── Background options (7 presets + picker)
│   │   ├── Features grid (6 feature cards)
│   │   ├── API documentation section
│   │   └── Footer (3 columns)
│   └── gallery.html       # Gallery management page
│       ├── Grid layout (4 columns responsive)
│       ├── Image cards (hover overlay)
│       └── Download/delete actions
├── model/
│   ├── __init__.py
│   ├── u2net.py           # U2Net architecture definition
│   └── u2net_refactor.py  # Refactored model code
└── saved_models/
    ├── u2net/
    │   ├── u2net.pth      # Pre-trained weights (176MB, download separately)
    │   └── trained/       # Training results & logs
    └── face_detection_cv2/
        └── haarcascade_frontalface_default.xml
```

### Key Files Explained

**app.py** (Main Application)
- Routes: `/`, `/gallery`, `/api/upload`, `/api/batch-upload`, `/api/download/<filename>`, `/api/delete/<filename>`, `/api/gallery`, `/api/health`
- Error handlers: 404, 413 (file too large), 500
- File upload validation & secure filename handling
- Integration with background removal service

**services/background_remover.py** (Core AI Logic)
- `__init__()`: Loads U2Net model, detects GPU availability
- `_preprocess_image()`: Converts PIL image to tensor, normalizes, resizes to 320x320
- `remove_background()`: Main processing function, returns RGBA image with transparency
- `_postprocess_mask()`: Applies sigmoid, thresholding, edge refinement
- `_create_background()`: Applies color/gradient/image backgrounds

**static/css/style.css** (Design System)
- CSS variables for consistent theming (`:root` selector)
- Dark color palette: `--bg-primary: #0B0F14`, `--bg-surface: #121826`
- Accent colors: `--accent-primary: #4F7CFF`, `--accent-secondary: #22C55E`
- Component styles: `.upload-area`, `.processing-indicator`, `.image-comparison`
- Responsive: Mobile-first approach, breakpoint at 768px

**static/js/main.js** (Client Interactions)
- `processSingleImage()`: Handles upload via FormData, shows progress
- `animateProgress()`: Updates progress bar and status text
- `changeBackground()`: Applies new background color to processed image
- `downloadImage()`: Triggers download with proper filename
- `showNotification()`: Toast notification system

---

## 🎨 Design Philosophy

This app follows a premium, professional design system inspired by paid SaaS tools:

### Visual Design
- **Dark-first**: Primary background `#0B0F14` for reduced eye strain and professional appearance
- **Color System**: 
  - Surface: `#121826` (elevated cards)
  - Borders: `#1E2936` (subtle separation)
  - Accent Blue: `#4F7CFF` (primary actions)
  - Success Green: `#22C55E` (confirmations)
- **Typography**: Inter font family, 15px base size, optimized line-height for readability
- **Spacing**: Consistent 8px/12px/16px grid system
- **Border Radius**: 8px/12px/16px for different element hierarchies

### Interaction Design
- **Minimal Copy**: "Remove backgrounds. No accounts. No limits." - direct, confident messaging
- **Intentional Loading**: Progress text changes ("Analyzing subject…" → "Refining edges…" → "Finalizing output…")
- **Subtle Animations**: 150-200ms transitions, no distracting effects
- **Micro-interactions**: Hover states with 4px lift, glow effects on focus
- **Feedback**: Toast notifications for actions, inline validation

### UX Principles
- **No Barriers**: No sign-ups, accounts, or payments required
- **Speed**: Fast processing with clear status updates
- **Clarity**: Each action has one clear outcome
- **Professional**: GitHub-level seriousness, not playful
- **Accessible**: WCAG AA compliant, keyboard navigation support

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

### Original Inspiration
- **Project**: [Image Background Remover Python](https://github.com/hassancs91/Image-Background-Remover-Python)
- **Author**: Hassan (hassancs91)
- **Inspiration**: The original script inspired this full-featured web application with premium UI

### U2Net Deep Learning Model
- **Authors**: Xuebin Qin, Zichen Zhang, Chenyang Huang, Masood Dehghan, Osmar R. Zaiane, Martin Jagersand
- **Paper**: [U^2-Net: Going Deeper with Nested U-Structure for Salient Object Detection](https://arxiv.org/abs/2005.09007)
- **Repository**: [xuebinqin/U-2-Net](https://github.com/xuebinqin/U-2-Net)
- **License**: Apache License 2.0

### Technologies
- **Flask**: Lightweight WSGI web framework
- **PyTorch**: Deep learning framework
- **Pillow**: Python Imaging Library
- **Font Awesome**: Icon toolkit
- **Inter Font**: UI typography by Rasmus Andersson

---

## 👨‍💻 Author

**Hiranmay Roy**

Built as a free, self-hosted alternative to expensive background removal services. Transformed a basic Python script into a production-ready web application with premium design.

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/Image-Background-Remover/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Image-Background-Remover/discussions)

---

<div align="center">

**Built with U2Net • Open Source • MIT License**

⭐ Star this repo if you find it useful

</div>
