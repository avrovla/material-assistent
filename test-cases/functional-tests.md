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
- **TC-MP-001**: Health Check — Success (1 test)

---

## 2. Dataset Expert

> See detailed test cases: [module-dataset-expert.md](./module-dataset-expert.md)

### Test Cases
- **TC-DS-001**: Get Material by ID — Success
- **TC-DS-002**: Get Material by ID — Not Found
- **TC-DS-003**: Get Material by ID — Missing API Key (3 tests)

---

## 3. Fine-Tuning Expert

> See detailed test cases: [module-fine-tuning-expert.md](./module-fine-tuning-expert.md)

### Test Cases
- **TC-FT-001**: Search Materials — Success with Results
- **TC-FT-002**: Search Materials — Multiple Element Combinations
- **TC-FT-003**: Search Materials — No Results
- **TC-FT-004**: Search Materials — Invalid Request Body
- **TC-FT-005**: Search Materials — Caching Behavior (5 tests)

---

## 4. Formation Energy Prediction

> See detailed test cases: [module-formation-energy-prediction.md](./module-formation-energy-prediction.md)

### Test Cases
- **TC-FE-001**: Clear Search Cache — Success (1 test)

---

## Test Coverage Summary

| Module | Endpoints | Test Cases |
|--------|-----------|------------|
| Health | 1 | 1 |
| Materials (lookup) | 1 | 3 |
| Materials (search) | 2 | 5 |
| Datasets | 5 | 8 |
| Prediction | 1 | 5 |
| Fine-Tuning | 2 | 8 |
| Error Handling | N/A | 6 |
| **Total** | **12** | **36** |
