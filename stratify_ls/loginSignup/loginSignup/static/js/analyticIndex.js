const pemasukanChart = document.getElementById("pemasukan-chart");
const pengeluaranChart = document.getElementById("pengeluaran-chart");
const keuntunganChart = document.getElementById("keuntungan-chart");
const growthChart = document.getElementById("growth-chart");
const pembeliChart = document.getElementById("pembeli-chart");
const pembelian_penjualanChart = document.getElementById("pemasukan_pengeluaran-chart");
const uploadedFile = document.getElementById("uploaded-form");

new Chart(pemasukanChart, {
  type: "line",
  data: {
    labels: ["Januari", "Februari", "Maret", "April", "Mei", "Juni"],
    datasets: [
      {
        label: "Pemasukan",
        data: [1200000, 1500000, 1300000, 1700000, 1600000, 1800000],
        backgroundColor: "#4CAF50",
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
    },
  },
});

new Chart(pengeluaranChart, {
    type: "line",
    data: {
        labels: ["Januari", "Februari", "Maret", "April", "Mei", "Juni"],
        datasets: [
        {
            label: "Pengeluaran",
            data: [800000, 900000, 850000, 950000, 1000000, 1100000],
            backgroundColor: "#F44336",
        },
        ],
    },
    options: {
        responsive: true,
        plugins: {
        legend: {
            display: false,
        },
        },
    },
    });

new Chart(keuntunganChart, {
    type: "bar",
    data: {
        labels: ["Januari", "Februari", "Maret", "April", "Mei", "Juni"],
        datasets: [
        {
            label: "Keuntungan",
            data: [400000, 600000, 450000, 750000, 600000, 700000],
            backgroundColor: "#2196F3",
        },
        ],
    },
    options: {
        responsive: true,
        plugins: {
        legend: {
            display: false,
        },
        },
    },
});

new Chart(growthChart, {
    type: "doughnut",
    data: {
        labels: ["Pemasukan", "Pengeluaran", "Keuntungan"],
        datasets: [
        {
            label: "Growth",
            data: [1200000, 800000, 400000],
            backgroundColor: ["#4CAF50", "#F44336", "#2196F3"],
        },
        ],
    },
    options: {
        responsive: true,
        plugins: {
        legend: {
            display: true,
        },
        },
    },
});

new Chart(pembeliChart, {
    type: "line",
    data: {
        labels: ["Januari", "Februari", "Maret", "April", "Mei", "Juni"],
        datasets: [
        {
            label: "Pembeli",
            data: [50, 60, 55, 70, 65, 80],
            backgroundColor: "#FF9800",
        },
        ],
    },
    options: {
        responsive: true,
        plugins: {
        legend: {
            display: true,
        },
        },
    },
});

new Chart(pembelian_penjualanChart, {
    type: "bar",
    data: {
        labels: ["Januari", "Februari", "Maret", "April", "Mei", "Juni"],
        datasets: [
        {
            label: "Pemasukan",
            data: [1200000, 1500000, 1300000, 1700000, 1600000, 1800000],
            backgroundColor: "#9C27B0",
        },
        {
            label: "Pengeluaran",
            data: [800000, 900000, 850000, 950000, 1000000, 1100000],
            backgroundColor: "#3F51B5",
        },
        ],
    },
    options: {
        responsive: true,
        plugins: {
        legend: {
            display: true,
        },
        },
    },
});