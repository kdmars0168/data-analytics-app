document.addEventListener('DOMContentLoaded', function () {
  const stepsCanvas = document.getElementById('stepsChart');
  const sleepCanvas = document.getElementById('sleepChart');
  const moodCanvas = document.getElementById('moodChart');
  const sleepMoodCanvas = document.getElementById('sleepMoodChart');

  let stepsChart, sleepChart, moodChart, sleepMoodChart;
  let currentTimeframe = 'weekly';

  // Use real data from backend
  const chartData = window.chartData;

  function getLabels() {
    if (currentTimeframe === 'daily')
      return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    if (currentTimeframe === 'weekly')
      return ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
    if (currentTimeframe === 'monthly')
      return ['Month 1', 'Month 2', 'Month 3'];
    return ['Year 1', 'Year 2'];
  }

  function destroyAllCharts() {
    stepsChart && stepsChart.destroy();
    sleepChart && sleepChart.destroy();
    moodChart && moodChart.destroy();
    sleepMoodChart && sleepMoodChart.destroy();
  }

  function createAllCharts(filter = 'all') {
    const labels = getLabels();

    // Only show steps chart if 'all' or 'steps'
    stepsChart = new Chart(stepsCanvas.getContext('2d'), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Steps',
            data:
              filter === 'all' || filter === 'steps'
                ? chartData[currentTimeframe].mood
                : [],
            backgroundColor: '#5D3FD3',
          },
        ],
      },
      options: { responsive: true, maintainAspectRatio: false },
    });

    sleepChart = new Chart(sleepCanvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Sleep (hours)',
            data:
              filter === 'all' || filter === 'sleep'
                ? chartData[currentTimeframe].steps
                : [],
            backgroundColor: '#5D3FD3',
          },
        ],
      },
      options: { responsive: true, maintainAspectRatio: false },
    });

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

    moodChart = new Chart(moodCanvas.getContext('2d'), {
      type: 'pie',
      data: {
        labels: ['Happy', 'Neutral', 'Tired', 'Stressed'],
        datasets: [
          {
            data:
              filter === 'all' || filter === 'mood'
                ? chartData[currentTimeframe].mood
                : [],
            backgroundColor: ['#5D3FD3', '#20B2AA', '#FF7F50', '#FFBB28'],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom' },
        },
      },
    });

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
            tension: 0.4,
            yAxisID: 'y1',
            fill: false,
          },
          {
            label: 'Mood (score)',
            data:
              filter === 'all' || filter === 'mood'
                ? chartData[currentTimeframe].mood
                : [],
            borderColor: '#FF7F50',
            tension: 0.4,
            yAxisID: 'y2',
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

  // Initialize
  createAllCharts();

  // Event Listeners
  document
    .getElementById('time-filter')
    .addEventListener('change', function (e) {
      currentTimeframe = e.target.value;
      updateDashboard();
    });

  document.querySelectorAll('#data-filters button').forEach((button) => {
    button.addEventListener('click', () => {
      document
        .querySelectorAll('#data-filters button')
        .forEach((b) => b.classList.remove('bg-purple-600', 'text-white'));
      button.classList.add('bg-purple-600', 'text-white');

      const selectedFilter = button.id.replace('filter-', '');
      updateDashboard(selectedFilter);
    });
  });
});
