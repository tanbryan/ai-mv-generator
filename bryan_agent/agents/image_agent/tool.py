import os
import threading
import sys
import json
import openai
from PIL import Image
from bryan_agent.llm.openai.response import create_image_prompt
from bryan_agent.utils.tool import log_with_loading, log_completion, is_file_valid
from bryan_agent.utils.io import resize_image


class ImageGenerator:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.stop_loading = [False] 

    def generate_images(self, lrc, resolution):
        width, height = map(int, resolution.split(":"))
        image_save_directory = os.path.join(os.path.dirname(lrc), 'background_images')
        prompts_file = os.path.join(os.path.dirname(lrc), 'generated_prompts.json')

        with open(prompts_file, 'r') as file:
            prompts_data = json.load(file)
        # Generate images
        if not os.path.exists(image_save_directory):
            try:
                for section_idx, section_prompts in enumerate(prompts_data):
                    print(f"⌛️ Generating image for section {section_idx + 1}...")
                    loading_thread = log_with_loading(self.agent_name, "generating images", self.stop_loading)
                    self.process_prompts(lrc, section_idx, prompts_data, width, height)
            except openai.error.OpenAIError as e:
                print(f"❌ OpenAI API error: {e}")
            finally:
                log_completion(self.agent_name, self.stop_loading, loading_thread)

        # If folder exists, check for missing or invalid images
        else:
            try:
                missing_or_invalid_images = self.check_missing_images(lrc, prompts_data, width, height)
                if missing_or_invalid_images:
                    self.regenerate_images(lrc, missing_or_invalid_images, prompts_data, width, height)
            except openai.error.OpenAIError as e:
                print(f"❌ OpenAI API error: {e}")
            
        # Ask for user satisfaction
        self.ask_user_for_satisfaction(lrc, len(prompts_data), prompts_data, width, height)

    def process_prompts(self, lrc, section_idx, prompts, width, height):
        for sub_idx, individual_prompt in enumerate(prompts[section_idx]):
            prompt_text = ' '.join(individual_prompt)
            img = create_image_prompt(prompt_text)
            if img:
                self.save_image(lrc, section_idx, sub_idx, img, width, height)
            else:
                print(f"❌ Failed to download image for section {section_idx + 1}_{sub_idx + 1}")

    def save_image(self, lrc, idx, sub_idx, img, width, height):
        image_save_directory = os.path.join(os.path.dirname(lrc), 'background_images')
        os.makedirs(image_save_directory, exist_ok=True)
        img_resized = resize_image(img, width, height)
        img_resized.save(os.path.join(image_save_directory, f"background_{idx + 1}_{sub_idx + 1}.png"))
        sys.stdout.write("\r\033[K")
        print(f"✅ Image_{idx + 1}_{sub_idx + 1} saved as background_{idx + 1}_{sub_idx + 1}.png")

    def check_missing_images(self, lrc, prompts, width, height):
        missing_or_invalid_images = []
        image_save_directory = os.path.join(os.path.dirname(lrc), 'background_images')
        for idx in range(len(prompts)):
            for sub_idx in range(len(prompts[idx])):
                file_path = os.path.join(image_save_directory, f"background_{idx + 1}_{sub_idx + 1}.png")
                if not is_file_valid(file_path):
                    print(f"❌ Missing or invalid image: background_{idx + 1}_{sub_idx + 1}.png")
                    missing_or_invalid_images.append((idx, sub_idx))
        return missing_or_invalid_images

    def regenerate_images(self, lrc, missing_or_invalid_images, prompts_data, width, height):
        loading_thread = log_with_loading(self.agent_name, "regenerating images", self.stop_loading)
        for section_idx, prompt_idx in missing_or_invalid_images:
            prompt_text = ''.join(prompts_data[section_idx][prompt_idx])
            img = create_image_prompt(prompt_text)
            if img:
                self.save_image(lrc, section_idx, prompt_idx, img, width, height)
            else:
                print(f"❌ Failed to regenerate image for section {section_idx + 1}, image {prompt_idx + 1}")
        log_completion(self.agent_name, self.stop_loading, loading_thread)

    def ask_user_for_satisfaction(self, lrc, num_sections, prompts, width, height):
        while True:
            user_input = input("Are you satisfied with the images? (y/n): ").strip().lower()
            if user_input == 'y':
                break
            elif user_input == 'n':
                image_num = input("Please enter the section and image number to regenerate (e.g., 1_2 for section 1, image 2): ").strip()
                try:
                    section, image = map(int, image_num.split('_'))
                    if 1 <= section <= num_sections and 1 <= image <= len(prompts[section - 1]):
                        self.regenerate_images(lrc, [(section - 1, image - 1)], prompts, width, height)
                    else:
                        print("❌ Invalid section or image number.")
                except ValueError:
                    print("❌ Invalid input format. Please enter in the format section_image (e.g., 1_2).")
            else:
                print("❌ Invalid input. Please enter 'y' or 'n'.")

