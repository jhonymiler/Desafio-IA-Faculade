function formater(value) {
    if (typeof value !== 'number' || isNaN(value)) {
        return '-'; // evita NaN
    }
    const absValue = Math.abs(value);
    let formattedValue = absValue;

    if (absValue >= 1_000_000_000) {
        formattedValue = (absValue / 1_000_000_000).toFixed(0) + 'B';
    } else if (absValue >= 1_000_000) {
        formattedValue = (absValue / 1_000_000).toFixed(0) + 'M';
    } else if (absValue >= 1_000) {
        formattedValue = (absValue / 1_000).toFixed(0) + 'K';
    }

    return value < 0 ? `-${formattedValue}` : formattedValue;
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
                    return formater(value);
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

// 2. Gráfico: Barras Empilhadas - IRPF, IRPJ e CSLL 2023 (Placeholder)
function renderStackedBarChart() {
    var options = {
        chart: { type: 'bar', height: 350, stacked: true },
        series: top5_irpf_irpj_csll.series,
        xaxis: {
            categories: top5_irpf_irpj_csll.categorias // nomes de estados, não formate aqui
        },
        yaxis: {
            labels: {
                formatter: formater // só no eixo Y
            }
        },
        tooltip: {
            y: {
                formatter: formater // e no tooltip
            }
        }
    };
    new ApexCharts(document.querySelector("#stackedBarChart"), options).render();
}

function renderCSLLHorizontalChart() {
    var options = {
        chart: {
            type: 'bar',
            height: 350,
            stacked: true // barras empilhadas
        },
        plotOptions: {
            bar: {
                horizontal: true, // barras na horizontal
                barHeight: '50%'  // ajuste a espessura conforme desejar
            }
        },
        dataLabels: {
            enabled: false
        },
        series: csll_por_estado.series,
        xaxis: {
            // Mesmo sendo "xaxis", as categorias aparecerão no eixo Y,
            // pois 'horizontal' inverte internamente
            categories: csll_por_estado.categorias,
            labels: {
                formatter: formater // formata valores (1K, 10M, etc.)
            }
        },
        tooltip: {
            y: {
                formatter: formater
            }
        }
    };

    new ApexCharts(document.querySelector("#csllHorizontalChart"), options).render();
}






// Renderiza o gráfico com a primeira categoria ao carregar a página
document.addEventListener('DOMContentLoaded', function () {
    updateChart();
    renderCPMFChart()
    renderStackedBarChart()
    renderCSLLHorizontalChart()
});



$(document).ready(function () {

    // 1. Converte as chaves para minúsculo:
    var newData = {};
    Object.keys(heatmapData).forEach((uf) => {
        newData[uf.toLowerCase()] = heatmapData[uf];
    });

    // 2. Inicializa o mapa com stroke-width menor e a escala progressiva:
    $('#world-map').vectorMap({
        map: 'brazil',
        backgroundColor: 'transparent',
        zoomButtons: true,
        regionStyle: {
            initial: {
                fill: '#FFFFFF',       // Base neutra branca
                'fill-opacity': 1,
                stroke: '#000',
                'stroke-width': 1,
                'stroke-opacity': 1
            },
            hover: {
                fill: '#CCCCCC'       // Cor ao passar o mouse
            }
        },
        series: {
            regions: [{
                values: newData,
                // Escala mais dramática: vai de claro até um tom mais escuro de vermelho
                scale: ['#FFFFFF', '#fc0303'],
                // Tente 'linear', 'polynomial' ou 'log' para ver qual distribui melhor
                normalizeFunction: 'polynomial'
            }]
        },
        onRegionTipShow: function (e, el, code) {

            let value = newData[code];
            if (value !== undefined) {
                if (value >= 1_000_000_000_000) {
                    value = (value / 1_000_000_000_000).toFixed(2) + ' Tri';
                } else if (value >= 1_000_000_000) {
                    value = (value / 1_000_000_000).toFixed(2) + ' Bi';
                } else if (value >= 1_000_000) {
                    value = (value / 1_000_000).toFixed(2) + 'Mi';
                } else if (value >= 1_000) {
                    value = (value / 1_000).toFixed(2) + ' Mil';
                }
                el.html(el.html() + ' - R$ ' + value);
            }

        }
    });
});