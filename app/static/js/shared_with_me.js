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
