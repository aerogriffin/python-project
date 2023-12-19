// Get the file input and the container for the file name
const fileInput = document.getElementById('fileInput');
const fileNameContainer = document.getElementById('fileName');

// Add a change event to the input to update the selected file name
fileInput.addEventListener('change', () => {
  if (fileInput.files.length > 0) {
    fileNameContainer.textContent = `Selected Video: ${fileInput.files[0].name}`;
  } else {
    fileNameContainer.textContent = ''; // Clear if no file is selected
  }
});