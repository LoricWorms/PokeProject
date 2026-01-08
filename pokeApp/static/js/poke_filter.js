document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('filter-form');
    const searchInput = document.getElementById('search-input');
    const generationSelect = document.getElementById('generation-select');

    let searchTimeout;

    // Déclenche la soumission du formulaire après un court délai lorsque l'utilisateur tape
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(function() {
            form.submit();
        }, 500); // Délai de 500ms pour éviter les soumissions trop fréquentes
    });

    // Déclenche la soumission du formulaire lorsque la génération est modifiée
    generationSelect.addEventListener('change', function() {
        form.submit();
    });
});
