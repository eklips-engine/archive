from PIL import Image
import pyperclip

def image_to_hex_string(image_path):
    # Open the image
    with Image.open(image_path) as img:
        # Ensure the image is in RGB mode
        img = img.convert('RGB')
        # Get the pixel data
        pixels = img.getdata()

        # Convert the pixel data to a hex string
        hex_string = ""
        for pixel in pixels:
            r, g, b = pixel
            hex_string += f"{r:02x}{g:02x}{b:02x}"

    # Remove the trailing space and return the string
    return hex_string.strip()

# Example usage
image_path = input("file: ")
hex_string = image_to_hex_string(image_path)
pyperclip.copy(hex_string)
print("Image data saved to Clipboard.")