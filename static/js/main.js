document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.querySelector('.mobile-menu');
    const sidebar = document.querySelector('.sidebar');

    menuButton?.addEventListener('click', () => {
        sidebar?.classList.toggle('open');
    });

    document.querySelectorAll('.pill.selectable').forEach(btn => {
        btn.addEventListener('click', () => {
            const group = btn.parentElement;
            group?.querySelectorAll('.pill.selectable').forEach(el => el.classList.remove('active'));
            btn.classList.add('active');
        });
    });
});
