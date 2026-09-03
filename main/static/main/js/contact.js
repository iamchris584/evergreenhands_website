document.addEventListener('DOMContentLoaded', () => {
  const contactForm = document.getElementById('contact-form');
  const alertContainer = document.getElementById('alert-container');
  
  if (!contactForm) return;

  const submitBtn = contactForm.querySelector('button[type="submit"]');

  const clearErrors = () => {
    contactForm.querySelectorAll('.field-error').forEach(span => span.textContent = '');
    contactForm.querySelectorAll('.input-invalid').forEach(input => input.classList.remove('input-invalid'));
  };

  contactForm.addEventListener('submit', (e) => {
    e.preventDefault(); // Prevents full page reload/redirect
    clearErrors();

    // 1. Disable button and update text
    let originalBtnText = '';
    if (submitBtn) {
      originalBtnText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = 'Please wait...';
    }

    const formData = new FormData(contactForm);

    fetch(contactForm.action, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    })
    .then(async (res) => {
      const data = await res.json();

      if (res.ok && data.status === 'success') {
        contactForm.reset(); 
        
        if (alertContainer) {
          alertContainer.innerHTML = `
            <div class="modal-overlay" id="message-modal">
              <div class="centered-alert alert--success" role="alert">
                <svg class="alert__icon" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <p>${data.message}</p>
                <button type="button" class="centered-alert__close" id="close-modal-btn">&times;</button>
              </div>
            </div>
          `;

          const modal = document.getElementById('message-modal');
          const closeBtn = document.getElementById('close-modal-btn');
          
          if (closeBtn) {
            closeBtn.addEventListener('click', () => modal.remove());
          }
          if (modal) {
            modal.addEventListener('click', (ev) => { if (ev.target === modal) modal.remove(); });
            setTimeout(() => { if (modal) modal.remove(); }, 4000);
          }
        }

      } else if (data.errors) {
        Object.keys(data.errors).forEach(fieldName => {
          const input = contactForm.querySelector(`[name="${fieldName}"]`);
          if (input) {
            input.classList.add('input-invalid');
            const fieldWrap = input.closest('.contact-form__field, .donation-form__checkbox, .contact-form__checkbox');
            const errorSpan = fieldWrap ? fieldWrap.querySelector('.field-error') : null;
            if (errorSpan) {
              errorSpan.textContent = data.errors[fieldName][0];
            }
          }
        });
      }
    })
    .catch(err => console.error('Fetch error:', err))
    .finally(() => {
      // 2. Restore button state once fetch completes (success or error)
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      }
    });
  });
});