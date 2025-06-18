console.log('viewProfile Js loaded..')

document.addEventListener("DOMContentLoaded", function () {
    console.log(chartData);

    if (chartData.length > 0) {
        const chart1 = chartData[0];
        const categories = chart1.labels;
        const values = chart1.values;
        const title = chart1.title;

        const chartElement = document.querySelector(`#chart-1`);
        if (!chartElement) return;

        const options = {
            chart: {
                type: 'bar',
                height: 200,
                toolbar: { show: false }
            },
            series: [{
                name: title,
                data: values
            }],
            xaxis: {
                categories: categories,
                labels: { style: { colors: '#D9D9D9' } }
            },
            yaxis: {
                labels: { style: { colors: '#D9D9D9' } }
            },
            grid: { borderColor: '#3e3d3d' },
            colors: ['#f44336'],
            plotOptions: { bar: { columnWidth: '50%' } }
        };

        const chart = new ApexCharts(chartElement, options);
        chart.render();
    }
});