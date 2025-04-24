let intervalId = null;
console.log("📦 script.js loaded");

function fetchGridData() {
    console.log("🫀 Tick - requesting grid data");
    fetch('/grid_data')
        .then(res => res.json())
        .then(data => {
            renderGrid(data.grid);
            document.getElementById("status").innerText = 
                `✅ Deliveries: ${data.successful_deliveries} | ❌ Failures: ${data.failed_attempts}`;
        })        
        .catch(err => console.error("❌ Error fetching grid:", err));
}


function renderGrid(data) {
    const container = document.getElementById("simulation-container");
    container.innerHTML = ""; // Clear previous cells
    const cellSize = 20;

    if (!data || !data.cells || data.cells.length === 0) {
        console.warn("⚠ No data received or empty grid");
        return;
    }

    console.log("🧩 Rendering", data.cells.length, "agents");

    data.cells.forEach(cell => {
        const div = document.createElement("div");
        div.className = "grid-cell";
        div.style.left = `${cell.x * cellSize}px`;
        div.style.top = `${cell.y * cellSize}px`;

        if (cell.status === "DonorAgent") {
            div.style.backgroundColor = "blue";
            div.innerText = "D";
        } else if (cell.status === "RecipientAgent") {
            div.style.backgroundColor = "green";
            div.innerText = "R";
        } else if (cell.status === "TransportAgent") {
            div.style.backgroundColor = "red";
            div.innerText = "T";
        }

        container.appendChild(div);
    });
}

function startSimulation() {
    console.log("▶️ Start button clicked");
    if (!intervalId) {
        intervalId = setInterval(fetchGridData, 1000);
        fetchGridData();
    }
}

function pauseSimulation() {
    console.log("⏸ Pause button clicked");
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
}


function resetSimulation() {
    
    fetch("/reset")
        .then(() => {
            fetchGridData(); // Render immediately
        });
}

window.onload = () => {
    fetchGridData(); // Load once on page load, but not auto-starting
};
