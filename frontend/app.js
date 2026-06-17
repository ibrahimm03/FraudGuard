const CARD_NUMBER = '4111111111111111'
const API = 'http://127.0.0.1:5000'

// Load data when page opens
window.onload = () => {
    loadTransactions()
    loadAlerts()
}

// Fetch and display all transactions
async function loadTransactions() {
    const response = await fetch(`${API}/transactions`)
    const transactions = await response.json()

    const list = document.getElementById('transactions-list')
    document.getElementById('total-transactions').textContent = transactions.length
    document.getElementById('total-flagged').textContent = transactions.filter(t => t.is_fraudulent).length

    if (transactions.length === 0) {
        list.innerHTML = '<p class="empty">No transactions yet</p>'
        return
    }

    list.innerHTML = transactions.map(t => `
        <div class="transaction-item ${t.is_fraudulent ? 'fraudulent' : ''}">
            <div>
                <div class="amount">£${t.amount}</div>
                <div class="details">${t.merchant} — ${t.location}</div>
            </div>
            <span class="badge ${t.is_fraudulent ? 'fraud' : 'safe'}">
                ${t.is_fraudulent ? 'FRAUD' : 'SAFE'}
            </span>
        </div>
    `).join('')
}

// Fetch and display all alerts
async function loadAlerts() {
    const response = await fetch(`${API}/alerts`)
    const alerts = await response.json()

    const list = document.getElementById('alerts-list')
    document.getElementById('total-alerts').textContent = alerts.length

    if (alerts.length === 0) {
        list.innerHTML = '<p class="empty">No alerts yet</p>'
        return
    }

    list.innerHTML = alerts.map(a => `
        <div class="alert-item">
            <div class="reason">${a.reason}</div>
            <div class="severity">Severity: ${a.severity} — Transaction #${a.transaction_id}</div>
        </div>
    `).join('')
}

// Submit a new transaction
async function submitTransaction() {
    const amount = document.getElementById('amount').value
    const merchant = document.getElementById('merchant').value
    const location = document.getElementById('location').value

    if (!amount || !merchant || !location) {
        alert('Please fill in all fields')
        return
    }

    const response = await fetch(`${API}/transactions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            card_number: CARD_NUMBER,
            amount: parseFloat(amount),
            merchant: merchant,
            location: location
        })
    })

    const data = await response.json()

    if (data.alerts && data.alerts.length > 0) {
        alert(`🚨 FRAUD DETECTED\n${data.alerts.map(a => a.reason).join('\n')}`)
    }

    // Refresh the dashboard
    loadTransactions()
    loadAlerts()

    // Clear the form
    document.getElementById('amount').value = ''
    document.getElementById('merchant').value = ''
    document.getElementById('location').value = ''
}