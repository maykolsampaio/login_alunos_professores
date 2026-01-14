function toggleFields() {
    const tipo = document.getElementById('tipo').value;
    const professorFields = document.getElementById('professor-fields');
    const alunoFields = document.getElementById('aluno-fields');

    if (professorFields) {
        professorFields.style.display = (tipo === 'professor') ? 'block' : 'none';
        const areaInput = document.getElementById('area');
        if (areaInput) areaInput.required = (tipo === 'professor');
    }

    if (alunoFields) {
        alunoFields.style.display = (tipo === 'aluno') ? 'block' : 'none';
    }
}

// Execute on load to set initial state
document.addEventListener('DOMContentLoaded', toggleFields);
