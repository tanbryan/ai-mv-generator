import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from bryan_agent.agents.style_agent.agent import StyleAgent
from bryan_agent.utils.io import load_parameters
from bryan_agent.agents.base_agent.utils import organize_lrc

class TestStyleAnalyzeAgent(unittest.TestCase):
    def setUp(self):
        self.config = {}
        self.agent = StyleAgent(self.config)
        test_lrc = "test/LoveStory-TaylorSwift.lrc"
        self.lyrics_text_file = Path(__file__).resolve().parent.parent.parent.parent / test_lrc
        # self.customization = "vibrant colors, realistic style"
    
    def test_analyze_style(self):
        self.dic = organize_lrc(self.lyrics_text_file)
        base_style_settings = self.agent.run(self.dic)
        print(base_style_settings)

if __name__ == '__main__':
    unittest.main()