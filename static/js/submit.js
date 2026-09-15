// Complaint Submission Client Logic

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('complaintForm');
  const analyzeBtn = document.getElementById('analyzeBtn');
  const gpsBtn = document.getElementById('useGpsBtn');
  const latInput = document.getElementById('latitude');
  const lonInput = document.getElementById('longitude');
  const locTextInput = document.getElementById('locationText');
  const evidenceInput = document.getElementById('evidenceFile');
  const evidencePreview = document.getElementById('evidencePreview');
  const duplicateModal = document.getElementById('duplicateModal');

  let currentAnalysisPayload = null;

  // HTML5 Browser Geolocation
  if (gpsBtn) {
    gpsBtn.addEventListener('click', () => {
      if (!navigator.geolocation) {
        showToast('Geolocation is not supported by your browser.', 'warning');
        return;
      }

      gpsBtn.disabled = true;
      gpsBtn.innerHTML = 'Detecting GPS...';

      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const lat = pos.coords.latitude.toFixed(4);
          const lon = pos.coords.longitude.toFixed(4);
          latInput.value = lat;
          lonInput.value = lon;
          locTextInput.value = `Current Device Location (${lat}, ${lon})`;
          gpsBtn.disabled = false;
          gpsBtn.innerHTML = '✓ GPS Locked';
          showToast(`Location captured: ${lat}, ${lon}`, 'success');
        },
        (err) => {
          gpsBtn.disabled = false;
          gpsBtn.innerHTML = 'Use Current Location';
          showToast('Could not access GPS. Please allow location permissions.', 'warning');
        }
      );
    });
  }

  // File Upload Preview
  if (evidenceInput) {
    evidenceInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
          evidencePreview.src = event.target.result;
          evidencePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Location Preset Selector
  const presetSelect = document.getElementById('locationPreset');
  if (presetSelect) {
    presetSelect.addEventListener('change', (e) => {
      const val = e.target.value;
      if (!val) return;
      const [lat, lon, name] = val.split('|');
      latInput.value = lat;
      lonInput.value = lon;
      locTextInput.value = name;
      showToast(`Selected: ${name}`, 'info');
    });
  }

  // Form Analysis Trigger
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const description = document.getElementById('description').value.trim();
      const location = locTextInput.value.trim() || 'Civic Ward 4';
      const lat = parseFloat(latInput.value) || 13.0850;
      const lon = parseFloat(lonInput.value) || 80.2101;
      const evidenceUrl = evidencePreview ? evidencePreview.src : null;

      if (!description) {
        showToast('Please describe the municipal issue before submitting.', 'error');
        return;
      }

      analyzeBtn.disabled = true;
      analyzeBtn.innerHTML = `
        <svg style="animation: spin 1s linear infinite; width: 18px; height: 18px; display:inline-block; vertical-align:middle; margin-right:8px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
          <path d="M12 2a10 10 0 0 1 10 10"></path>
        </svg>
        Analyzing with AI...
      `;

      try {
        const res = await fetch('/api/analyze-complaint', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ description, latitude: lat, longitude: lon })
        });

        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.error || 'Failed to analyze complaint.');
        }

        currentAnalysisPayload = {
          description,
          location,
          latitude: lat,
          longitude: lon,
          evidenceUrl,
          ai: data.ai,
          duplicates: data.duplicates
        };

        // Check if duplicates were detected
        if (data.duplicates && data.duplicates.found) {
          renderDuplicateModal(data.duplicates);
          openModal('duplicateModal');
        } else {
          // No duplicate, proceed directly to confirmation
          submitToConfirmation(currentAnalysisPayload);
        }
      } catch (err) {
        showToast(err.message, 'error');
      } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = 'Analyze & Proceed to Confirmation &rarr;';
      }
    });
  }

  function renderDuplicateModal(duplicates) {
    const countEl = document.getElementById('duplicateCount');
    const listEl = document.getElementById('duplicateList');

    if (countEl) countEl.innerText = duplicates.count;
    if (listEl) {
      listEl.innerHTML = duplicates.similarTickets.map(t => `
        <div style="background: rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:12px; margin-bottom:10px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-family:monospace; font-weight:700; color:#38bdf8;">${t.ticketId}</span>
            <span class="badge status-${t.status.replace(' ', '_')}">${t.status}</span>
          </div>
          <p style="font-size:0.85rem; color:#cbd5e1; margin-bottom:6px;">${t.description}</p>
          <div style="font-size:0.75rem; color:#94a3b8; display:flex; justify-content:space-between;">
            <span>📍 ${t.location} (~${t.distanceMeters}m away)</span>
            <span>📅 ${t.createdAt}</span>
          </div>
        </div>
      `).join('');
    }
  }

  // Join Existing Issue Button
  const joinBtn = document.getElementById('joinIssueBtn');
  if (joinBtn) {
    joinBtn.addEventListener('click', () => {
      closeModal('duplicateModal');
      if (currentAnalysisPayload) {
        currentAnalysisPayload.joinedExisting = true;
        submitToConfirmation(currentAnalysisPayload);
      }
    });
  }

  // Create New Issue Button
  const createNewBtn = document.getElementById('createNewBtn');
  if (createNewBtn) {
    createNewBtn.addEventListener('click', () => {
      closeModal('duplicateModal');
      if (currentAnalysisPayload) {
        currentAnalysisPayload.joinedExisting = false;
        submitToConfirmation(currentAnalysisPayload);
      }
    });
  }

  function submitToConfirmation(payload) {
    // Create dynamic form to POST payload to /confirmation view
    const postForm = document.createElement('form');
    postForm.method = 'POST';
    postForm.action = '/confirmation';

    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'analysis_payload';
    hiddenInput.value = JSON.stringify(payload);

    postForm.appendChild(hiddenInput);
    document.body.appendChild(postForm);
    postForm.submit();
  }
});
