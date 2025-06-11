document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("sentForm");
  const backBtn = document.getElementById("backBtn");
  const articlesBtn = document.getElementById("articlesBtn");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    await analyze();
  });

  backBtn.addEventListener("click", () => {
    document.getElementById("input").classList.remove("hidden");
    document.getElementById("output").classList.add("hidden");
    document.getElementById("scoreBarContainer").classList.add("hidden");
    document.getElementById("bottomButtons").classList.add("hidden");
    document.getElementById("articlesSection").classList.add("hidden");
    document.getElementById("priceChart").classList.add("hidden");
    document.getElementById("ticker").value = "";

    if (window.priceChartInstance) {
      window.priceChartInstance.destroy();
      window.priceChartInstance = null;
    }
  });

  articlesBtn.addEventListener("click", () => {
    const section = document.getElementById("articlesSection");
    section.classList.toggle("hidden");
    articlesBtn.textContent = section.classList.contains("hidden") ? "Show Articles" : "Hide Articles";
  });

  const range = document.getElementById("articleCount");
  const label = document.getElementById("articleVal");
  range.addEventListener("input", () => {
    label.textContent = range.value;
  });
});

async function analyze() {
  const ticker = document.getElementById("ticker").value.trim();
  const articleCount = document.getElementById("articleCount").value;

  const spinner = document.getElementById("spinner");
  const output = document.getElementById("output");
  const scoreBarContainer = document.getElementById("scoreBarContainer");
  const outputTicker = document.getElementById("outputTicker");
  const outputName = document.getElementById("outputName");
  const outputBadge = document.getElementById("outputBadge");
  const marker = document.getElementById("marker");

  output.classList.add("hidden");
  scoreBarContainer.classList.add("hidden");
  spinner.classList.remove("hidden");

  // disable inputs 
  document.getElementById("ticker").disabled = true;
  document.getElementById("articleCount").disabled = true;
  document.querySelector("#sentForm button[type='submit']").disabled = true;

  try {
    const query = new URLSearchParams({
      ticker,
      article_count: articleCount
    }).toString();

    const res = await fetch(`/analyze?${query}`);
    const data = await res.json();

    spinner.classList.add("hidden");

    document.getElementById("ticker").disabled = false;
    document.getElementById("articleCount").disabled = false;
    document.querySelector("#sentForm button[type='submit']").disabled = false;

    if (data.error) {
      output.classList.remove("hidden");
      outputTicker.textContent = "Error";
      outputName.textContent = data.error;
      outputBadge.textContent = "";
      outputBadge.className = "";
      return;
    }

    const sentiment = data.recommendation.toLowerCase();
    let badgeColor = "bg-gray-400";
    if (sentiment === "buy") badgeColor = "bg-green-500";
    else if (sentiment === "hold") badgeColor = "bg-yellow-400";
    else if (sentiment === "sell") badgeColor = "bg-red-500";

    outputTicker.textContent = data.ticker;
    outputName.textContent = data.company_name;
    outputBadge.textContent = data.recommendation.toUpperCase();
    outputBadge.className = `text-white text-2xl font-bold px-5 py-2 rounded-md ${badgeColor}`;

    document.getElementById("input").classList.add("hidden");
    output.classList.remove("hidden");
    scoreBarContainer.classList.remove("hidden");
    document.getElementById("backBtn").classList.remove("hidden");

    const score = parseFloat(data.sentiment_score);
    const percentage = Math.max(0, Math.min(100, (score / 10) * 100));
    marker.style.left = '0%';
    void marker.offsetWidth;
    marker.style.left = `calc(${percentage}% - 0.5rem)`;

    const tooltip = document.getElementById("markerTooltip");
    tooltip.textContent = `${score.toFixed(1)}`;

    await renderChart(ticker, data.ticker);
    await renderArticles(ticker);

    document.getElementById("bottomButtons").classList.remove("hidden");

  } catch (err) {
    spinner.classList.add("hidden");
    document.getElementById("ticker").disabled = false;
    document.getElementById("articleCount").disabled = false;
    document.querySelector("#sentForm button[type='submit']").disabled = false;
    output.classList.remove("hidden");
    outputTicker.textContent = "Error";
    outputName.textContent = err.message;
    outputBadge.textContent = "";
    outputBadge.className = "";
  }
}

async function renderChart(ticker, displayTicker) {
  const chartCanvas = document.getElementById("priceChart");
  chartCanvas.classList.remove("hidden");

  const res = await fetch(`/price-history?ticker=${ticker}`);
  const data = await res.json();

  if (data.error) throw new Error(data.error);

  const labels = data.labels;
  const prices = data.prices;

  if (window.priceChartInstance) {
    window.priceChartInstance.destroy();
  }

  window.priceChartInstance = new Chart(chartCanvas, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: `${displayTicker} Price`,
        data: prices,
        borderColor: "#2563eb",
        borderWidth: 2,
        tension: 0.3,
        pointRadius: 1.5,
        pointHoverRadius: 2.5,
        pointBackgroundColor: "#2563eb",
        fill: false,
      }]
    },
    options: {
      animation: {
        delay: 100,
        duration: 1000,
        easing: 'easeOut',
      },
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: `Price Movement - Past 12 Months`,
          font: { size: 14, weight: 'bold' },
          padding: { top: 10, bottom: 10 }
        }
      },
      scales: {
        x: {
          title: { display: true, text: "Date", font: { weight: 'bold' } },
          ticks: { autoSkip: false, maxRotation: 45, minRotation: 45 }
        },
        y: {
          title: { display: true, text: "Price ($)", font: { weight: 'bold' } },
          ticks: { autoSkip: true, maxRotation: 45, minRotation: 45 },
          beginAtZero: false
        }
      }
    }
  });
}

async function renderArticles(ticker) {
  const res = await fetch(`/articles?ticker=${ticker}`);
  const data = await res.json();

  const articlesList = document.getElementById("articlesList");
  articlesList.innerHTML = "";

  data.forEach(article => {
    const articleDiv = document.createElement("div");
    articleDiv.className = "border rounded-lg p-4 hover:bg-gray-50 transition";
    articleDiv.innerHTML = `
      <a href="${article.url}" target="_blank" class="text-blue-600 font-semibold text-lg hover:underline">
        ${article.title}
      </a>
      <p class="text-gray-700 text-sm mt-1">${article.summary}</p>
    `;
    articlesList.appendChild(articleDiv);
  });
}
