# Phase 0

## Project Charter

### 1. Background

**TheLook's E-Commerce** is a fictional online retailer that sells apparel and accessories to customers across multiple regions. The business team seeks to understand s**ales performance, customer behaviors,** and **product trends** to make data-driven decisions. While the company collects rich transactional data, strategic decisions are still guided by intuition rather than evidence.

To remain competitive, the company wims to leverage data analytics to better understand customer behavior, optimize sales strategies, and support data-informed business deciosions.

### 2. Problem Statement

Despite steady customer acquisition, revenue growth has stagnated, and repeated purchase are declining. The management team seeks to uncover what drives **repeat purchases**, identify **profitable customer segments**, and determine how **marketing and product performance** influence sales.

Key Challenges:

- Fragmented understanding of customer lifetime value (CLV)
- Lack of data-driven targeting in marketing campaigns
- Inventory imbalances due to poor demand forecasting

### 3. Objectives

- Analyze historical customer and order data to identify factors influencing repeat purchases.
- Segment customers based on purchase frequency, demographics, and monetary value.
- Evaluate the effectiveness of marketing channels in driving conversions.
- Detect sales trends and seasonal demand fluctuations to improve inventory allocation.
- Develop a preliminary churn prediction model to flag at-risk customers.

### 4. Business Success Criteria (KPIS)

Project success will be measured through quantifiable outcomes that align with TheLook’s business goals:

| Area | KPI | Target |
| --- | --- | --- |
| Customer Retention | Repeat purchase rate | +5 % |
| Churn Modeling | Predictive accuracy (ROC-AUC) | ≥ 0.85 |
| Revenue Growth | Quarterly sales | +10 % |
| Inventory Efficiency | Overstock / stock-out reduction | –15 % |
| Marketing ROI | Conversion rate | +7 % |

### 5. Constraints and Assumptions

- Data is sourced from Google BigQuery’s public *TheLook* dataset.
- Analysis timeframe: 6–8 weeks.
- Tools: Python (3.11), PostgreSQL (Docker), PyCharm, Pandas, Seaborn, Scikit-learn.
- The data is static and anonymized; external real-time integrations are out of scope.

### 6. Impact

By delivering a comprehensive analytical framework, the project will enable TheLook’s leadership to make **evidence-based strategic decisions**. Insights will inform targeted marketing, improve customer engagement, and reduce operational inefficiencies. The final deliverables—exploratory reports, predictive models, and dashboards—will provide lasting value by integrating data analytics into the company’s decision-making culture.

---

---

## **Business Questions**

1. Which product categories and regions generate the highest revenue and profit margin?
2. How do age, gender, or region influence purchase frequency and spend?
3. What is the average time between first and repeat purchases?
4. Which marketing channels yield the highest customer retention?
5. Which products experience the highest return or cancellation rates?
6. What seasonal patterns exist in monthly or weekly sales volume?
7. Can we predict which customers are likely to churn within the next quarter?

---

---

## Success Metrics (KPIS)

| Area | Metric | Target | Computation | Data Source |
| --- | --- | --- | --- | --- |
| **Sales** | Total quarterly revenue | +10 % | (Current Quarter – Previous) / Previous × 100 | Orders |
| **Customer Behavior** | Repeat purchase rate | +5 % | Repeat Orders / Total Customers | Orders × Customers |
| **Churn Prediction** | Model accuracy (ROC-AUC) | ≥ 0.85 | Model Evaluation | Customer history |
| **Marketing** | Conversion rate | +7 % | Orders / Campaign Interactions | Marketing attribution |
| **Inventory** | Overstock / stock-out rate | –15 % | Stock-out Frequency | Products + Orders |
| **Operational Efficiency** | ETL pipeline reliability | ≥ 99 % | Successful Runs / Total Runs | Logs |

## Roadmap and Tech Stack Outline

| Phase | Goal | Tools / Tech | Key Deliverables |
| --- | --- | --- | --- |
| **0 – Business Understanding** | Define goals, KPIs, success criteria | — | Project Charter, KPIs |
| **1 – Data Acquisition** | Ingest data from BigQuery (TheLook) | **PostgreSQL / Docker** | Raw tables schema |
| **2 – Data Preparation** | Clean, join, and validate datasets | **Python (Pandas, SQLAlchemy)** | Clean dataset |
| **3 – Exploratory Analysis** | Identify key trends & patterns | **Matplotlib, Seaborn** | EDA report |
| **4 – Modeling & Insights** | Predict churn & segment customers | **Scikit-learn** | Predictive Model |
| **5 – Visualization & Reporting** | Communicate insights interactively | **Power BI / Streamlit** | Dashboard |
| **6 – Documentation & Deployment** | Ensure reproducibility | **GitHub, PyCharm** | Final report + README |

**Tech Stack:**

- **Programming:** Python (3.11)
- **Database:** PostgreSQL + pgAdmin via Docker
- **IDE:** PyCharm
- **Version Control:** Git + GitHub
- **Analytics:** Pandas, Matplotlib, Seaborn, Scikit-learn
- **Visualization:** Power BI / Streamlit

-----------------------------------------------------------------------------------------------------------------------------

# Phase 1
## Environment Setup

I ran **PostgresSQL** and **pgAdmin4** with Docker Compose for a reproducible, portable setup.

- **Postgres** stores the project data; it is exposed on host port 5433 to avoid clashing with any local Postgres
- **pgAdmin** gives a friendly DB GUI at http://localhost:8080
- A **healthcheck** waits for Postgres to be ready before pgAdmin starts, making startup more relaible.
### a. Launch docker and verify details 

``docker --version``\
``docker info``\
``docker ps``


## Project Structure
````
lookecommerce-sql-analytics/
├── docker-compose.yml
├── README.md
├── data/
│   ├── raw/
│   ├── processed/
│   └── schema/
├── sql/
│   ├── 01_schema/
│   ├── 02_ingestion/
│   ├── 03_exploration/
│   ├── 04_analysis/
│   └── 05_advanced/
├── scripts/
│   ├── etl/
│   ├── validation/
│   └── utilities/
├── docs/
├── tests/
└── screenshots/
````

Troubleshooting
- **Port already in use:** change to ``- "5434:5432"`` and use 5434 in your IDE.
- **pgAdmin can’t connect:** ensure you used ``Host=db, Port=5432`` inside pgAdmin.
- **Healthcheck keeps failing:** docker compose logs -f db and verify credentials/DB name.
- **Windows volume errors:** you’re using named volumes (good). If you later bind-mount host folders, use absolute paths.
