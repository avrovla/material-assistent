# Functional Test Cases — MATGL API

## Project Overview
REST API for materials science built with FastAPI, providing:
- Materials Project data lookup
- Material search by chemical elements
- Formation energy prediction using M3GNet models
- Dataset management (create, read, delete)
- Model fine-tuning capabilities

---

## Table of Contents
1. [Max-Phase Expert](#1-max-phase-expert)
2. [Dataset Expert](#2-dataset-expert)
3. [Fine-Tuning expert](#3-fine-tuning-expert)
4. [Formation Energy Prediction](#4-formation-energy-prediction)

---

## 1. Max-Phase Expert

> See detailed test cases: [module-max-phase-expert.md](./module-max-phase-expert.md)

### Test Cases
- **TC-MP-001**: Get MAX Phases — Success with Mixed Results (1 Test)

---

## 2. Dataset Expert

> See detailed test cases: [module-dataset-expert.md](./module-dataset-expert.md)

### Test Cases
- **TC-DS-001**: Create Dataset — Success with New Name
- **TC-DS-002**: Create Dataset — Reject Existing Name
- **TC-DS-003**: Create Dataset — Large File Performance (3 Tests)

---

## 3. Fine-Tuning Expert

> See detailed test cases: [module-fine-tuning-expert.md](./module-fine-tuning-expert.md)

### Test Cases
- **TC-FT-001**: Start Fine-Tuning — Success with New Model Name
- **TC-FT-002**: Start Fine-Tuning — Reject Existing Model Name

---

## 4. Formation Energy Prediction

> See detailed test cases: [module-formation-energy-prediction.md](./module-formation-energy-prediction.md)

### Test Cases
- **TC-FE-001**: Predict Formation Energy via Fine-Tuned Model — Success
- **TC-FE-002**: Predict Formation Energy via Base Model — Success

---

## Test Coverage Summary

| Module | Tool | Test Cases |
|--------|-----------|------------|
| MAX-Phase Expert | 1 | 1 |
| Dataset Expert | 1 | 3 |
| Fine-Tuning Expert | 1 | 2 |
| Formation Energy Prediction | 1 | 2 |
| **Total** | **4** | **8** |
