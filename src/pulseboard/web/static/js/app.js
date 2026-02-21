document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/charts/data');
        const data = await response.json();
        
        const ctx = document.getElementById('mainChart').getContext('2d');
        new Chart(ctx, {
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
});
