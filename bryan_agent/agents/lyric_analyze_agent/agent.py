from .tool import LyricAnalyze


class LyricAnalyzeAgent:
    name = "Lyric Analyze Agent"

    def __init__(self, config):
        self.config = config
        self.stop_loading = False
        self.analyzer = LyricAnalyze(self.name)

    def run(self, dic: dict):
        return self.analyzer.analyze_lrc(dic)
