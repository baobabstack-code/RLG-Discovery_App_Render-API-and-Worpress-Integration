from PIL import ImageFont
import platform

def load_font(font_name: str, size: int):
    """
    Load a font from common system paths or fallback to default.
    """
    # Common paths for Arial or similar sans-serif
    candidates = [
        # User requested specific path (if provided as absolute path)
        font_name,
        # macOS
        f"/Library/Fonts/{font_name}.ttf",
        f"/System/Library/Fonts/{font_name}.ttf",
        # Linux (Debian/Ubuntu/Render)
        f"/usr/share/fonts/truetype/msttcorefonts/{font_name}.ttf",
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", # Fallback 1
        f"/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", # Fallback 2
    ]
    
    print(f"Searching for font: {font_name}")
    for path in candidates:
        try:
            font = ImageFont.truetype(path, size)
            print(f"Found font at: {path}")
            return font
        except Exception:
            continue
            
    # If all else fails, try loading by name (OS might resolve it)
    try:
        font = ImageFont.truetype(f"{font_name}.ttf", size)
        print(f"Found font by name: {font_name}.ttf")
        return font
    except Exception:
        pass
        
    print("Falling back to default font")
    return ImageFont.load_default()

if __name__ == "__main__":
    font = load_font("Arial", 12)
    print(f"Loaded font object: {font}")
