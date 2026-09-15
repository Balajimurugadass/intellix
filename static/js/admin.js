// Admin Dashboard and Management Client Logic

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Chart.js charts if canvas elements exist
  const categoryCanvas = document.getElementById('categoryChart');
  const deptCanvas = document.getElementById('departmentChart');

  if (categoryCanvas && window.Chart) {
    const rawCategoryData = JSON.parse(categoryCanvas.dataset.chart || '{}');
    const labels = Object.keys(rawCategoryData);
    const data = Object.values(rawCategoryData);

    new Chart(categoryCanvas, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: [
            '#38bdf8', '#818cf8', '#34d399', '#f59e0b',
            '#f43f5e', '#a78bfa', '#06b6d4', '#94a3b8'
          ],
          borderWidth: 2,
          borderColor: '#111827'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
            labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', size: 11 } }
          }
        },
        cutout: '68%'
      }
    });
  }

  if (deptCanvas && window.Chart) {
    const rawDeptData = JSON.parse(deptCanvas.dataset.chart || '{}');
    const labels = Object.keys(rawDeptData);
    const data = Object.values(rawDeptData);

    new Chart(deptCanvas, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Active Tickets',
          data: data,
          backgroundColor: 'rgba(56, 189, 248, 0.75)',
          borderRadius: 6,
          borderColor: '#38bdf8',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            ticks: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', size: 10 } },
            grid: { display: false }
          },
          y: {
            ticks: { color: '#94a3b8', stepSize: 1 },
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  // Admin Status Update Modal Handler
  window.openStatusModal = function(ticketId, currentStatus) {
    const modal = document.getElementById('statusModal');
    const idInput = document.getElementById('modalTicketId');
    const statusSelect = document.getElementById('modalStatusSelect');
    const titleEl = document.getElementById('modalTicketTitle');

    if (idInput) idInput.value = ticketId;
    if (statusSelect) statusSelect.value = currentStatus;
    if (titleEl) titleEl.innerText = `Update Ticket: ${ticketId}`;

    openModal('statusModal');
  };

  const statusForm = document.getElementById('statusUpdateForm');
  if (statusForm) {
    statusForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const ticketId = document.getElementById('modalTicketId').value;
      const newStatus = document.getElementById('modalStatusSelect').value;
      const notes = document.getElementById('modalStatusNotes').value;
      const submitBtn = statusForm.querySelector('button[type="submit"]');

      submitBtn.disabled = true;
      submitBtn.innerText = 'Updating...';

      try {
        const res = await fetch(`/api/admin/complaints/${ticketId}/status`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status: newStatus, notes })
        });

        const result = await res.json();
        if (!res.ok) throw new Error(result.error || 'Failed to update status');

        showToast(`Ticket ${ticketId} status updated to ${newStatus}`, 'success');
        closeModal('statusModal');
        setTimeout(() => location.reload(), 600);
      } catch (err) {
        showToast(err.message, 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerText = 'Save Status Update';
      }
    });
  }
});
