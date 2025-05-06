function openCandidateModal(candidateId) {
    fetch(`/candidates/candidate-modal/${candidateId}/`)
      .then(response => response.json())
      .then(data => {
        document.getElementById("candidateModalContent").innerHTML = data.html;
        new bootstrap.Modal(document.getElementById('candidateModal')).show();
        initUploadScript();
        loadCandidateFiles(candidateId);
      });
  }
  
  function openDeleteCandidateModal(candidateId, name = '') {
    const modalEl = document.getElementById('deleteCandidateModal');
    const form = document.getElementById('deleteCandidateForm');
    modalEl.querySelector('h5').innerHTML = `Are you sure you want to delete candidate <strong>${name}</strong>?`;
    form.action = `/candidates/${candidateId}/delete/`;
  
    const newForm = form.cloneNode(true);
    form.parentNode.replaceChild(newForm, form);
    new bootstrap.Modal(modalEl).show();
  }
  
  function openDeleteFileModal(fileId, fileName = '') {
    const modalEl = document.getElementById('deleteFileModal');
    const form = document.getElementById('deleteFileForm');
    modalEl.querySelector('h5').innerHTML = `Are you sure you want to delete file <strong>${fileName}</strong>?`;
    form.action = `/candidates/file/${fileId}/delete/`;
  
    const newForm = form.cloneNode(true);
    form.parentNode.replaceChild(newForm, form);
  
    newForm.addEventListener('submit', function (e) {
      e.preventDefault();
      fetch(newForm.action, {
        method: 'POST',
        headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
      })
        .then(res => res.json())
        .then(() => reloadFiles());
  
      bootstrap.Modal.getInstance(modalEl).hide();
    });
  
    new bootstrap.Modal(modalEl).show();
  }
  