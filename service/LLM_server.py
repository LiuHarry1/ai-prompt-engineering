class LLM:
    def __init__(self, name):
        self.name = name

    def completion(self, prompt, history=""):
        raise NotImplementedError("completion method must be implemented in subclass")

    def chat(self, prompt, history=""):
        raise NotImplementedError("completion method must be implemented in subclass")

