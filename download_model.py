"""
Model Downloader
Downloads the U2Net model file if it doesn't exist locally
Supports multiple hosting sources for redundancy
"""

import os
import sys
import requests
from pathlib import Path
from tqdm import tqdm

# Model file configuration
MODEL_DIR = Path(__file__).parent / 'saved_models' / 'u2net'
MODEL_PATH = MODEL_DIR / 'u2net.pth'
MODEL_SIZE = 176_127_824  # Approximate size in bytes

# Multiple download sources for redundancy
MODEL_URLS = [
    # Option 1: Hugging Face (Recommended - free and reliable)
    "https://huggingface.co/spaces/bharath/background-remover/resolve/main/u2net.pth",
    
    # Option 2: GitHub Release (if you create a release with the model)
    # "https://github.com/YOUR_USERNAME/YOUR_REPO/releases/download/v1.0/u2net.pth",
    
    # Option 3: Original U2Net model from the paper authors
    "https://drive.google.com/uc?export=download&id=1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ",
]

def download_file(url, destination, chunk_size=8192):
    """Download file with progress bar"""
    try:
        print(f"\n📥 Downloading model from: {url}")
        
        # Make request with stream=True
        response = requests.get(url, stream=True, timeout=30, allow_redirects=True)
        response.raise_for_status()
        
        # Get total file size
        total_size = int(response.headers.get('content-length', 0))
        
        # Create progress bar
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        
        # Download and write to file
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    size = f.write(chunk)
                    progress_bar.update(size)
        
        progress_bar.close()
        
        # Verify file size
        downloaded_size = os.path.getsize(destination)
        if total_size > 0 and downloaded_size != total_size:
            print(f"⚠️  Warning: Downloaded size ({downloaded_size}) doesn't match expected ({total_size})")
        
        print(f"✅ Download complete: {destination}")
        return True
        
    except Exception as e:
        print(f"❌ Download failed: {str(e)}")
        if os.path.exists(destination):
            os.remove(destination)
        return False

def check_model_exists():
    """Check if model file already exists"""
    if MODEL_PATH.exists():
        file_size = os.path.getsize(MODEL_PATH)
        if file_size > 100_000_000:  # At least 100MB
            print(f"✅ Model already exists: {MODEL_PATH} ({file_size:,} bytes)")
            return True
        else:
            print(f"⚠️  Model file exists but seems corrupted (too small: {file_size} bytes)")
            return False
    return False

def download_model():
    """Download model from available sources"""
    
    # Create model directory if it doesn't exist
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check if model already exists
    if check_model_exists():
        return True
    
    print("\n" + "="*60)
    print("🤖 U2Net Model Download Required")
    print("="*60)
    print(f"Model will be saved to: {MODEL_PATH}")
    print(f"Approximate size: {MODEL_SIZE / (1024*1024):.1f} MB")
    print("="*60 + "\n")
    
    # Try each URL until one succeeds
    for i, url in enumerate(MODEL_URLS, 1):
        print(f"\n📡 Attempt {i}/{len(MODEL_URLS)}")
        
        if download_file(url, MODEL_PATH):
            # Verify the downloaded file
            if check_model_exists():
                print("\n" + "="*60)
                print("✅ Model downloaded and verified successfully!")
                print("="*60 + "\n")
                return True
        
        print(f"Trying next source...\n")
    
    # All downloads failed
    print("\n" + "="*60)
    print("❌ All download attempts failed!")
    print("="*60)
    print("\n📋 Manual Download Instructions:")
    print("1. Download the model from: https://huggingface.co/spaces/bharath/background-remover/resolve/main/u2net.pth")
    print("2. Save it to:", MODEL_PATH)
    print("3. Or use this direct link: https://drive.google.com/uc?export=download&id=1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ")
    print("="*60 + "\n")
    return False

if __name__ == "__main__":
    try:
        success = download_model()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Download cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
