import os
from qwen_agent.agents import Assistant

class MaterialAgent:
    def __init__(self, use_mcp: bool = True):
        # Конфигурация для Ollama
        self.llm_cfg = {
            'model': 'qwen3:4b',  # или другая ваша модель
            'model_server': 'http://localhost:11434/v1',
            'api_key': 'ollama',
            'generate_cfg': {
                'top_p': 0.8,
                'temperature': 0.7,
                'max_tokens': 2000
            }
        }

        self.tools = []

        if use_mcp:
            self.tools.append({
                'mcpServers': {
                    'matgl-mcp': {
                        'command': 'npx',
                        'args': [
                            '-y',
                            '@ivotoby/openapi-mcp-server'
                        ],
                        'env': {
                            'API_BASE_URL': 'http://localhost:8000',
                            'OPENAPI_SPEC_PATH': 'http://localhost:8000/openapi.json'
                        }
                    }
                }
            })
        
        self.bot = Assistant(
            llm=self.llm_cfg,
            system_message="""Ты полезный ассистент-эксперт в области материаловедения.
Ты отлично разбираешься в металлах, полимерах, композитах, керамике и других материалах.
Отвечай подробно, но по существу. Если не знаешь ответа, честно скажи об этом.
Всегда отвечай на русском языке, даже если вопрос задан на другом языке.
Поддерживай контекст диалога - помни, о чем говорили ранее.""",
            name="Материаловед",
            description="Эксперт по материалам"
        )

    def ask(self, question: str, history: list = None) -> str:
        """Получить ответ от агента с учетом истории диалога"""
        
        # Формируем сообщения с историей
        messages = []
        
        # Добавляем историю, если она есть
        if history:
            messages.extend(history)
        
        # Добавляем текущий вопрос
        messages.append({'role': 'user', 'content': question})
        
        # Получаем ответ от агента (с поддержкой стриминга)
        response = []
        for response_part in self.bot.run(messages):
            response = response_part
        
        # Извлекаем текст ответа
        if response and len(response) > 0:
            # response - это список сообщений, последнее - ответ ассистента
            last_message = response[-1]
            if isinstance(last_message, dict):
                return last_message.get('content', 'Не удалось получить ответ')
            else:
                return str(last_message)
        return "Извините, не удалось сформировать ответ"

    def ask_streaming(self, question: str, history: list = None):
        """Получить ответ с потоковой передачей (по словам/токенам)"""
        messages = []
        if history:
            messages.extend(history)
        messages.append({'role': 'user', 'content': question})
        
        for response_part in self.bot.run(messages):
            if response_part and len(response_part) > 0:
                last_message = response_part[-1]
                if isinstance(last_message, dict):
                    yield last_message.get('content', '')
                else:
                    yield str(last_message)