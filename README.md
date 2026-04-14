# 🚀 Modern Data Pipeline (PostgreSQL + dbt + Streamlit)

## 📌 Overview

This project demonstrates a modern end-to-end data pipeline using open-source tools:

- 🐍 Python for data ingestion  
- 🐘 PostgreSQL for data storage  
- ⚙️ dbt (data build tool) for transformations  
- 📊 Streamlit for data visualization  

The goal is to simulate a **production-ready analytics workflow** with a scalable architecture.

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

- Python  
- PostgreSQL  
- dbt-core  
- Streamlit  

---

---

## 🚀 Features

- Automated data ingestion  
- Layered data modeling (raw → staging → mart)  
- SQL transformations with dbt  
- Interactive dashboards with Streamlit  
- Modular and reproducible pipeline  

---

pip install -r requirements.txt


<img width="956" height="490" alt="image" src="https://github.com/user-attachments/assets/ea772d7c-084c-4640-b508-f944a203bd6f" />
