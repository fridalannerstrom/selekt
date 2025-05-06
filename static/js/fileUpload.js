function initUploadScript() {
    const fileElem = document.getElementById("fileElem");
    const uploadBtn = document.getElementById("uploadBtn");
    const selectedFilesList = document.getElementById("selectedFilesList");
    const uploadArea = document.getElementById("fileUploadArea");
    const fileListArea = document.getElementById("fileListArea");
    let selectedFiles = [];
  
    if (!uploadArea) return;
    const candidateId = uploadArea.dataset.candidateId;
  
    fileElem.addEventListener("change", function () {
      selectedFiles = Array.from(fileElem.files);
      selectedFilesList.innerHTML = selectedFiles.map(f => `<div>${f.name}</div>`).join("");
      uploadBtn.classList.remove("d-none");
    });
  
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
          bindDeleteButtons();
        });
    });
  
    function bindDeleteButtons() {
      document.querySelectorAll(".delete-file-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          const fileId = btn.dataset.fileId;
          fetch(`/candidates/delete-file/${fileId}/`, {
            method: "POST",
            headers: {
              "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
          })
            .then(() => fetch(`/candidates/${candidateId}/files/`))
            .then(res => res.json())
            .then(data => {
              fileListArea.innerHTML = data.html;
              bindDeleteButtons();
            });
        });
      })
    }
  
    bindDeleteButtons();
  }