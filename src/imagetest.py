import random
import os
from PIL import Image, ImageDraw, ImageFont

# updated version at backgrounds.py

def layer_png_with_border(background_path, foreground_path, output_path, border_size_pixels):
    """
    Layers a PNG image (foreground) onto a square background image.
    The PNG is scaled to be as large as possible within a frame,
    maintaining its aspect ratio and not touching the border.

    stuff.png should be scatted on top of paper.png which should be layerd over square.jpg

    background_path (str): File path to the square background image (e.g., 'bg.jpg').
    foreground_path (str): File path to the transparent PNG (foreground) (e.g., 'fg.png').
    output_path (str): File path to save the resulting image (e.g., 'layered_image.png').
    border_size_pixels (int): The minimum border distance in pixels from the edge of the background image to the foreground image.
    """
    try:
        # 1. Open Images and Convert to RGBA
        background = Image.open(background_path).convert("RGBA")
        foreground = Image.open(foreground_path).convert("RGBA")
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
        return

    # Check if the background is square (optional, but good practice based on prompt)
    bg_width, bg_height = background.size
    if bg_width != bg_height:
        print("Warning: Background image is not square. Proceeding with largest dimension as reference.")

    # 2. Calculate the maximum available size for the foreground image
    # The frame size is the background dimension minus twice the desired border.
    frame_max_dim = min(bg_width, bg_height) - (2 * border_size_pixels)

    if frame_max_dim <= 0:
        print("Error: Border size is too large for the background image size.")
        return

    # 3. Calculate the required scaling for the foreground
    fg_width, fg_height = foreground.size
    
    # Calculate the scale factor required to fit the PNG within the square frame
    # We take the minimum of the ratios (max_frame_dim / fg_dim) to ensure both 
    # width and height fit within the frame while preserving the aspect ratio.
    scale_factor = min(frame_max_dim / fg_width, frame_max_dim / fg_height)

    # Calculate the new dimensions for the foreground image
    new_fg_width = int(fg_width * scale_factor)
    new_fg_height = int(fg_height * scale_factor)
    
    # 4. Resize the foreground image
    # Use Image.Resampling.LANCZOS for high-quality downscaling
    resized_foreground = foreground.resize((new_fg_width, new_fg_height), Image.Resampling.LANCZOS)

    # 5. Calculate the center position for pasting
    # The position is (left, top) corner. 
    # To center: (Total_Background_Dim - Resized_Foreground_Dim) // 2
    x_center = (bg_width - new_fg_width) // 2
    y_center = (bg_height - new_fg_height) // 2
    
    position = (x_center, y_center)
    
    # 6. Layer the transparent PNG onto the background
    # The third argument, `resized_foreground` (the mask), is crucial for 
    # transparent PNGs. Pillow uses the alpha channel of the image itself as the mask.
    background.paste(resized_foreground, position, resized_foreground)

    # 7. Save the final image
    # Save as PNG to preserve the layering and potential alpha if the background was transparent
    background.save(output_path, "PNG")
    print(f"Successfully layered and saved image to {output_path}")
    
    # Optional: Display the image
    # background.show()

# --- Example Usage ---

# Create dummy files for demonstration if they don't exist
# You should replace 'background.jpg' and 'foreground.png' with your actual file paths.

# Example: A 500x500 background with a 20-pixel border

# NOTE: You must have actual image files named 'background.jpg' and 'foreground.png'
# for this code to run successfully in your environment.

# border_size = 20
# background_file = "background.jpg"
# foreground_file = "foreground.png"
# output_file = "final_image.png"

# layer_png_with_border(background_file, foreground_file, output_file, border_size)


# -----------

def layer_random_pngs_on_border(background_path, foreground_paths, output_path, scale_ratio=5.0, padding=10):
    """
    Layers 3-5 randomly selected PNGs around the border of a square background.

    Args:
        background_path (str): Path to the square background image.
        foreground_paths (list): List of paths to the PNG foreground images.
        output_path (str): Path to save the resulting image.
        scale_ratio (float): The foreground image's target dimension will be 
                             (Background Dimension / scale_ratio).
        padding (int): A small pixel offset from the true edge.
    """
    try:
        # 1. Load Background and get its size
        background = Image.open(background_path).convert("RGBA")
        bg_width, bg_height = background.size
        
        if bg_width != bg_height:
             print("Error: Background image is not perfectly square. Exiting.")
             return
             
    except FileNotFoundError:
        print(f"Error: Background file not found at {background_path}")
        return
    except Exception as e:
        print(f"Error loading background: {e}")
        return

    # 2. Determine the target size for all layered PNGs (relative to background)
    # Target dimension (all PNGs will be scaled to fit inside this square)
    target_dim = int(bg_width / scale_ratio)
    
    if target_dim <= 0:
        print("Error: Target dimension is zero or negative. Adjust scale_ratio.")
        return
        
    print(f"Background size: {bg_width}x{bg_height}. Target PNG max dimension: {target_dim}px.")

    # 3. Define 8 fixed center points for border placement
    center_offset = target_dim // 2 # Center to Corner distance of the PNG
    border_pos = padding + center_offset # Center distance from the edge

    # The four corners and four midpoints (8 potential slots)
    center_slots = [
        # Corners
        (border_pos, border_pos),                                         # Top-Left
        (bg_width - border_pos, border_pos),                              # Top-Right
        (bg_width - border_pos, bg_height - border_pos),                  # Bottom-Right
        (border_pos, bg_height - border_pos),                             # Bottom-Left
        # Midpoints
        (bg_width // 2, border_pos),                                      # Top-Mid
        (bg_width - border_pos, bg_height // 2),                          # Right-Mid
        (bg_width // 2, bg_height - border_pos),                          # Bottom-Mid
        (border_pos, bg_height // 2),                                     # Left-Mid
    ]
    
    # 4. Randomly select 3 to 5 unique slots and PNGs
    num_pngs = random.randint(3, 5)
    
    # Select unique slots (positions)
    random.shuffle(center_slots)
    selected_slots = center_slots[:num_pngs]
    
    # Select random PNGs (allowing duplicates if foreground_paths is small)
    selected_pngs = random.sample(foreground_paths, num_pngs)


    # 5. Process and paste each selected PNG
    for i in range(num_pngs):
        png_path = selected_pngs[i]
        center_x, center_y = selected_slots[i]
        
        try:
            # Load and convert PNG
            foreground = Image.open(png_path).convert("RGBA")
            fg_width, fg_height = foreground.size

            # Calculate the scale factor to fit the PNG inside the target_dim square
            scale_factor = min(target_dim / fg_width, target_dim / fg_height)
            
            new_fg_width = int(fg_width * scale_factor)
            new_fg_height = int(fg_height * scale_factor)

            # Resize the PNG
            resized_foreground = foreground.resize((new_fg_width, new_fg_height), Image.Resampling.LANCZOS)
            
            # Calculate the top-left paste position to center the resized PNG at (center_x, center_y)
            paste_x = center_x - (new_fg_width // 2)
            paste_y = center_y - (new_fg_height // 2)
            
            position = (paste_x, paste_y)
            
            # Layer the transparent PNG onto the background using its alpha channel as mask
            background.paste(resized_foreground, position, resized_foreground)
            
            print(f"Pasted '{os.path.basename(png_path)}' at slot {i+1}/{num_pngs}")

        except FileNotFoundError:
            print(f"Warning: Foreground file not found: {png_path}. Skipping.")
        except Exception as e:
            print(f"Error processing {png_path}: {e}. Skipping.")


    # 6. Save the final image
    background.save(output_path, "PNG")
    print(f"\nSuccessfully created and saved image to {output_path}")


# --- Execution ---

# 1. Define image parameters
BG_DIM = 800
OUTPUT_FILE = "final_layered_border_image.png"

# 2. Setup mock files (replace this with your actual file loading logic)
mock_bg_file, mock_png_files = setup_mock_files(BG_DIM)

# 3. Run the main layering function
# scale_ratio=6 means the PNGs will be a max size of 800/6 (~133px)
layer_random_pngs_on_border(
    background_path=mock_bg_file, 
    foreground_paths=mock_png_files, 
    output_path=OUTPUT_FILE, 
    scale_ratio=6.0,
    padding=15
)
