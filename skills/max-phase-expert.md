---
name: max-phase-expert
description: Помощник по работе с MAX-фазами: запрашивает список химических формул по списку химических элементов, фильтрует полученный список, оставляя только MAX-фазы, сохраняет итоговый список MAX-фаз 
---

## Определение MAX-фазы

MAX phases are nanolaminated, hexagonal, early transition-metal carbides and nitrides with the general formula **Mₙ₊₁AXₙ**, where:
- **n = 1, 2, or 3** (number of M layers)- **M** = early transition metal (e.g., Ti, V, Cr, Zr, Nb, Mo, Hf, Ta) [citation:2]
- **A** = A-group element (mostly Groups 13 and 14: Al, Si, Ga, Ge, Sn, etc.) [citation:2]
- **X** = carbon and/or nitrogen [citation:1]

# Работа с MAX-фазами через matgl-mcp

Когда пользователь просит:
- дать список MAX-фаз по списку химических элементов

**Твой алгоритм:**
1. Используй MCP-инструмент `matgl-mcp/search-materials` для извлечения получения списка химических формул
2. Из полученного списка отбери только те, которые являются MAX-фазами
3. Отобранные MAX-фазы сохрани в текущий каталог в JSON-файл max.json, используя инструмент `write_file`

## Пример

**Пользователь:** «Сформируй список MAX-фаз по списку [[Ti, Cr],[Al, Si],[C, N]]»

**Твои действия:**
Вызови MCP-инструмент: `matgl-mcp/search-materials` с параметром `element_lists: [["Ti", "Cr"],["Al", "Si"],["C", "N"]]`