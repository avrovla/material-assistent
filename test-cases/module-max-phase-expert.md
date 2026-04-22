# MAX-Phase Expert Module — Test Cases

> Source: [functional-tests.md](../functional-tests.md#1-max-phase-expert)

## 1. MAX-Phase Expert Skill

### TC-MP-001: Get MAX Phases — Success with Mixed Results
**Skill:** `max-phase-expert`
**Description:** Successfully retrieve and filter MAX phases from mixed material results
**Preconditions:** 
- search returns mix of MAX phases and non-MAX phases

**Test Steps:**
1. User sends request: "дай список MAX-фаз по списку химических элементов `[["Ti", "V"], ["Al", "Si"], ["C", "N"]]`"
2. Verify skill calls `matgl-mcp/search_materials` with elements `[["Ti", "V"], ["Al", "Si"], ["C", "N"]]` (Step 1)
3. Verify response contains results array with multiple materials
4. Verify skill filters results keeping only MAX-phases (Step 2):
5. Verify skill calls `write_file` with filtered list to `max.json` (Step 3)
6. Verify user receives confirmation with count of MAX-phases found

**Expected Result:** `max.json` contains only valid MAX phase formulas from the search results
