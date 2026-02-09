# 📦 FMCG Demand Intelligence Platform
### Hybrid AI (Rules + ML + RAG + GPT) | SAP-Ready | FastAPI

---

## 🚀 Overview

This project is an **enterprise-grade FMCG Demand Intelligence platform** designed to **explain demand behavior**, **quantify supply risk**, and **support planner decisions** across **multiple products, channels, and regions**.

The system follows a **hybrid AI architecture**:

- **Rules** explain **WHY** demand changed  
- **ML** quantifies **HOW RISKY / HOW LIKELY**  
- **RAG** provides organizational memory  
- **GPT** generates governed, business-ready explanations  
- **Humans** remain the final decision-makers  

This design avoids black-box forecasting and is **SAP-compatible, auditable, and production-ready**.

---

## 🧠 Architecture (High Level)

```
SAP-like Data
   ↓
Signal Engineering
   ↓
Decision Graph (Rules – WHY)
   ↓
ML Risk Layer (Probability & Uncertainty)
   ↓
Channel + SKU Class Intelligence
   ↓
RAG (Historical Memory)
   ↓
GPT (Explanation Only)
   ↓
FastAPI Response
```

---

## 📊 Data Model (SAP-Like)

| Column | Description |
|------|------------|
| MATNR | SKU / Material |
| CATEGORY | Product category |
| SKU_CLASS | A / B |
| REGION | Sales region |
| VTWEG | Channel (GT / MT / ECOM / INST) |
| VKORG | Sales Organization |
| WERKS | Plant |
| CALWEEK | ISO Week |
| PROMO_FLAG | Promotion indicator |
| STOCK_QTY | Inventory quantity |
| SALES_QTY | Weekly sales |

---

## 🏪 Channels Supported

- **GT** – General Trade  
- **MT** – Modern Trade  
- **ECOM** – E‑Commerce  
- **INST** – Institutional / HoReCa  

Each channel has **distinct demand, volatility, and promo behavior**.

---

## 🧩 Core Capabilities

- Multi-SKU, multi-channel, multi-region support
- Channel-specific & SKU-class-specific rules
- Promotion & post-promotion logic
- Stock-out & availability impact detection
- Explainable ML risk scoring
- GPT-based explanation with strict guardrails

---

## 📂 Project Structure

```
fmcg_fastapi/
│
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── schemas.py           # API request/response models
│   ├── pipeline.py          # End-to-end orchestration
│
│   ├── logic/
│   │   ├── signals.py
│   │   ├── decision_graph.py
│   │   ├── ml_risk.py
│   │   ├── rag.py
│   │   └── gpt.py
│
│   ├── config/
│   │   ├── channel_thresholds.py
│   │   └── sku_channel_sensitivity.py
│
│   └── data/
│       └── sap_like_fmcg_sales_poc_all_channels.csv
│
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run the Application

### 1️⃣ Prerequisites
- Python **3.9+**
- pip installed

(Optional)
- Virtual environment recommended

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Start FastAPI Server

From the project root:

```bash
uvicorn app.main:app --reload
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

---

### 4️⃣ Open API Documentation (Swagger UI)

Open in browser:

```
http://127.0.0.1:8000/docs
```

This auto-generated UI allows you to **test all APIs interactively**.

---

## 🔌 Available APIs

### ✅ Health Check

**GET** `/health`

**Response**
```json
{
  "status": "ok"
}
```

Used for monitoring & readiness checks.

---

### ✅ Demand Explanation API

**POST** `/explain-demand`

This is the **core API** of the platform.

#### Request Body
```json
{
  "matnr": "BIS200",
  "region": "South",
  "channel": "ECOM",
  "calweek": "2024-W12"
}
```

#### Response
```json
{
  "matnr": "BIS200",
  "calweek": "2024-W12",
  "demand_reason": "PROMOTION_UPLIFT_STRONG",
  "confidence_level": "MEDIUM",
  "stockout_risk": "LOW",
  "forecast_uncertainty": "MEDIUM",
  "explanation": "Demand increase is driven by promotional activity in the E-commerce channel...",
  "historical_context": [
    "E-commerce promotions typically recover faster than GT."
  ]
}
```

---

## 🧪 How to Test Using curl (Optional)

```bash
curl -X POST "http://127.0.0.1:8000/explain-demand" -H "Content-Type: application/json" -d '{
  "matnr": "BIS200",
  "region": "South",
  "channel": "GT",
  "calweek": "2024-W15"
}'
```

---

## 🔐 GPT Configuration (Summary)

- GPT is used **only for explanation**
- No decisions, no predictions, no recommendations
- Low temperature, fixed system prompt
- MCP-controlled input

This prevents hallucinations and ensures governance.

---

## 🛡️ Enterprise Readiness

- Deterministic rules
- Config-driven thresholds
- Explainable ML
- SAP-like schema
- Audit-friendly logic
- Easy extension to SAP IBP / S&OP

---

## 🧭 Roadmap

- Bulk / batch S&OP APIs
- Seasonality & festival signals
- Planner feedback → RAG learning
- Authentication & RBAC
- Docker & CI/CD
- Real SAP data integration

---

## 🏁 Final Note

> **This project demonstrates how GenAI should be used in Supply Chain**  
> — as a governed, explainable decision-support system, not a black box.

