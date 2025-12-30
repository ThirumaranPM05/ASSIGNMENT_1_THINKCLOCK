function handleBatteryImage() {
  const input = document.getElementById("batteryImage");
  const img = document.getElementById("batteryImg");

  if (!input.files.length) return;

  img.src = URL.createObjectURL(input.files[0]);

  const cellId = Math.floor(1000000000 + Math.random() * 9000000000);
  document.getElementById("cellId").innerText = cellId;

  JsBarcode("#barcode", cellId.toString(), {
    format: "CODE128",
    width: 2,
    height: 60
  });

  document.getElementById("cellSection").classList.remove("hidden");
}

function uploadCSV() {
  const fileInput = document.getElementById("csvFile");
  if (!fileInput.files.length) {
    alert("Please select a CSV file");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  fetch("http://127.0.0.1:5000/upload_csv", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {

    const plot = typeof data.bode_plot === "string"
      ? JSON.parse(data.bode_plot)
      : data.bode_plot;

    plot.layout.paper_bgcolor = "#f1f5f9";
    plot.layout.plot_bgcolor = "#f1f5f9";

    Plotly.newPlot("bodePlot", plot.data, plot.layout);

    const sohEl = document.getElementById("sohValue");
    sohEl.innerText = data.soh.toFixed(2) + " %";

    if (data.soh > 80) sohEl.style.color = "#16a34a";
    else if (data.soh > 50) sohEl.style.color = "#f59e0b";
    else sohEl.style.color = "#dc2626";

    document.getElementById("rb").innerText = data.params.Rb;
    document.getElementById("rsei").innerText = data.params.R_SEI;
    document.getElementById("cpesei").innerText = data.params.CPE_SEI;
    document.getElementById("rct").innerText = data.params.R_CT;
    document.getElementById("warburg").innerText = data.params.Warburg;
  });
}
