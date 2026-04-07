---
title: Data Cleaning Environment
emoji: 🧹
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
---

# 🧹 Data Cleaning Environment API

🔗 Live Demo: https://huggingface.co/spaces/elveena05/data-cleaning-env
🔗 API Docs: https://huggingface.co/spaces/elveena05/data-cleaning-env/docs

A FastAPI-based simulation environment for structured data cleaning tasks, supporting step-wise actions, reward feedback, and evaluation.

---

## 🚀 Features

* Multi-level tasks: Easy, Medium, Hard
* Action-based data cleaning:

  * Fill missing values
  * Standardize names
  * Convert data types
  * Fix date formats
  * Remove duplicates
* Reward system for evaluating progress
* Baseline agent to solve tasks automatically
* Grader to evaluate final dataset accuracy

---

## 📂 Project Structure

```bash
api/            # FastAPI routes
env/            # Environment logic (core system)
graders/        # Evaluation logic
tasks/          # Dataset definitions (easy, medium, hard)
server/         # Entry point for deployment
```

---

## ⚙️ Setup & Run Locally

### 1. Clone repo

```bash
git clone https://github.com/elveena-castelino/data-cleaning-env.git
cd data-cleaning-env
```

---

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

OR (recommended):

```bash
pip install uv
uv sync
```

---

### 4. Run server

```bash
uvicorn api.app:app --reload
```

---

## 📡 API Endpoints

### 🔹 Reset environment

```http
POST /reset?task=easy
```

---

### 🔹 Perform action

```http
POST /step
```

Example:

```json
{
  "action_type": "fill_missing",
  "column": "age"
}
```

---

### 🔹 Get current state

```http
GET /state
```

Response:

```json
{
  "step_count": 1,
  "remaining_errors": 0
}
```

---

### 🔹 Evaluate dataset

```http
GET /grader
```

---

### 🔹 Run baseline agent

```http
GET /baseline?task=easy
```

---

## 🧠 How it Works

* The environment starts with a **dirty dataset**
* Each action modifies the dataset
* Errors are tracked dynamically
* Rewards are assigned based on improvement
* Goal: reach **0 remaining errors**

---

## 🎯 Example Flow

1. Reset environment
2. Apply actions step-by-step
3. Observe rewards and error reduction
4. Reach a clean dataset

---

## 📸 Sample Output

```json
{
  "step_count": 3,
  "remaining_errors": 0
}
```

---

## 🏁 Deployment

This project is compatible with:

* Hugging Face Spaces (Docker)
* OpenEnv validation system

---

## 📌 Notes

* Date format is standardized to:
  **"March 12, 2024"**
* Only `"age"` column is used for:

  * fill_missing
  * convert_type

---

## 👥 Team

* Team Bug Smashers: Rian, Amogh, Elveena

---

## 📌 Final Note

This project demonstrates how structured environments enable intelligent decision-making systems by combining rule-based transformations with agent-driven workflows.

---
