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
