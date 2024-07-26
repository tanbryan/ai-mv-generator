import unittest
from pathlib import Path
from bryan_agent.agents.prompt_agent.agent import PromptAgent
from bryan_agent.agents.base_agent.utils import organize_lrc

class TestPromptAgent(unittest.TestCase):
    def setUp(self):
        self.agent = PromptAgent(config={})
        test_lrc = "test/LoveStory-TaylorSwift.lrc"
        self.lyrics_text_file = Path(__file__).resolve().parent.parent.parent.parent / test_lrc
        self.grouped_ids = [[0, 1, 2, 3], [4, 5, 6, 7, 8]]
        self.base_style_settings = "artStyles: Realism, Romanticism, Impressionism, artMedium - Drawing: Illustration, Storybook Illustration, Hand-Drawn, artMedium - Paint: Oil Paint, Watercolor, Camera - Scenes: Cinematic, Golden Hour, Dramatic, Camera - Film Types: 35mm, Kodak Portra, Vintage, Camera - Lenses and Perspective: Wide Angle, Closeup, First-Person, Camera - Blur and Distortion: Tilt Blur, Camera - Camera Settings: Soft Lighting, Low Contrast, Long Exposure, Color - Chromatic Palettes: Warm Color Palette, Light Blue Background, Light Blue Foreground, Saturated, Color - Monochromatic Palettes: Sepia, Color - Contrast: High Contrast, Dimensionality - 2D-5D: 3D, Intangibles - Emotions and Qualities: Happy, Lonely, Excited, Sad, Intangibles - Concepts: Refreshing, Essence, Divine, Lighting - Types: Natural Lighting, Sunlight, Rays of Shimmering Light, Lighting - Styles: Moody Lighting, Cinematic Lighting, Soft Lighting, Material - Opacity: Translucent, Material - Light: Ambient Occlusion, Material - Luminescence: Glow-In-The-Dark, Material - Reflection and Refraction: Glossy, Shiny, Reflective, Material - Color: Iridescent, Material - Maps: Normal Map"

    def test_generate_prompt(self):
        self.dic = organize_lrc(self.lyrics_text_file)
        self.agent.prompt.generate_prompt(self.lyrics_text_file, self.dic, self.grouped_ids, self.base_style_settings)


if __name__ == '__main__':
    unittest.main()
