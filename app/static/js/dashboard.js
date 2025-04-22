document.addEventListener('DOMContentLoaded', function () {
  const stepsCanvas = document.getElementById('stepsChart');
  const sleepCanvas = document.getElementById('sleepChart');
  const moodCanvas = document.getElementById('moodChart');
  const sleepMoodCanvas = document.getElementById('sleepMoodChart');

  let stepsChart, sleepChart, moodChart, sleepMoodChart;
  let currentTimeframe = 'weekly';

  const dummyData = {
    daily: {
      steps: [7200, 8500, 9100, 7000, 10400, 11500, 9600],
      sleep: [7, 6.5, 8, 7, 6, 8.5, 9],
      mood: [8, 7, 9, 6, 8, 9, 10],
    },
    weekly: {
      steps: [48000, 52000, 55000, 47000],
      sleep: [7.2, 6.9, 7.8, 7.5],
      mood: [8.2, 7.5, 8.7, 7.9],
    },
    monthly: {
      steps: [190000, 205000, 198000],
      sleep: [7.1, 7.4, 7.6],
      mood: [8.3, 8.0, 8.5],
    },
    yearly: {
      steps: [2200000, 2300000],
      sleep: [7.3, 7.5],
      mood: [8.4, 8.5],
    },
  };

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
                ? dummyData[currentTimeframe].steps
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
                ? dummyData[currentTimeframe].sleep
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
        labels: ['Happy 45%', 'Neutral 30%', 'Tired 15%', 'Stressed 10%'],
        datasets: [
          {
            data: [45, 30, 15, 10],
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
                ? dummyData[currentTimeframe].sleep
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
                ? dummyData[currentTimeframe].mood
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
