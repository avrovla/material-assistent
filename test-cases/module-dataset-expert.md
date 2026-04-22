# Dataset Expert Module — Test Cases

> Source: [functional-tests.md](../functional-tests.md#2-dataset-expert)

## 2. Dataset Expert Skill

### TC-DS-001: Create Dataset — Success with New Name
**Skill:** `dataset-expert`
**Description:** Successfully create a new dataset when name doesn't exist
**Preconditions:** 
- file `materials.json` exists with content `["Ti2AlC", "Ti3AlC2", "Ti4AlN3", "Cr2SiC"]`
- dataset `test_new_dataset` does not exist in system

**Test Steps:**
1. User sends request: "сформируй датасет по списку материалов из файла materials.json с именем test_new_dataset"
2. Verify skill calls `matgl-mcp/list_datasets` (Step 1)
3. Verify skill shows dataset list to user
4. Verify skill checks that test_new_dataset is NOT in the list (Step 2)
5. Verify skill calls read_file with filename="materials.txt" (Step 3)
6. Verify skill calls matgl-mcp/list_datasets with:
- `input`=`["SiO2", "TiO2", "Al2O3"]`
- `ds_name`=`test_new_dataset` (Step 4)
7. Verify user receives success confirmation

**Expected Result:** Dataset `test_new_dataset` created successfully with 4 formulas

---

### TC-DS-002: Create Dataset — Reject Existing Name
**Skill:** `dataset-expert`
**Description:** Reject dataset creation when name already exists
**Preconditions:** 
- file `materials.json` exists with content `["Ti2AlC", "Ti3AlC2", "Ti4AlN3", "Cr2SiC"]`
- dataset `test_new_dataset` exists in system

**Test Steps:**
1. User sends request: "сформируй датасет по списку материалов из файла materials.json с именем test_new_dataset"
2. Verify skill calls `matgl-mcp/list_datasets` (Step 1)
3. Verify skill shows dataset list to user
4. Verify skill finds `test_new_dataset` in the list (Step 2)
5. Verify skill does NOT proceed to Step 3
6. Verify read_file is NEVER called
7. Verify user receives success confirmation
8. Verify `matgl-mcp/list_datasets` (creation) is NEVER called

**Expected Result:** Operation rejected with user-friendly message about duplicate name

---

### TC-DS-003: Create Dataset — Large File Performance
**Skill:** `dataset-expert`
**Description:** Test performance with large file containing many formulas
**Preconditions:** 
- file `large.json` exists with 10,000 chemical formulas
- dataset `test_new_dataset` does not exist in system

**Test Steps:**
1. User sends request with large file
2. Verify Step 1 completes within 5 seconds
3. Verify Step 2 completes within 1 second
4. Verify `read_file` loads file efficiently (Step 3)
5. Verify Step 4 processes all formulas
6. Measure total execution time

**Expected Result:** Operation completes within reasonable time
