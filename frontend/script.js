document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById("fileInput");
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  // Step 1: upload the file
  const uploadRes = await fetch("http://localhost:8000/upload", {
    method: "POST",
    body: formData,
  });
  const uploadResult = await uploadRes.json();

  // Step 2: request parsing and validation
  const parseRes = await fetch("http://localhost:8000/parse", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ filename: uploadResult.filename }),
  });
  const parsed = await parseRes.json();

  displayValidation(parsed.validation.is_valid);
  displayTable(parsed.transactions);
});

function displayValidation(isValid) {
  const el = document.getElementById("validationResult");
  el.textContent = isValid ? "✅ All balances verified." : "❌ Discrepancy found!";
}

function displayTable(data) {
  const container = document.getElementById("tableContainer");
  let html = "<table><tr><th>Date</th><th>Description</th><th>Debit</th><th>Credit</th><th>Balance</th></tr>";
  data.forEach(row => {
    html += `<tr>
      <td>${row.date}</td>
      <td>${row.description}</td>
      <td>${row.debit}</td>
      <td>${row.credit}</td>
      <td>${row.balance}</td>
    </tr>`;
  });
  html += "</table>";
  container.innerHTML = html;
}
