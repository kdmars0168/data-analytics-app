document.addEventListener('DOMContentLoaded', function () {
  const fileInput = document.getElementById('file-upload');
  const filePreview = document.getElementById('file-preview');
  const fileName = document.getElementById('selected-filename');

  if (fileInput) {
    fileInput.addEventListener('change', function () {
      if (fileInput.files.length > 0) {
        const name = fileInput.files[0].name;
        fileName.textContent = `Selected file: ${name}`;
        filePreview.classList.remove('hidden');
      } else {
        filePreview.classList.add('hidden');
      }
    });
  }
});
