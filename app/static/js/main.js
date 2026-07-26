/**
 * Event Management System - Primary JavaScript
 * 
 * Sections:
 * 1. DOM Ready Wrapper
 * 2. Flash Alert Auto-Dismiss
 * 3. Delete Confirmation
 * 4. Prevent Double Submission & Loading Indicators
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================================================
    // 2. Flash Alert Auto-Dismiss
    // ==========================================================================
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        // Only auto-dismiss success and info alerts, keep errors visible until dismissed
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // ==========================================================================
    // 3. Delete Confirmation
    // ==========================================================================
    const deleteForms = document.querySelectorAll('.form-delete');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to proceed? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // ==========================================================================
    // 4. Prevent Double Submission & Loading Indicators
    // ==========================================================================
    const loadingForms = document.querySelectorAll('.form-loading');
    loadingForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            // If the form is already submitting, prevent duplicate
            if (form.classList.contains('is-submitting')) {
                e.preventDefault();
                return;
            }
            
            // Check HTML5 validation first
            if (!form.checkValidity()) {
                return; // Let browser handle the validation UI
            }

            form.classList.add('is-submitting');
            
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                // Save original text
                const originalText = submitBtn.innerHTML;
                
                // Disable button and show spinner
                submitBtn.disabled = true;
                submitBtn.innerHTML = `
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    <span aria-live="polite">Please wait...</span>
                `;
            }
    // ==========================================================================
    // 5. Form Validation & Date Limits
    // ==========================================================================
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    const dateInput = document.getElementById('event_date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }

});
