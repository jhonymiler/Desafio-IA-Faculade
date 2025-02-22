function formater(value) {
    const absValue = Math.abs(value);
    let formattedValue = absValue;

    if (absValue >= 1_000_000_000) {
        formattedValue = (absValue / 1_000_000_000).toFixed(0) + 'B'; // Bilhões
    } else if (absValue >= 1_000_000) {
        formattedValue = (absValue / 1_000_000).toFixed(0) + 'M'; // Milhões
    } else if (absValue >= 1_000) {
        formattedValue = (absValue / 1_000).toFixed(0) + 'K'; // Milhares
    }

    return value < 0 ? `-${formattedValue}` : formattedValue; // Mantém o sinal negativo
}


var categoryChart = null
function renderCategoryChart(categoryData) {
    const anos = categoryData.anos;
    const seriesData = Object.entries(categoryData.series).map(([estado, valores]) => ({
        name: estado,
        data: valores
    }));

    const options = {
        chart: { type: 'line', height: 400 },
        series: seriesData,
        xaxis: {
            categories: anos, title: { text: 'Ano' }
        },
        yaxis: {
            labels: {
                formatter: function (value) {
                    return formater(value);
                }
            }
        },
        stroke: { curve: 'smooth' }
    };

    if (!categoryChart) {
        categoryChart = new ApexCharts(document.querySelector("#chartContainer"), options);
        categoryChart.render();
    } else {
        categoryChart.updateOptions({
            series: seriesData,
            xaxis: { categories: anos }
        });
    }
}

function updateChart() {
    const select = document.getElementById('categoriaSelect');
    const selectedCategoryName = select.value; // Pega o nome da categoria
    const selectedCategory = visao_geral.find(cat => cat.categoria == selectedCategoryName); // Filtra pelo nome

    if (selectedCategory) {
        renderCategoryChart(selectedCategory);
        renderStatePieChart(selectedCategory);
    }
}

var statePieChart = null;
function renderStatePieChart(categoryData) {
    // Calcula o total de arrecadação por estado
    const labels = [];
    const data = [];
    Object.entries(categoryData.series).forEach(([estado, valores]) => {
        labels.push(estado);
        data.push(valores.reduce((acc, cur) => acc + cur, 0));
    });

    const options = {
        chart: { type: 'pie', height: 500 },
        series: data,
        labels: labels,
        plotOptions: {
            pie: {
                dataLabels: {
                    dropShadow: {
                        enabled: true,
                    },
                },
            }
        },
        legend: {
            position: 'bottom',
            horizontalAlign: 'center' // Align the legend horizontally
        },
        responsive: [{
            breakpoint: 480,
            options: {
                legend: {
                    show: false,
                    position: 'bottom', // Ensure the legend is at the bottom
                    horizontalAlign: 'center', // Align the legend horizontally
                    offsetX: -10,
                    offsetY: 0
                }
            }
        }],
        tooltip: {
            y: {
                formatter: function (value) {
                    const absValue = Math.abs(value);
                    let formattedValue = absValue;
                    if (absValue >= 1_000_000_000) {
                        formattedValue = (absValue / 1_000_000_000).toFixed(1) + 'B';
                    } else if (absValue >= 1_000_000) {
                        formattedValue = (absValue / 1_000_000).toFixed(1) + 'M';
                    } else if (absValue >= 1_000) {
                        formattedValue = (absValue / 1_000).toFixed(1) + 'K';
                    }
                    return value < 0 ? `-${formattedValue}` : formattedValue;
                }
            }
        }
    };

    if (!statePieChart) {
        statePieChart = new ApexCharts(document.querySelector("#pieChartContainer"), options);
        statePieChart.render();
    } else {
        statePieChart.updateOptions({
            series: data,
            labels: labels
        });
    }
}


function renderCPMFChart() {

    const anos = state_cpmf.anos;
    const seriesData = Object.entries(state_cpmf.series).map(([estado, valores]) => ({
        name: estado,
        data: valores
    }));
    var options = {
        chart: { type: 'line', height: 350 },
        series: seriesData,
        xaxis: { categories: anos, title: { text: 'Ano' } },
        yaxis: {
            labels: {
                formatter: function (value) {
                    return formater(value);
                }
            }
        }
    };
    categoryChart = new ApexCharts(document.querySelector("#cpmfChart"), options).render();
}


// Renderiza o gráfico com a primeira categoria ao carregar a página
document.addEventListener('DOMContentLoaded', function () {
    updateChart();
    renderCPMFChart()


});