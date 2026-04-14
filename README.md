# 🚀 Modern Data Pipeline — PostgreSQL + dbt + Streamlit

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

---

## 📌 Overview

This project showcases a **modern end-to-end data pipeline** built using open-source tools, following DataOps and Analytics Engineering best practices.

It simulates a **production-ready data workflow**, from ingestion to business insights.

### 🔍 Key Objectives

- Build a scalable and modular data pipeline  
- Apply layered data modeling (raw → staging → mart)  
- Deliver business-ready insights through dashboards  

---

## 🏗️ Architecture

---

## 🏗️ Architecture

    +-------------+
    |   Python    |
    |  Ingestion  |
    +------+------+
           |
           v
    +-------------+
    | PostgreSQL  |
    |  Raw Data   |
    +------+------+
           |
           v
    +-------------+
    |     dbt     |
    | Transform   |
    +------+------+
           |
           v
    +-------------+
    |  Streamlit  |
    | Dashboard   |
    +-------------+

    ---

---

## ⚙️ Tech Stack

- 🐍 Python — data ingestion & processing  
- 🐘 PostgreSQL — relational data storage  
- ⚙️ dbt-core — data transformation (ELT)  
- 📊 Streamlit — interactive dashboards  

---

## 🚀 Features

- 🔄 Automated data ingestion pipeline  
- 🧱 Layered data modeling (raw → staging → mart)  
- ⚡ SQL-based transformations with dbt  
- 📈 Interactive dashboards with Streamlit  
- ♻️ Modular and reusable architecture  

---

## 📊 Data Pipeline Flow

1. **Ingestion (Python)**  
   - Collects and loads raw data into PostgreSQL  

2. **Storage (PostgreSQL)**  
   - Centralized structured data storage  

3. **Transformation (dbt)**  
   - Data cleaning and modeling  
   - Creation of analytics-ready tables  

4. **Visualization (Streamlit)**  
   - Interactive dashboards for business insights  

---

## 📈 Dashboard Preview

![Dashboard](https://github.com/user-attachments/assets/ea772d7c-084c-4640-b508-f944a203bd6f)

---

## 🧠 Data Modeling (dbt)

The project follows a **layered architecture**:

- **Raw Layer** → Ingested data  
- **Staging Layer** → Cleaned & standardized data  
- **Mart Layer** → Business-ready datasets  

---

## ▶️ Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
