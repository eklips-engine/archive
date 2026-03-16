import cv2
import json
import os
import zipfile

def convert_to_kink(mp4_file, output_kink):
    # Create a directory to store frames
    frame_directory = 'vid'
    if not os.path.exists(frame_directory):
        os.makedirs(frame_directory)
    
    # Open the MP4 file
    cap = cv2.VideoCapture(mp4_file)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Extract frames from MP4 and save as PNGs
    for i in range(frame_count):
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(os.path.join(frame_directory, f"{i + 1}.png"), frame)
    
    # Close the MP4 file
    cap.release()
    
    # Create metadata
    metadata = {
        "EndFrame": frame_count,
        "StartFrame": 1
    }
    
    # Write metadata to JSON file
    with open(os.path.join(frame_directory, 'meta.json'), 'w') as json_file:
        json.dump(metadata, json_file)
    
    # Create the Kink file
    with zipfile.ZipFile(output_kink, 'w') as kink_file:
        # Add frame images to the Kink file
        for frame_image in os.listdir(frame_directory):
            if frame_image != 'meta.json':
                kink_file.write(os.path.join(frame_directory, frame_image), frame_image)
        
        # Add metadata JSON file to the Kink file
        kink_file.write(os.path.join(frame_directory, 'meta.json'), 'meta.json')
    
    # Remove the temporary directory with frame images
    os.rmdir(frame_directory)

# Example usage
mp4_file_path = input("MP4 filename: ")
output_kink_path = f"{mp4_file_path}.kink"
convert_to_kink(mp4_file_path, output_kink_path)
