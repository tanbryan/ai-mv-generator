from bryan_agent.llm.openai.response import create_chat_completion

class LLMChain:
    def __init__(self, agent_name):
        self.agent_name = agent_name

    def send_to_llm(self, prompt, system_message, parse_response=True):
        messages = [{"role": "system", "content": system_message}]
        if isinstance(prompt, list):
            for p in prompt:
                messages.append({"role": "user", "content": p})
        else:
            messages.append({"role": "user", "content": prompt})

        response = create_chat_completion(messages, parse_response=parse_response)
        return response

