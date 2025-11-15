document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Encontra o 'container' que o Python preencheu
    const dataContainer = document.getElementById('dashboard-data-container');
    if (!dataContainer) {
        console.error('Container de dados do dashboard não encontrado!');
        return;
    }

    // 2. Lê os dados do atributo 'data-json' e converte de texto para objeto
    const dados = JSON.parse(dataContainer.dataset.json);

    // 3. Lógica do Gráfico de Pizza
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
                plugins: { legend: { position: 'top' } }
            }
        });
    }

    // 4. Lógica do Gráfico de Barras
    const ctxBar = document.getElementById('barChart');
    if (ctxBar) {
        new Chart(ctxBar.getContext('2d'), {
            type: 'bar',
            data: {
                labels: dados.barras.labels, // As datas
                datasets: [{
                    label: 'E-mails Processados',
                    data: dados.barras.data, // As contagens
                    backgroundColor: '#0a2540', // Cor primária
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true, grace: 1 }
                },
                plugins: { legend: { display: false } }
            }
        });
    }
});