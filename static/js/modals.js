// Open Candidate Detail Modal
function openCandidateModal(candidateId) {
    // Fetch candidate modal HTML from backend
    fetch(`/candidates/candidate-modal/${candidateId}/`)
      .then(response => response.json())
      .then(data => {
        // Inject received HTML into modal content container
        document.getElementById("candidateModalContent").innerHTML = data.html;
  
        // Show the modal using Bootstrap
        new bootstrap.Modal(document.getElementById('candidateModal')).show();
  
        // Initialize file upload functionality inside the modal
        initUploadScript();
  
        // Load and render uploaded files for this candidate
        loadCandidateFiles(candidateId);
      });
  }
  
  // Open Delete Candidate Modal
  function openDeleteCandidateModal(candidateId, name = '') {
    const modalEl = document.getElementById('deleteCandidateModal');
    const form = document.getElementById('deleteCandidateForm');
  
    // Update the confirmation message in the modal with the candidate name
    modalEl.querySelector('h5').innerHTML = `Are you sure you want to delete candidate <strong>${name}</strong>?`;
  
    // Set form action to the correct delete endpoint
    form.action = `/candidates/${candidateId}/delete/`;
  
    // Replace the form with a clone to avoid multiple submit listeners
    const newForm = form.cloneNode(true);
    form.parentNode.replaceChild(newForm, form);
  
    // Show the modal
    new bootstrap.Modal(modalEl).show();
  }
  
  // Open Delete File Modal
  function openDeleteFileModal(fileId, fileName = '') {
    const modalEl = document.getElementById('deleteFileModal');
    const form = document.getElementById('deleteFileForm');
  
    // Update modal text with file name
    modalEl.querySelector('h5').innerHTML = `Are you sure you want to delete file <strong>${fileName}</strong>?`;
  
    // Set the form's action URL to the delete file endpoint
    form.action = `/candidates/file/${fileId}/delete/`;
  
    // Replace form element to reset previous event listeners
    const newForm = form.cloneNode(true);
    form.parentNode.replaceChild(newForm, form);
  
    // Handle form submission (file deletion)
    newForm.addEventListener('submit', function (e) {
      e.preventDefault();
  
      // Send POST request to delete the file
      fetch(newForm.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
      })
        .then(res => res.json())
        .then(() => {
          // Reload file list after deletion
          reloadFiles();
        });
  
      // Hide the modal
      bootstrap.Modal.getInstance(modalEl).hide();
    });
  
    // Show the delete confirmation modal
    new bootstrap.Modal(modalEl).show();
  }