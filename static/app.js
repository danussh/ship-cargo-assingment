const API_BASE_URL = '/api/v1';

// Color palette for different cargos
const CARGO_COLORS = [
    '#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
    '#ec4899', '#06b6d4', '#84cc16', '#f97316', '#6366f1'
];

// Add cargo row
document.getElementById('addCargoBtn').addEventListener('click', () => {
    const container = document.getElementById('cargoInputs');
    const row = document.createElement('div');
    row.className = 'input-row';
    row.innerHTML = `
        <input type="text" placeholder="ID (e.g., C${container.children.length + 1})" class="cargo-id">
        <input type="number" placeholder="Volume" class="cargo-volume" min="0" step="0.01">
        <button class="btn-remove" onclick="removeRow(this)">×</button>
    `;
    container.appendChild(row);
});

// Add tank row
document.getElementById('addTankBtn').addEventListener('click', () => {
    const container = document.getElementById('tankInputs');
    const row = document.createElement('div');
    row.className = 'input-row';
    row.innerHTML = `
        <input type="text" placeholder="ID (e.g., T${container.children.length + 1})" class="tank-id">
        <input type="number" placeholder="Capacity" class="tank-capacity" min="0" step="0.01">
        <button class="btn-remove" onclick="removeRow(this)">×</button>
    `;
    container.appendChild(row);
});

// Remove row
function removeRow(button) {
    button.parentElement.remove();
}

// Load sample data
document.getElementById('loadSampleBtn').addEventListener('click', () => {
    const sampleCargos = [
        { id: 'C1', volume: 1234 },
        { id: 'C2', volume: 4352 },
        { id: 'C3', volume: 3321 },
        { id: 'C4', volume: 2456 },
        { id: 'C5', volume: 5123 },
        { id: 'C6', volume: 1879 },
        { id: 'C7', volume: 4987 },
        { id: 'C8', volume: 2050 },
        { id: 'C9', volume: 3678 },
        { id: 'C10', volume: 5432 }
    ];

    const sampleTanks = [
        { id: 'T1', capacity: 5000 },
        { id: 'T2', capacity: 3000 },
        { id: 'T3', capacity: 4500 },
        { id: 'T4', capacity: 6000 },
        { id: 'T5', capacity: 2500 },
        { id: 'T6', capacity: 3500 },
        { id: 'T7', capacity: 4000 },
        { id: 'T8', capacity: 5500 },
        { id: 'T9', capacity: 3200 },
        { id: 'T10', capacity: 2800 }
    ];

    loadData(sampleCargos, sampleTanks);
});

// Clear all
document.getElementById('clearBtn').addEventListener('click', () => {
    document.getElementById('cargoInputs').innerHTML = `
        <div class="input-row">
            <input type="text" placeholder="ID (e.g., C1)" class="cargo-id">
            <input type="number" placeholder="Volume" class="cargo-volume" min="0" step="0.01">
            <button class="btn-remove" onclick="removeRow(this)">×</button>
        </div>
    `;
    document.getElementById('tankInputs').innerHTML = `
        <div class="input-row">
            <input type="text" placeholder="ID (e.g., T1)" class="tank-id">
            <input type="number" placeholder="Capacity" class="tank-capacity" min="0" step="0.01">
            <button class="btn-remove" onclick="removeRow(this)">×</button>
        </div>
    `;
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
});

// Load data into inputs
function loadData(cargos, tanks) {
    const cargoContainer = document.getElementById('cargoInputs');
    cargoContainer.innerHTML = '';
    cargos.forEach(cargo => {
        const row = document.createElement('div');
        row.className = 'input-row';
        row.innerHTML = `
            <input type="text" placeholder="ID" class="cargo-id" value="${cargo.id}">
            <input type="number" placeholder="Volume" class="cargo-volume" value="${cargo.volume}" min="0" step="0.01">
            <button class="btn-remove" onclick="removeRow(this)">×</button>
        `;
        cargoContainer.appendChild(row);
    });

    const tankContainer = document.getElementById('tankInputs');
    tankContainer.innerHTML = '';
    tanks.forEach(tank => {
        const row = document.createElement('div');
        row.className = 'input-row';
        row.innerHTML = `
            <input type="text" placeholder="ID" class="tank-id" value="${tank.id}">
            <input type="number" placeholder="Capacity" class="tank-capacity" value="${tank.capacity}" min="0" step="0.01">
            <button class="btn-remove" onclick="removeRow(this)">×</button>
        `;
        tankContainer.appendChild(row);
    });
}

// Collect input data
function collectInputData() {
    const cargos = [];
    const cargoRows = document.querySelectorAll('#cargoInputs .input-row');
    cargoRows.forEach(row => {
        const id = row.querySelector('.cargo-id').value.trim();
        const volume = parseFloat(row.querySelector('.cargo-volume').value);
        if (id && volume > 0) {
            cargos.push({ id, volume });
        }
    });

    const tanks = [];
    const tankRows = document.querySelectorAll('#tankInputs .input-row');
    tankRows.forEach(row => {
        const id = row.querySelector('.tank-id').value.trim();
        const capacity = parseFloat(row.querySelector('.tank-capacity').value);
        if (id && capacity > 0) {
            tanks.push({ id, capacity });
        }
    });

    return { cargos, tanks };
}

// Optimize button
document.getElementById('optimizeBtn').addEventListener('click', async () => {
    const inputData = collectInputData();

    if (inputData.cargos.length === 0 || inputData.tanks.length === 0) {
        showError('Please add at least one cargo and one tank.');
        return;
    }

    showLoading(true);
    hideError();

    try {
        const response = await fetch(`${API_BASE_URL}/optimize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(inputData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Optimization failed');
        }

        const result = await response.json();
        displayResults(result);
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
});

// Display results
function displayResults(result) {
    const { metrics, allocations, tank_details, unallocated_cargo } = result;

    // Update metrics
    document.getElementById('totalCargoVolume').textContent = metrics.total_cargo_volume.toLocaleString();
    document.getElementById('totalTankCapacity').textContent = metrics.total_tank_capacity.toLocaleString();
    document.getElementById('totalLoaded').textContent = metrics.total_loaded_volume.toLocaleString();
    document.getElementById('tankUtilization').textContent = `${metrics.tank_utilization_percentage}%`;
    document.getElementById('cargoLoaded').textContent = `${metrics.cargo_loaded_percentage}%`;
    document.getElementById('tanksUsed').textContent = `${metrics.tanks_used}/${metrics.tanks_total}`;

    // Visualize tanks
    visualizeTanks(tank_details);

    // Display allocations table
    displayAllocationsTable(allocations, tank_details);

    // Display unallocated cargo
    if (unallocated_cargo.length > 0) {
        displayUnallocatedCargo(unallocated_cargo);
    } else {
        document.getElementById('unallocatedSection').style.display = 'none';
    }

    // Show results section
    document.getElementById('resultsSection').style.display = 'block';
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

// Visualize tanks
function visualizeTanks(tankDetails) {
    const container = document.getElementById('tankVisualization');
    container.innerHTML = '';

    // Create cargo color map
    const cargoColorMap = {};
    let colorIndex = 0;

    tankDetails.forEach(tank => {
        const tankDiv = document.createElement('div');
        tankDiv.className = 'tank-visual';

        const utilizationPercent = tank.utilization_percentage;
        const cargoId = tank.cargo_id || 'Empty';

        // Assign color to cargo
        if (cargoId !== 'Empty' && !cargoColorMap[cargoId]) {
            cargoColorMap[cargoId] = CARGO_COLORS[colorIndex % CARGO_COLORS.length];
            colorIndex++;
        }

        const fillColor = cargoId !== 'Empty' ? cargoColorMap[cargoId] : '#cbd5e1';

        tankDiv.innerHTML = `
            <div class="tank-header">${tank.tank_id}</div>
            <div class="tank-bar-container">
                <div class="tank-bar-fill" style="height: ${utilizationPercent}%; background: ${fillColor};">
                    ${utilizationPercent > 15 ? utilizationPercent.toFixed(1) + '%' : ''}
                </div>
            </div>
            <div class="tank-info">
                <div><strong>${cargoId}</strong></div>
                <div>${tank.allocated_volume.toLocaleString()} / ${tank.capacity.toLocaleString()}</div>
            </div>
        `;

        container.appendChild(tankDiv);
    });
}

// Display allocations table
function displayAllocationsTable(allocations, tankDetails) {
    const tbody = document.getElementById('allocationsBody');
    tbody.innerHTML = '';

    // Group allocations by tank
    const tankMap = {};
    tankDetails.forEach(tank => {
        tankMap[tank.tank_id] = tank;
    });

    allocations.forEach(alloc => {
        const tank = tankMap[alloc.tank_id];
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${alloc.tank_id}</strong></td>
            <td>${alloc.cargo_id}</td>
            <td>${alloc.volume_allocated.toLocaleString()}</td>
            <td>${tank.capacity.toLocaleString()}</td>
            <td>${tank.utilization_percentage.toFixed(2)}%</td>
        `;
        tbody.appendChild(row);
    });
}

// Display unallocated cargo
function displayUnallocatedCargo(unallocatedCargo) {
    const container = document.getElementById('unallocatedList');
    container.innerHTML = '';

    unallocatedCargo.forEach(cargo => {
        const div = document.createElement('div');
        div.className = 'unallocated-item';
        div.innerHTML = `
            <strong>${cargo.cargo_id}</strong>: 
            ${cargo.unallocated_volume.toLocaleString()} of ${cargo.original_volume.toLocaleString()} units unallocated
            (${((cargo.unallocated_volume / cargo.original_volume) * 100).toFixed(1)}%)
        `;
        container.appendChild(div);
    });

    document.getElementById('unallocatedSection').style.display = 'block';
}

// Show/hide loading
function showLoading(show) {
    document.getElementById('loadingSpinner').style.display = show ? 'block' : 'none';
}

// Show error
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = `❌ Error: ${message}`;
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth' });
}

// Hide error
function hideError() {
    document.getElementById('errorMessage').style.display = 'none';
}
