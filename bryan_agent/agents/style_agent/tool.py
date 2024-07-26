import os
import threading
import sys
import json
from bryan_agent.llm.openai.response import create_chat_completion
from bryan_agent.utils.tool import log_with_loading, log_completion, show_loading_animation
from bryan_agent.agents.base_agent.llm_chain import LLMChain
from .prompt import style_prompt
from bryan_agent.utils.tool import get_full_lyrics
from bryan_agent.utils.io import load_parameters

class StyleAnalyze:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.stop_loading = [False]
        self.llm_chain = LLMChain(agent_name)

    def analyze_style(self, dic):
        customization = self.get_customized_image_style() 

        loading_thread = log_with_loading(self.agent_name, "analyzing style", self.stop_loading)
        
        param_file_path = os.path.join(os.path.dirname(__file__), 'prompt_param.json')
        parameters = load_parameters(param_file_path)

        full_lyrics = get_full_lyrics(dic)
        parameters_json = json.dumps(parameters, indent=4)
        customization_prompt = self.customization(customization)
        
        prompt = style_prompt.format(full_lyrics=full_lyrics, parameters_json=parameters_json, customization_prompt=customization_prompt)

        system_message = "You are an expert in analyzing lyrics and generating stylistic settings for visual representation."
        response = self.llm_chain.send_to_llm(prompt, system_message, parse_response=True)
        log_completion(self.agent_name, self.stop_loading, loading_thread)

        base_style_settings = self.format_base_style_details(response)
        return base_style_settings

    def format_base_style_details(self, base_style_settings):
        details = []
        for key, value in base_style_settings.items():
            if isinstance(value, list):
                details.append(f"{key}: {', '.join(value)}")
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, list):
                        details.append(f"{key} - {sub_key}: {', '.join(sub_value)}")
                    else:
                        details.append(f"{key} - {sub_key}: {sub_value}")
            else:
                details.append(f"{key}: {value}") 

        formatted_details = ', '.join(details)
        return formatted_details

    def get_customized_image_style(self):
        user_input = input("""
        ❗️❗️❗️ Our model can create stunning background images inspired by the lyrics of a song.
        ❗️❗️❗️ You have the power to customize these images to match your vision. 
        ❗️❗️❗️ Our model will generate images based on the song's mood and theme.

        Here are some sample styles you can customize:
        - Color scheme (e.g., dark, vibrant, pastel)
        - Art style (e.g., abstract, realistic, cartoon)
        - Medium (e.g., watercolor, oil painting, digital art)
        - Mood (e.g., happy, sad, energetic)
        - Theme (e.g., nature, cityscape, fantasy)
        - Visual elements (e.g., stars, clouds, flowers)
        - Textures (e.g., smooth, rough, glossy)
        - Lighting (e.g., bright, dim, neon)
        - Composition (e.g., centered, asymmetrical, panoramic)
        - Art techniques (e.g., pointillism, chiaroscuro, collage)
        - Other preferences (e.g., minimalistic, detailed, surreal)
        
        ❗️❗️❗️ If you prefer not to customize (simply press Enter)
        🌟 Please describe your customized styles prompt for the background images generation:
        """)

        if user_input and user_input.strip() and len(user_input.split()) > 2:  
            return user_input
        else:
            return None

    def customization(self, customization):
        if customization: 
            customization_prompt = f"Customized Image Style: \n{customization}. Use this prompt as the foundation for analyzing and identifying the most suitable art style for the song."
            return customization_prompt
        else:
            customization_prompt = ""
            return customization_prompt
            