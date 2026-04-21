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
            function_list=self.tools if self.tools else None,
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
    
    def get_mcp_tools_list(self):
        """Получает список инструментов из подключенного MCP сервера"""

        if not self.tools:
            print("Нет подключенных MCP серверов")
            return []

        tools_info = []

        # Qwen-Agent внутренне создает MCP клиент
        # Мы можем получить инструменты из его конфигурации
        for tool_config in self.tools:
            if 'mcpServers' in tool_config:
                for server_name, server_config in tool_config['mcpServers'].items():
                    tools_info.append({
                        'server': server_name,
                        'command': server_config['command'],
                        'args': server_config['args'],
                        'status': 'connected',
                        'note': 'Инструменты будут определены MCP сервером автоматически'
                    })

                    # Qwen-Agent сам получит инструменты через MCP протокол
                    # и они станут доступны через self.bot.function_map

        # Проверяем, какие инструменты реально зарегистрированы
        if hasattr(self.bot, 'function_map'):
            registered_tools = list(self.bot.function_map.keys())
            if registered_tools:
                print(f"Зарегистрированные инструменты: {registered_tools}")
                tools_info.append({
                    'registered_tools': registered_tools
                })

        return tools_info