import itertools
import sys
import time
import threading
import os
import cv2 
import json

def show_loading_animation(task, stop_loading, delay=0.5):
    emojis = itertools.cycle(["😊", "😐", "😢", "😂", "😴"])
    while not stop_loading[0]:
        sys.stdout.write(f"\r{task} {next(emojis)} {next(emojis)} {next(emojis)} {next(emojis)}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\r\033[K")

def log_status(agent_name, message):
    print(f"⌛️ {agent_name} is {message}, please be patient")

def log_completion(agent_name, stop_loading, loading_thread):
    stop_loading[0] = True
    loading_thread.join()
    print(f"✅ {agent_name} has finished its job")

def log_with_loading(agent_name, task, stop_loading):
    stop_loading[0] = False
    loading_thread = threading.Thread(target=show_loading_animation, args=(f"⌛️ {agent_name} is {task}, please be patient", stop_loading))
    loading_thread.start()
    return loading_thread 

def is_file_valid(file_path):
    try:
        if not os.path.isfile(file_path) or os.path.getsize(file_path) <= 0:
            return False
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print(f"❌ Error: The specified file could not be opened: {file_path}")
            return False
        cap.release()
        return True
    except Exception as e:
        print(f"❌ Error: An error occurred while trying to open the file: {file_path}")
        print(f"Exception: {e}")
        return False

def parse_response_content(response_content):
    try:
        cleaned_content = response_content.strip().replace('```', '').strip()
        return eval(cleaned_content)
    except (SyntaxError, json.JSONDecodeError) as e:
        sys.stdout.write(f"\r\033[K")
        raise ValueError(f"\nFailed to parse response content: {e}")

def get_full_lyrics(dic):
    return "\n".join([dic[i]["text"] for i in dic.keys()])