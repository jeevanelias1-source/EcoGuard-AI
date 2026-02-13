const API_URL = '/api';

// State
let map;
let riskChart;
let trendChart;

// Default location (New York)
let currentLocation = {
    lat: 40.7128,
    lon: -74.0060,
    name: "New York"
};

// DOM Elements
const views = document.querySelectorAll('.view');
const navLinks = document.querySelectorAll('.nav-links li');
const searchInput = document.getElementById('location-search');
const searchBtn = document.getElementById('search-btn');

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    initCharts();
    loadDashboard(currentLocation.lat, currentLocation.lon);

    // Set Date
    const dateStr = new Date().toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    document.getElementById('current-date').innerHTML = `${dateStr} <span class="live-badge"><i class="fa-solid fa-circle"></i> Live (30s)</span>`;

    // Auto-refresh Interval (30 Seconds)
    setInterval(() => {
        loadDashboard(currentLocation.lat, currentLocation.lon);
    }, 30000);

    // Event Listeners
    setupNavigation();
    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSearch();
    });
});

// --- Navigation ---
function setupNavigation() {
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            const tabId = link.getAttribute('data-tab');

            // Remove active classes
            navLinks.forEach(l => l.classList.remove('active'));
            views.forEach(v => v.classList.remove('active'));

            // Add active class
            link.classList.add('active');
            document.getElementById(tabId).classList.add('active');

            // Resize map if needed
            if (tabId === 'map' && map) {
                setTimeout(() => map.invalidateSize(), 100);
            }
        });
    });
}

// --- Map Logic ---
function initMap() {
    map = L.map('map-container').setView([currentLocation.lat, currentLocation.lon], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19,
    }).addTo(map);

    // Initial Marker
    L.marker([currentLocation.lat, currentLocation.lon])
        .addTo(map)
        .bindPopup(`<b>${currentLocation.name}</b><br>Initial Scan Location`)
        .openPopup();
}

function updateMap(lat, lon, riskData) {
    if (!map) return;
    map.flyTo([lat, lon], 13);

    const riskColor = getRiskColor(riskData.risk_assessment.level);
    L.circle([lat, lon], {
        color: riskColor,
        fillColor: riskColor,
        fillOpacity: 0.5,
        radius: 2000
    }).addTo(map)
        .bindPopup(`
            <b>Risk Level: ${riskData.risk_assessment.level}</b><br>
            Score: ${riskData.risk_assessment.score}/10
        `)
        .openPopup();
}

// --- Charts Logic ---
function initCharts() {
    const ctxRisk = document.getElementById('riskChart').getContext('2d');
    riskChart = new Chart(ctxRisk, {
        type: 'doughnut',
        data: {
            labels: ['Risk', 'Safety Buffer'],
            datasets: [{
                data: [0, 10],
                backgroundColor: ['#10b981', '#161b22'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    const ctxTrend = document.getElementById('trendChart').getContext('2d');
    trendChart = new Chart(ctxTrend, {
        type: 'line',
        data: {
            labels: ['Now', '+1h', '+2h', '+3h', '+4h', '+5h'],
            datasets: [{
                label: 'Projected Risk Trend',
                data: [3, 4, 3, 5, 6, 4],
                borderColor: '#3b82f6',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10
                }
            }
        }
    });
}

// --- Data Fetching ---
async function handleSearch() {
    const query = searchInput.value;
    if (!query) return;

    searchBtn.textContent = 'Searching...';

    try {
        const geoRes = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`);
        const geoData = await geoRes.json();

        if (geoData && geoData.length > 0) {
            const { lat, lon, display_name } = geoData[0];
            currentLocation = {
                lat: parseFloat(lat),
                lon: parseFloat(lon),
                name: display_name.split(',')[0]
            };
            await loadDashboard(currentLocation.lat, currentLocation.lon);
            updateMap(currentLocation.lat, currentLocation.lon, window.lastRiskData);
        } else {
            alert('Location not found!');
        }
    } catch (e) {
        console.error(e);
        alert('Error fetching location.');
    } finally {
        searchBtn.textContent = 'Analyze';
    }
}

async function loadDashboard(lat, lon) {
    try {
        const response = await fetch(`${API_URL}/risk-data?lat=${lat}&lon=${lon}`);
        const data = await response.json();
        window.lastRiskData = data;
        updateUI(data);
        addToAdminLog(data);
    } catch (e) {
        console.error("Backend Error:", e);
    }
}

// --- UI Updates ---
function updateUI(data) {
    const { weather, air_quality, risk_assessment, aggregated_metrics } = data;

    const temp = aggregated_metrics ? (aggregated_metrics.temperature !== undefined ? aggregated_metrics.temperature : aggregated_metrics.temp) : (weather.main?.temp || 0);
    const tempHigh = aggregated_metrics ? (aggregated_metrics.temp_max !== undefined ? aggregated_metrics.temp_max : (weather.main?.temp_max || temp)) : (weather.main?.temp_max || temp);
    const tempLow = aggregated_metrics ? (aggregated_metrics.temp_min !== undefined ? aggregated_metrics.temp_min : (weather.main?.temp_min || temp)) : (weather.main?.temp_min || temp);
    const hum = aggregated_metrics ? (aggregated_metrics.humidity !== undefined ? aggregated_metrics.humidity : (weather.main?.humidity || 0)) : (weather.main?.humidity || 0);
    const pm25 = aggregated_metrics ? (aggregated_metrics.pm25 !== undefined ? aggregated_metrics.pm25 : 0) : 0;

    document.getElementById('temp-val').textContent = `${Math.round(temp)}°C`;
    document.getElementById('temp-high').textContent = Math.round(tempHigh);
    document.getElementById('temp-low').textContent = Math.round(tempLow);
    document.getElementById('humidity-val').textContent = `${Math.round(hum)}%`;

    let aqi = air_quality.aqi || air_quality.main?.aqi || 0;
    document.getElementById('aqi-val').textContent = `AQI: ${aqi}`;
    const pmEl = document.getElementById('pm25-val');
    if (pmEl) pmEl.textContent = Math.round(pm25);

    const riskLevel = risk_assessment.level;
    const riskScore = risk_assessment.score;
    const riskEl = document.getElementById('risk-val');
    riskEl.textContent = riskLevel;
    riskEl.className = getRiskColorClass(riskLevel);

    document.getElementById('risk-desc').textContent = `Driven by: ${risk_assessment.factors.join(', ') || 'Normal Conditions'}`;

    const mlPred = risk_assessment.ml_model_prediction || 'N/A';
    const mlBadge = document.getElementById('ml-pred-val');
    mlBadge.innerHTML = `<i class="fa-solid fa-robot"></i> ML: ${mlPred}`;
    if (mlPred.includes('High')) {
        mlBadge.style.color = '#f85149';
        mlBadge.style.background = 'rgba(248, 81, 73, 0.1)';
    } else {
        mlBadge.style.color = '#58a6ff';
        mlBadge.style.background = 'rgba(88, 166, 255, 0.1)';
    }

    const social = data.social_data || {};
    const socialVal = document.getElementById('social-val');
    const socialSent = document.getElementById('social-sentiment');
    if (socialVal) socialVal.textContent = social.score || '--';
    if (socialSent) {
        const sentiment = social.sentiment_average || 0;
        socialSent.textContent = sentiment > 0 ? `Positive (${sentiment})` : sentiment < 0 ? `Negative (${sentiment})` : `Neutral (${sentiment})`;
        socialSent.className = sentiment > 0 ? 'sub-stat text-success' : sentiment < 0 ? 'sub-stat text-danger' : 'sub-stat';
    }

    const feed = document.getElementById('social-feed');
    if (feed && social.recent_shouts) {
        feed.innerHTML = '';
        social.recent_shouts.forEach(msg => {
            const div = document.createElement('div');
            div.className = 'social-shout';
            div.innerHTML = `
                <p>${msg}</p>
                <span class="shout-sentiment"><i class="fa-solid fa-brain"></i> Sentiment: Analyzed</span>
            `;
            feed.appendChild(div);
        });
    }

    if (social.score >= 7) {
        document.getElementById('risk-desc').textContent += ` + High Social Stress (${social.severity})`;
    }

    riskChart.data.datasets[0].data = [riskScore, 10 - riskScore];
    riskChart.data.datasets[0].backgroundColor = [getRiskColor(riskLevel), '#161b22'];
    riskChart.update();

    const alertList = document.getElementById('alert-list');
    alertList.innerHTML = '';
    if (riskScore >= 6) {
        const li = document.createElement('li');
        li.className = 'alert-item alert-high';
        li.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> <span><b>High Risk Alert:</b> Conditions are unfavorable in ${currentLocation.name}.</span>`;
        alertList.appendChild(li);
    } else {
        alertList.innerHTML = '<li class="alert-item">No active alerts for this region.</li>';
    }
}

// --- Helpers ---
function getRiskColor(level) {
    if (level === 'Critical') return '#ef4444';
    if (level === 'High') return '#f97316';
    if (level === 'Moderate') return '#eab308';
    return '#10b981';
}

function getRiskColorClass(level) {
    if (level === 'Critical') return 'text-danger';
    if (level === 'High') return 'text-danger';
    if (level === 'Moderate') return 'text-warning';
    return 'text-success';
}

function addToAdminLog(data) {
    const tbody = document.getElementById('admin-table-body');
    const tr = document.createElement('tr');
    const id = Math.floor(Math.random() * 10000);
    const time = new Date().toLocaleTimeString();
    tr.innerHTML = `
        <td>#${id}</td>
        <td>${time}</td>
        <td>${currentLocation.name}</td>
        <td>${data.risk_assessment.score}/10</td>
        <td><span class="badge ${getRiskColorClass(data.risk_assessment.level)}">${data.risk_assessment.level}</span></td>
        <td>Completed</td>
    `;
    tbody.prepend(tr);
    if (tbody.children.length > 10) tbody.removeChild(tbody.lastChild);
    const totalEl = document.getElementById('total-preds');
    let currentTotal = parseInt(totalEl.textContent.replace(',', ''));
    totalEl.textContent = (currentTotal + 1).toLocaleString();
                                     }
