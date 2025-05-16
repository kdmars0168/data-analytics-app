<<<<<<< HEAD
document.addEventListener('DOMContentLoaded', () => {
  const userCards = document.querySelectorAll('.user-card');
  const datasetGrid = document.getElementById('dataset-grid');
  const chartSection = document.getElementById('chart-section');
  const placeholder = document.getElementById('placeholder');
  const toast = document.getElementById('toast');
  const backBtn = document.getElementById('backBtn');
  const chartTitle = document.getElementById('chart-title');
  const filterDropdown = document.getElementById('filter-dropdown');
  const searchInput = document.getElementById('search-box');
  const datasetHeaderBlock = document.getElementById('dataset-header-block');

  let chartInstance = null;
  let selectedUser = null;

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 3000);
  }

  function filterUsers() {
    const searchTerm = searchInput.value.toLowerCase();
    const filterValue = filterDropdown.value;

    userCards.forEach((card) => {
      const name = card.dataset.name.toLowerCase();
      const email = card.dataset.email.toLowerCase();
      const tags = card.dataset.tags.toLowerCase();

      const matchesSearch =
        name.includes(searchTerm) || email.includes(searchTerm);
      const matchesFilter = filterValue === 'all' || tags.includes(filterValue);

      if (matchesSearch && matchesFilter) {
        card.classList.remove('hidden');
      } else {
        card.classList.add('hidden');
      }
    });
  }

  filterDropdown.addEventListener('change', filterUsers);
  searchInput.addEventListener('input', filterUsers);

  userCards.forEach((card) => {
    card.addEventListener('click', () => {
      // Highlight selected card
      userCards.forEach((c) =>
        c.classList.remove('bg-purple-100', 'border-purple-400')
      );
      card.classList.add('bg-purple-100', 'border-purple-400');

      selectedUser = card.dataset.name;

      placeholder.classList.add('hidden');
      datasetGrid.classList.remove('hidden');
      chartSection.classList.add('hidden');

      showToast(`Viewing shared datasets from ${selectedUser}`);
      datasetHeaderBlock.classList.remove('hidden');
      document.getElementById(
        'dataset-header'
      ).textContent = `Shared Datasets from ${selectedUser}`;
    });
  });

  document.querySelectorAll('.dataset-card').forEach((card) => {
    card.addEventListener('click', () => {
      datasetGrid.classList.add('hidden');
      chartSection.classList.remove('hidden');

      const chartType = card.dataset.chart.toLowerCase();
      const title = card.dataset.title;
      chartTitle.textContent = title;

      const ctx = document.getElementById('sharedChart').getContext('2d');
      if (chartInstance) chartInstance.destroy();

      chartInstance = new Chart(ctx, {
        type: chartType.includes('bar')
          ? 'bar'
          : chartType.includes('line')
          ? 'line'
          : 'pie',
        data: {
          labels:
            chartType === 'pie'
              ? ['Happy', 'Tired', 'Stressed', 'Sad']
              : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          datasets: [
            {
              label: title,
              data:
                chartType === 'pie'
                  ? [35, 25, 20, 20]
                  : [7000, 8500, 9200, 7800, 10800, 9000, 8700],
              backgroundColor: [
                '#8b5cf6',
                '#f97316',
                '#60a5fa',
                '#facc15',
                '#10b981',
                '#ef4444',
                '#c084fc',
              ],
              borderColor: '#e5e7eb',
              borderWidth: 1,
              tension: 0.4,
              fill: false,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: chartType === 'pie' ? 'bottom' : 'top',
            },
          },
        },
      });

      showToast(`Dataset loaded: ${title}`);
    });
  });

  backBtn.addEventListener('click', () => {
    chartSection.classList.add('hidden');
    datasetGrid.classList.remove('hidden');
  });
});
=======
function extractXY(data, yKey) {
  return {
    labels: data.map(d => d.date),
    values: data.map(d => d[yKey])
  };
}


if (stepsData.length) {
  const ctxSteps = document.getElementById('stepsChart').getContext('2d');
  const stepsXY = extractXY(stepsData, 'steps');
  new Chart(ctxSteps, {
    type: 'bar',
    data: {
      labels: stepsXY.labels,
      datasets: [{
        label: 'Steps',
        data: stepsXY.values,
        backgroundColor: 'rgba(54, 162, 235, 0.7)'
      }]
    },
    options: {
      scales: {
        x: { title: { display: true, text: 'Date' } },
        y: { title: { display: true, text: 'Steps' }, beginAtZero: true }
      }
    }
  });
}


if (sleepData.length) {
  const ctxSleep = document.getElementById('sleepChart').getContext('2d');
  const sleepXY = extractXY(sleepData, 'sleep_hours');
  new Chart(ctxSleep, {
    type: 'line',
    data: {
      labels: sleepXY.labels,
      datasets: [{
        label: 'Sleep Hours',
        data: sleepXY.values,
        fill: false,
        borderColor: 'rgba(255, 99, 132, 0.7)',
        tension: 0.1
      }]
    },
    options: {
      scales: {
        x: { title: { display: true, text: 'Date' } },
        y: { title: { display: true, text: 'Hours' }, beginAtZero: true }
      }
    }
  });
}
if (moodData && moodData.length) {
  const ctxMood = document.getElementById('moodChart').getContext('2d');

  const MOOD_LABELS = ['Sad', 'Stressed', 'Tired', 'Neutral', 'Happy'];


  const moodCounts = {};

  moodData.forEach(d => {
    const moodLabel = MOOD_LABELS[d.mood];
    if (moodLabel) {
      moodCounts[moodLabel] = (moodCounts[moodLabel] || 0) + 1;
    }
  });

  const labels = Object.keys(moodCounts);
  const counts = Object.values(moodCounts);

  const colors = ['#808080', '#FFBB28', '#FF7F50', '#20B2AA', '#5D3FD3'];

  if (window.moodChartInstance) {
    window.moodChartInstance.destroy();
  }

  window.moodChartInstance = new Chart(ctxMood, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Mood Distribution',
        data: counts,
        backgroundColor: colors,
      }]
    },
    options: {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      align: 'start',
      labels: {
        boxWidth: 20,    
        padding: 5,     
        usePointStyle: false, 
      },
      maxHeight: 60,   
    },
    tooltip: {
      callbacks: {
        label: ctx => `${ctx.label}: ${ctx.parsed}`
      }
    }
  }
}

  });
}


if (sleepVsMoodData.length) {
  const ctxSleepMood = document.getElementById('sleepMoodChart').getContext('2d');
  const labels = sleepVsMoodData.map(d => d.date);
  const sleepValues = sleepVsMoodData.map(d => d.sleep_hours);
  const moodValues2 = sleepVsMoodData.map(d => d.mood);

  new Chart(ctxSleepMood, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Sleep Hours',
          data: sleepValues,
          borderColor: 'rgba(255, 159, 64, 0.7)',
          fill: false,
          yAxisID: 'y1',
          tension: 0.1
        },
        {
          label: 'Mood',
          data: moodValues2,
          borderColor: 'rgba(153, 102, 255, 0.7)',
          fill: false,
          yAxisID: 'y2',
          tension: 0.1
        }
      ]
    },
    options: {
      scales: {
        x: { title: { display: true, text: 'Date' } },
        y1: {
          type: 'linear',
          position: 'left',
          title: { display: true, text: 'Sleep Hours' },
          beginAtZero: true
        },
        y2: {
          type: 'linear',
          position: 'right',
          title: { display: true, text: 'Mood' },
          beginAtZero: true,
          grid: { drawOnChartArea: false }
        }
      }
    }
  });
}
>>>>>>> share_part
