# Deployment Guide

This guide covers how to deploy and run the Image Background Remover both locally and on Render.com.

## 📋 Table of Contents
- [Local Development](#local-development)
- [Deploying to Render.com](#deploying-to-rendercom)
- [Model File Management](#model-file-management)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

## 🖥️ Local Development

### Prerequisites
- Python 3.11 or higher
- Git
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Image-Background-Remover.git
   cd Image-Background-Remover
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Download the model file**
   ```bash
   python download_model.py
   ```
   
   The script will automatically download the U2Net model (~168MB) to `saved_models/u2net/u2net.pth`.
   
   If automatic download fails, manually download from:
   - https://huggingface.co/spaces/bharath/background-remover/resolve/main/u2net.pth
   - Or: https://drive.google.com/uc?export=download&id=1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ

5. **Set up environment variables**
   ```bash
   # Copy example file
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   
   # Edit .env with your settings
   ```

6. **Run the application**
   ```bash
   # Development mode
   python app.py
   
   # Production mode with Gunicorn
   gunicorn app:app --bind 0.0.0.0:5000 --workers 2
   ```

7. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## ☁️ Deploying to Render.com

### Method 1: One-Click Deploy (Recommended)

1. **Prepare your repository**
   ```bash
   # Commit all changes
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [Render.com](https://render.com) and sign in
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Click "Create Web Service"
   - Wait for the build and deploy (takes 5-10 minutes)

3. **Monitor deployment**
   - Check the logs to ensure the model downloads successfully
   - Once deployed, you'll get a URL like: `https://your-app.onrender.com`

### Method 2: Manual Configuration

If `render.yaml` doesn't auto-configure:

1. **Create New Web Service** on Render.com

2. **Configure Build & Deploy**
   - **Environment**: Python 3
   - **Build Command**: 
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt && python download_model.py
     ```
   - **Start Command**: 
     ```bash
     gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
     ```

3. **Set Environment Variables**
   - `PYTHON_VERSION`: `3.11.0`
   - `SECRET_KEY`: (auto-generate or set your own)
   - `DEBUG`: `False`
   - `FLASK_ENV`: `production`

4. **Configure Disk Storage** (Optional)
   - Add persistent disk at `/opt/render/project/src/static`
   - Size: 1GB (free tier)
   - This preserves uploaded/processed images across deploys

5. **Deploy**
   - Click "Create Web Service"
   - Monitor the deploy logs

## 📦 Model File Management

### Why Not Commit the Model to Git?

The U2Net model file (`u2net.pth`) is ~168MB, which exceeds GitHub's file size limits and makes the repository unnecessarily large.

### How It Works

1. **Automatic Download**: The `download_model.py` script automatically downloads the model during:
   - Local setup (when you run it manually)
   - Render.com deployment (as part of build command)

2. **Model Sources**: The script tries multiple sources:
   - Hugging Face (primary)
   - Google Drive (fallback)
   - Your own GitHub Release (if configured)

3. **Caching**: Once downloaded:
   - **Locally**: Model stays in `saved_models/u2net/`
   - **Render.com**: Model is cached in the build environment

### Alternative: Host Your Own Model

If you want to host the model yourself:

1. **Upload to GitHub Release**:
   ```bash
   # Create a new release on GitHub
   # Upload u2net.pth as a release asset
   # Update MODEL_URLS in download_model.py with your release URL
   ```

2. **Or use cloud storage**:
   - Upload to Google Drive, Dropbox, or S3
   - Get a direct download link
   - Update MODEL_URLS in download_model.py

## 🔧 Environment Variables

### Local Development (.env file)
```env
SECRET_KEY=your-secret-key
DEBUG=True
FLASK_ENV=development
HOST=0.0.0.0
PORT=5000
```

### Production (Render.com)
Set in Render Dashboard under "Environment":
```
SECRET_KEY=(auto-generated)
DEBUG=False
FLASK_ENV=production
PYTHON_VERSION=3.11.0
```

## 🔍 Troubleshooting

### Model Download Fails

**Problem**: Model won't download during deployment

**Solutions**:
1. Check Render logs for specific error
2. Try manually downloading and uploading to your own storage
3. Increase timeout in download_model.py
4. Use alternative MODEL_URLS

### Memory Issues on Render

**Problem**: App crashes with memory errors

**Solutions**:
1. Upgrade to Render's paid plan (more RAM)
2. Reduce `--workers` count in start command
3. Process smaller images only
4. Add memory limits in code

### Build Timeout

**Problem**: Build takes too long and times out

**Solutions**:
1. Model download is cached after first successful build
2. Use smaller dependencies if possible
3. Upgrade to paid plan for faster builds

### File Upload Errors

**Problem**: Files don't persist across deployments

**Solutions**:
1. Configure persistent disk in render.yaml
2. Use cloud storage (S3, Cloudinary) for uploads
3. Store files in the mounted disk path

### Port Binding Issues

**Problem**: App won't start, port errors

**Solution**: Ensure you're using `$PORT` environment variable:
```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### CUDA/PyTorch Issues

**Problem**: PyTorch CUDA errors on Render

**Solution**: This is normal! Render uses CPU. The code handles this:
```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
```

## 📊 Performance Tips

### For Better Performance on Render Free Tier:
1. Use `--workers 1` (save memory)
2. Limit max file size to 10MB
3. Add image optimization before processing
4. Implement request queuing for batch processing

### For Production:
1. Upgrade to paid plan (more RAM/CPU)
2. Use CDN for static files
3. Implement caching for common operations
4. Add background job queue (Redis + Celery)
5. Use cloud storage for file uploads

## 🎉 Success Indicators

Your deployment is successful when:
- ✅ Build completes without errors
- ✅ Model downloads successfully
- ✅ App starts and responds to health checks
- ✅ You can access the web interface
- ✅ Image upload and processing works
- ✅ Logs show no critical errors

## 📞 Support

If you encounter issues:
1. Check Render logs: Dashboard → Logs
2. Review this guide's troubleshooting section
3. Check GitHub issues
4. Render documentation: https://render.com/docs

## 🔄 Updating the App

To deploy updates:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically rebuild and deploy (if auto-deploy is enabled).

---

**Happy Deploying! 🚀**
