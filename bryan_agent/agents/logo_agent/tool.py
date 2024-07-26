import os
import threading
import sys
import openai
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFilter
from bryan_agent.llm.openai.response import create_image_prompt
from bryan_agent.utils.tool import log_with_loading, log_completion, is_file_valid
from bryan_agent.utils.io import resize_image
from bryan_agent.utils.tool import get_full_lyrics
from .prompt import prompt


class LogoGenerator:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.stop_loading = [False]
    
    def generate_logo(self, lrc, dic, settings, based_style_settings):
        logo_path = os.path.join(os.path.dirname(lrc), "logo.png")  
        if is_file_valid(logo_path):
            print(f"✅ Logo already exists and is valid. Skipping generation...")
            return
        try:
            logo_created = self.create_logo(lrc, dic, settings, based_style_settings)
        except openai.error.OpenAIError as e:
            print(f"❌ OpenAI API error: {e}")
        self.ask_user_for_satisfaction(lrc, dic, settings, based_style_settings) 

    def create_logo(self, lrc, dic, settings, base_style_settings):
        loading_thread = log_with_loading(self.agent_name, "generating logo", self.stop_loading)
        full_lyrics = get_full_lyrics(dic)
        logo = create_image_prompt(prompt.format(full_lyrics=full_lyrics, base_style_settings=base_style_settings))
        if logo:
            logo_size = tuple(map(int, settings["logo_size"].split("x")))
            resized_img = resize_image(logo, *logo_size)
            rounded_img = self.round_corners(resized_img, 40)
            self.logo_effect(rounded_img, os.path.join(os.path.dirname(lrc), "logo.png"))
            log_completion(self.agent_name, self.stop_loading, loading_thread)
            print("✅ Image saved as logo.png")
        else:
            print("❌ Failed to download image")


    def round_corners(self, image, radius):
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], radius=radius, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(1))
        
        rounded_image = image.copy()
        rounded_image.putalpha(mask)
        return rounded_image

    def logo_effect(self, resized_img, output_path):

            image = resized_img
            image_width, image_height = image.size

            fig_size_inch = (image_width / 100, image_height / 100)
            fig_dpi = 100
            fig, ax = plt.subplots(figsize=fig_size_inch, dpi=fig_dpi)
            ax.imshow(image, extent=[0, 1, 0, 1])

            color = (211/255, 211/255, 211/255, 1)
            rounded_rect = patches.FancyBboxPatch((0, 0), 1, 1,
                                                boxstyle="round,pad=0,rounding_size=0.1",
                                                linewidth=3, edgecolor=color, facecolor='none')
            ax.add_patch(rounded_rect)

            ax.set_xlim(-0.25, 1.25)
            ax.set_ylim(-0.25, 1.25)
            ax.set_aspect('equal')

            ax.axis('off')
            plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1, transparent=True, dpi=fig_dpi)
            plt.close()


    def ask_user_for_satisfaction(self, lrc, dic, settings, based_style_settings):
        while True:
            user_satisfaction = input("Are you satisfied with the generated images? (y/n): ").strip().lower()
            if user_satisfaction == "y":
                print("✅ Logos are ready for use")
                break
            elif user_satisfaction == "n":
                self.create_logo(lrc, dic, settings, based_style_settings)
            else:
                print("❌ Invalid input. Please enter 'y' or 'n'.")
