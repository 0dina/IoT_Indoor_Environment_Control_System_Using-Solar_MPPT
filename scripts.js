async function fetchData() {
    const response = await fetch('/data');
    const data = await response.json();

    if (!data.error) {
        document.getElementById("temperature").textContent = data.temperature;
        document.getElementById("humidity").textContent = data.humidity;
        document.getElementById("pressure").textContent = data.pressure;
        document.getElementById("wind_speed").textContent = data.wind_speed;
        document.getElementById("wind_direction").textContent = data.wind_direction;
        document.getElementById("rainfall").textContent = data.rainfall;
        document.getElementById("dust").textContent = data.dust;
    }
}

async function controlWindow(action) {
    const response = await fetch('/window', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: action })
    });

    const result = await response.json();
    document.getElementById("window_status").textContent = result.status;
}

// 차트 데이터 및 테이블 업데이트
function updateCharts() {
    // Fetch and update chart data here (use Chart.js for dynamic charts)
}

setInterval(() => {
    fetchData();
    updateCharts();
}, 5000);  // Fetch new data every 5 seconds
