# 🧾 Data Cleaning Analyst Environment (OpenEnv)

## 🚀 Overview

This project implements a **real-world OpenEnv environment** simulating the task of a data analyst cleaning messy datasets.

Data cleaning is one of the most time-consuming and critical steps in real-world data workflows. This environment allows AI agents to learn and be evaluated on:

* Handling missing values
* Standardizing inconsistent formats
* Converting incorrect data types
* Removing duplicates
* Fixing real-world noisy data

---

## 🎯 Why this matters

In real-world data science pipelines:

> **Up to 80% of time is spent cleaning data**

This environment models that exact workflow in a structured, testable way — making it highly useful for training and evaluating AI agents.

---

## 🧠 Environment Design

### Observation Space

```json
{
  "dataset": [...],
  "step_count": int,
  "remaining_errors": int
}
```

---

### Action Space

```json
{
  "action_type": "fill_missing | standardize_name | convert_type | fix_date_format | remove_duplicates",
  "column": "optional"
}
```

---

### Reward Function

The reward is **dense and progressive**, encouraging efficient and correct cleaning:

* +0.15 per error fixed
* +0.05 efficiency bonus
* -0.05 for ineffective actions
* -0.25 for worsening dataset
* +0.5 completion bonus

---

## 🧪 Tasks

### 🟢 Easy — Missing Values

* Single error type
* Objective: fill missing values

---

### 🟡 Medium — Mixed Issues

* Missing values + inconsistent formats
* Requires multi-step reasoning

---

### 🔴 Hard — Real-world Noisy Data

* Duplicates
* Incorrect types ("thirty")
* Multiple date formats
* Extra spaces and inconsistencies

---

## 🧠 Grading System

Evaluation is deterministic and returns a score between **0.0 → 1.0**.

* Field-level accuracy scoring
* Partial credit for partially correct rows
* Exact match yields full score

---

## 🤖 Baseline Agent

A hybrid baseline agent is provided:

* Uses rule-based heuristics for stability
* Falls back to LLM for generalization

This ensures **reproducible and meaningful baseline scores**.

---

## 🌐 API Endpoints

| Endpoint    | Description            |
| ----------- | ---------------------- |
| `/reset`    | Initialize environment |
| `/step`     | Apply action           |
| `/state`    | Get current state      |
| `/tasks`    | List tasks             |
| `/grader`   | Get final score        |
| `/baseline` | Run baseline agent     |

---

## 🐳 Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run locally

```bash
uvicorn api.app:app --reload
```

### 3. Run baseline

```bash
python inference.py
```

---

## 🧪 Example (Before → After)

### Input

```json
{"name": "JOHN    DOE", "age": "thirty", "date": "03-12-24"}
```

### Output

```json
{"name": "John Doe", "age": 30, "date": "2024-03-12"}
```

---

## 🏆 Key Highlights

* Real-world task simulation
* Deterministic grading
* Dense reward shaping
* Multi-step reasoning environment
* Fully OpenEnv compliant
* Dockerized + deployable

---

## 📦 Deployment

This environment is containerized and deployable on **Hugging Face Spaces** using Docker.

---

## 👥 Team

* Team Bug Smashers: Rian, Amogh, Elveena

---

## 📌 Final Note

This project demonstrates how structured environments can bridge the gap between **LLMs and real-world decision-making tasks**.

---
