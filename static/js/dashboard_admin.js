document.addEventListener('DOMContentLoaded', function () {
    const chartData = document.getElementById('dashboard-data');
    if (!chartData) return;

    // User Distribution Chart
    const userCtx = document.getElementById('userDistChart').getContext('2d');
    const totalAlunos = Number(chartData.dataset.totalAlunos || 0);
    const totalProfessores = Number(chartData.dataset.totalProfessores || 0);
    const totalUsuarios = Number(chartData.dataset.totalUsuarios || 0);
    const totalAdmin = totalUsuarios - totalAlunos - totalProfessores;

    new Chart(userCtx, {
        type: 'doughnut',
        data: {
            labels: ['Alunos', 'Professores', 'Administradores'],
            datasets: [{
                data: [totalAlunos, totalProfessores, totalAdmin],
                backgroundColor: [
                    '#6366f1', // Indigo (Primary)
                    '#10b981', // Emerald (Success)
                    '#ef4444'  // Red (Error/Admin)
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8' // text-muted
                    }
                }
            }
        }
    });

    // Gender Distribution Chart
    const genderCtx = document.getElementById('genderChart').getContext('2d');
    const alunosMasc = Number(chartData.dataset.alunosMasc || 0);
    const alunosFem = Number(chartData.dataset.alunosFem || 0);

    new Chart(genderCtx, {
        type: 'pie',
        data: {
            labels: ['Masculino', 'Feminino'],
            datasets: [{
                data: [alunosMasc, alunosFem],
                backgroundColor: [
                    '#3b82f6', // Blue
                    '#ec4899'  // Pink
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8'
                    }
                }
            }
        }
    });
});
