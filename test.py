from app.langgraph.graph import graph_app

result = graph_app.invoke({
  "store_id": 18,
  "product_id": 105,
  "brand": "Pepsi",
  "category": "Beverages",
  "store_type": "Supermarket",
  "month": "2022-10",
  "cluster": 4,
  "promo_flag": True
})

print(result)
