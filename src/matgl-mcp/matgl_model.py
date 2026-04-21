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
