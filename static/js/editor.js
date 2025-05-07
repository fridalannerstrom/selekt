// When the DOM is fully loaded, initialize Trumbowyg editors on specified textareas
$(document).ready(function () {
    $('#profile_summary').trumbowyg();  
    $('#work_experience').trumbowyg();  
    $('#education').trumbowyg();   
    $('#other').trumbowyg();         
    $('#notes').trumbowyg();      
});

// Shows the form to add a new link
function showAddLinkForm() {
    document.getElementById('addLinkForm').classList.remove('d-none');
}

// Adds a new row of inputs for a link (name + URL) with a remove button
function addLinkRow(name = '', url = '') {
    const linkRow = document.createElement('div');
    linkRow.className = 'd-flex align-items-center gap-2 mb-2 link-row'; // Flexbox styling

    // Input field for link name
    const nameInput = document.createElement('input');
    nameInput.type = 'text';
    nameInput.name = 'link_names';
    nameInput.className = 'form-control';
    nameInput.placeholder = 'Link name';
    nameInput.value = name;

    // Input field for link URL
    const urlInput = document.createElement('input');
    urlInput.type = 'text';
    urlInput.name = 'link_urls';
    urlInput.className = 'form-control';
    urlInput.placeholder = 'Link URL';
    urlInput.value = url;

    // Button to remove this link row
    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.className = 'btn btn-outline-danger btn-sm';
    removeButton.innerHTML = 'X';
    removeButton.onclick = function () {
        linkRow.remove();
    };

    // Append inputs and button to the row
    linkRow.appendChild(nameInput);
    linkRow.appendChild(urlInput);
    linkRow.appendChild(removeButton);

    // Add the row to the container
    document.getElementById('linkFields').appendChild(linkRow);

    // Update the hidden input field with current link values
    updateHiddenLinks();
}

// Combines all link input rows into a single string and updates a hidden input
function updateHiddenLinks() {
    const hiddenInput = document.getElementById('linksField'); 
    const linkRows = document.querySelectorAll('#linkFields > div'); 
    const jsonInput = document.getElementById("hiddenLinksInput");

    let linksData = '';
    let linksArray = []; 

    linkRows.forEach(row => {
        const inputs = row.querySelectorAll('input');
        const name = inputs[0].value.trim();
        const url = inputs[1].value.trim();

        if (name && url) {
            linksData += `${name}:::${url};;;`;
            linksArray.push({ name, url });
        }
    });

    if (hiddenInput) {
        hiddenInput.value = linksData;
    } else {
        console.warn("Hidden input with id='linksField' not found.");
    }

    if (jsonInput) {
        jsonInput.value = JSON.stringify(linksArray);
    } else {
        console.warn("Hidden input with id='hiddenLinksInput' not found.");
    }
}

// Removes a link row when the remove button is clicked (alternative method)
function removeLink(button) {
    const row = button.parentElement;
    row.remove();
}