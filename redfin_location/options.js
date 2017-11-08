// Saves options to chrome.storage
function save_options() {
  var place1Label = document.getElementById('place1Label').value;
  var place2Label = document.getElementById('place2Label').value;
  var place3Label = document.getElementById('place3Label').value;
  var place4Label = document.getElementById('place4Label').value;
  var place1Address = document.getElementById('place1Address').value;
  var place2Address = document.getElementById('place2Address').value;
  var place3Address = document.getElementById('place3Address').value;
  var place4Address = document.getElementById('place4Address').value;
  chrome.storage.sync.set({
    place1Label: place1Label,
    place2Label: place2Label,
    place3Label: place3Label,
    place4Label: place4Label,
    place1Address: place1Address,
    place2Address: place2Address,
    place3Address: place3Address,
    place4Address: place4Address
  }, function() {
    // Update status to let user know options were saved.
    var status = document.getElementById('status');
    status.textContent = 'Options saved.';
    setTimeout(function() {
      status.textContent = '';
    }, 750);
  });
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
function restore_options() {
  chrome.storage.sync.get({
    place1Label: '',
    place2Label: '',
    place3Label: '',
    place4Label: '',
    place1Address: '',
    place2Address: '',
    place3Address: '',
    place4Address: ''
  }, function(items) {
    document.getElementById('place1Label').value = items.place1Label;
    document.getElementById('place1Address').value = items.place1Address;
    document.getElementById('place2Label').value = items.place2Label;
    document.getElementById('place2Address').value = items.place2Address;
    document.getElementById('place3Label').value = items.place3Label;
    document.getElementById('place3Address').value = items.place3Address;
    document.getElementById('place4Label').value = items.place4Label;
    document.getElementById('place4Address').value = items.place4Address;
  });
}
document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click',
    save_options);
