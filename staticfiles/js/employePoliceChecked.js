// Get the last checkbox element
var lastCheckbox = document.getElementById('inlineFormCheckMane');

// Get all checkboxes
var checkboxes = document.querySelectorAll('.form-check-input');

// Add click event listener to the last checkbox
lastCheckbox.addEventListener('click', function() {
  var isChecked = lastCheckbox.checked;

  // Check or uncheck all checkboxes based on the last checkbox state
  checkboxes.forEach(function(checkbox) {
    checkbox.checked = isChecked;
  });
});
// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')
    }, false)
  })
})()
