import os
from .tool import LogoGenerator
from bryan_agent.agents.base_agent.settings import settings

class LogoAgent:
    name = "Logo Agent"

    def __init__(self, config):
        self.config = config
        self.stop_loading = False
        self.logo = LogoGenerator(self.name)

    def run(self, lrc: str, dic: dict, base_style_settings: dict):
        self.logo.generate_logo(lrc, dic, settings, base_style_settings)
