from pydantic import BaseModel, Field


class MaterialSearchRequest(BaseModel):
    """Запрос на поиск материалов по химическим системам."""

    element_lists: list[list[str]] = Field(
        ...,
        description="Список списков элементов для перебора комбинаций",
        examples=[[["Ti", "Cr", "V"], ["Al", "Si", "Ga"], ["C", "N"]]],
    )


class SearchResultEntry(BaseModel):
    """Один результат поиска материала."""

    material_id: str = Field(..., description="Materials Project ID", examples=["mp-149"])
    formula_pretty: str = Field(..., description="Химическая формула", examples=["Ti2AlC"])
    chemsys: str = Field(
        ...,
        description="Химическая система, по которой найден материал",
        examples=["Al-C-Ti"],
    )


class MaterialSearchResponse(BaseModel):
    """Результат поиска материалов."""

    results: list[SearchResultEntry] = Field(
        default_factory=list, description="Список найденных материалов"
    )


class DatasetListResponse(BaseModel):
    """Список доступных датасетов."""

    datasets: list[str] = Field(
        default_factory=list, description="Имена доступных датасетов", examples=[["max-phase", "vanad"]]
    )
    total: int = Field(..., description="Общее количество датасетов", examples=[2])


class DatasetRequest(BaseModel):
    """Запрос на создание датасета из химических формул."""

    formulas: list[str] = Field(
        ...,
        description="Список химических формул (например, ['MgSn(GeO3)2', 'Cr3O8'])",
        examples=[["MgSn(GeO3)2", "Cr3O8"]],
    )
    dataset_name: str = Field(
        ...,
        description="Имя датасета (будет использовано как имя файла)",
        examples=["my_dataset"],
    )


class DatasetResponse(BaseModel):
    """Результат создания датасета."""

    status: str = Field(..., description="Статус операции", examples=["success"])
    dataset_name: str = Field(..., description="Имя созданного датасета", examples=["my_dataset"])
    file_path: str = Field(..., description="Путь к сохранённому JSON-файлу")
    total_materials: int = Field(
        ..., description="Общее количество материалов в датасете", examples=[42]
    )
    formulas_processed: int = Field(
        ..., description="Количество обработанных формул", examples=[2]
    )    