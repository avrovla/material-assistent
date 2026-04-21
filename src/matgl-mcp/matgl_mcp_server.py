#!/usr/bin/env python3
"""
MCP сервер для matgl-api
Использует fastmcp для создания инструментов
"""

from fastmcp import FastMCP
import httpx
from typing import Optional, Dict, Any, List
import os
from matgl_model import MaterialSearchRequest, MaterialSearchResponse, DatasetListResponse, DatasetRequest, DatasetResponse

# Инициализируем MCP сервер
mcp = FastMCP("matgl-mcp")

# Конфигурация вашего API
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# HTTP клиент для запросов
client = httpx.AsyncClient(timeout=30.0)

# ========== Инструменты для работы с API ==========

@mcp.tool()
async def search_materials(input: List[List[str]]) -> MaterialSearchResponse:
    """
    Поиск материалов по химическим системам.
    
    Args:
        input: Список списков элементов для перебора комбинаций.
                      Например: [["Ti", "Cr", "V"], ["Al", "Si", "Ga"], ["C", "N"]]
    
    Returns:
        Словарь с ключом "results", содержащий список найденных материалов.
        Каждый материал содержит формулу и другие свойства.
    
    Example:
        >>> await search_materials([["Ti", "V"], ["Al", "Si"], ["C", "N"]])
    """
    
        # Формируем тело запроса согласно MaterialSearchRequest
    payload = MaterialSearchRequest(element_lists=input)
    
    # Отправляем POST запрос
    response = await client.post(
        f"{API_BASE_URL}/api/v1/material/search",
        json=payload.model_dump()
    )
    response.raise_for_status()
    
    # Возвращаем результат согласно MaterialSearchResponse
    data = response.json()
    if "results" in data:
        return MaterialSearchResponse(**data)
    else:
        # Если API возвращает список напрямую
        return MaterialSearchResponse(results=data)
      

@mcp.tool()
async def list_datasets() -> DatasetListResponse:
    """
    Получение списка датасетов
   
    Returns:
        Словарь с ключом "datasets", содержащий список датасетов.
    
    Example:
        >>> await list_datasets()
    """
    
    # Отправляем GET запрос
    response = await client.get(
        f"{API_BASE_URL}/api/v1/material/dataset",
    )
    response.raise_for_status()
    
    # Возвращаем результат согласно DatasetListResponse
    data = response.json()
    return DatasetListResponse(**data)


@mcp.tool()
async def create_dataset(input: List[str], ds_name: str) -> DatasetResponse:
    """
    Создание датасета по списку химических формул
    
    Args:
        input: Список списков химических формул.
                      Например: ["Ti2AlC", "Ti3AlC2"]
    
    Returns:
        Словарь с ключом "results", содержащий список найденных материалов.
        Каждый материал содержит формулу и другие свойства.
    
    Example:
        >>> await create_dataset(["Ti2AlC", "Ti3AlC2"], "custom_dataset")
    """
    
    # Формируем тело запроса согласно DatasetRequest
    payload = DatasetRequest(formulas=input, dataset_name=ds_name)
    
    # Отправляем POST запрос
    response = await client.post(
        f"{API_BASE_URL}/api/v1/material/dataset",
        json=payload.model_dump()
    )
    response.raise_for_status()
    
    # Возвращаем результат согласно DatasetResponse
    data = response.json()
    return DatasetResponse(**data)
        



if __name__ == "__main__":
    mcp.run(transport="stdio")