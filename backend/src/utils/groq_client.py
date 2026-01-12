"""
PlanBel 2.0 - Cliente Groq com rate limiting
"""

import os
import time
from typing import Any
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GroqClient:
    """Cliente Groq com rate limiting para free tier."""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.delay = float(os.getenv("GROQ_DELAY_SECONDS", "2.5"))
        self.last_call = 0.0
    
    def _wait_rate_limit(self) -> None:
        """Aguarda tempo necessário para respeitar rate limit."""
        elapsed = time.time() - self.last_call
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> dict[str, Any]:
        """
        Gera resposta usando Groq API.
        
        Args:
            prompt: Prompt do usuário
            system_prompt: Prompt de sistema (role)
            temperature: Criatividade (0.0-1.0)
            max_tokens: Máximo de tokens na resposta
            
        Returns:
            Dict com 'content', 'tokens_used', 'model'
        """
        self._wait_rate_limit()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            self.last_call = time.time()
            
            return {
                "content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "model": self.model,
                "success": True
            }
            
        except Exception as e:
            return {
                "content": "",
                "error": str(e),
                "success": False
            }


# Singleton para uso global
_client: GroqClient | None = None


def get_groq_client() -> GroqClient:
    """Retorna instância singleton do cliente Groq."""
    global _client
    if _client is None:
        _client = GroqClient()
    return _client
