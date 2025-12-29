"""
Image Processor Service
Handles image manipulation operations like background changes, filters, etc.
"""

import os
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

class ImageProcessor:
    """Service for additional image processing operations"""
    
    def __init__(self):
        """Initialize image processor"""
        pass
    
    def change_background(self, image_path, background_type, background_value):
        """
        Change the background of an already processed image
        
        Args:
            image_path: Path to the transparent PNG image
            background_type: 'color', 'image', or 'gradient'
            background_value: Color hex, image path, or gradient config
        
        Returns:
            Filename of the new image
        """
        try:
            # Load the transparent image
            img = Image.open(image_path).convert('RGBA')
            
            # Create background
            bg = self._create_background(img.size, background_type, background_value)
            
            # Composite
            result = Image.alpha_composite(bg, img)
            
            # Save
            filename = os.path.basename(image_path).replace('.png', f'_bg_{background_type}.png')
            output_path = os.path.join('static/processed', filename)
            result.save(output_path, 'PNG')
            
            return filename
            
        except Exception as e:
            raise Exception(f"Error changing background: {str(e)}")
    
    def _create_background(self, size, bg_type, bg_value):
        """Create background based on type"""
        
        if bg_type == 'color':
            # Solid color
            color = self._hex_to_rgb(bg_value)
            return Image.new('RGBA', size, color + (255,))
        
        elif bg_type == 'image':
            # Background image
            if os.path.exists(bg_value):
                bg_img = Image.open(bg_value).convert('RGBA')
                bg_img = bg_img.resize(size, Image.BILINEAR)
                return bg_img
            else:
                # Default to white if image not found
                return Image.new('RGBA', size, (255, 255, 255, 255))
        
        elif bg_type == 'gradient':
            # Create gradient
            return self._create_gradient(size, bg_value)
        
        else:
            # Default white
            return Image.new('RGBA', size, (255, 255, 255, 255))
    
    def _create_gradient(self, size, config):
        """Create a gradient background"""
        # Default gradient from top to bottom
        color1 = self._hex_to_rgb(config.get('color1', '#667eea'))
        color2 = self._hex_to_rgb(config.get('color2', '#764ba2'))
        
        # Create gradient
        gradient = np.zeros((size[1], size[0], 4), dtype=np.uint8)
        
        for i in range(size[1]):
            ratio = i / size[1]
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            gradient[i, :] = [r, g, b, 255]
        
        return Image.fromarray(gradient, 'RGBA')
    
    def apply_filter(self, image_path, filter_name):
        """Apply filters to image"""
        img = Image.open(image_path)
        
        if filter_name == 'blur':
            img = img.filter(ImageFilter.GaussianBlur(radius=2))
        elif filter_name == 'sharpen':
            img = img.filter(ImageFilter.SHARPEN)
        elif filter_name == 'smooth':
            img = img.filter(ImageFilter.SMOOTH)
        elif filter_name == 'enhance':
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.5)
        
        # Save filtered image
        filename = os.path.basename(image_path).replace('.png', f'_{filter_name}.png')
        output_path = os.path.join('static/processed', filename)
        img.save(output_path)
        
        return filename
    
    def resize_image(self, image_path, width, height, maintain_aspect=True):
        """Resize image to specific dimensions"""
        img = Image.open(image_path)
        
        if maintain_aspect:
            img.thumbnail((width, height), Image.LANCZOS)
        else:
            img = img.resize((width, height), Image.LANCZOS)
        
        filename = os.path.basename(image_path).replace('.png', f'_resized.png')
        output_path = os.path.join('static/processed', filename)
        img.save(output_path)
        
        return filename
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def compress_image(self, image_path, quality=85):
        """Compress image to reduce file size"""
        img = Image.open(image_path)
        
        filename = os.path.basename(image_path).replace('.png', '_compressed.jpg')
        output_path = os.path.join('static/processed', filename)
        
        if img.mode == 'RGBA':
            # Convert to RGB for JPEG
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
            img = rgb_img
        
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        return filename
