import os
import sys
import openai
import time
import threading
import logging
from bryan_agent.utils.tool import log_with_loading, log_completion, is_file_valid
from .settings import settings
from .utils import organize_lrc, start_activity_checker
from bryan_agent.agents.lyric_analyze_agent.agent import LyricAnalyzeAgent
from bryan_agent.agents.style_agent.agent import StyleAgent
from bryan_agent.agents.prompt_agent.agent import PromptAgent
from bryan_agent.agents.image_agent.agent import ImageAgent
from bryan_agent.agents.logo_agent.agent import LogoAgent
from bryan_agent.agents.video_agent.agent import VideoAgent
from .utils import load_status, save_status, load_results, save_results

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class BaseAgent:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.agents = []
        self.stop_loading = [False]
        self.status = load_status()
        self.results = {}
        self.last_activity_time = time.time()

    def add_agent(self, agent):
        self.agents.append(agent)

    def update_status(self, agent):
        self.status[agent.name] = True
        save_status(self.status)

    def check_activity(self):
        while True:
            if time.time() - self.last_activity_time > 600:  # Check if more than 10 min
                logging.warning("❗️ No activity detected for a long time. Please rerun the program.")
                os._exit(0)
            time.sleep(10)

    def run(self, lrc, mp3):
        start_activity_checker(self)

        results_file = os.path.join(os.path.dirname(lrc), 'results.json')
        self.results = load_results(results_file)
        dic = organize_lrc(lrc)

        for agent in self.agents:
            if not self.status.get(agent.name, False):
                try:
                    self.run_agent(agent, dic, lrc, mp3)
                    self.last_activity_time = time.time()
                except Exception as e:
                    logging.error(f"❌ An error occurred while running {agent.__class__.__name__}: {e}", exc_info=True)
                else:
                    self.update_status(agent)
                    save_results(self.results, results_file)
                finally:
                    save_status(self.status)

    def run_agent(self, agent, dic, lrc, mp3):
        if isinstance(agent, LyricAnalyzeAgent):
            self.run_lyric_analyze_agent(agent, dic)
        elif isinstance(agent, StyleAgent):
            self.run_style_agent(agent, dic)
        elif isinstance(agent, PromptAgent):
            self.run_prompt_agent(agent, lrc, dic)
        elif isinstance(agent, ImageAgent):
            self.run_image_agent(agent, lrc)
        elif isinstance(agent, LogoAgent):
            self.run_logo_agent(agent, lrc, dic)
        elif isinstance(agent, VideoAgent):
            self.run_video_agent(agent, dic, lrc, mp3)

    def run_lyric_analyze_agent(self, agent, dic):
        grouped_lyrics, grouped_ids = agent.run(dic)
        self.results['grouped_lyrics'] = grouped_lyrics
        self.results['grouped_ids'] = grouped_ids

    def run_style_agent(self, agent, dic):
        base_style_settings = agent.run(dic)
        self.results['base_style_settings'] = base_style_settings

    def run_prompt_agent(self, agent, lrc, dic):
        agent.run(lrc, dic, self.results.get('grouped_ids', None), self.results.get('base_style_settings', None))

    def run_image_agent(self, agent, lrc):
        agent.run(lrc, settings["background_resolution"])

    def run_logo_agent(self, agent, lrc, dic):
        agent.run(lrc, dic, self.results.get('base_style_settings', None))

    def run_video_agent(self, agent, dic, lrc, mp3):
        agent.run(dic, lrc, mp3)
