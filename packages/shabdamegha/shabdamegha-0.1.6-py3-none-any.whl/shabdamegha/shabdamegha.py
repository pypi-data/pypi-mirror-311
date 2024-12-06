import os
import platform
import random
from PIL import Image, ImageDraw, ImageOps
import uharfbuzz as hb
import freetype
import numpy as np
import secrets

def _get_font_paths():
    system_platform = platform.system().lower()
    
    if system_platform == 'darwin':  # macOS
        font_paths = [
            "/System/Library/Fonts/NotoSansOriya.ttc",  # Example path on macOS
        ]
    elif system_platform == 'windows':  # Windows
        font_paths = [
            "C:/Windows/Fonts/Kalinga.ttf",  # Example path on Windows
        ]
    elif system_platform == 'linux':  # Linux (Ubuntu, etc.)
        font_paths = [
            #todo
            "/usr/share/fonts/truetype/lohit-oriya/Lohit-Odia.ttf"
        ]
    else:
        raise ValueError("Unsupported Operating System")
    
    return font_paths

def _get_platform_specific_paddding():
    platform_specific_padding_and_fontfactor = (0,0)
    system_platform = platform.system().lower()
    
    if system_platform == 'darwin':  # macOS
        platform_specific_padding_and_fontfactor = (15,64)
    elif system_platform == 'windows':  # Windows
        platform_specific_padding_and_fontfactor = (0,64)
    elif system_platform == 'linux':  # Linux (Ubuntu, etc.)
        platform_specific_padding_and_fontfactor = (10,54)

    return platform_specific_padding_and_fontfactor



# Function to render text using HarfBuzz and FreeType
def _render_text(text, font_path, font_size, color, platform_specific_padding_and_fontfactor):
    """
    Renders text using HarfBuzz and FreeType.

    Args:
        text (str): The text to render.
        font_path (str): The file path to the font.
        font_size (int): The size of the font in points.
        color (tuple): A tuple of RGB values (0-255) representing the text color.
        platform_specific_padding_and_fontfactor (tuple): Platform specific padding in pixels and font factor

    Returns:
        PIL.Image.Image: The rendered text as a PIL image.
        None: If an error occurs during rendering.
    """
    try:
        extra_padding = platform_specific_padding_and_fontfactor[0]
        font_factor = platform_specific_padding_and_fontfactor[1]

        # Load font
        face = freetype.Face(font_path)
        face.set_char_size(font_size * font_factor)

        # Initialize HarfBuzz
        with open(font_path, "rb") as font_file:
            font_data = font_file.read()
        hb_blob = hb.Blob(font_data)
        hb_face = hb.Face(hb_blob, 0)
        hb_font = hb.Font(hb_face)
        hb_font.scale = (face.size.ascender, face.size.ascender)

        # Create HarfBuzz buffer and shape the text
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(hb_font, buf)

        # Calculate dimensions
        total_width, max_top, max_bottom = 0, 0, 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            glyph_index = info.codepoint
            face.load_glyph(glyph_index, freetype.FT_LOAD_RENDER)
            bitmap = face.glyph.bitmap
            top = face.glyph.bitmap_top
            bottom = bitmap.rows - top
            max_top = max(max_top, top)
            max_bottom = max(max_bottom, bottom)
            total_width += pos.x_advance // font_factor

        canvas_width, canvas_height = total_width, max_top + max_bottom
        
        text_image = Image.new("RGBA", (canvas_width + extra_padding, canvas_height), (255, 255, 255, 0))
        #text_image = Image.new("RGBA", (canvas_width + extra_padding, canvas_height), (0, 0, 0, 255)) #black background

        pen_x, pen_y = 0, max_top
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            glyph_index = info.codepoint
            face.load_glyph(glyph_index, freetype.FT_LOAD_RENDER)
            bitmap = face.glyph.bitmap

            # Skip empty glyphs
            if bitmap.width == 0 or bitmap.rows == 0:
                pen_x += pos.x_advance // font_factor
                continue

            # Create transparent glyph
            glyph_image = Image.frombytes("L", (bitmap.width, bitmap.rows), bytes(bitmap.buffer), "raw", "L", 0, 1)
            transparent_glyph = Image.new("RGBA", glyph_image.size, (color[0], color[1], color[2], 0))
            for px in range(glyph_image.width):
                for py in range(glyph_image.height):
                    alpha = glyph_image.getpixel((px, py))
                    transparent_glyph.putpixel((px, py), (color[0], color[1], color[2], alpha))

            # Paste glyph into the text image
            text_image.paste(transparent_glyph, (pen_x + face.glyph.bitmap_left, pen_y - face.glyph.bitmap_top), transparent_glyph)
            pen_x += pos.x_advance // font_factor

        return text_image

    except Exception as e:
        print(f"Error rendering text '{text}' with font '{font_path}': {e}")
        return None

# Function to draw word cloud with a radiating placement and canvas expansion
def draw_shabdamegha(   data, 
                        font_file_paths=None,
                        save_file_path="wordcloud.png",
                        show_image=True,
                        background_RGBA_color=(255, 255, 255, 0),
                        initial_width=800, initial_height=800,
                        padding=5,
                        expanding_factor=2,
                        orientations=[0,90],
                        colors=True):
    """
    Generates a word cloud with radiating word placement and adaptive canvas expansion. 
    The function supports input in string, list, or dictionary format and allows extensive customization.

    Args:
        data (str | list | dict): 
            Input data for the word cloud. 
            - If `str`, words are split by whitespace and assigned random weights between 1 to 20.
            - If `list`, each item is treated as a word with random weights between 1 to 20
            - If `dict`, keys are words and values are their weights.
        font_file_paths (list of str, optional): 
            List of file paths to font files for rendering text. If `None`, 
            system fonts are used (Kalinga in Windows, NotoSansOriya in Mac, Lohit-Oriya in Ubuntu). Defaults to `None`.
        save_file_path (str, optional): 
            Path to save the generated word cloud image. Defaults to "wordcloud.png".
        show_image (bool, optional): 
            If `True`, displays the generated word cloud using the default 
            image viewer. Defaults to `True`.
        background_RGBA_color (tuple of int, optional): 
            Background color of the word cloud in RGBA format. Defaults to transparent 
            white (255, 255, 255, 0).
        initial_width (int, optional): 
            Initial width of the canvas in pixels. Defaults to 800.
        initial_height (int, optional): 
            Initial height of the canvas in pixels. Defaults to 800.
        padding (int, optional): 
            Padding around each word in pixels. Defaults to 5.
        expanding_factor (float, optional): 
            Factor by which the canvas size is increased as 50 multplied by expanding_factor, if words do not fit. Defaults to 2.
        orientations (list of int, optional): 
            List of orientations (in degrees) for word placement. Defaults to [0, 90].
        colors (bool | list of tuple, optional): 
            Specifies the text colors. 
            - If `True`, random RGB colors are used.
            - If `None`, black is used.
            - If a list of RGB tuples is provided, colors are sampled from the list.
            Defaults to `True`.

    Raises:
        TypeError: If `data` is not a string, list, or dictionary.

    Returns:
        None

    Saves:
        The word cloud image to the specified `save_file_path`.

    Example:
        >>> draw_shabdamegha(
        ...     data="ଶ୍ରୀଜଗନ୍ନାଥ ଓଡ଼ିଶା ଦୁର୍ଗାପୂଜା କଟକ ପୁରୀ ଭୁବନେଶ୍ୱର ନବରଙ୍ଗପୁର କୋରାପୁଟ ମୟୂରଭଞ୍ଜ",
        ...     save_file_path="example_wordcloud.png",
        ...     orientations=[-90, -60, -30, 0, 30, 60, 90]
        ... )

        >>> districts_of_odisha = {
        ... "ଅନୁଗୋଳ": 13, "କଟକ": 8, "କଳାହାଣ୍ଡି": 16, "କନ୍ଧମାଳ": 16, "କେନ୍ଦୁଝର": 17, "କେନ୍ଦ୍ରାପଡ଼ା": 5, "କୋରାପୁଟ": 18, "ଖୋର୍ଦ୍ଧା": 6,
        ... "ଗଜପତି": 8, "ଗଞ୍ଜାମ": 16, "ଜଗତସିଂହପୁର": 4, "ଝାରସୁଗୁଡ଼ା": 4, "ଢେଙ୍କାନାଳ": 9, "ଦେବଗଡ଼": 6, "ନବରଙ୍ଗପୁର": 11, "ନୟାଗଡ଼": 8,
        ... "ନୂଆପଡ଼ା": 8, "ପୁରୀ": 6, "ବରଗଡ଼": 12, "ବଲାଙ୍ଗୀର": 13, "ବାଲେଶ୍ୱର": 7, "ବୌଦ୍ଧ": 7, "ଭଦ୍ରକ": 5, "ମୟୂରଭଞ୍ଜ": 21, "ମାଲକାନଗିରି": 12,
        ... "ଯାଜପୁର": 6, "ରାୟଗଡ଼ା": 14, "ସମ୍ବଲପୁର": 13, "ସୁବର୍ଣ୍ଣପୁର": 5, "ସୁନ୍ଦରଗଡ଼": 19
        ... }
        >>> draw_shabdamegha(districts_of_odisha, colors=[(148, 0, 211), (0, 0, 255), (5, 108, 8), (255, 127, 0), (255, 0, 0)])

        >>> words = ["ଶ୍ଳେଷ", "ସନ୍ନିବେଶ", "ଶୃଙ୍ଖଳା", "ଚାଞ୍ଛିବା", "ଝୁଣ୍ଟିଆ", "ରୋମନ୍ଥନ", "କୁମ୍ଭୀର", "ବାଗ୍ଦେବୀ", "କଚ୍ଛପ", "ଖଡ୍ଗଧାରି", "ଅକ୍ଷୁର୍ଣ୍ଣ", "ଉଡ୍ଡୀୟମାନ", "ଉତ୍କଣ୍ଠା", "ସମ୍ଭତ୍ସର", "ଉଦ୍ଘାଟନ", "ଉଦ୍ଦେଶ୍ୟ", "ଉଦ୍ଧାର", "ମୁଦ୍ଗର", "ଅଦ୍ଭୁତ", "ପିପ୍ପଳୀ", "ଅପ୍ସରା", "କୁବ୍ଜ", "ତିବ୍ବତ", "ସମ୍ମାନ", "ବଳ୍କଳ", "ଫାଲ୍ଗୁନ", "ସଂକଳ୍ପ", " ବଲ୍ଲଭ", "ଶିରଶ୍ଛେଦ", "ନିଷ୍ପୀଡନ", "ମାହାତ୍ମ୍ୟ", "ନିର୍ଦ୍ଧାରିତ", "ପଶ୍ଚିମ", "ପରିଷ୍କାର", "ଆସ୍ଫାଳନ", "ସମ୍ପ୍ରଦାନ", "ନିଷ୍ପ୍ରୟୋଜନ"]
        >>> draw_shabdamegha(words, font_file_paths=['C:/Windows/Fonts/Kalinga.ttf', 'C:/Windows/Fonts/nirmala.ttc'], colors=True)
        
    """
    

    # Check the type of input
    if isinstance(data, str):
        # If it's a string, split by whitespace and assign random weights
        words = data.split()  # Split the string into words
        # Create a dictionary with random weights between 1 and 20 for each word
        data = {word: random.randint(1, 20) for word in words}
        # Create a dictionary with weights sampled from a normal distribution with mean=10 and std=5
        #data = {word: max(1, int(random.gauss(10, 5))) for word in words}  # Ensure the weight is at least 1

    elif isinstance(data, list):
        # If it's a list, treat each item as a word and assign random weights
        data = {item: random.randint(1, 20) for item in data}
        # If it's a list, treat each item as a word and assign random weights from a normal distribution
        #data = {item: max(1, int(random.gauss(10, 5))) for item in data}  # Ensure the weight is at least 1

    elif isinstance(data, dict):
        # If it's already a dictionary, use it as is
        pass
    else:
        # If it's not a string, list, or dictionary, raise an error
        raise TypeError("Input must be a string, list, or dictionary")

    # If fonts not specified by user, use default ones
    # Get the font paths based on the operating system
    if font_file_paths is None:
        font_file_paths = _get_font_paths()

    platform_specific_padding_and_fontfactor = _get_platform_specific_paddding()

    image_width, image_height = initial_width, initial_height

    last_color = (255,0,0)
    while True:
        word_cloud_image = Image.new("RGBA", (image_width, image_height), background_RGBA_color)
        center_x, center_y = image_width // 2, image_height // 2
        used_positions = []
        all_placed = True  # Flag to track if all words are placed

        words_with_frequencies = sorted(data.items(), key=lambda x: -x[1])  # Place larger words first

        for word, frequency in words_with_frequencies:
            font_path = random.choice(font_file_paths)
            font_size = frequency * 10 + 20
            
            if colors == None or colors == False:
                color = (0, 0, 0)
            elif colors == True:
                color = list(np.random.choice(range(256), size=3))
                if (color == last_color):
                    color = list(np.random.choice(range(256), size=3))
                    last_color = color
            else:
                color = secrets.choice(colors)
                if (color == last_color):
                    color = secrets.choice(colors)
                    last_color = color

            orientation = secrets.choice(orientations)

            rendered_text = _render_text(word, font_path, font_size, color, platform_specific_padding_and_fontfactor)
            if rendered_text is None:
                continue

            if orientation != 0:
                rendered_text = rendered_text.rotate(orientation, expand=True)

            text_width, text_height = rendered_text.size
            padded_width, padded_height = text_width + padding, text_height + padding

            for radius in range(0, max(image_width, image_height), 10):
                angle_step = 2 if radius > 50 else 5  # Use smaller angular steps for larger radii
                for angle in range(0, 360, angle_step):  # Try all angles at the given radius
                    x = int(center_x + radius * np.cos(np.radians(angle)) - padded_width // 2)
                    y = int(center_y + radius * np.sin(np.radians(angle)) - padded_height // 2)

                    bbox = (x, y, x + padded_width, y + padded_height)
                    if (bbox[0] < 0 or bbox[1] < 0 or bbox[2] > image_width or bbox[3] > image_height):
                        continue  # Skip if out of bounds

                    if all(pos[0] >= bbox[2] or pos[2] <= bbox[0] or pos[1] >= bbox[3] or pos[3] <= bbox[1] for pos in used_positions):
                        used_positions.append(bbox)
                        word_cloud_image.paste(rendered_text, (x + padding // 2, y + padding // 2 ), rendered_text)
                        break
                else:
                    continue
                break
            else:
                all_placed = False
                break

        if all_placed:
            break
        else:
            image_width += int(50 * expanding_factor)
            image_height += int(50 * expanding_factor)

    if show_image == True:
        word_cloud_image.show()
    word_cloud_image.save(save_file_path)
    #print(f"Word cloud saved to {save_file_path}, final size: {image_width}x{image_height}")