import os
import re
from PIL import Image
import pylrc
import json
import textwrap
import subprocess

def get_env(key: str, default_value=None):
    return os.environ.get(key, default_value)

def resize_image(image, width, height):
    return image.resize((width, height), Image.LANCZOS)

def load_lrc(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lrc_content = f.read()
    return pylrc.parse(lrc_content)

def load_parameters(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def wrap_text(text, width=100):
    wrapped_lines = textwrap.fill(text, width).split('\n')
    return wrapped_lines

def extract_number(file_name):
    matches = re.findall(r'\d+', file_name) 
    return tuple(map(int, matches)) if matches else (0,)

def get_output_path(input_file, output_filename):
    input_dir = os.path.dirname(input_file)
    return os.path.join(input_dir, output_filename)

def get_audio_duration(input_audio):
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_audio],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
        duration = float(result.stdout)
        return duration
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while getting audio duration: {e}")
        return None
    except ValueError as e:
        print(f"Could not convert duration to float: {e}")
        return None

def format_timestamp(seconds):
    if seconds is None:
        return "00 00"
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02} {seconds:02}"

def cleanup_files(directory):
    generated_files = ['final_visual_video.mp4', 'output_with_subtitles.mp4', 'cropped_subtitle.mp4', 'final_output_with_subtitles.mp4']
    for filename in generated_files:
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)