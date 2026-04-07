# 🧹 Data Cleaning Environment API

A FastAPI-based simulation environment for structured data cleaning tasks.
This project models data cleaning as a step-by-step decision-making process with rewards and evaluation.

---

## 🚀 Features

* Multi-level datasets: **Easy, Medium, Hard**
* Action-based data cleaning:

  * Fill missing values
  * Standardize names
  * Convert data types
  * Fix date formats
  * Remove duplicates
* Reward system for tracking progress
* Baseline agent for automated solving
* Grader for evaluating dataset accuracy

---

## 📂 Project Structure

```
api/            # FastAPI routes
env/            # Environment logic
graders/        # Evaluation logic
tasks/          # Dataset definitions
server/         # Deployment entry point
```

---

## ⚙️ Setup & Run Locally

### 1. Clone the repository

```
git clone https://github.com/elveena-castelino/data-cleaning-env.git
cd data-cleaning-env
```

---

### 2. Create virtual environment

```
python -m venv .venv
```

Activate:

* Windows (PowerShell):

```
.\.venv\Scripts\Activate.ps1
```

* Windows (CMD):

```
.venv\Scripts\activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

OR:

```
pip install uv
uv sync
```

---

### 4. Run server

```
uvicorn api.app:app --reload
```

---

## 📡 API Endpoints

### Reset environment

```
POST /reset?task=easy
```

---

### Perform action

```
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

### Get state

```
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

### Evaluate dataset

```
GET /grader
```

---

### Run baseline

```
GET /baseline?task=easy
```

---

## 🧠 How It Works

* Start with a dirty dataset
* Apply actions step-by-step
* Track remaining errors
* Receive rewards for improvements
* Goal: **clean dataset completely**

---

## 📌 Notes

* Date format: **"March 12, 2024"**
* Only `"age"` column is used for:

  * fill_missing
  * convert_type

---

## 👥 Team

Team Bug Smashers

* Rian
* Amogh
* Elveena

---

## 📌 Final Note

This project demonstrates how structured environments can support intelligent decision-making systems using rule-based transformations and agent workflows.
