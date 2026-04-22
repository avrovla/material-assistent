# Журнал изменений по разработке ИИ-ассистента для материаловедения

**Студент:** Авакумов Роман Владимирович  
**Тема:** Разработка ИИ-ассистента для настройки модели M3GNet


---

## 21.04.2026

### Добавлено
- MCP-сервер matgl-mcp с инструментом: 
  - search_materials
  - list_datasets
  - create_dataset
  - get_material_from_mp
  - get_dataset
  - delete_dataset
- Навыки для ИИ-агента
  - max-phase-expert
  - dataset-expert

## 22.04.2026

### Добавлено
- Инструмент для MCP-сервера: 
  - get_material_from_mp
  - predict_formation_energy
  - predict_formation_energy_default
  - start_fine_tuning
  - list_fine_tuned_models
  - get_fine_tuning_status
- Навык для ИИ-агента
  - fine-tuning-expert


## 23.04.2026

### Добавлено
- Тест-кейсы: 
  - module-max-phase-expert
  - module-dataset-expert
  - module-fine-tuning-expert
  - module-formation-energy-prediction-expert
