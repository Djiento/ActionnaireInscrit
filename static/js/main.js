// Main JavaScript for investor registration platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeFormValidation();
    initializeFileUpload();
    initializeTooltips();
    initializeSearchDebounce();
    initializeClipboard();
    initializeConfirmations();
});

// Form validation enhancements
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[novalidate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            
            form.classList.add('was-validated');
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(input);
            });
            
            input.addEventListener('input', function() {
                if (input.classList.contains('is-invalid')) {
                    validateField(input);
                }
            });
        });
    });
}

function validateField(field) {
    const isValid = field.checkValidity();
    
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
    
    // Special validation for WhatsApp number
    if (field.name === 'whatsapp_number') {
        validateWhatsAppNumber(field);
    }
    
    // Special validation for email
    if (field.type === 'email') {
        validateEmail(field);
    }
}

function validateWhatsAppNumber(field) {
    const value = field.value.replace(/[\s\-\(\)\+]/g, '');
    const isNumeric = /^\d+$/.test(value);
    const isValidLength = value.length >= 8 && value.length <= 20;
    
    if (field.value && (!isNumeric || !isValidLength)) {
        field.setCustomValidity('Veuillez entrer un numéro WhatsApp valide (chiffres uniquement)');
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
    } else {
        field.setCustomValidity('');
        if (field.value) {
            field.classList.add('is-valid');
            field.classList.remove('is-invalid');
        }
    }
}

function validateEmail(field) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (field.value && !emailRegex.test(field.value)) {
        field.setCustomValidity('Veuillez entrer une adresse e-mail valide');
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
    } else {
        field.setCustomValidity('');
        if (field.value) {
            field.classList.add('is-valid');
            field.classList.remove('is-invalid');
        }
    }
}

// File upload enhancements
function initializeFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            const feedback = this.parentNode.querySelector('.file-feedback') || createFileFeedback(this);
            
            if (file) {
                const isValidType = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'].includes(file.type);
                const isValidSize = file.size <= 16 * 1024 * 1024; // 16MB
                
                if (!isValidType) {
                    showFileError(feedback, 'Type de fichier non autorisé. Utilisez PDF, JPG, JPEG ou PNG.');
                    this.value = '';
                } else if (!isValidSize) {
                    showFileError(feedback, 'Fichier trop volumineux. Taille maximale : 16 MB.');
                    this.value = '';
                } else {
                    showFileSuccess(feedback, `Fichier sélectionné : ${file.name} (${formatFileSize(file.size)})`);
                }
            } else {
                feedback.textContent = '';
                feedback.className = 'file-feedback';
            }
        });
        
        // Drag and drop functionality
        const parent = input.parentNode;
        
        parent.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('drag-over');
        });
        
        parent.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');
        });
        
        parent.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                input.files = files;
                input.dispatchEvent(new Event('change'));
            }
        });
    });
}

function createFileFeedback(input) {
    const feedback = document.createElement('div');
    feedback.className = 'file-feedback mt-1';
    input.parentNode.appendChild(feedback);
    return feedback;
}

function showFileError(feedback, message) {
    feedback.textContent = message;
    feedback.className = 'file-feedback mt-1 text-danger';
}

function showFileSuccess(feedback, message) {
    feedback.textContent = message;
    feedback.className = 'file-feedback mt-1 text-success';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Search debounce for admin dashboard
function initializeSearchDebounce() {
    const searchInput = document.querySelector('input[name="search"]');
    
    if (searchInput) {
        let debounceTimer;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            
            debounceTimer = setTimeout(() => {
                // Auto-submit search after 500ms of no typing
                const form = this.closest('form');
                if (form && this.value.length >= 3) {
                    // Only auto-submit if search term is 3+ characters
                    form.submit();
                }
            }, 500);
        });
    }
}

// Clipboard functionality
function initializeClipboard() {
    const copyButtons = document.querySelectorAll('[data-copy]');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            
            navigator.clipboard.writeText(textToCopy).then(() => {
                showToast('Copié dans le presse-papiers !', 'success');
                
                // Temporarily change button text
                const originalText = this.textContent;
                this.textContent = 'Copié !';
                this.disabled = true;
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.disabled = false;
                }, 2000);
            }).catch(() => {
                showToast('Erreur lors de la copie', 'error');
            });
        });
    });
}

// Confirmation dialogs
function initializeConfirmations() {
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    
    confirmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });
}

// Toast notifications
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1060';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : type}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    // Initialize and show toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 5000
    });
    
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// Format phone numbers on input
function formatPhoneNumber(input) {
    // Remove all non-digit characters
    let value = input.value.replace(/\D/g, '');
    
    // Format based on length
    if (value.length >= 10) {
        // International format: +XX X XX XX XX XX
        value = value.replace(/(\d{2})(\d{1})(\d{2})(\d{2})(\d{2})(\d{2})/, '+$1 $2 $3 $4 $5 $6');
    } else if (value.length >= 6) {
        // Partial format
        value = value.replace(/(\d{2})(\d{1})(\d{2})(\d{2})/, '+$1 $2 $3 $4');
    }
    
    input.value = value;
}

// Auto-resize textareas
function autoResizeTextarea() {
    const textareas = document.querySelectorAll('textarea');
    
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
        
        // Initial resize
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    });
}

// Initialize auto-resize for textareas
document.addEventListener('DOMContentLoaded', autoResizeTextarea);

// Loading states for forms
function setFormLoading(form, loading = true) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const inputs = form.querySelectorAll('input, select, textarea');
    
    if (loading) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Traitement en cours...';
        inputs.forEach(input => input.disabled = true);
    } else {
        submitBtn.disabled = false;
        submitBtn.innerHTML = submitBtn.getAttribute('data-original-text') || 'Soumettre';
        inputs.forEach(input => input.disabled = false);
    }
}

// Handle form submissions with loading states
document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.tagName === 'FORM') {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn && !submitBtn.getAttribute('data-original-text')) {
            submitBtn.setAttribute('data-original-text', submitBtn.textContent);
        }
        setFormLoading(form, true);
    }
});

// Table enhancements
function initializeTableEnhancements() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        // Add click handlers for sortable columns
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                const sortBy = this.getAttribute('data-sort');
                const currentSort = new URLSearchParams(window.location.search).get('sort');
                const currentOrder = new URLSearchParams(window.location.search).get('order') || 'asc';
                
                let newOrder = 'asc';
                if (currentSort === sortBy && currentOrder === 'asc') {
                    newOrder = 'desc';
                }
                
                const url = new URL(window.location);
                url.searchParams.set('sort', sortBy);
                url.searchParams.set('order', newOrder);
                
                window.location.href = url.toString();
            });
        });
    });
}

// Initialize table enhancements if tables exist
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.table')) {
        initializeTableEnhancements();
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[name="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to clear search
    if (e.key === 'Escape') {
        const searchInput = document.querySelector('input[name="search"]');
        if (searchInput && searchInput === document.activeElement) {
            searchInput.value = '';
            searchInput.blur();
        }
    }
});

// Smooth scrolling for anchor links
document.addEventListener('click', function(e) {
    if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const targetId = e.target.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});

// Console welcome message for developers
console.log('%c🚀 Investisseurs Platform', 'color: #0d6efd; font-size: 20px; font-weight: bold;');
console.log('%cVersion 1.0.0 - Built with Flask & Bootstrap', 'color: #6c757d; font-size: 12px;');
