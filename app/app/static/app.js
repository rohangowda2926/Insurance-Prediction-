document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("predict-form");
  const resultDiv = document.getElementById("result");
  const insightDiv = document.getElementById("insight");
  const insightText = document.getElementById("insight-text");
  const chipRow = document.getElementById("chip-row");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const payload = {
      age: Number(formData.get("age")),
      sex: formData.get("sex"),
      bmi: Number(formData.get("bmi")),
      children: Number(formData.get("children")),
      smoker: formData.get("smoker"),
      region: formData.get("region"),
    };

    const button = form.querySelector("button");
    const originalText = button.textContent;

    button.textContent = "Predicting...";
    button.disabled = true;
    resultDiv.style.display = "none";
    insightDiv.textContent = "";
    chipRow.innerHTML = "";

    try {
      const res = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Request failed");

      const data = await res.json();
      const amountNumber = data.predicted_charge;

      const amount = amountNumber.toLocaleString("en-US", {
        style: "currency",
        currency: "USD",
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });

      // Show main result
      resultDiv.style.display = "block";
      resultDiv.className = "result";
      resultDiv.textContent = `Predicted yearly charges: ${amount}`;

      // Derive a simple risk band from the prediction
      let band = "";
      let bandLabel = "";
      let explanation = "";

      if (amountNumber < 8000) {
        band = "low";
        bandLabel = "Low risk";
        explanation =
          "Your predicted charges are on the lower side compared to typical policy holders.";
      } else if (amountNumber < 20000) {
        band = "medium";
        bandLabel = "Moderate risk";
        explanation =
          "Your predicted charges sit in a moderate band. Lifestyle improvements may reduce future costs.";
      } else {
        band = "high";
        bandLabel = "Higher risk";
        explanation =
          "Your predicted charges are relatively high. Risk factors like smoking, high BMI or age strongly influence this.";
      }

      // Update right-hand insight panel
      const chips = [];

      chips.push(`<span class="chip ${band}">${bandLabel}</span>`);
      chips.push(
        `<span class="chip">${payload.smoker === "yes" ? "Smoker" : "Non-smoker"}</span>`
      );
      chips.push(`<span class="chip">BMI: ${payload.bmi}</span>`);
      chips.push(`<span class="chip">Age: ${payload.age}</span>`);

      chipRow.innerHTML = chips.join("");
      insightText.textContent = explanation;
      insightDiv.textContent =
        "These bands are for demonstration only and are not medical or financial advice.";
    } catch (err) {
      console.error(err);
      resultDiv.style.display = "block";
      resultDiv.className = "result error";
      resultDiv.textContent = "Something went wrong while predicting.";
      insightText.textContent =
        "An error occurred. Try again or check your internet connection.";
    } finally {
      button.textContent = originalText;
      button.disabled = false;
    }
  });
});
