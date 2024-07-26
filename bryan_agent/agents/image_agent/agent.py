import os
from .tool import ImageGenerator
from bryan_agent.agents.base_agent.settings import settings

class ImageAgent:
    name = "Image Agent"

    def __init__(self, config):
        self.config = config
        self.stop_loading = False
        self.generator = ImageGenerator(self.name)

    def run(self, lyrics_text_file: str, resolution: str = settings["background_resolution"]):
        self.generator.generate_images(lyrics_text_file, resolution)
