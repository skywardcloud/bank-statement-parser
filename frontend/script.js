document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById("fileInput");
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const response = await fetch("http://localhost:8000/upload", {
    method: "POST",
    body: formData,
  });

  const result = await response.json();

  displayValidation(result.validation_status);
  displayTable(result.data);
});

function displayValidation(status) {
  const el = document.getElementById("validationResult");
  el.textContent = status === "valid" ? "✅ All balances verified." : "❌ Discrepancy found!";
}

function displayTable(data) {
  const container = document.getElementById("tableContainer");
  let html = "<table><tr><th>Date</th><th>Description</th><th>Debit</th><th>Credit</th><th>Balance</th></tr>";
  data.forEach(row => {
    html += `<tr>
      <td>${row.Date}</td>
      <td>${row.Description}</td>
      <td>${row.Debit}</td>
      <td>${row.Credit}</td>
      <td>${row.Balance}</td>
    </tr>`;
  });
  html += "</table>";
  container.innerHTML = html;
}
