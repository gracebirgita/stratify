const barChart = document.getElementById('barChart').getContext('2d');
console.log(barChart.textContent);

const pieChart = document.getElementById('pieChart').getContext('2d');
console.log(pieChart.textContent);

new Chart(barChart, {
    type: 'bar',
    data: {
        labels:['Week1', 'Week2', 'Week3', 'Week4'],
        datasets:[{
            label: 'Sales This Month',
            data:[80123,120123,70123,91234],
            borderWidth: 1,
            backgroundColor:'#D9D9D9',
            color:'#fffff',
        }],
    },
    options: {
        scales: {
            y: {
                beginAtOne:true,
                ticks:{
                    color:'#D9D9D9',
                },
                grid:{
                    color:'#3e3d3d',
                },
            },
            
            x: {
                ticks:{
                    color:'#D9D9D9',
                },
                grid:{
                    color:'#3e3d3d',
                },
            },
        },
        plugins:{
            legend:{
                labels:{
                    color:'#D9D9D9',
                }
            }
        }
    }

});

new Chart(pieChart,{
    type:'doughnut',
    data: {
        labels:['Week1', 'Week2', 'Week3', 'Week4'],
        datasets:[{
            label: 'Sales This Month',
            data:[300,50,100,50],
            borderWidth: 0,
            backgroundColor: [
                '#D9D9D9',
                '#A9A9A9',
                '#828282',
                '#504C4C',
            ]
        }],
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        cutout:'50%',
        plugins: {
            legend: {
                position: 'left', // or 'bottom', 'left', 'right'
                labels:{
                    padding:15,
                    color:'#D9D9D9',
                    boxwidth:20,
                }
            },
            title: {
                display: true,
                text: 'Sales Distribution',
                color:'#D9D9D9'
            }
        }
    }
});

