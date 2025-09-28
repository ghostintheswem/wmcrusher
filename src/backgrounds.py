import random
import os
from PIL import Image, ImageDraw, ImageFont

def layer_png_with_border(background_path, foreground_path, output_path, border_size_pixels):
    """
    Layers a PNG image (foreground) onto a square background image.
    The PNG is scaled to be as large as possible within a frame,
    maintaining its aspect ratio and not touching the border.

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
            bg_width, bg_height = min(bg_width, bg_height), min(bg_width, bg_height)
            #  print("Error: Background image is not perfectly square. Exiting.")
            #  return
             
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
        png_path = "resources/stuff/" + selected_pngs[i]
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
foreground_paths = ["decoration100.png","decoration101.png","decoration105.png","decoration106.png","decoration107.png","decoration110.png","decoration111.png","decoration112.png","decoration115.png","decoration116.png","decoration118.png","decoration119.png","decoration120.png","decoration121.png","decoration122.png","decoration124.png","decoration125.png","decoration126.png","decoration127.png","decoration128.png","decoration131.png","decoration135.png","decoration136.png","decoration140.png","decoration142.png","decoration145.png","decoration148.png","decoration150.png","decoration151.png","decoration153.png","decoration154.png","decoration155.png","decoration158.png","decoration163.png","decoration170.png","decoration171.png","decoration172.png","decoration173.png","decoration174.png","decoration176.png","decoration177.png","decoration182.png","decoration192.png","decoration198.png","decoration203.png","decoration204.png","decoration206.png","decoration213.png","decoration214.png","decoration219.png","decoration228.png","decoration231.png","decoration239.png","decoration248.png","decoration253.png","decoration261.png","decoration262.png","decoration278.png","decoration279.png","decoration280.png","decoration281.png","decoration282.png","decoration283.png","decoration284.png","decoration285.png","decoration286.png","decoration287.png","decoration288.png","decoration289.png","decoration290.png","decoration291.png","decoration292.png","decoration293.png","decoration294.png","decoration295.png","decoration296.png","decoration297.png","decoration298.png","decoration299.png","decoration300.png","decoration301.png","decoration302.png","decoration303.png","decoration304.png","decoration305.png","decoration306.png","decoration307.png","decoration308.png","decoration309.png","decoration310.png","decoration311.png","decoration312.png","decoration313.png","decoration314.png","decoration315.png","decoration316.png","decoration317.png","decoration318.png","decoration319.png","decoration321.png","decoration322.png","decoration323.png","decoration324.png","decoration325.png","decoration326.png","decoration327.png","decoration328.png","decoration329.png","decoration330.png","decoration331.png","decoration332.png","decoration333.png","decoration334.png","decoration335.png","decoration336.png","decoration337.png","decoration338.png","decoration339.png","decoration340.png","decoration342.png","decoration343.png","decoration344.png","decoration345.png","decoration346.png","decoration347.png","decoration348.png","decoration349.png","decoration350.png","decoration351.png","decoration352.png","decoration353.png","decoration354.png","decoration355.png","decoration356.png","decoration357.png","decoration358.png","decoration359.jpg","decoration360.png","decoration361.png","decoration362.png","decoration363.png","decoration364.png","decoration365.png","decoration366.png","decoration367.png","decoration368.png","decoration369.png","decoration370.png","decoration371.png","decoration372.png","decoration373.png","decoration374.png","decoration375.png","decoration376.png","decoration377.png","decoration77.png","decoration83.png","decoration95.png","decoration98.png","paper0.png",]
background_paths = ["decoration0.png","decoration102.png","decoration103.png","decoration104.png","decoration134.png","decoration147.png","decoration152.png","decoration161.png","decoration167.png","decoration178.png","decoration183.png","decoration185.png","decoration191.png","decoration194.png","decoration215.png","decoration216.png","decoration217.png","decoration225.png","decoration244.png","decoration255.png","decoration40.png","decoration41.png","decoration45.png","decoration46.png","decoration47.png","decoration48.png","decoration57.png","decoration69.png","decoration78.png","decoration87.png","decoration88.png","decoration93.png","decoration94.png","decoration96.png","decoration97.png","decoration99.png","paper1.png","paper2.png","paper3.png","paper4.png","paper5.png","paper6.png",]
BACKGROUND_paths = ["background0.png","background1.png","background10.jpg","background11.jpg","background12.jpg","background13.jpg","background14.jpg","background15.jpg","background16.jpg","background17.jpg","background18.jpg","background19.jpg","background2.png","background20.jpg","background21.png","background22.png","background23.jpg","background24.jpg","background25.png","background26.png","background27.png","background3.jpg","background4.jpg","background5.jpg","background6.jpg","background7.jpg","background8.jpg","background9.jpg",]
BG_DIM = 800
OUTPUT_FILE = "final_layered_border_image.png"

def create_image():
    layer_png_with_border(
        background_path=f"resources/square/{random.choice(BACKGROUND_paths)}", 
        foreground_path=f"resources/paper/{random.choice(background_paths)}", 
        output_path="test_layered_image.png", 
        border_size_pixels=20
    )
    
    # 3. Run the main layering function
    # scale_ratio=6 means the PNGs will be a max size of 800/6 (~133px)

    
    layer_random_pngs_on_border(
        background_path= "test_layered_image.png", 
        foreground_paths=foreground_paths, 
        output_path=OUTPUT_FILE, 
        scale_ratio=6.0,
        padding=15
    )

    return OUTPUT_FILE

if __name__ == "__main__":
    # 1. Define image parameters

    layer_png_with_border(
        background_path=f"resources/square/{random.choice(BACKGROUND_paths)}", 
        foreground_path=f"resources/paper/{random.choice(background_paths)}", 
        output_path="test_layered_image.png", 
        border_size_pixels=20
    )
    
    # 3. Run the main layering function
    # scale_ratio=6 means the PNGs will be a max size of 800/6 (~133px)

    
    layer_random_pngs_on_border(
        background_path= "test_layered_image.png", 
        foreground_paths=foreground_paths, 
        output_path=OUTPUT_FILE, 
        scale_ratio=6.0,
        padding=15
    )