# Human Development Index (HDI) Prediction — ML Web Application

A machine learning web application that predicts a country's **Human
Development Index (HDI)** score and classifies it into one of four
development tiers — **Very High, High, Medium, Low** — based on life
expectancy, education, and income indicators. Built with **Scikit-learn**
(Linear Regression) and deployed through a **Flask** web interface.

---
Project video Url : https://youtu.be/QeJ3HT0UWyI
## Table of Contents

- [Human Development Index (HDI) Prediction — ML Web Application](#human-development-index-hdi-prediction--ml-web-application)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Project Structure](#project-structure)
  - [Entity-Relationship Diagram](#entity-relationship-diagram)
  - [Tech Stack](#tech-stack)
  - [Dataset](#dataset)
  - [Machine Learning Workflow](#machine-learning-workflow)
  - [Setup \& Installation](#setup--installation)
  - [Running the Notebook](#running-the-notebook)
  - [Running the Flask App](#running-the-flask-app)
  - [Usage Scenarios](#usage-scenarios)
  - [Model Performance](#model-performance)
  - [Project Epics \& Stories](#project-epics--stories)
  - [Future Scope](#future-scope)

---

## Overview

The Human Development Index (HDI) is a statistical composite index of life
expectancy, education, and per-capita income indicators used to rank
countries into four tiers of human development. A country achieves a
higher HDI when its population enjoys a longer lifespan, better educational
attainment, and a higher Gross National Income (GNI PPP) per capita.

The HDI was developed to emphasize that **people and their capabilities**
should be the primary measure of a country's development, rather than
economic growth alone. It is widely used by governments, researchers,
policymakers, and international organizations to evaluate progress, compare
countries, and identify areas requiring improvement.

This project trains a **Linear Regression** model on socio-economic
indicators to predict a country's HDI score, then serves that model through
a Flask web application with an interactive prediction form.

---

## Project Structure

```
ML - 0027 - Human Development Index/
│
├── Dataset/
│   └── HDI.csv                  # Training dataset (country-level indicators)
│
├── Flask/
│   ├── app.py                   # Flask backend (routes + prediction logic)
│   ├── HDI.pkl                  # Trained Linear Regression model (Pickle)
│   ├── country_encoder.pkl      # Fitted LabelEncoder for country names
│   ├── countries_list.pkl       # Country list used for the dropdown UI
│   ├── templates/
│   │   ├── home.html            # Landing / introduction page
│   │   └── indexnew.html        # Prediction form + result page
│   └── static/                  # (reserved for CSS/JS/images, if added)
│
├── Training/
│   └── HumDevIndex.ipynb        # Full ML workflow notebook (EDA → training → export)
│
└── README.md                    # Project documentation (this file)
```

This mirrors the intended project layout: a dedicated `Dataset` folder for
raw data, a `Training` folder for the notebook that produces the model
artifacts, and a `Flask` folder that contains everything needed to run the
web app in isolation (it only depends on the three `.pkl` files, not on the
notebook or CSV).

---

## Entity-Relationship Diagram

The application's data model (for a full production system with user
accounts, sessions, and stored predictions) is composed of eight entities:

| Entity | Primary Key | Purpose |
|---|---|---|
| **User** | `user_id` | Registered users of the platform |
| **Session** | `session_id` | Login/logout session tracking per user |
| **Country** | `country_id` | Reference data for each country/region |
| **HDI_Input_Data** | `input_id` | Raw indicators submitted for prediction |
| **Dataset** | `dataset_id` | Metadata about training datasets |
| **ML_Model** | `model_id` | Metadata about trained models |
| **HDI_Prediction** | `prediction_id` | Model output for a given input |
| **Visualization_Report** | `report_id` | Generated charts/reports per prediction |

**Key relationships:**
- `User` → `HDI_Input_Data`: One user can submit many prediction inputs (1:N)
- `Country` → `HDI_Input_Data`: One country can have many input records (1:N)
- `HDI_Input_Data` → `HDI_Prediction`: One input produces one prediction (1:1)
- `ML_Model` → `HDI_Prediction`: One model produces many predictions (1:N)
- `HDI_Prediction` → `Visualization_Report`: One prediction can generate many reports (1:N)
- `Dataset` → `ML_Model`: One dataset can train many models (1:N)
- `User` → `Session`: One user can have many sessions (1:N)

*(This notebook/Flask app implements the core prediction pipeline —
`HDI_Input_Data` → `ML_Model` → `HDI_Prediction` — described in the ERD. The
`User`, `Session`, and `Visualization_Report` entities represent the natural
extension points for adding authentication and report history.)*

---

## Tech Stack

| Tool | Purpose |
|---|---|
| **Anaconda Navigator** | Environment & package management |
| **PyCharm** | IDE for development |
| **NumPy** | Numerical computing |
| **Pandas** | Data loading, cleaning, manipulation |
| **Matplotlib** | Base plotting |
| **Seaborn** | Statistical visualizations |
| **Scikit-learn** | Model training & evaluation (Linear Regression) |
| **Pickle** | Model serialization |
| **Flask** | Web application framework |

---

## Dataset

`Dataset/HDI.csv` contains country-level records with the following columns:

| Column | Description |
|---|---|
| `country_name` | Name of the country |
| `region` | Geographic region |
| `population` | Population count |
| `life_expectancy` | Life expectancy at birth (years) |
| `mean_years_schooling` | Average years of schooling completed (adults 25+) |
| `expected_years_schooling` | Expected years of schooling for a child entering school |
| `gni_per_capita` | Gross National Income per capita (PPP $) |
| `internet_users_pct` | Percentage of population using the internet |
| `hdi_score` | Target variable — computed HDI score (0–1) |
| `hdi_category` | Derived label: Low / Medium / High / Very High |

> The dataset provided here is a **synthetic but realistic** dataset built
> to mirror standard HDI methodology and value ranges (comparable to UNDP
> Human Development Report data). To use real-world data instead, replace
> `HDI.csv` with a dataset from a source such as
> [Kaggle's Human Development Index dataset](https://www.kaggle.com/) —
> just keep the same column names, or update `Training/HumDevIndex.ipynb`
> and `Flask/app.py` to match your column names.

---

## Machine Learning Workflow

1. **Import libraries** — NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, Pickle
2. **Load & understand the dataset** — shape, types, summary statistics
3. **Exploratory Data Analysis** — distribution plots, scatter plots, strip
   plots, and a correlation heatmap
4. **Preprocessing**
   - Select independent variables (X) and target (Y)
   - Check and fill missing values using column means
   - Label-encode the categorical `country_name` column
5. **Train/Test Split** — 80% training, 20% testing
6. **Model Training** — `sklearn.linear_model.LinearRegression`
7. **Evaluation** — R², MAE, RMSE, and actual-vs-predicted visualization
8. **Serialization** — save the model, encoder, and country list with
   Pickle into `Flask/`

All of the above is implemented, in order, inside
`Training/HumDevIndex.ipynb` with explanatory markdown and inline code
comments for every step.

---

## Setup & Installation

```bash
# 1. Clone / copy the project, then move into it
cd "ML - 0027 - Human Development Index"

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the Notebook

```bash
cd Training
jupyter notebook HumDevIndex.ipynb
```

Run all cells top-to-bottom. This will:
- Load `../Dataset/HDI.csv`
- Perform EDA and preprocessing
- Train and evaluate the Linear Regression model
- Save `HDI.pkl`, `country_encoder.pkl`, and `countries_list.pkl` into `../Flask/`

> The `Flask/` folder already ships with pre-trained artifacts, so you can
> run the web app immediately without re-running the notebook. Re-run the
> notebook only if you change the dataset or want to retrain the model.

---

## Running the Flask App

```bash
cd Flask
python3 app.py
```

Then open **http://127.0.0.1:5000/** in your browser.

- **Home page (`/`)** — introduces the HDI project
- **Prediction page (`/predict`)** — select a country and enter:
  - Life expectancy (30–89)
  - Mean years of schooling (1–19)
  - Expected years of schooling (1–19)
  - GNI per capita (400–120,000)
  - Percentage of internet users (0–100)

  Click **Predict** to see the estimated HDI score and its development tier
  (Low / Medium / High / Very High).

---

## Usage Scenarios

**Scenario 1 — Predicting Very High Human Development**
A user selects a country with high life expectancy, strong schooling
indicators, and a high GNI per capita. The model predicts a **Very High**
HDI score, classifying the country among the most developed nations.

**Scenario 2 — Identifying Development Gaps in Emerging Economies**
A policymaker inputs mid-range values representing a developing nation. The
model returns a **Medium** HDI score, highlighting areas — healthcare,
education, or income — where targeted improvement could raise overall human
development.

**Scenario 3 — Assessing Countries Requiring Development Intervention**
A researcher evaluates a country with low life expectancy, limited
educational opportunities, and low GNI per capita. The model predicts a
**Low** HDI score, supporting governments and development organizations in
prioritizing investments and policy interventions.

---

## Model Performance

Trained on an 80/20 train/test split of the bundled dataset:

| Metric | Value |
|---|---|
| R² (coefficient of determination) | ≈ 0.97 |
| Mean Absolute Error (MAE) | ≈ 0.02 |
| Root Mean Squared Error (RMSE) | ≈ 0.03 |

(Exact values are printed inside the notebook each time it is executed, and
may vary slightly depending on the random train/test split and any dataset
updates.)

---

## Project Epics & Stories

**Epic 1 — Environment Setup and Package Installation**
- Install required Python packages, ML libraries, and Flask dependencies.
- Organize the project folder structure (Dataset, Flask, Training).

**Epic 2 — Importing Required Libraries**
- Import NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, Pickle, Flask.

**Epic 3 — Dataset Download and Understanding**
- Load the dataset; explore structure, features, target, and data types.
- Visualize patterns, trends, distributions, and relationships.

**Epic 4 — Data Preprocessing and Label Encoding**
- Select dependent/independent variables.
- Handle missing values (fill with column mean).
- Label-encode categorical `country_name`.

**Epic 5 — Dividing the Dataset into Train and Test Data**
- 80/20 split using `train_test_split`.

**Epic 6 — Fitting the Model**
- Train a Linear Regression model.
- Generate and inspect predictions.
- Evaluate with R², MAE, RMSE, and visual comparisons.

**Epic 7 — Saving the Model**
- Serialize the model, encoder, and country list with Pickle for reuse in
  the Flask app.

**Epic 8 — Building the Flask Web Application**
- Build routes (`/`, `/predict`) to handle requests, load the model, and
  return predictions.
- Create HTML templates (`home.html`, `indexnew.html`) for a user-friendly
  interface.
- Run, test, and validate the full web application.

---

## Future Scope

- Persist predictions and generated reports to a database using the full
  ER schema (`User`, `Session`, `HDI_Prediction`, `Visualization_Report`).
- Add user authentication so predictions can be tied to individual users
  and revisited later.
- Swap Linear Regression for ensemble models (Random Forest, Gradient
  Boosting) and compare performance.
- Replace the synthetic dataset with the official UNDP Human Development
  Report data for production-grade accuracy.
- Deploy the Flask app to a cloud platform (Render, Heroku, AWS) behind a
  production WSGI server (e.g. Gunicorn).

---

