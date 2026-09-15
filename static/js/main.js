// Main CivicRoute AI Shared Client Utilities

function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast-item toast-${type}`;
  
  let borderColor = '#38bdf8';
  if (type === 'success') borderColor = '#10b981';
  if (type === 'error') borderColor = '#f43f5e';
  if (type === 'warning') borderColor = '#f59e0b';
  toast.style.borderLeft = `4px solid ${borderColor}`;

  toast.innerHTML = `
    <span>${message}</span>
    <button style="background:none; border:none; color:#94a3b8; cursor:pointer; margin-left:10px;" onclick="this.parentElement.remove()">&times;</button>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Modal helper functions
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
  }
}

// Global modal close on click outside
window.addEventListener('click', (e) => {
  if (e.target.classList && e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('active');
    document.body.style.overflow = 'auto';
  }
});
