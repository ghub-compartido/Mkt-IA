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

    // Video Format Selection
    const videoFormatOptions = document.querySelectorAll('.video-format-option');
    videoFormatOptions.forEach(label => {
        const radio = label.querySelector('input[type="radio"]');
        const badges = label.querySelectorAll('.badge');
        
        // Set initial state
        if (radio && radio.checked) {
            label.style.border = '2px solid #7C3AED';
            label.style.background = '#F5F3FF';
            badges.forEach(badge => {
                badge.style.background = 'white';
            });
        }
        
        radio?.addEventListener('change', () => {
            videoFormatOptions.forEach(opt => {
                const optBadges = opt.querySelectorAll('.badge');
                opt.style.border = '2px solid #E0E0E0';
                opt.style.background = 'white';
                optBadges.forEach(badge => {
                    badge.style.background = '#F5F5F5';
                });
            });
            
            if (radio.checked) {
                label.style.border = '2px solid #7C3AED';
                label.style.background = '#F5F3FF';
                badges.forEach(badge => {
                    badge.style.background = 'white';
                });
            }
        });
    });

    // Video Duration Selection
    const durationButtons = document.querySelectorAll('.duration-btn');
    durationButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            durationButtons.forEach(b => {
                b.style.border = '2px solid #E0E0E0';
                b.style.background = 'white';
                const title = b.querySelector('.duration-title');
                if (title) title.style.color = '#333';
            });
            btn.style.border = '2px solid #7C3AED';
            btn.style.background = '#F5F3FF';
            const title = btn.querySelector('.duration-title');
            if (title) title.style.color = '#7C3AED';
        });
    });

    // Video Resolution Selection
    const resolutionButtons = document.querySelectorAll('.resolution-btn');
    resolutionButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            resolutionButtons.forEach(b => {
                b.style.border = '2px solid #E0E0E0';
                b.style.background = 'white';
                const title = b.querySelector('.resolution-title');
                if (title) title.style.color = '#333';
            });
            btn.style.border = '2px solid #7C3AED';
            btn.style.background = '#F5F3FF';
            const title = btn.querySelector('.resolution-title');
            if (title) title.style.color = '#7C3AED';
        });
    });
});

// Modal Functions
function openCampaignModal() {
    const modal = document.getElementById('campaignModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeCampaignModal() {
    const modal = document.getElementById('campaignModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    const modal = document.getElementById('campaignModal');
    if (e.target === modal) {
        closeCampaignModal();
    }
});
