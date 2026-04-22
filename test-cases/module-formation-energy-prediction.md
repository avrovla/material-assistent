# Formation Energy Prediction Module — Test Cases

> Source: [functional-tests.md](../functional-tests.md#1-max-phase-expert)

## 1. Formation Energy Prediction

### TC-FE-001: Predict Formation Energy via Fine-Tuned Model — Success
**Skill:** 
**Description:** Successfully retrieve formation energy via fine-tuned model
**Preconditions:** 
- model `test_model` exists in system
- valid cif data

**Test Steps:**
1. User sends request: "вызови инструмент `matgl-mcp/predict_formation_energy` с параметром model_name равным `test_model` и параметром cif равным `<valid cif data>`"
2. Verify skill calls `matgl-mcp/predict_formation_energy` with model_name="test_model" and cif="<valid cif data>"
3. Verify response contains formation energy value

**Expected Result:** agent shows formation energy


### TC-FE-002: Predict Formation Energy via Base Model — Success
**Skill:** 
**Description:** Successfully retrieve formation energy via base model
**Preconditions:** 
- model `test_model` exists in system
- valid cif data

**Test Steps:**
1. User sends request: "вызови инструмент `matgl-mcp/predict_formation_energy_default` с параметром cif равным `<valid cif data>`"
2. Verify skill calls `matgl-mcp/predict_formation_energy_default` with cif="<valid cif data>"
3. Verify response contains formation energy value

**Expected Result:** agent shows formation energy