$(document).ready(function () {
    $('#profile_summary').trumbowyg();
    $('#work_experience').trumbowyg();
    $('#education').trumbowyg();
    $('#other').trumbowyg();
    $('#notes').trumbowyg();
  });
  
  function showAddLinkForm() {
    document.getElementById('addLinkForm').classList.remove('d-none');
  }
  
  function addLinkRow(name = '', url = '') {
    const linkRow = document.createElement('div');
    linkRow.className = 'd-flex align-items-center gap-2 mb-2 link-row';
  
    const nameInput = document.createElement('input');
    nameInput.type = 'text';
    nameInput.name = 'link_names';
    nameInput.className = 'form-control';
    nameInput.placeholder = 'Link name';
    nameInput.value = name;
  
    const urlInput = document.createElement('input');
    urlInput.type = 'text';
    urlInput.name = 'link_urls';
    urlInput.className = 'form-control';
    urlInput.placeholder = 'Link URL';
    urlInput.value = url;
  
    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.className = 'btn btn-outline-danger btn-sm';
    removeButton.innerHTML = '✖️';
    removeButton.onclick = function () {
      linkRow.remove();
    };
  
    linkRow.appendChild(nameInput);
    linkRow.appendChild(urlInput);
    linkRow.appendChild(removeButton);
    document.getElementById('linkFields').appendChild(linkRow);
  
    updateHiddenLinks();
  }
  
  function updateHiddenLinks() {
    const hiddenInput = document.getElementById('linksField');
    const linkRows = document.querySelectorAll('#linkFields > div');
    let linksData = '';
  
    linkRows.forEach(row => {
      const inputs = row.querySelectorAll('input');
      const name = inputs[0].value.trim();
      const url = inputs[1].value.trim();
      if (name && url) {
        linksData += `${name}:::${url};;;`;
      }
    });
  
    hiddenInput.value = linksData;
  }
  
  function removeLink(button) {
    const row = button.parentElement;
    row.remove();
  }
  