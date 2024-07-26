import unittest
from unittest.mock import patch
from pathlib import Path
from bryan_agent.agents.image_agent.agent import ImageAgent
from bryan_agent.agents.base_agent.settings import settings
# from bryan_agent.agents.image_agent.test_prompt import sample_prompt

class TestImageAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ImageAgent(config={})
    

    @patch('builtins.input', side_effect=['n', '1_1', 'y'])
    def test_generate_images(self, mock_input):

        test_lrc = "test/LoveStory-TaylorSwift.lrc"
        lyrics_text_file = Path(__file__).resolve().parent.parent.parent.parent / test_lrc

        self.agent.run(lyrics_text_file, settings["background_resolution"])

if __name__ == '__main__':
    unittest.main()
