import os
import re
from PIL import Image
import pylrc
import json
import textwrap

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
    match = re.search(r'\d+', file_name) 
    return int(match.group()) if match else 0 