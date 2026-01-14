function openModal(id) {
    document.getElementById(id).style.display = 'flex';
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

function handleDetailsClick(btn) {
    const nome = btn.getAttribute('data-nome');
    const ementa = btn.getAttribute('data-ementa');
    const prof_nome = btn.getAttribute('data-prof-nome');
    const prof_email = btn.getAttribute('data-prof-email');
    openDetailsModal(nome, ementa, prof_nome, prof_email);
}

function openDetailsModal(nome, ementa, prof_nome, prof_email) {
    document.getElementById('det_nome').innerText = nome;
    document.getElementById('det_ementa').innerText = ementa;
    document.getElementById('det_prof_nome').innerText = prof_nome;
    document.getElementById('det_prof_email').innerText = prof_email;
    document.getElementById('det_prof_avatar').innerText = prof_nome.charAt(0).toUpperCase();
    openModal('detailsModal');
}

// Fechar ao clicar fora
window.onclick = function (event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}
