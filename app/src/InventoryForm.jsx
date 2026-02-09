import { useState } from "react";

export default function InventoryForm() {
  const [form, setForm] = useState({
    store_id: 18,
    product_id: 105,
    month: "2022-10",
    promo_flag: true,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const submit = async () => {
    setLoading(true);
    const response = await fetch("http://192.168.0.106:8000/agentic/inventory", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const data = await response.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 500, margin: "40px auto" }}>
      <h2>FMCG Inventory Forecast</h2>

      <label>Store ID</label>
      <input name="store_id" value={form.store_id} onChange={handleChange} />

      <label>Product ID</label>
      <input name="product_id" value={form.product_id} onChange={handleChange} />

      <label>Month</label>
      <input name="month" value={form.month} onChange={handleChange} />

      <label>
        <input
          type="checkbox"
          name="promo_flag"
          checked={form.promo_flag}
          onChange={handleChange}
        />
        Promo Active
      </label>

      <button onClick={submit} disabled={loading}>
        {loading ? "Running..." : "Run Forecast"}
      </button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h3>Results</h3>
          <p>Base Demand: {result.base_demand}</p>
          <p>Promo Uplift: {result.promo_uplift}</p>
          <p>Total Demand: {result.total_demand}</p>
          <p>Safety Stock: {result.recommended_safety_stock}</p>
          <p>Service Level: {result.service_level}</p>
        </div>
      )}
    </div>
  );
}
