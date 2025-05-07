// Handles PDF upload and automatic candidate creation via OpenAI.

// Run this once the entire DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    const uploadArea = document.getElementById("fileUploadArea");

    // Binds the file input and sets up the upload process
    function setupFileInput() {
        const fileElem = document.getElementById("fileElem");
        if (!fileElem) return;

        fileElem.addEventListener("change", function () {
            const selectedFile = fileElem.files[0];
            if (!selectedFile) return;

            // Validate file type
            if (!selectedFile.name.toLowerCase().endsWith(".pdf")) {
                alert("Only PDF files are allowed.");
                return;
            }

            // Show loading screen while processing
            uploadArea.innerHTML = `
          <div class="text-center py-4">
            <img class="loading-icon mb-3" src="/static/media/images/selekt-loading.gif" alt="Loading...">
            <h3 class="mb-2">Scanning your PDF...</h3>
            <p class="text-muted">Please wait while we scan your PDF for candidate details...</p>
          </div>
        `;

            // Prepare FormData and send file to backend
            const formData = new FormData();
            formData.append("file", selectedFile);

            fetch("/candidates/upload/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: formData,
            })
                .then(res => res.json())
                .then(data => {
                    // If upload and extraction were successful, send structured data to create candidate
                    if (data.results && data.results[0].status === "success" && data.results[0].structured) {
                        return fetch("/candidates/create-from-openai/", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                            },
                            body: JSON.stringify(data.results[0].structured)
                        });
                    } else {
                        // Extract error message or show generic one
                        const errMsg = data.results && data.results[0].error
                            ? data.results[0].error
                            : "No structured data returned from OpenAI";
                        throw new Error(errMsg);
                    }
                })
                .then(res => res.json())
                .then(data => {
                    // Redirect to candidate form if everything succeeded
                    if (data.redirect_url) {
                        window.location.href = data.redirect_url;
                    }
                })
                .catch(err => {
                    console.error("Upload or parsing failed:", err);

                    // Show error message and allow user to try again
                    uploadArea.innerHTML = `
              <div class="alert alert-danger text-center p-4">
                ❌ <strong>Something went wrong:</strong><br>
                ${err.message}
              </div>
              <div class="text-center mt-3">
                <label for="fileElem" class="btn button-base scn-button">Choose a new file</label>
                <input type="file" id="fileElem" name="file" style="display:none">
              </div>
            `;

                    setupFileInput(); // Re-bind event listener on the new input
                });
        });
    }

    // Initial binding on page load
    setupFileInput();
});
