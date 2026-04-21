import os
from qwen_agent.agents import Assistant
from qwen_agent.llm.schema import Message

class MaterialAgent:
    def __init__(self):
        # Это и есть главная "магия" подключения к Ollama
        self.llm_cfg = {
            # Название модели должно точно совпадать с тем, что вы скачали через ollama pull
            'model': 'qwen3:4b',
            # Адрес сервера Ollama. Суффикс /v1 ОБЯЗАТЕЛЕН!
            'model_server': 'http://localhost:11434/v1',
            # Для локальных моделей API-ключ не нужен, можно указать что угодно
            'api_key': 'ollama',
            # Необязательные параметры генерации
            'generate_cfg': {
                'top_p': 0.8,
                'temperature': 0.7
            }
        }
        self.bot = Assistant(
            llm=self.llm_cfg,
            system_message="Ты полезный ассистент-эксперт в области материаловедения. Отвечай на русском языке."
        )

    def ask(self, question: str) -> str:
        messages = [{'role': 'user', 'content': question}]
        response = []
        for response_part in self.bot.run(messages):
            # Функция run возвращает ответы частями (стриминг), 
            # последняя часть будет содержать полный ответ.
            response = response_part
        # Извлекаем текст ответа
        return response[-1]['content']