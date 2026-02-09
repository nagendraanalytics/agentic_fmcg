from app.ml.predict import predict_base_demand, predict_promo_uplift
from app.ml.transformers import to_list_of_strings


base = predict_base_demand(
    store_id=18,
    product_id=105,
    category="Beverages",
    store_type="MT",
    month_num=10,
    cluster=4,
    lag_1=120,
    lag_2=115,
    rolling_mean_3=118,
    rolling_std_3=5,
)

uplift = predict_promo_uplift(
    store_id=18,
    product_id=105,
    category="Beverages",
    store_type="MT",
    month_num=10,
    cluster=4,
    lag_1=120,
    rolling_mean_3=118,
    rolling_std_3=5,
)

print("Base demand:", base, type(base))
print("Promo uplift:", uplift, type(uplift))
print("Total demand:", base + uplift)
