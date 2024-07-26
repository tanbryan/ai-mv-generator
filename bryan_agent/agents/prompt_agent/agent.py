from .tool import CreatePrompt

class PromptAgent:
    name = "Prompt Agent"  

    def __init__(self, config):
        self.config = config
        self.stop_loading = False
        self.prompt = CreatePrompt(self.name)  


    def run(self, lrc: str, dic: dict, grouped_ids: list, base_style_settings: dict):
        return self.prompt.generate_prompt(lrc, dic, grouped_ids, base_style_settings)
