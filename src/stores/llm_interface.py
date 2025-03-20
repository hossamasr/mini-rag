from abc import ABC, abstractmethod
from typing import Optional


class LLMInterface(ABC):

    @abstractmethod
    def set_generation_model(self, model_id: str):
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass

    @abstractmethod
    def generate_text(self, prompt: str, max_output_tokens: Optional[int] = None, temperature: Optional[float] = None, chat_history: list = []):
        pass

    @abstractmethod
    def embed_text(self, text: str, document_type: Optional[str] = None):
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass
