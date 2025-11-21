from typing import Any, Dict, List


class AIProvider:
    def complete(self, prompt: str, **_: Dict) -> str:
        raise NotImplementedError

    def chat(self, messages: List[Dict[str, str]], **_: Dict) -> str:
        raise NotImplementedError


class NoopAIProvider(AIProvider):
    def __init__(self, tag: str = "noop"):
        self.tag = tag

    def complete(self, prompt: str, **kwargs: Any) -> str:
        return f"[{self.tag}] {prompt}"

    def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        last = messages[-1]["content"] if messages else ""
        return f"[{self.tag}] {last}"
