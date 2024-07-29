import unittest
from unittest.mock import patch
from pathlib import Path
import subprocess
from PIL import Image
import json
import librosa

class TestMain(unittest.TestCase):
    def setUp(self):
        self.lyrics_text_file = Path("test/LoveStory-TaylorSwift.lrc")
        self.audio_file = Path("test/LoveStory-TaylorSwift.mp3")
        self.results_file = self.lyrics_text_file.parent / "results.json"
        self.prompts_file = self.lyrics_text_file.parent / "generated_prompts.json"
        self.background_images_dir = self.lyrics_text_file.parent / "background_images"
        self.logo_file = self.lyrics_text_file.parent / "logo.png"
        self.agent_status_file = self.lyrics_text_file.parent / "agent_status.json"
        
        if self.results_file.exists():
            os.remove(self.results_file)
        if self.prompts_file.exists():
            os.remove(self.prompts_file)
        if self.background_images_dir.exists():
            for file in os.listdir(self.background_images_dir):
                os.remove(self.background_images_dir / file)
        if self.logo_file.exists():
            os.remove(self.logo_file)
        if self.agent_status_file.exists():
            os.remove(self.agent_status_file)
        
    @patch('builtins.input', side_effect=['', '', 'n', '1_1', 'y'])  # Mock input for StyleAgent and ImageAgent
    def test_base_agent(self, mock_input):
        # Run the runner.py script
        result = subprocess.run(
            ["python", "runner.py"],
            cwd="../bryan_agent", 
            capture_output=True, text=True
        )

        if result.returncode != 0:
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)
        
        self.assertEqual(result.returncode, 0, msg="runner.py did not execute successfully")

        with open(self.results_file, 'r') as file:
            results = json.load(file)
        
        # check LyricAnalyzeAgent output
        self.assertIn('grouped_lyrics', results)
        self.assertIsInstance(results['grouped_lyrics'], dict)
        self.assertGreater(len(results['grouped_lyrics']), 0)

        for group_id, lyrics in results['grouped_lyrics'].items():
            self.assertIsInstance(group_id, int)
            self.assertIsInstance(lyrics, list)
            self.assertGreater(len(lyrics), 0)
            for line in lyrics:
                self.assertIsInstance(line, str)
                self.assertGreater(len(line.strip()), 0)

        self.assertIn('grouped_ids', results)
        self.assertIsInstance(results['grouped_ids'], list)
        self.assertGreater(len(results['grouped_ids']), 0)
        for group in results['grouped_ids']:
            self.assertIsInstance(group, list)
            self.assertGreater(len(group), 0)
            for id in group:
                self.assertIsInstance(id, int)
                self.assertGreaterEqual(id, 0)

        # check StyleAgent output
        self.assertIn('base_style_settings', results)
        self.assertIsInstance(results['base_style_settings'], str)
        self.assertGreater(len(results['base_style_settings']), 0)

        # check PromptAgent output
        with open(self.prompts_file, 'r') as file:
            prompts = json.load(file)
        
        self.assertIsInstance(prompts, list)
        self.assertGreater(len(prompts), 0)
        for section in prompts:
            self.assertIsInstance(section, list)
            self.assertGreater(len(section), 0)
            for prompt in section:
                self.assertIsInstance(prompt, str)
                self.assertGreater(len(prompt.strip()), 0)
        
        # Check that the number of prompts
        self.assertEqual(len(prompts), len(results['grouped_ids']))

        # check the number of generated images
        generated_images = list(self.background_images_dir.glob("*.png"))
        total_prompts = sum(len(section) for section in prompts)
        self.assertEqual(len(generated_images), total_prompts)

        # check the logo can be opened
        self.assertTrue(self.logo_file.exists())
        try:
            img = Image.open(self.logo_file)
            img.verify() 
        except (IOError, SyntaxError) as e:
            self.fail(f"Logo verification failed: {e}")

        # Verify the input.txt duration matches the mp3 file duration
        input_txt = self.lyrics_text_file.parent / "input.txt"
        with open(input_txt, 'r') as file:
            lines = file.readlines()

        total_duration = sum(float(lines[i+1].split(' ')[1].strip()) for i in range(0, len(lines), 2))
        mp3_duration = librosa.get_duration(filename=str(self.audio_file))
        self.assertAlmostEqual(total_duration, mp3_duration, places=1)

        # check background.mp4 is openable and check the length
        background_video = self.lyrics_text_file.parent / "background.mp4"
        self.assertTrue(background_video.exists())
        try:
            background_info = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(background_video)], capture_output=True, text=True)
            background_duration = float(background_info.stdout.strip())
            self.assertAlmostEqual(background_duration, mp3_duration, places=1)
        except subprocess.CalledProcessError as e:
            self.fail(f"background.mp4 could not be opened or is corrupted: {e}")

        # check the final output video is openable and has valid audio
        final_output_video = self.lyrics_text_file.parent / f"{self.audio_file.stem}.mp4"
        self.assertTrue(final_output_video.exists())
        try:
            final_info = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(final_output_video)], capture_output=True, text=True)
            final_duration = float(final_info.stdout.strip())
            self.assertAlmostEqual(final_duration, mp3_duration, places=1)

            # Check if final output has valid audio
            audio_check = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type", "-of", "default=noprint_wrappers=1:nokey=1", str(final_output_video)], capture_output=True, text=True)
            self.assertIn("audio", audio_check.stdout.strip())
        except subprocess.CalledProcessError as e:
            self.fail(f"Final output video could not be opened or is corrupted: {e}")

        # check agent_status.json
        status_file = self.lyrics_text_file.parent / "base_agent" / "status" / "agent_status.json"
        with open(status_file, 'r') as file:
            status = json.load(file)

        for agent_name in ['Lyric Analyze Agent', 'Style Agent', 'Prompt Agent', 'Image Agent', 'Logo Agent', 'Video Agent']:
            self.assertIn(agent_name, status)
            self.assertTrue(status[agent_name])

if __name__ == '__main__':
    unittest.main()
