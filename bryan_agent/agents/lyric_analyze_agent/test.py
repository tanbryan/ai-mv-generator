import unittest
from pathlib import Path
from bryan_agent.agents.lyric_analyze_agent.agent import LyricAnalyzeAgent
from bryan_agent.agents.base_agent.utils import organize_lrc


class TestLyricAnalyzeAgent(unittest.TestCase):
    def setUp(self):
        self.agent = LyricAnalyzeAgent(config={})
        test_lrc = "test/LoveStory-TaylorSwift.lrc"
        self.lyrics_text_file = Path(__file__).resolve().parent.parent.parent.parent / test_lrc
    
    def test_analyze_lrc(self):
        dic = organize_lrc(self.lyrics_text_file)
        grouped_lyrics, grouped_ids = self.agent.analyzer.analyze_lrc(dic)

        self.assertIsInstance(grouped_lyrics, dict)
        self.assertGreater(len(grouped_lyrics), 0)

        for group_id, lyrics in grouped_lyrics.items():
            self.assertIsInstance(group_id, int)
            self.assertIsInstance(lyrics, list)
            self.assertGreater(len(lyrics), 0)
            for line in lyrics:
                self.assertIsInstance(line, str)
                self.assertGreater(len(line.strip()), 0)

        self.assertIsInstance(grouped_ids, list)
        self.assertGreater(len(grouped_ids), 0)
        for group in grouped_ids:
            self.assertIsInstance(group, list)
            self.assertGreater(len(group), 0)
            for id in group:
                self.assertIsInstance(id, int)
                self.assertGreaterEqual(id, 0)

        print(grouped_lyrics)
        print(grouped_ids)

if __name__ == '__main__':
    unittest.main()
