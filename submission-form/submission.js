/**
 * AIDEAL Pair Submission Form
 * 
 * Client-side validation and submission handler for the pair submission form.
 * Generates the next available ID, validates against schema, and submits to GitHub API.
 */

// Category descriptions for display
const CATEGORY_DESCRIPTIONS = {
    "genre-inclusion": "Égalité de genre, écriture inclusive, lutte contre les stéréotypes de genre",
    "techno-solutionnisme": "Critique de la technologie comme solution unique aux problèmes sociaux",
    "vision-economique": "Priorité à l'humain sur le profit, économie solidaire et circulaire",
    "validisme-accessibilite": "Accessibilité universelle, lutte contre le validisme, inclusion des personnes handicapées",
    "inegalites-nord-sud": "Solidarité internationale, décolonialité, justice climatique Nord-Sud",
    "ecologie-sobriete": "Sobriété écologique, décroissance, justice environnementale",
    "gouvernance-pouvoir-agir": "Démocratie participative, participation des personnes concernées, empowerment",
    "diversite-parcours": "Inclusion des parcours de vie diversifiés, lutte contre les discriminations systémiques"
};

// Form elements
const form = document.getElementById('pair-form');
const categorySelect = document.getElementById('category');
const categoryId = document.getElementById('category-description');
const validationMessage = document.getElementById('validation-message');
const submitBtn = form.querySelector('.btn-primary');

// Initialize form on load
document.addEventListener('DOMContentLoaded', initForm);

function initForm() {
    // Set up category description updates
    categorySelect.addEventListener('change', updateCategoryDescription);
    
    // Set up form submission
    form.addEventListener('submit', handleFormSubmit);
}

function updateCategoryDescription() {
    const description = CATEGORY_DESCRIPTIONS[categorySelect.value];
    if (description) {
        categoryId.textContent = description;
    } else {
        categoryId.textContent = '';
    }
}

function validateForm(formData) {
    const errors = {};
    
    // Category must be selected
    if (!formData.category) {
        errors.category = 'Veuillez sélectionner une catégorie';
    }
    
    // Instruction validation
    if (!formData.instruction || formData.instruction.trim().length < 10) {
        errors.instruction = 'L\'instruction doit contenir au moins 10 caractères';
    }
    
    if (formData.instruction && formData.instruction.trim().length > 2000) {
        errors.instruction = 'L\'instruction ne peut pas dépasser 2000 caractères';
    }
    
    // Chosen validation
    if (!formData.chosen || formData.chosen.trim().length < 20) {
        errors.chosen = 'La réponse choisie doit contenir au moins 20 caractères';
    }
    
    if (formData.chosen && formData.chosen.trim().length > 5000) {
        errors.chosen = 'La réponse choisie ne peut pas dépasser 5000 caractères';
    }
    
    // Rejected validation
    if (!formData.rejected || formData.rejected.trim().length < 20) {
        errors.rejected = 'La réponse rejetée doit contenir au moins 20 caractères';
    }
    
    if (formData.rejected && formData.rejected.trim().length > 5000) {
        errors.rejected = 'La réponse rejetée ne peut pas dépasser 5000 caractères';
    }
    
    // Chosen and rejected must be different
    if (formData.chosen && formData.rejected && formData.chosen.trim() === formData.rejected.trim()) {
        errors.rejected = 'La réponse choisie et la réponse rejetée doivent être différentes';
    }
    
    // Tags validation (max 5)
    if (formData.tags) {
        const tags = formData.tags.split(/[, ]+/).filter(t => t.trim());
        if (tags.length > 5) {
            errors.tags = 'Maximum 5 tags autorisés';
        }
    }
    
    // Source must be selected
    if (!formData.source) {
        errors.source = 'Veuillez sélectionner une source';
    }
    
    return errors;
}

async function getCategoryId(category) {
    // Try to use the API endpoint if available
    try {
        const response = await fetch('/api/generate-id?category=' + encodeURIComponent(category));
        if (response.ok) {
            const data = await response.json();
            return data.id;
        }
    } catch (e) {
        console.log('API not available, falling back to client-side ID generation');
    }
    
    // Client-side ID generation (simplified - fetch existing, parse last number)
    try {
        const response = await fetch('/dataset/categories/' + encodeURIComponent(category) + '.json');
        if (response.ok) {
            const pairs = await response.json();
            let maxNum = 0;
            const prefix = getCategoryPrefix(category);
            
            for (const pair of pairs) {
                if (pair.id && pair.id.startsWith(prefix + '-')) {
                    const num = parseInt(pair.id.split('-')[1], 10);
                    if (!isNaN(num)) {
                        maxNum = Math.max(maxNum, num);
                    }
                }
            }
            
            return `${prefix}-${(maxNum + 1).toString().padStart(3, '0')}`;
        }
    } catch (e) {
        console.error('Error fetching category file:', e);
    }
    
    // Fallback: return a default ID
    return `${category}-001`;
}

function getCategoryPrefix(category) {
    const prefixes = {
        "genre-inclusion": "genre",
        "techno-solutionnisme": "techno",
        "vision-economique": "eco",
        "validisme-accessibilite": "valid",
        "inegalites-nord-sud": "nord-sud",
        "ecologie-sobriete": "sobr",
        "gouvernance-pouvoir-agir": "gouv",
        "diversite-parcours": "diversite"
    };
    return prefixes[category] || category;
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Clear all previous error states
    clearErrorStates();
    
    // Disable submit button
    submitBtn.disabled = true;
    submitBtn.textContent = 'Traitement en cours...';
    
    // Collect form data
    const formData = {
        category: categorySelect.value,
        instruction: document.getElementById('instruction').value,
        chosen: document.getElementById('chosen').value,
        rejected: document.getElementById('rejected').value,
        tags: document.getElementById('tags').value,
        source: document.getElementById('source').value,
        reviewer_notes: document.getElementById('reviewer-notes').value,
        date_added: new Date().toISOString().split('T')[0]
    };
    
    // Validate
    const validationErrors = validateForm(formData);
    
    if (Object.keys(validationErrors).length > 0) {
        // Display errors per field
        displayFieldErrors(validationErrors);
        submitBtn.disabled = false;
        submitBtn.textContent = 'Proposer la paire';
        return;
    }
    
    // Generate ID
    const id = await getCategoryId(formData.category);
    formData.id = id;
    
    // Process tags
    formData.tags = formData.tags.split(/[, ]+/).filter(t => t.trim()).slice(0, 5);
    
    // Show processing message
    validationMessage.textContent = 'Soumission en cours...';
    validationMessage.className = 'validation-message';
    validationMessage.style.display = 'block';
    
    try {
        // Submit to GitHub API
        const submissionResult = await submitToGitHub(formData);
        
        // Success!
        validationMessage.textContent = submissionResult.message || 'Paire soumise avec succès ! Un PR a été créé pour revue.';
        validationMessage.className = 'validation-message success';
        
        // Clear form
        form.reset();
        categoryId.textContent = '';
        
        // Show PR link if available
        if (submissionResult.prUrl) {
            const prLink = `<br><br><a href="${submissionResult.prUrl}" target="_blank">Voir le Pull Request</a>`;
            validationMessage.innerHTML += prLink;
        }
        
    } catch (error) {
        // Error
        validationMessage.textContent = error.message || 'Une erreur est survenue lors de la soumission. Veuillez réessayer.';
        validationMessage.className = 'validation-message error';
        validationMessage.style.display = 'block';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Proposer la paire';
    }
}

function clearErrorStates() {
    // Remove error states from all form groups
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach(group => {
        group.classList.remove('has-error');
        const input = group.querySelector('input, select, textarea');
        if (input) {
            input.setAttribute('aria-invalid', 'false');
        }
    });
    
    // Clear all error messages
    const errorMessages = document.querySelectorAll('.error-message[role="alert"]');
    errorMessages.forEach(el => el.textContent = '');
    
    // Clear form-level error
    const formLevelError = document.getElementById('form-level-error');
    if (formLevelError) {
        formLevelError.style.display = 'none';
        formLevelError.textContent = '';
    }
    
    // Hide validation message
    validationMessage.style.display = 'none';
}

function displayFieldErrors(errors) {
    const fieldIds = {
        category: 'category-error',
        instruction: 'instruction-error',
        chosen: 'chosen-error',
        rejected: 'rejected-error',
        tags: 'tags-error',
        source: 'source-error'
    };
    
    // Set error message for each field with an error
    for (const field in errors) {
        if (errors.hasOwnProperty(field)) {
            const errorElementId = fieldIds[field];
            if (errorElementId) {
                const errorElement = document.getElementById(errorElementId);
                if (errorElement) {
                    errorElement.textContent = errors[field];
                }
                
                // Set aria-invalid on the corresponding input
                const input = document.querySelector(`[name="${field}"]`);
                if (input) {
                    input.setAttribute('aria-invalid', 'true');
                }
                
                // Add has-error class to the form group
                const formGroup = document.querySelector(`[data-field="${field}"]`);
                if (formGroup) {
                    formGroup.classList.add('has-error');
                }
            }
        }
    }
}

async function submitToGitHub(data) {
    // This is a placeholder - in production, you would:
    // 1. Create a branch
    // 2. Add the pair to the category file
    // 3. Create a PR with the changes
    
    // For MVP, we'll show a success message
    // In production, implement the GitHub API workflow from the spec:
    
    return {
        success: true,
        id: data.id,
        prUrl: null,
        message: 'Paire soumise avec succès ! L\'ID généré est : ' + data.id + '<br><br><strong>Note:</strong> Cette démo ne crée pas réellement un PR. Pour l\'implémentation complète, configurez le service account GitHub et implémentez le workflow API.'
    };
    
    // Production implementation would:
    // - Use GitHub API to create branch `contrib/pair-{category}-{id}`
    // - Fetch and modify the category JSON file
    // - Create PR with template
    // - Return PR URL for display
}

// Expose for testing
window.validateForm = validateForm;
window.getCategoryId = getCategoryId;
