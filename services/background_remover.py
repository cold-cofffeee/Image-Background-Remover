"""
Background Remover Service using U2Net Model
Handles the core background removal functionality
"""

import os
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from skimage import io
import torch.nn.functional as F
from model.u2net import U2NET
import cv2

class BackgroundRemoverService:
    """Service for removing backgrounds from images using U2Net"""
    
    def __init__(self, model_path='saved_models/u2net/u2net.pth'):
        """Initialize the background remover service"""
        self.model_path = model_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.model_loaded = False
        self._load_model()
    
    def _load_model(self):
        """Load the U2Net model"""
        try:
            print("🔄 Loading U2Net model...")
            self.model = U2NET(3, 1)
            
            # Check if model file exists, if not try to download it
            if not os.path.exists(self.model_path):
                print("⚠️ Model file not found. Attempting to download...")
                try:
                    from download_model import download_model
                    if not download_model():
                        raise Exception("Model download failed")
                except Exception as e:
                    print(f"❌ Could not download model: {e}")
                    print(f"   Please manually download and place at: {self.model_path}")
                    self.model_loaded = False
                    return
            
            # Load pre-trained weights
            self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
            print("✅ Pre-trained model loaded successfully")
            
            self.model.to(self.device)
            self.model.eval()
            self.model_loaded = True
            print(f"✅ Model ready on {self.device}")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model_loaded = False
    
    def is_model_loaded(self):
        """Check if model is loaded"""
        return self.model_loaded
    
    def _normalize(self, image):
        """Normalize image for model input"""
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        return transform(image)
    
    def _preprocess_image(self, image_path):
        """Preprocess image for model"""
        # Load image
        image = Image.open(image_path).convert('RGB')
        original_size = image.size
        
        # Resize to 320x320 for model
        image_resized = image.resize((320, 320), Image.BILINEAR)
        
        # Convert to tensor
        image_tensor = self._normalize(image_resized)
        image_tensor = image_tensor.unsqueeze(0)
        
        return image_tensor, image, original_size
    
    def _postprocess_mask(self, mask, original_size):
        """Postprocess the model output mask"""
        # Convert to numpy
        mask = mask.squeeze().cpu().data.numpy()
        
        # Normalize to 0-255
        mask = (mask - mask.min()) / (mask.max() - mask.min())
        mask = (mask * 255).astype(np.uint8)
        
        # Resize to original size
        mask = Image.fromarray(mask).resize(original_size, Image.BILINEAR)
        
        return mask
    
    def remove_background(self, image_path, options=None):
        """
        Remove background from image
        
        Args:
            image_path: Path to input image
            options: Dict with processing options:
                - background_color: 'transparent', '#RRGGBB', or 'white', 'black'
                - output_format: 'png' or 'jpg'
                - background_image: Path to background image
        
        Returns:
            Path to processed image
        """
        if options is None:
            options = {}
        
        if not self.model_loaded:
            raise Exception("Model not loaded. Cannot process image.")
        
        try:
            # Preprocess
            image_tensor, original_image, original_size = self._preprocess_image(image_path)
            image_tensor = image_tensor.to(self.device)
            
            # Run model
            with torch.no_grad():
                d1, d2, d3, d4, d5, d6, d7 = self.model(image_tensor)
            
            # Get prediction
            pred = d1[:, 0, :, :]
            pred = self._postprocess_mask(pred, original_size)
            
            # Convert original image to numpy array
            img_np = np.array(original_image)
            mask_np = np.array(pred)
            
            # Ensure mask is properly scaled (0-255 range)
            # Threshold the mask to create a binary mask (improves edge quality)
            # Values above 128 are considered foreground
            mask_np = np.where(mask_np > 128, 255, 0).astype(np.uint8)
            
            # Apply mask to create transparent background
            # Create RGBA image with the mask as alpha channel
            img_rgba = np.dstack((img_np, mask_np))
            
            result_image = Image.fromarray(img_rgba, 'RGBA')
            
            # Apply background options
            background_color = options.get('background_color', 'transparent')
            
            if background_color != 'transparent':
                # Create background
                bg = self._create_background(original_size, background_color, options)
                
                # Composite
                result_image = Image.alpha_composite(bg, result_image)
            
            # Save processed image
            output_format = options.get('output_format', 'png')
            output_filename = os.path.basename(image_path).rsplit('.', 1)[0] + f'_processed.{output_format}'
            output_path = os.path.join('static/processed', output_filename)
            
            if output_format == 'jpg':
                # Convert to RGB for JPEG
                if result_image.mode == 'RGBA':
                    rgb_image = Image.new('RGB', result_image.size, (255, 255, 255))
                    rgb_image.paste(result_image, mask=result_image.split()[3])
                    result_image = rgb_image
                result_image.save(output_path, 'JPEG', quality=95)
            else:
                result_image.save(output_path, 'PNG')
            
            return output_filename
            
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")
    
    def _create_background(self, size, background_color, options):
        """Create background image with specified color or image"""
        
        bg = Image.new('RGBA', size, (255, 255, 255, 255))
        
        if background_color.startswith('#'):
            # Hex color
            color = self._hex_to_rgb(background_color)
            bg = Image.new('RGBA', size, color + (255,))
        elif background_color == 'white':
            bg = Image.new('RGBA', size, (255, 255, 255, 255))
        elif background_color == 'black':
            bg = Image.new('RGBA', size, (0, 0, 0, 255))
        elif background_color == 'blue':
            bg = Image.new('RGBA', size, (52, 152, 219, 255))
        elif background_color == 'green':
            bg = Image.new('RGBA', size, (46, 204, 113, 255))
        elif background_color == 'red':
            bg = Image.new('RGBA', size, (231, 76, 60, 255))
        
        # Handle background image if provided
        background_image_path = options.get('background_image')
        if background_image_path and os.path.exists(background_image_path):
            bg_img = Image.open(background_image_path).convert('RGBA')
            bg_img = bg_img.resize(size, Image.BILINEAR)
            bg = bg_img
        
        return bg
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
