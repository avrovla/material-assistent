# src/material_assistent/main_streaming.py - потоковая версия
import sys
from .agent import MaterialAgent

def main():
    agent = MaterialAgent()
    
    print("=" * 60)
    print("🤖 Материаловедческий ассистент (с потоковым выводом)")
    print("=" * 60)
    print("Команды: /exit - выход, /clear - очистка, /help - справка")
    print("=" * 60)
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("\n❓ Вы: ").strip()
            
            if user_input.lower() in ['/exit', '/quit', '/q']:
                print("\n👋 До свидания!")
                break
            elif user_input.lower() in ['/clear', '/c']:
                import os
                os.system('cls' if sys.platform == 'win32' else 'clear')
                conversation_history = []
                print("✨ Экран очищен")
                continue
            elif user_input.lower() in ['/help', '/h']:
                print("\n💡 Подсказки:")
                print("  • Задавайте вопросы по материалам")
                print("  • Агент помнит последние сообщения")
                print("  • Используйте /exit для выхода")
                continue
            elif not user_input:
                continue
            
            conversation_history.append({"role": "user", "content": user_input})
            
            print("\n🤖 Ассистент: ", end="", flush=True)
            
            # Потоковый вывод
            full_response = ""
            for chunk in agent.ask_streaming(user_input, conversation_history[:-1]):
                if chunk and chunk != full_response:
                    new_text = chunk[len(full_response):]
                    print(new_text, end="", flush=True)
                    full_response = chunk
            
            print()  # Переход на новую строку
            conversation_history.append({"role": "assistant", "content": full_response})
            
        except KeyboardInterrupt:
            print("\n\n👋 До свидания!")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")

if __name__ == "__main__":
    main()