import cv2
import os

def process_video(video_file_path, frame_interval, use_gpu=False, img_format='png'):
    cap = cv2.VideoCapture(video_file_path)
    frame_count = 0
    image_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if use_gpu:
            frame = cv2.cuda_GpuMat(frame)

        if frame_count % frame_interval == 0:
            img_file_path = os.path.join(export_folder, f"{output_name}_{image_count:04d}.{img_format}")

            if use_gpu:
                frame = frame.download()
                
            cv2.imwrite(img_file_path, frame)
            print(f"Frame {frame_count} saved as {img_file_path}")
            image_count += 1

        frame_count += 1

    cap.release()

# Get the script's directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Prompt the user for the video file name
video_file_name = input("Please enter the video file name to process: ")
video_file_path = os.path.join(script_dir, video_file_name)

if not os.path.isfile(video_file_path):
    print(f"Video file '{video_file_name}' not found in the script's directory.")
    exit()

# Prompt the user for the output name
output_name = input("Please enter the output name for the exported frames: ")

# Prompt the user for the frame interval in FPS, whether to use GPU, and the image format
frame_interval = int(input("Please enter the frame interval in FPS: "))
use_gpu = input("Would you like to use GPU for processing? (y/n): ").lower() == 'y'
img_format_choice = input("Please choose the image format for export: 1. JPG or 2. PNG: ")

if img_format_choice == '1':
    img_format = 'jpg'
elif img_format_choice == '2':
    img_format = 'png'
else:
    print("Invalid choice. Defaulting to PNG format.")
    img_format = 'png'

# Create an "Export" folder in the script's directory if it doesn't exist
export_folder = os.path.join(script_dir, 'Export')
if not os.path.exists(export_folder):
    os.makedirs(export_folder)

process_video(video_file_path, frame_interval, use_gpu, img_format)
print("Video processing completed.")
