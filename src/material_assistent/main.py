import sys
from .agent import MaterialAgent

def main():
    agent = MaterialAgent()
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = input("Ваш вопрос: ")
    
    answer = agent.ask(question)
    print(f"\nОтвет: {answer}")

if __name__ == "__main__":
    main()