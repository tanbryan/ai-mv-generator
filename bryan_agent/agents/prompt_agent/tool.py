import os
import threading
import sys
import openai
import json
from bryan_agent.llm.openai.response import create_chat_completion
from bryan_agent.utils.tool import log_with_loading, log_completion, show_loading_animation
from bryan_agent.agents.base_agent.llm_chain import LLMChain
from bryan_agent.utils.tool import get_full_lyrics
from bryan_agent.utils.io import wrap_text
from .prompt import base_prompt,section_prompt, group_prompt

class CreatePrompt:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.stop_loading = [False]
        self.llm_chain = LLMChain(agent_name)

    def generate_prompt(self, lrc, dic, grouped_ids, base_style_settings):
        loading_thread = log_with_loading(self.agent_name, "generating prompts", self.stop_loading)
        try:
            full_lyrics = get_full_lyrics(dic)

            base_prompt_filled = base_prompt.format(full_lyrics=full_lyrics)

            system_message = "You are an expert in generating detailed prompts for creating music video background images."

            detailed_prompts = self.generate_section_prompts(lrc, dic, grouped_ids, base_style_settings, base_prompt_filled, system_message)
        except openai.error.OpenAIError as e:
            print(f"❌ OpenAI API error: {e}")
        finally:
            log_completion(self.agent_name, self.stop_loading, loading_thread)

        return detailed_prompts

    def generate_section_prompts(self, lrc, dic, grouped_ids, base_style_settings, base_prompt_filled, system_message):
        loading_thread = log_with_loading(self.agent_name, "generating prompts", self.stop_loading)
        prompts_file_path = os.path.join(os.path.dirname(lrc), 'generated_prompts.json')
        detailed_prompts = []

        for idx, group in enumerate(grouped_ids):
            prompts = [base_prompt_filled]
            num_images = len(group)
            group_lyrics = "\n".join([dic[i]["text"] for i in group])
            section_prompts = section_prompt.format(idx=idx + 1, group_lyrics=group_lyrics, num_images=num_images)
            prompts.append(section_prompts)

            for image_idx in range(num_images):
                individual_group_prompt = group_prompt.format(idx=idx + 1, image_idx=image_idx + 1, base_style_settings=base_style_settings)
                prompts.append(individual_group_prompt)

            response = self.llm_chain.send_to_llm(prompts, system_message, parse_response=False).strip().split('\n\n')

            sys.stdout.write("\r\033[K")
            print(f"✅ Section {idx + 1} prompt generated. Moving to next section...")

            wrapped_prompts = [wrap_text(prompt) for prompt in response]
            detailed_prompts.append(wrapped_prompts)

        with open(prompts_file_path, 'w') as file:
            json.dump(detailed_prompts, file, indent=4)

