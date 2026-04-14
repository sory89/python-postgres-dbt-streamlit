# 🚀 Modern Data Pipeline — PostgreSQL + dbt + Streamlit

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

---

## 📌 Overview

This project demonstrates a **production-grade modern data pipeline** built with open-source technologies, following **DataOps and Analytics Engineering best practices**.

It simulates a **real-world data platform**, covering the full lifecycle:
**data ingestion → transformation → analytics → visualization**

---

## 🎯 Business Value

- Deliver **clean, reliable, and analytics-ready datasets**
- Enable **data-driven decision making**
- Reduce data processing complexity through **modular architecture**
- Improve scalability and maintainability of data workflows

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
<img width="959" height="512" alt="image" src="https://github.com/user-attachments/assets/66f82678-309a-446a-9c5e-31b76a53438b" />


---

## 🧠 Data Modeling (dbt)

The project follows a **layered architecture**:

- **Raw Layer** → Ingested data  
- **Staging Layer** → Cleaned & standardized data  
- **Mart Layer** → Business-ready datasets  

---

## ▶️ Getting Started


### 1. Create virtual environment

python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

#### 2. Install dependencies

pip install -r requirements.txt

##### 3. Setup PostgreSQL
Create a database
Update connection settings in your config file

##### 4. Run dbt
dbt run
dbt test

###### 5. Launch Streamlit
streamlit run dashboard/app.py
