from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import FunctionAgent
import asyncio

async def main():
    # Создаем MCP клиент
    mcp_client = BasicMCPClient(
        "E:\\ПП\\projects\\material-assistent\\.venv\\Scripts\\python.exe",
        args=[
            "E:\\ПП\\projects\\material-assistent\\src\\matgl-mcp\\matgl_mcp_server.py"
        ],
        env={
            "API_BASE_URL": "http://localhost:8000",
            "PYTHONIOENCODING": "utf-8"
        }
    )
    
    # Создаем спецификацию инструментов MCP
    mcp_tool_spec = McpToolSpec(client=mcp_client)
    
    # Получаем инструменты (асинхронно)
    tools = await mcp_tool_spec.to_tool_list_async()
    
    # Инициализируем LLM
    llm = Ollama(
        model="qwen3:8b-16k",
        base_url="http://localhost:11434",
        temperature=0.5,
        num_predict=16384,
        request_timeout=120.0
    )
    
    # Создаем агента (альтернативный способ)
    agent = FunctionAgent(
        tools=tools,
        llm=llm
    )
    
    # Выполняем запрос
    response = await agent.run(user_msg="покажи список датасетов")
    print(response)

# Запускаем асинхронную функцию
if __name__ == "__main__":
    asyncio.run(main())