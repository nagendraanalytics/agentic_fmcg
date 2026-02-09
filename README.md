# 📦 FMCG Demand Intelligence Platform
### Hybrid AI (Rules + ML + RAG + GPT) | SAP-Ready | FastAPI

## 🚀 Overview
This project is an enterprise-grade FMCG Demand Intelligence platform designed to explain demand behavior, quantify supply risk, and support planner decisions across multiple products, channels, and regions.

It uses a hybrid architecture:
- Rules explain WHY demand changed
- ML quantifies HOW RISKY the situation is
- RAG provides organizational memory
- GPT generates governed, business-ready explanations
- Humans remain the final decision makers

## 🎯 Key Objectives
- Explain demand changes (promo, post-promo, stock-out, baseline)
- Support multi-channel FMCG reality (GT, MT, ECOM, INST)
- Respect SKU class behavior (A vs B SKUs)
- Avoid hallucinations and black-box decisions
- SAP-like and audit-friendly
- FastAPI backend for easy integration

## 🧠 Architecture
SAP-like Data
 → Data Cleaning & Signals
 → Decision Graph (Rules – WHY)
 → ML Risk Layer (HOW LIKELY / HOW RISKY)
 → Channel + SKU Class Logic
 → RAG (Historical Memory)
 → GPT (Explanation Only)
 → FastAPI Response

## 📊 Data Model (SAP-Like)
MATNR, CATEGORY, SKU_CLASS, REGION, VTWEG, VKORG, WERKS, CALWEEK, PROMO_FLAG, STOCK_QTY, SALES_QTY

## 🏪 Channels Supported
GT (General Trade), MT (Modern Trade), ECOM (E-Commerce), INST (Institutional / HoReCa)

## 🔌 API
POST /explain-demand

Request:
{
  "matnr": "BIS200",
  "region": "South",
  "channel": "ECOM",
  "calweek": "2024-W12"
}

## ▶️ How to Run
pip install -r requirements.txt
uvicorn app.main:app --reload

Open:
http://127.0.0.1:8000/docs

## 🏁 Final Note
This project demonstrates how GenAI should be used in Supply Chain — as a governed, explainable decision-support system.
