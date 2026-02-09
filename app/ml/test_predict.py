from app.ml.predict import (
    predict_base_demand,
    predict_promo_uplift
)

def test_local_prediction():
    print("Running local prediction test...")

    base_qty = predict_base_demand(
        store_id=18,
        product_id=105,
        brand="Pepsi",
        category="Beverages",
        store_type="MT",
        month_num=10,
        cluster=4,
        lag_1=120,
        lag_2=115,
        rolling_mean_3=118,
        rolling_std_3=5
    )

    promo_uplift = predict_promo_uplift(
        store_id=18,
        product_id=105,
        brand="Pepsi",
        category="Beverages",
        store_type="MT",
        month_num=10,
        cluster=4,
        lag_1=120,
        rolling_mean_3=118,
        rolling_std_3=5
    )

    print("Base demand:", base_qty, type(base_qty))
    print("Promo uplift:", promo_uplift, type(promo_uplift))
    print("Total demand:", base_qty + promo_uplift)

if __name__ == "__main__":
    test_local_prediction()
