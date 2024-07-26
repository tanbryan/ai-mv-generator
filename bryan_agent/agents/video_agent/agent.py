from .tool import CreateVideo
from bryan_agent.agents.base_agent.settings import settings

class VideoAgent:
    name = "Video Agent"

    def __init__(self, config):
        self.config = config
        self.stop_loading = False
        self.video = CreateVideo(self.name)

    def run(self, dic: dict, lrc: str):
        input_txt = self.video.write_input(lrc, dic)
        self.video.create_video(input_txt, lrc, settings)