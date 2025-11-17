document.addEventListener('DOMContentLoaded', function() {
    
    // Registrar o plugin datalabels globalmente
    Chart.register(ChartDataLabels);

    const dataContainer = document.getElementById('dashboard-data-container');
    if (!dataContainer) {
        console.error('Container de dados do dashboard não encontrado!');
        return;
    }

    const dados = JSON.parse(dataContainer.dataset.json);

    // Calcula o total para as porcentagens
    const totalPizza = dados.pizza.produtivo + dados.pizza.improdutivo;

    const isDarkMode = document.body.classList.contains('dark-mode');
    const labelColor = isDarkMode ? '#f0f0f0' : '#32325d'; // Cor do texto
    const gridColor = isDarkMode ? '#3a3a5a' : '#e6ebf1';  // Cor das linhas do grid
    const barColor = isDarkMode ? '#00d4ff' : '#0a2540';

    // Gráfico de Pizza (com porcentagens)
    const ctxPizza = document.getElementById('pizzaChart');
    if (ctxPizza) {
        new Chart(ctxPizza.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Produtivo', 'Improdutivo'],
                datasets: [{
                    label: 'Total',
                    data: [
                        dados.pizza.produtivo, 
                        dados.pizza.improdutivo
                    ],
                    backgroundColor: [
                        '#e0315a', // Cor Produtivo
                        '#7795f8'  // Cor Improdutivo
                    ],
                    borderColor: isDarkMode ? 'var(--card-bg)' : '#fff', // Borda do gráfico
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, // Permitir que o CSS controle o tamanho
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: labelColor // <-- 2. APLICA A COR CORRETA NA LEGENDA
                        }
                    },
                    datalabels: { 
                        formatter: (value, ctx) => {
                            if (totalPizza === 0) return '0%';
                            let percentage = (value * 100 / totalPizza).toFixed(1) + '%';
                            return percentage;
                        },
                        color: '#fff', 
                        font: {
                            weight: 'bold',
                            size: 14,
                        }
                    }
                }
            }
        });
    }

    // Gráfico de Barras
    const ctxBar = document.getElementById('barChart');
    if (ctxBar) {
        new Chart(ctxBar.getContext('2d'), {
            type: 'bar',
            data: {
                labels: dados.barras.labels, // As datas
                datasets: [{
                    label: 'E-mails Processados',
                    data: dados.barras.data, // As contagens
                    backgroundColor: barColor, // <-- USA A VARIÁVEL
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { 
                        beginAtZero: true, 
                        grace: 1,
                        ticks: { color: labelColor }, // Cor da escala Y
                        grid: { color: isDarkMode ? '#3a3a5a' : '#e6ebf1' } // Cor das linhas do grid
                    },
                    x: {
                        ticks: { color: labelColor }, // Cor da escala X
                        grid: { display: false }
                    }
                },
                plugins: { 
                    legend: { display: false },
                    datalabels: { // Plugin para mostrar os valores nas barras
                        anchor: 'end',
                        align: 'top',
                        formatter: (value) => value > 0 ? value : '',
                        color: labelColor, // <-- USA A VARIÁVEL
                        font: {
                            weight: 'bold'
                        }
                    }
                }
            }
        });
    }
});