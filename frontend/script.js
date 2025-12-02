const API_URL = "http://127.0.0.1:8000";
let chart;

document.getElementById("add-btn").addEventListener("click", addExpense);

window.onload = () => {
    loadExpenses();
    loadSummary();
};

/* ---------- Add Expense ---------- */
async function addExpense() {
    const title = document.getElementById("title").value;
    const amount = parseFloat(document.getElementById("amount").value);
    const category = document.getElementById("category").value;

    if (!title || isNaN(amount) || !category) {
        alert("Please enter title, amount, and category.");
        return;
    }

    await fetch(`${API_URL}/expenses`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, amount, category })
    });

    // clear inputs
    document.getElementById("title").value = "";
    document.getElementById("amount").value = "";
    document.getElementById("category").value = "";

    await loadExpenses();
    await loadSummary();
}

/* ---------- Load Expenses ---------- */
async function loadExpenses() {
    const res = await fetch(`${API_URL}/expenses`);
    const data = await res.json();

    const list = document.getElementById("expenses-list");
    list.innerHTML = "";

    data.forEach(exp => {
        const li = document.createElement("li");
        li.innerHTML = `
            ${exp.title} - $${exp.amount} (${exp.category})
            <span class="delete-icon" onclick="deleteExpense(${exp.id})">❌</span>
        `;
        list.appendChild(li);
    });

    updatePieChart(data);
}

/* ---------- Delete Expense ---------- */
async function deleteExpense(id) {
    await fetch(`${API_URL}/expenses/${id}`, { method: "DELETE" });
    await loadExpenses();
    await loadSummary();
}

/* ---------- Load Summary ---------- */
async function loadSummary() {
    const res = await fetch(`${API_URL}/expenses/summary`);
    const data = await res.json();

    document.getElementById("total-count").innerText = data.total_count;
    document.getElementById("total-amount").innerText = data.total_amount;
}

/* ---------- Pie Chart ---------- */
function updatePieChart(expenses) {
    const totals = {};

    expenses.forEach(e => {
        totals[e.category] = (totals[e.category] || 0) + e.amount;
    });

    const labels = Object.keys(totals);
    const values = Object.values(totals);

    if (chart) chart.destroy();

    const ctx = document.getElementById("expense-chart").getContext("2d");

    chart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    "#ff9999",
                    "#66b3ff",
                    "#99ff99",
                    "#ffcc99",
                    "#c2c2f0",
                    "#ffb3e6"
                ]
            }]
        },
        options: {
            // IMPORTANT: fixed 300×300 size from HTML, no auto full-screen
            responsive: false,
            maintainAspectRatio: true
        }
    });
}
