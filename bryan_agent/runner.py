import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bryan_agent.agents.base_agent.agent import BaseAgent
from bryan_agent.agents.lyric_analyze_agent.agent import LyricAnalyzeAgent
from bryan_agent.agents.style_agent.agent import StyleAgent
from bryan_agent.agents.prompt_agent.agent import PromptAgent
from bryan_agent.agents.image_agent.agent import ImageAgent
from bryan_agent.agents.logo_agent.agent import LogoAgent
from bryan_agent.agents.video_agent.agent import VideoAgent

def main(lyrics_text_file, audio_file):
    base_agent = BaseAgent("Base Agent")
    base_agent.add_agent(LyricAnalyzeAgent({}))
    base_agent.add_agent(StyleAgent({}))
    base_agent.add_agent(PromptAgent({}))
    base_agent.add_agent(ImageAgent({}))
    base_agent.add_agent(LogoAgent({}))
    base_agent.add_agent(VideoAgent({}))

    base_agent.run(lyrics_text_file, audio_file)

if __name__ == '__main__':
    ### replace the path with the path to the lyrics file
    lrc_file_complete_path = "/path/to/your/.lrc"
    mp3_file_complete_path = "/path/to/your/.mp3"
    main(lrc_file_complete_path, mp3_file_complete_path)


