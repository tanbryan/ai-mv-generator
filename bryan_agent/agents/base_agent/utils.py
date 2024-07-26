# utils.py
from bryan_agent.utils.io import load_lrc

import time
import sys
import threading
import os
import json


def organize_lrc(lyrics_text_file):
    dic = {}
    subs = load_lrc(lyrics_text_file)
    for i, sub in enumerate(subs):
        time = sub.time
        text = sub.text.replace("'", r"\'")
        duration = subs[i+1].time - sub.time if i < len(subs) - 1 else 10
        dic[i] = {
            "time": time,
            "text": text,
            "duration": duration
        }
    return dic

BASE_AGENT_DIR = os.path.join(os.path.dirname(__file__), 'status')
STATUS_FILE = os.path.join(BASE_AGENT_DIR, 'agent_status.json')

def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_status(status):
    os.makedirs(BASE_AGENT_DIR, exist_ok=True)
    with open(STATUS_FILE, 'w') as file:
        json.dump(status, file, indent=4)

def load_results(results_file):
    if os.path.exists(results_file):
        with open(results_file, 'r') as file:
            return json.load(file)
    return {}

def save_results(results, results_file):
    with open(results_file, 'w') as file:
        json.dump(results, file, indent=4)


def start_activity_checker(base_agent):
    activity_checker = threading.Thread(target=base_agent.check_activity)
    activity_checker.daemon = True
    activity_checker.start()




