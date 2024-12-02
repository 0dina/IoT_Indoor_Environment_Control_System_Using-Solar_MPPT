// 센서 데이터를 가져오는 함수
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();

        if (!data.error) {
            // 센서 데이터를 HTML에 업데이트
            document.getElementById("temperature").textContent = data.temperature;
            document.getElementById("humidity").textContent = data.humidity;
            document.getElementById("pressure").textContent = data.pressure;
            document.getElementById("wind_speed").textContent = data.wind_speed;
            document.getElementById("wind_direction").textContent = data.wind_direction;
            document.getElementById("rainfall").textContent = data.rainfall;
            document.getElementById("dust").textContent = data.dust;

            // 창문 상태 업데이트
            document.getElementById("window_status").textContent = data.window_state;

            // 차트 업데이트
            updateCharts(data);
        }
    } catch (error) {
        console.error("Error fetching sensor data:", error);
    }
}

// 창문을 열거나 닫는 함수
async function controlWindow(action) {
    try {
        const response = await fetch('/update', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: action })
        });

        const result = await response.json();

        if (result.status === 'success') {
            // 창문 상태 성공적으로 업데이트
            document.getElementById("window_status").textContent = result.message;
        } else {
            alert(result.message);  // 예외 처리, 이미 창문이 열려있거나 닫혀있을 때
        }
    } catch (error) {
        console.error("Error controlling window:", error);
    }
}

// 차트 데이터를 업데이트하는 함수
function updateCharts(sensorData) {
    // 온도 차트
    const timeChart = document.getElementById("timeChart").getContext('2d');
    const timeData = {
        labels: ['1', '2', '3', '4', '5'], // 시간 데이터 (임시 값)
        datasets: [{
            label: 'Temperature (°C)',
            data: [sensorData.temperature, sensorData.temperature + 1, sensorData.temperature - 1, sensorData.temperature, sensorData.temperature + 2], // 센서 값
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false,
        }]
    };
    const timeChartInstance = new Chart(timeChart, {
        type: 'line',
        data: timeData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // 월별 차트 (예시)
    const monthlyChart = document.getElementById("monthlyChart").getContext('2d');
    const monthlyData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        datasets: [{
            label: 'Monthly Temperature',
            data: [sensorData.temperature, sensorData.temperature + 1, sensorData.temperature - 1, sensorData.temperature, sensorData.temperature + 2], // 센서 값
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    };
    const monthlyChartInstance = new Chart(monthlyChart, {
        type: 'bar',
        data: monthlyData,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// 5초마다 데이터 갱신 및 차트 업데이트
setInterval(() => {
    fetchData();
}, 5000);  // 데이터 및 차트를 5초마다 갱신
