# Fine-Tuning Expert Module — Test Cases

> Source: [functional-tests.md](../functional-tests.md#3-fine-tuning-expert)

## 3. Fine-Tuning Expert Skill

### TC-FT-001: Start Fine-Tuning — Success with New Model Name
**Skill:** `fine-tuning-expert`
**Description:** Successfully start fine-tuning with unique model name and existing dataset
**Preconditions:** 
- dataset `training_dataset` exists in system
- model `my_finetuned_model` does NOT exist

**Test Steps:**
1. User sends request: "выполнить дообучение модели с именем `my_finetuned_model` на основе датасета `training_dataset`"
2. Verify skill calls `matgl-mcp/list_fine_tuned_models` (Step 1)
3. Verify skill shows existing models list to user
4. Verify skill checks that `my_finetuned_model` is NOT in the list (Step 2)
5. Verify skill calls `matgl-mcp/start_fine_tuning` with:
- model_name="my_finetuned_model"
- dataset_name="training_dataset" (Step 3)
6. Verify skill calls `matgl-mcp/get_fine_tuning_status` with model_name="my_finetuned_model" (Step 4)
7. Verify status is "running"
8. Verify user informed: "дообучение (fine-tuning) в процессе"
9. Verify skill asks: "нужно ли повторить проверку статуса дообучения?" (Step 5)

**Expected Result:** fine-tuning started successfully, user sees running status and gets follow-up prompt


### TC-FT-002: Start Fine-Tuning — Reject Existing Model Name
**Skill:** `fine-tuning-expert`
**Description:** Reject fine-tuning when model name already exists
**Preconditions:** 
- dataset `training_dataset` exists in system
- model `my_finetuned_model` already exists in system

**Test Steps:**
User sends request: "выполнить дообучение модели с именем existing_model на основе датасета training_dataset"

1. Verify skill calls `matgl-mcp/list_fine_tuned_models` (Step 1)
2. Verify skill shows existing models list
3. Verify skill finds `existing_model` in the list (Step 2)
4. Verify skill does NOT proceed to Step 3
5. Verify `matgl-mcp/start_fine_tuning` is NEVER called
6. Verify `matgl-mcp/get_fine_tuning_status` is NEVER called
7. Verify user receives message: "пользователь должен использовать другое имя для модели"

**Expected Result:** Operation rejected with message about duplicate model name
