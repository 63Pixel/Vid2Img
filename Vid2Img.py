import cv2
import os
import sys

def list_videos(script_dir, video_extensions):
    videos = []
    for file in os.listdir(script_dir):
        if file.lower().endswith(video_extensions):
            videos.append(file)
    return videos

def display_video_list(videos):
    print("Available videos:")
    for i, video in enumerate(videos, start=1):
        print(f"{i}. {video}")

def time_to_frames(time_str, fps):
    time_parts = time_str.split(':')
    seconds = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2])
    return seconds * fps

def process_video(video_file_path, frame_interval, start_time='', end_time='', img_format='png', output_name='', export_folder=''):
    cap = cv2.VideoCapture(video_file_path)
    frame_count = 0
    image_count = 0
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    start_frame = time_to_frames(start_time, fps) if start_time else 0
    end_frame = time_to_frames(end_time, fps) if end_time else int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while True:
        ret, frame = cap.read()

        if not ret or frame_count > end_frame:
            break

        if frame_count >= start_frame and frame_count % frame_interval == 0:
            img_file_path = os.path.join(export_folder, f"{output_name}_{image_count:04d}.{img_format}")
            cv2.imwrite(img_file_path, frame)
            print(f"Frame {frame_count} saved as {img_file_path}")
            image_count += 1

        frame_count += 1

    cap.release()

script_dir = os.path.dirname(os.path.realpath(__file__))
video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv')
videos = list_videos(script_dir, video_extensions)

if not videos:
    print("No video files found in the script's directory.")
    sys.exit()

display_video_list(videos)

video_choice = int(input("Please enter the number of the video you want to process: "))
if 0 < video_choice <= len(videos):
    video_file_name = videos[video_choice - 1]
else:
    print("Invalid choice. Exiting.")
    exit()

video_file_path = os.path.join(script_dir, video_file_name)
output_name = input("Please enter the output name for the exported frames: ")
frame_interval = int(input("Please enter the frame interval in FPS: "))

img_format_choice = input("Please choose the image format for export: 1. JPG or 2. PNG: ")

if img_format_choice == '1':
    img_format = 'jpg'
elif img_format_choice == '2':
    img_format = 'png'
else:
    print("Invalid choice. Defaulting to PNG format.")
    img_format = 'png'

start_time_str = input("Please enter the start time for the extraction (HH:MM:SS), or press Enter to start from the beginning: ")
end_time_str = input("Please enter the end time for the extraction (HH:MM:SS), or press Enter to process until the end: ")

export_folder = os.path.join(script_dir, 'Export')
if not os.path.exists(export_folder):
    os.makedirs(export_folder)

process_video(video_file_path, frame_interval, start_time_str, end_time_str, img_format, output_name, export_folder)
print("Video processing completed.")
