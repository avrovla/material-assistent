from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import FunctionAgent
from llama_index.core.memory import ChatMemoryBuffer
import asyncio
import json
from datetime import datetime
from pathlib import Path
import time

class ChatBotWithHistory:
    def __init__(self, history_file="chat_history.json"):
        self.mcp_client = None
        self.agent = None
        self.history_file = Path(history_file)
        self.conversation_history = []
        
    async def initialize(self):
        """Инициализация MCP клиента и агента"""
        self.mcp_client = BasicMCPClient(
            "E:\\ПП\\projects\\material-assistent\\.venv\\Scripts\\python.exe",
            args=[
                "E:\\ПП\\projects\\material-assistent\\src\\matgl-mcp\\matgl_mcp_server.py"
            ],
            env={
                "API_BASE_URL": "http://localhost:8000",
                "PYTHONIOENCODING": "utf-8",
                "WORKING_DIR": "E:\\ПП\\projects\\material-assistent\\working_dir"
            }
        )
        
        mcp_tool_spec = McpToolSpec(client=self.mcp_client)
        tools = await mcp_tool_spec.to_tool_list_async()
        
        # Создаем память для хранения истории диалога
        memory = ChatMemoryBuffer.from_defaults(token_limit=16384)
        
        self.llm = Ollama(
            model="qwen3:8b-16k",
            base_url="http://localhost:11434",
            temperature=0.3,
            num_predict=16384,
            request_timeout=120.0
        )
        
        self.agent = FunctionAgent(
            tools=tools,
            llm=self.llm,
            memory=memory  # Добавляем память
        )
        
        self.load_history()
        print("✓ Чат-бот инициализирован с сохранением истории!")
        
    def load_history(self):
        """Загрузка истории из файла"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.conversation_history = json.load(f)
                print(f"✓ Загружено {len(self.conversation_history)} сообщений из истории")
            except:
                print("⚠️ Не удалось загрузить историю")
                
    def format_time(self, seconds):
        """Форматирование времени обработки"""
        if seconds < 60:
            return f"{seconds:.2f} сек"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes} мин {secs:.1f} сек"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours} ч {minutes} мин"
                
    def save_to_history(self, user_msg, bot_response, processing_time):
        """Сохранение сообщения в историю"""
        message = {
            "timestamp": datetime.now().isoformat(),
            "user": user_msg,
            "bot": str(bot_response),
            "processing_time": processing_time,
            "processing_time_formatted": self.format_time(processing_time)
        }
        self.conversation_history.append(message)
        
        # Сохраняем последние 100 сообщений
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-100:]
            
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
    
    async def chat(self):
        """Основной цикл чата"""
        print("\n" + "="*60)
        print("🤖 МАТЕРИАЛОВЕДЧЕСКИЙ АССИСТЕНТ")
        print("="*60)
        print("💡 Команды:")
        print("   /history  - показать историю диалога")
        print("   /clear    - очистить историю")
        print("   /save     - сохранить текущий диалог")
        print("   /exit     - выйти")
        print("="*60)
        
        while True:
            try:
                user_input = input("\n👤 Вы: ").strip()
                
                if user_input.lower() in ['/exit', '/quit', 'выход']:
                    print("\n👋 До свидания!")
                    break
                
                if user_input == '/history':
                    self.show_history()
                    continue
                    
                if user_input == '/clear':
                    self.conversation_history = []
                    self.save_to_history("=== ИСТОРИЯ ОЧИЩЕНА ===", "", 0)
                    print("✓ История очищена")
                    continue
                    
                if user_input == '/save':
                    self.save_dialog_to_file()
                    continue
                
                if not user_input:
                    continue
                
                print("\n🤔 Анализирую запрос...")
                
                # Засекаем время начала обработки
                start_time = time.time()
                
                response = await self.agent.run(user_msg=user_input)
                
                # Вычисляем время обработки
                end_time = time.time()
                processing_time = end_time - start_time
                
                # Форматируем время для отображения
                time_str = self.format_time(processing_time)
                
                # Сохраняем в историю
                self.save_to_history(user_input, response, processing_time)
                
                # Добавляем информацию о времени в ответ
                response_with_time = f"{response}\n\n⏱️ Время обработки: {time_str}"
                
                print(f"\n🤖 Ассистент: {response_with_time}")
                print("-"*60)
                
            except KeyboardInterrupt:
                print("\n\n👋 Прервано пользователем. До свидания!")
                break
            except Exception as e:
                print(f"\n❌ Ошибка: {e}")
    
    def show_history(self):
        """Показать историю диалога"""
        if not self.conversation_history:
            print("\n📭 История пуста")
            return
            
        print("\n📜 ИСТОРИЯ ДИАЛОГА:")
        print("-"*60)
        for i, msg in enumerate(self.conversation_history[-10:], 1):
            time = datetime.fromisoformat(msg['timestamp']).strftime("%H:%M:%S")
            processing_time = msg.get('processing_time_formatted', 'N/A')
            print(f"\n[{time}] Вы: {msg['user'][:100]}")
            print(f"[{time}] Бот: {msg['bot'][:100]}...")
            print(f"⏱️ Время обработки: {processing_time}")
        print("-"*60)
    
    def save_dialog_to_file(self):
        """Сохранить диалог в отдельный файл"""
        filename = f"dialog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            for msg in self.conversation_history:
                f.write(f"[{msg['timestamp']}] Пользователь: {msg['user']}\n")
                f.write(f"[{msg['timestamp']}] Ассистент: {msg['bot']}\n")
                f.write(f"⏱️ Время обработки: {msg.get('processing_time_formatted', 'N/A')}\n")
                f.write("-"*80 + "\n")
        print(f"✓ Диалог сохранен в файл {filename}")
    
    async def close(self):
        if self.mcp_client:
            await self.mcp_client.close()

async def main():
    bot = ChatBotWithHistory()
    try:
        await bot.initialize()
        await bot.chat()
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())