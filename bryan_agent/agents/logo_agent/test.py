import unittest
from unittest.mock import patch
from pathlib import Path
from bryan_agent.agents.logo_agent.agent import LogoAgent
from bryan_agent.agents.base_agent.utils import organize_lrc
from bryan_agent.agents.base_agent.settings import settings

class TestLogoAgent(unittest.TestCase):
    def setUp(self):
        self.config = {}
        self.agent = LogoAgent(self.config)
        test_lrc = "test/LoveStory-TaylorSwift.lrc"
        self.lyrics_text_file = Path(__file__).resolve().parent.parent.parent.parent / test_lrc
        self.base_style_settings = "artStyles: Realism, Romanticism, Impressionism, artMedium - Drawing: Illustration, Storybook Illustration, Hand-Drawn, artMedium - Paint: Oil Paint, Watercolor, Camera - Scenes: Cinematic, Golden Hour, Dramatic, Camera - Film Types: 35mm, Kodak Portra, Vintage, Camera - Lenses and Perspective: Wide Angle, Closeup, First-Person, Camera - Blur and Distortion: Tilt Blur, Camera - Camera Settings: Soft Lighting, Low Contrast, Long Exposure, Color - Chromatic Palettes: Warm Color Palette, Light Blue Background, Light Blue Foreground, Saturated, Color - Monochromatic Palettes: Sepia, Color - Contrast: High Contrast, Dimensionality - 2D-5D: 3D, Intangibles - Emotions and Qualities: Happy, Lonely, Excited, Sad, Intangibles - Concepts: Refreshing, Essence, Divine, Lighting - Types: Natural Lighting, Sunlight, Rays of Shimmering Light, Lighting - Styles: Moody Lighting, Cinematic Lighting, Soft Lighting, Material - Opacity: Translucent, Material - Light: Ambient Occlusion, Material - Luminescence: Glow-In-The-Dark, Material - Reflection and Refraction: Glossy, Shiny, Reflective, Material - Color: Iridescent, Material - Maps: Normal Map"

    @patch('builtins.input', side_effect=['n', 'y'])
    def test_generate_logo(self, mock_input):
        dic = organize_lrc(self.lyrics_text_file)
        self.agent.run(self.lyrics_text_file, dic, self.base_style_settings)

if __name__ == '__main__':
    unittest.main()