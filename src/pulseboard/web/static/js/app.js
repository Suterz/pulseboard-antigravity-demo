let mainChartInstance = null;

async function fetchAndRenderChart() {
    try {
        const response = await fetch('/api/charts/data');
        const data = await response.json();

        const ctx = document.getElementById('mainChart').getContext('2d');

        if (mainChartInstance) {
            mainChartInstance.destroy();
        }

        mainChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Monthly Activity',
                    data: data.values,
                    backgroundColor: 'rgba(59, 130, 246, 0.5)',
                    borderColor: 'rgb(59, 130, 246)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error fetching chart data:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchAndRenderChart();

    const addBtn = document.getElementById('add-point-btn');
    if (addBtn) {
        addBtn.addEventListener('click', async () => {
            const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
            const randomMonth = months[Math.floor(Math.random() * months.length)];
            const randomValue = Math.floor(Math.random() * 100);

            try {
                await fetch('/api/points', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ label: randomMonth, value: randomValue })
                });

                // Refresh chart
                await fetchAndRenderChart();
            } catch (error) {
                console.error("Error adding point:", error);
            }
        });
    }
});
