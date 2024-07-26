import os
import threading
import sys
import openai
from bryan_agent.llm.openai.response import create_chat_completion
from bryan_agent.utils.tool import log_with_loading, log_completion
from .prompt import lyric_analyze_prompt
from bryan_agent.agents.base_agent.llm_chain import LLMChain 

class LyricAnalyze:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.stop_loading = [False] 
        self.llm_chain = LLMChain(agent_name)

    def analyze_lrc(self, dic):
        loading_thread = log_with_loading(self.agent_name, "analyzing lyrics", self.stop_loading)
        try:
            prompt = lyric_analyze_prompt.format(dic=dic)
            system_message = "You are a skilled expert assisting with organizing lyrics for video generation."

            grouped_ids = self.llm_chain.send_to_llm(prompt, system_message, parse_response=True)
            grouped_lyrics = self.group_lyrics(grouped_ids, dic)

        except openai.error.OpenAIError as e:
            print(f"❌ OpenAI API error: {e}")
        finally:
            log_completion(self.agent_name, self.stop_loading, loading_thread)

        return grouped_lyrics, grouped_ids 

    def group_lyrics(self, grouped_ids, dic):
        grouped_lyrics = {}
        for idx, group in enumerate(grouped_ids):
            lyrics = [dic[int(i)]["text"] for i in group] 
            grouped_lyrics[idx] = lyrics
        return grouped_lyrics
