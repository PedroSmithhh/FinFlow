// frontend/dashboard.js

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

    // 3. Lógica do Gráfico de Pizza (com porcentagens)
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
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, // Permitir que o CSS controle o tamanho
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    datalabels: { // Plugin para mostrar os dados
                        formatter: (value, ctx) => {
                            if (totalPizza === 0) return '0%'; // Evita divisão por zero
                            let percentage = (value * 100 / totalPizza).toFixed(1) + '%';
                            return percentage;
                        },
                        color: '#fff', // Cor do texto da porcentagem
                        font: {
                            weight: 'bold',
                            size: 14,
                        }
                    }
                }
            }
        });
    }

    // 4. Lógica do Gráfico de Barras
    const ctxBar = document.getElementById('barChart');
    if (ctxBar) {
        new Chart(ctxBar.getContext('2d'), {
            type: 'bar',
            data: {
                labels: dados.barras.labels,
                datasets: [{
                    label: 'E-mails Processados',
                    data: dados.barras.data,
                    backgroundColor: '#0a2540',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, // Permitir que o CSS controle o tamanho
                scales: {
                    y: {
                        beginAtZero: true,
                        grace: 1,
                        ticks: {
                            precision: 0 // Garante que a escala Y mostre números inteiros
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    datalabels: { // Plugin para mostrar os valores nas barras
                        anchor: 'end',
                        align: 'top',
                        formatter: (value) => value > 0 ? value : '', // Só mostra se for > 0
                        color: '#32325d',
                        font: {
                            weight: 'bold'
                        }
                    }
                }
            }
        });
    }
});