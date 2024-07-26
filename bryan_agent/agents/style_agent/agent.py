from .tool import StyleAnalyze

class StyleAgent:
    name = "Style Agent"

    def __init__(self, config):
        self.config = config
        self.stop_loading = False
        self.style = StyleAnalyze(self.name)

    def run(self, dic: dict):
        return self.style.analyze_style(dic)

