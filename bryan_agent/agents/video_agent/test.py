import unittest
from pathlib import Path
import os
from bryan_agent.agents.video_agent.agent import VideoAgent
from bryan_agent.agents.base_agent.utils import organize_lrc
from bryan_agent.agents.base_agent.settings import settings

class TestVideoAgent(unittest.TestCase):
    def setUp(self):
        self.agent = VideoAgent(config={})
        test_lrc = "test/LoveStory-TaylorSwift.lrc"
        self.lyrics_text_file = Path(__file__).resolve().parent.parent.parent.parent / test_lrc

    def test_create_video(self):
        dic = organize_lrc(self.lyrics_text_file)
        self.agent.run(dic, self.lyrics_text_file)
        

if __name__ == '__main__':
    unittest.main()