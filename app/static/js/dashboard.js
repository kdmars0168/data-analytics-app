document.addEventListener('DOMContentLoaded', function () {
  const stepsCanvas = document.getElementById('stepsChart');
  const sleepCanvas = document.getElementById('sleepChart');
  const moodCanvas = document.getElementById('moodChart');
  const sleepMoodCanvas = document.getElementById('sleepMoodChart');

  let stepsChart, sleepChart, moodChart, sleepMoodChart;
  let currentTimeframe = 'weekly';

  const chartData = window.chartData;
  const moodData = window.moodData;

  const moodColorMap = {
    Happy: '#5D3FD3',
    Stressed: '#FFBB28',
    Sad: '#FF7F50',
    Tired: '#20B2AA'
  };

  function destroyAllCharts() {
    if (stepsChart) stepsChart.destroy();
    if (sleepChart) sleepChart.destroy();
    if (moodChart) moodChart.destroy();
    if (sleepMoodChart) sleepMoodChart.destroy();
  }

  function createAllCharts(filter = 'all') {
    const labels = chartData[currentTimeframe].labels;

    // Steps Chart
    stepsChart = new Chart(stepsCanvas.getContext('2d'), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Steps',
            data:
              filter === 'all' || filter === 'steps'
                ? chartData[currentTimeframe].steps
                : [],
            backgroundColor: '#5D3FD3',
          },
        ],
      },
      options: { responsive: true, maintainAspectRatio: false },
    });

    // Sleep Chart
    sleepChart = new Chart(sleepCanvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Sleep (hours)',
            data:
              filter === 'all' || filter === 'sleep'
                ? chartData[currentTimeframe].sleep
                : [],
            borderColor: '#20B2AA',
            tension: 0.4,
            fill: false,
          },
        ],
      },
      options: { responsive: true, maintainAspectRatio: false },
    });

    // Mood Pie Chart with consistent order
    const fixedOrder = ['Happy', 'Stressed', 'Sad', 'Tired'];
    const moodBreakdown = moodData[currentTimeframe] || {};

    const moodLabels = [];
    const moodPercentages = [];
    const moodColors = [];

    fixedOrder.forEach(label => {
      if (moodBreakdown[label] !== undefined) {
        moodLabels.push(label);
        moodPercentages.push(moodBreakdown[label]);
        moodColors.push(moodColorMap[label]);
      }
    });

    moodChart = new Chart(moodCanvas.getContext('2d'), {
      type: 'pie',
      data: {
        labels: moodLabels,
        datasets: [
          {
            data: moodPercentages,
            backgroundColor: moodColors,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom' },
          tooltip: {
            callbacks: {
              label: function (ctx) {
                return `${ctx.label}: ${ctx.parsed}%`;
              },
            },
          },
        },
      },
    });

    // Sleep vs Mood Correlation
    sleepMoodChart = new Chart(sleepMoodCanvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Sleep (hours)',
            data:
              filter === 'all' || filter === 'sleep'
                ? chartData[currentTimeframe].sleep
                : [],
            borderColor: '#20B2AA',
            yAxisID: 'y1',
            tension: 0.4,
            fill: false,
          },
          {
            label: 'Mood (score)',
            data:
              filter === 'all' || filter === 'mood'
                ? chartData[currentTimeframe].mood
                : [],
            borderColor: '#FF7F50',
            yAxisID: 'y2',
            tension: 0.4,
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y1: { type: 'linear', position: 'left' },
          y2: { type: 'linear', position: 'right' },
        },
      },
    });
  }

  function updateDashboard(filter = 'all') {
    destroyAllCharts();
    createAllCharts(filter);
  }

  // Initial Load
  createAllCharts();

  // Timeframe Filter
  document.getElementById('time-filter').addEventListener('change', function (e) {
    currentTimeframe = e.target.value;
    updateDashboard();
  });

  // Data Filter
  document.querySelectorAll('#data-filters button').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelectorAll('#data-filters button')
        .forEach((b) => b.classList.remove('bg-purple-600', 'text-white'));
      button.classList.add('bg-purple-600', 'text-white');

      const selectedFilter = button.id.replace('filter-', '');
      updateDashboard(selectedFilter);
    });
  });
});
