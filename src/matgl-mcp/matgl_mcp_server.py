#!/usr/bin/env python3
"""
MCP сервер для matgl-api
Использует fastmcp для создания инструментов
"""

from fastmcp import FastMCP
import httpx
from typing import List
import os
from matgl_model import (
    MaterialSearchRequest, 
    MaterialSearchResponse, 
    DatasetListResponse, 
    DatasetRequest, 
    DatasetResponse,
    MaterialDetail,
    DatasetDetailResponse,
    PredictRequest,
    PredictResponse,
    FineTuningRequest,
    ModelListResponse,
    FineTuningStatusResponse
)

# Инициализируем MCP сервер
mcp = FastMCP("matgl-mcp")

# Конфигурация API
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
    
    payload = MaterialSearchRequest(element_lists=input)
    
    response = await client.post(
        f"{API_BASE_URL}/api/v1/material/search",
        json=payload.model_dump()
    )
    response.raise_for_status()
    
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
    
    response = await client.get(
        f"{API_BASE_URL}/api/v1/material/dataset",
    )
    response.raise_for_status()
    
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
    
    payload = DatasetRequest(formulas=input, dataset_name=ds_name)
    
    response = await client.post(
        f"{API_BASE_URL}/api/v1/material/dataset",
        json=payload.model_dump()
    )
    response.raise_for_status()
    
    data = response.json()
    return DatasetResponse(**data)


@mcp.tool()
async def get_material_from_mp(material_id: str) -> MaterialDetail:
    """
    Возвращает химическую формулу, энергию формирования и структуру в формате CIF.
    
    Args:
        material_id: Идентификатор материала в Materials Project
                      Например: mp-149
   
    Example:
        >>> await get_material_from_mp("mp-149")
    """
    
    response = await client.get(
        f"{API_BASE_URL}/api/v1/material/{material_id}",
    )
    response.raise_for_status()
    
    data = response.json()
    return MaterialDetail(**data)
        

@mcp.tool()
async def get_dataset(dataset_name: str, with_struct: bool = False) -> DatasetDetailResponse:
    """
    Получить датасет по имени.

    Возвращает список материалов с material_id, formula и formation_energy_per_atom.
    Если with_struct=true, также включается структура в формате CIF.
    
    Args:
        dataset_name: имя датасета
        with_struct: включать ли структуры в ответ (по умолчанию false)
   
    Example:
        >>> await get_dataset("custom_ds", true)
    """
    response = await client.get(
        f"{API_BASE_URL}/api/v1/material/dataset/{dataset_name}?with_struct={with_struct}",
    )
    response.raise_for_status()
    
    data = response.json()
    return DatasetDetailResponse(**data)


@mcp.tool()
async def delete_dataset(dataset_name: str):

    """
    Удалить датасет по имени.
   
    Args:
        dataset_name: имя датасета
   
    Example:
        >>> await delete_dataset("custom_ds", true)
    """

    response = await client.delete(
        f"{API_BASE_URL}/api/v1/material/dataset/{dataset_name}",
    )
    response.raise_for_status()
    
    return response.json()


@mcp.tool()
async def predict_formation_energy(cif: str, model_name: str):
    """
    Предсказать энергию формирования для структуры в формате CIF.

    Args:
        cif: структура в формате cif
        model_name: имя модели предсказания
    """
    payload = PredictRequest(cif=cif, model_name=model_name)
    
    response = await client.post(
        f"{API_BASE_URL}/api/v1/predict",
        json=payload.model_dump()
    )
    response.raise_for_status()
    
    data = response.json()
    return PredictResponse(**data)


@mcp.tool()
async def start_fine_tuning(model_name: str, dataset_name: str):
    """
    Запустить дообучение модели M3GNet на пользовательском датасете.

    Дообучение выполняется асинхронно. Возвращает 200 с сообщением о запуске.

    Args:
        model_name: имя для новой дообученной модели
        dataset_name: имя датасета из каталога datasets
    """
    payload = FineTuningRequest(model_name=model_name, dataset_name=dataset_name)
    
    response = await client.post(
        f"{API_BASE_URL}/api/v1/material/fine-tuning",
        json=payload.model_dump()
    )
    response.raise_for_status()
    
    return response.json()


@mcp.tool()
async def list_fine_tuned_models():
    """
    Получить список всех доступных моделей.
    """
    response = await client.get(
        f"{API_BASE_URL}/api/v1/material/fine-tuning/models",
    )
    response.raise_for_status()
    
    data = response.json()
    return ModelListResponse(**data)


@mcp.tool()
async def get_fine_tuning_status(model_name: str):
    """
    Получить статус дообучения модели.

    Возвращает статус задачи и результат, если дообучение завершено.
    Если задача уже удалена из памяти, проверяет наличие файла модели
    и находит соответствующий лог.

    Args:
        model_name: имя для новой дообученной модели
    """
    response = await client.get(
        f"{API_BASE_URL}/api/v1/material/fine-tuning/{model_name}",
    )
    response.raise_for_status()
    
    data = response.json()
    return FineTuningStatusResponse(**data)


if __name__ == "__main__":
    mcp.run(transport="stdio")