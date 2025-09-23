document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('contactForm');
    const formStatus = form.querySelector('.form-status');

    // Error messages for validation
    const errorMessages = {
        firstName: {
            valueMissing: 'Please enter your first name',
            patternMismatch: 'Please use only letters in your first name',
            tooShort: 'First name must be at least 2 characters long'
        },
        lastName: {
            valueMissing: 'Please enter your last name',
            patternMismatch: 'Please use only letters in your last name',
            tooShort: 'Last name must be at least 2 characters long'
        },
        email: {
            valueMissing: 'Please enter your email address',
            typeMismatch: 'Please enter a valid email address'
        },
        subject: {
            valueMissing: 'Please select a subject'
        },
        message: {
            valueMissing: 'Please enter your message',
            tooShort: 'Message must be at least 10 characters long'
        }
    };

    // Show appropriate error message for each field
    const showError = (input) => {
        const errorElement = document.getElementById(`${input.id}-error`);
        if (!errorElement) return;

        let message = '';
        const messages = errorMessages[input.id];

        if (input.validity.valueMissing && messages.valueMissing) {
            message = messages.valueMissing;
        } else if (input.validity.typeMismatch && messages.typeMismatch) {
            message = messages.typeMismatch;
        } else if (input.validity.patternMismatch && messages.patternMismatch) {
            message = messages.patternMismatch;
        } else if (input.validity.tooShort && messages.tooShort) {
            message = messages.tooShort;
        }

        errorElement.textContent = message;
    };

    // Validate a single field
    const validateField = (input) => {
        if (input.validity.valid) {
            document.getElementById(`${input.id}-error`).textContent = '';
        } else {
            showError(input);
        }
    };

    // Add validation listeners to all form fields
    form.querySelectorAll('input, select, textarea').forEach(input => {
        input.addEventListener('blur', () => validateField(input));
        input.addEventListener('input', () => validateField(input));
    });

    // Form submission handler
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Check if the form is valid
        if (!form.checkValidity()) {
            // Show validation messages
            form.querySelectorAll('input, select, textarea').forEach(input => {
                validateField(input);
            });
            return;
        }

        // Show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.classList.add('loading');
        submitButton.disabled = true;

        try {
            // Collect form data
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            // Here you would normally send the data to your server
            // For demonstration, we'll simulate a server response
            await new Promise(resolve => setTimeout(resolve, 1500));

            // Show success message
            formStatus.className = 'form-status success';
            formStatus.textContent = 'Thank you! Your message has been sent successfully.';
            form.reset();

            // Hide success message after 5 seconds
            setTimeout(() => {
                formStatus.className = 'form-status';
                formStatus.textContent = '';
            }, 5000);

        } catch (error) {
            // Show error message
            formStatus.className = 'form-status error';
            formStatus.textContent = 'Sorry, there was a problem sending your message. Please try again later.';
        } finally {
            // Remove loading state
            submitButton.classList.remove('loading');
            submitButton.disabled = false;
        }
    });
});