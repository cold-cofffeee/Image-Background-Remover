# Quick Start Guide

## Get Running in 3 Minutes

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Model (if not included)

Place `u2net.pth` in `saved_models/u2net/` directory

Download from: https://drive.google.com/file/d/1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ/view

### 3. Run

```bash
python app.py
```

### 4. Open Browser

Navigate to: http://localhost:5000

---

## Features

- ✅ Drag & drop interface
- ✅ Batch processing (up to 10 images)
- ✅ Custom background colors
- ✅ PNG/JPG export
- ✅ RESTful API
- ✅ Gallery view
- ✅ No account required
- ✅ Unlimited processing

---

## API Usage

### Upload Image

```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@image.jpg" \
  -F "background_color=transparent"
```

### Response

```json
{
  "success": true,
  "processed_url": "/static/processed/image_processed.png"
}
```

---

## Troubleshooting

**Model not loading?**
- Ensure `u2net.pth` exists in `saved_models/u2net/`
- File size should be ~176 MB

**Out of memory?**
- Set `USE_GPU=False` in `.env`
- Process smaller images

**Port 5000 in use?**
- Change port in app.py or `.env`

---

Built with U2Net • MIT License
