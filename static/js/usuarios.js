function toggleSection(type) {
    // Remove active class from all cards and sections
    document.querySelectorAll('.category-card').forEach(card => card.classList.remove('active'));
    document.querySelectorAll('.user-list-section').forEach(sec => sec.classList.remove('active'));

    // Add active class to selected
    document.getElementById('card-' + type).classList.add('active');
    document.getElementById('section-' + type).classList.add('active');
}

// Initialize with Alunos visible
document.addEventListener('DOMContentLoaded', () => {
    toggleSection('alunos');
});
