// Initializes the file upload functionality for a candidate
function initUploadScript() {
    const fileElem = document.getElementById("fileElem");
    const uploadBtn = document.getElementById("uploadBtn");
    const selectedFilesList = document.getElementById("selectedFilesList");
    const uploadArea = document.getElementById("fileUploadArea");
    const fileListArea = document.getElementById("fileListArea");

    if (!uploadArea || !fileElem || !uploadBtn || !selectedFilesList || !fileListArea) {
        console.warn("Upload script not initialized: missing DOM elements.");
        return;
    }

    let selectedFiles = [];

    const candidateId = uploadArea.dataset.candidateId;
  
    // Handle file selection
    fileElem.addEventListener("change", function () {
        selectedFiles = Array.from(fileElem.files);
        selectedFilesList.innerHTML = selectedFiles.map(f => `<div>${f.name}</div>`).join("");
        uploadBtn.classList.remove("d-none");
    });
  
    // Handle upload click
    uploadBtn.addEventListener("click", function () {
      const formData = new FormData();
      selectedFiles.forEach(file => formData.append("files", file));
  
      fetch(`/candidates/${candidateId}/upload-files/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: formData
      })
        .then(res => res.json())
        .then(() => fetch(`/candidates/${candidateId}/files/`))
        .then(res => res.json())
        .then(data => {
          selectedFiles = [];
          selectedFilesList.innerHTML = "";
          uploadBtn.classList.add("d-none");
          fileListArea.innerHTML = data.html;
          bindDeleteButtons(); // Re-bind after DOM update
        });
    });
  
    bindDeleteButtons(); // Initial bind
  }
  
  // Loads file list for a candidate and binds delete buttons
  function loadCandidateFiles(candidateId) {
    fetch(`/candidates/${candidateId}/files/`)
      .then(res => res.json())
      .then(data => {
        document.getElementById('fileListArea').innerHTML = data.html;
        bindDeleteButtons();
      });
  }
  
  // Binds click events to delete buttons
  function bindDeleteButtons() {
    document.querySelectorAll(".delete-file-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const fileId = btn.dataset.fileId;
        const fileName = btn.dataset.fileName || 'this file';
  
        openDeleteFileModal(fileId, fileName);
      });
    });
  }

  // Reload files list
  function reloadFiles() {
    const candidateId = document.getElementById('fileUploadArea').getAttribute('data-candidate-id');
    loadCandidateFiles(candidateId);
}

