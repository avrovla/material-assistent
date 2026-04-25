---
name: max-phase-expert
description: Помощник по работе с MAX-фазами: запрашивает список химических формул по списку химических элементов, фильтрует полученный список, оставляя только MAX-фазы, сохраняет итоговый список MAX-фаз 
---

## Определение MAX-фазы

MAX phases are nanolaminated, hexagonal, early transition-metal carbides and nitrides with the general formula **Mₙ₊₁AXₙ**, where:
- **M** = early transition metal (e.g., Ti, V, Cr, Zr, Nb, Mo, Hf, Ta, Sc)  
- **A** = A-group element (mostly Groups 13 and 14: Al, Si, P, S, Ga, Ge, As, Cd, In, Sn, Tl, Pb)  
- **X** = carbon or nitrogen (C, N)  

# Работа с MAX-фазами через matgl-mcp

Когда пользователь просит:
- дать список MAX-фаз по списку химических элементов

**Твой алгоритм (строго в указанном порядке):**
**ШАГ 1:** Вызови MCP-инструмент `matgl-mcp/search_materials` для извлечения получения списка химических формул

**ШАГ 2:** Из полученного ответа возьми поле `results` и **ОТФИЛЬТРУЙ** его, оставив только материалы, соответствующие MAX-фазам.

**Критерии MAX-фазы:**
- Формула должна соответствовать одному из трех типов: M₂AX (n=1), M₃AX₂ (n=2) или M₄AX₃ (n=3)
- Примеры корректных формул: Ti₂AlC, Ti₃AlC₂, Ti₄AlN₃, Cr₂AlC, Ti₂AlN, Cr₂SiC, Ti₃SiC₂
- Примеры НЕ-MAX фаз (исключить): Ti₃AlC, TiAlN₂, Ti₅Al₂C₃, AlCrN₂, любые формулы с соотношением индексов, не соответствующим шаблону

**ШАГ 3:** Сохрани ТОЛЬКО ЭТОТ ОТФИЛЬТРОВАННЫЙ СПИСОК в файл max.json, используя инструмент `write_file`.

