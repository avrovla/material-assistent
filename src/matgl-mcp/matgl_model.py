"""Material-related Pydantic models."""

from pydantic import BaseModel, Field


class MaterialDetail(BaseModel):
    """Детальная информация о материале из Materials Project."""

    material_id: str = Field(..., description="Materials Project ID", examples=["mp-149"])
    formula_pretty: str = Field(..., description="Химическая формула", examples=["Si"])
    formation_energy_per_atom: float | None = Field(
        default=None, description="Энергия формирования на атом (эВ)", examples=[-5.2]
    )
    structure: str = Field(
        ..., description="Кристаллическая структура в формате CIF", examples=["#CIF data..."]
    )


class PredictRequest(BaseModel):
    """Запрос на предсказание энергии формирования."""

    cif: str = Field(
        ...,
        description="Кристаллическая структура в формате CIF",
        examples=["data_Si\n_symmetry_space_group_name_H-M   'F d -3 m'\n_cell_length_a   5.43\n..."],
    )
    model_name: str | None = Field(
        default=None,
        description="Имя модели matgl. По умолчанию M3GNet-MP-2018.6.1-Eform",
        examples=["M3GNet-MP-2021.2.8-DIRECT-PES"],
    )


class PredictResponse(BaseModel):
    """Результат предсказания."""

    formation_energy: float = Field(
        ..., description="Предсказанная энергия формирования (эВ)", examples=[-5.2]
    )


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


class DatasetMaterialEntry(BaseModel):
    """Один материал в датасете."""

    material_id: str = Field(..., description="Materials Project ID", examples=["mvc-8151"])
    formula: str = Field(..., description="Химическая формула", examples=["MgSn(GeO3)2"])
    structure: str = Field(..., description="Кристаллическая структура в формате CIF")
    formation_energy_per_atom: float | None = Field(
        default=None, description="Энергия формирования на атом (эВ)"
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


class DatasetMaterialEntryNoStructure(BaseModel):
    """Один материал в датасете (без структуры)."""

    material_id: str = Field(..., description="Materials Project ID", examples=["mvc-8151"])
    formula: str = Field(..., description="Химическая формула", examples=["MgSn(GeO3)2"])
    formation_energy_per_atom: float | None = Field(
        default=None, description="Энергия формирования на атом (эВ)"
    )


class DatasetMaterialEntryWithStructure(BaseModel):
    """Один материал в датасете (со структурой)."""

    material_id: str = Field(..., description="Materials Project ID", examples=["mvc-8151"])
    formula: str = Field(..., description="Химическая формула", examples=["MgSn(GeO3)2"])
    formation_energy_per_atom: float | None = Field(
        default=None, description="Энергия формирования на атом (эВ)"
    )
    structure: str = Field(..., description="Кристаллическая структура в формате CIF")


class DatasetDetailResponse(BaseModel):
    """Результат получения датасета."""

    dataset_name: str = Field(..., description="Имя датасета", examples=["my_dataset"])
    with_struct: bool = Field(
        default=False, description="Включены ли структуры в ответ", examples=[False]
    )
    total_materials: int = Field(
        ..., description="Общее количество материалов в датасете", examples=[42]
    )
    materials: list[DatasetMaterialEntryNoStructure | DatasetMaterialEntryWithStructure] = Field(
        default_factory=list, description="Список материалов (с или без структур)"
    )


class DatasetListResponse(BaseModel):
    """Список доступных датасетов."""

    datasets: list[str] = Field(
        default_factory=list, description="Имена доступных датасетов", examples=[["max-phase", "vanad"]]
    )
    total: int = Field(..., description="Общее количество датасетов", examples=[2])


class ModelListResponse(BaseModel):
    """Список доступных моделей."""

    models: list[str] = Field(
        default_factory=list, description="Имена доступных моделей", examples=[["max_phase_model", "test_model"]]
    )
    total: int = Field(..., description="Общее количество моделей", examples=[2])


class FineTuningRequest(BaseModel):
    """Запрос на дообучение модели."""

    model_name: str = Field(
        ...,
        description="Имя для новой дообученной модели",
        examples=["my_finetuned_model"],
    )
    dataset_name: str = Field(
        ...,
        description="Имя датасета для дообучения (файл из каталога datasets)",
        examples=["vanad"],
    )


class FineTuningResult(BaseModel):
    """Результат дообучения модели."""

    model_name: str = Field(..., description="Имя дообученной модели", examples=["my_finetuned_model"])
    dataset_name: str = Field(..., description="Имя использованного датасета", examples=["vanad"])
    status: str = Field(..., description="Статус дообучения", examples=["completed"])
    log_file: str = Field(..., description="Путь к файлу лога с метриками")
    final_train_mae: float | None = Field(
        default=None, description="Финальная MAE на обучающей выборке"
    )
    final_val_mae: float | None = Field(
        default=None, description="Финальная MAE на валидационной выборке"
    )
    final_train_loss: float | None = Field(
        default=None, description="Финальная общая потеря на обучающей выборке"
    )
    final_val_loss: float | None = Field(
        default=None, description="Финальная общая потеря на валидационной выборке"
    )


class FineTuningStatusResponse(BaseModel):
    """Статус задачи дообучения."""

    model_name: str = Field(..., description="Имя модели", examples=["my_finetuned_model"])
    status: str = Field(
        ...,
        description="Статус: running, completed, failed, not_found",
        examples=["completed"],
    )
    result: FineTuningResult | None = Field(
        default=None, description="Результат дообучения (если завершено)"
    )
    error: str | None = Field(
        default=None, description="Текст ошибки (если failed)"
    )
