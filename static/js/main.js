document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.querySelector('.mobile-menu');
    const sidebar = document.querySelector('.sidebar');

    menuButton?.addEventListener('click', () => {
        sidebar?.classList.toggle('open');
    });

    // Cargar saldo de OpenAI
    loadOpenAIBalance();

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
    let selectedDuration = '15';
    const customDurationInput = document.getElementById('customDurationInput');
    const customSecondsField = document.getElementById('customSeconds');
    
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
            if (title) {
                title.style.color = '#7C3AED';
            }
            
            // Manejar botón Custom
            const duration = btn.getAttribute('data-duration');
            if (duration === 'custom') {
                customDurationInput.style.display = 'block';
                selectedDuration = customSecondsField.value || '15';
                // Focus en el input
                setTimeout(() => customSecondsField.focus(), 100);
            } else {
                customDurationInput.style.display = 'none';
                selectedDuration = duration;
            }
        });
    });
    
    // Actualizar duración cuando cambia el input custom
    if (customSecondsField) {
        customSecondsField.addEventListener('input', (e) => {
            let value = parseInt(e.target.value);
            if (value < 4) value = 4;
            if (value > 60) value = 60;
            selectedDuration = value.toString();
        });
    }

    // Video Resolution Selection
    const resolutionButtons = document.querySelectorAll('.resolution-btn');
    let selectedResolution = '720x1280'; // Valor por defecto
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
            if (title) {
                title.style.color = '#7C3AED';
            }
            // Usar data-resolution en lugar de textContent
            selectedResolution = btn.getAttribute('data-resolution') || '720x1280';
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

// Create Campaign Function
async function createCampaign() {
    const campaignName = document.getElementById('campaignName')?.value || '';
    const description = document.getElementById('campaignDescription')?.value || '';
    
    if (!campaignName.trim()) {
        alert('Por favor ingresa un nombre para la campaña');
        return;
    }
    
    // Get selected video format
    const videoFormatRadio = document.querySelector('input[name="videoFormat"]:checked');
    const videoFormat = videoFormatRadio?.parentElement.querySelector('.option-title')?.textContent.includes('Short') ? 'short' : 'long';
    
    // Get selected duration
    let duration;
    const customDurationInputDiv = document.getElementById('customDurationInput');
    const isCustomVisible = customDurationInputDiv && customDurationInputDiv.style.display !== 'none';
    
    if (isCustomVisible) {
        // Si el input custom está visible, usar ese valor
        const customSecondsInput = document.getElementById('customSeconds');
        const customSeconds = customSecondsInput?.value;
        
        if (!customSeconds || customSeconds.trim() === '') {
            alert('Por favor ingresa una duración personalizada');
            customSecondsInput?.focus();
            return;
        }
        
        duration = customSeconds;
        // Validar rango
        const durationNum = parseInt(duration);
        if (isNaN(durationNum) || durationNum < 4 || durationNum > 60) {
            alert('La duración personalizada debe estar entre 4 y 60 segundos');
            customSecondsInput?.focus();
            return;
        }
    } else {
        // Usar el botón seleccionado
        const durationBtn = document.querySelector('.duration-btn[style*="7C3AED"]');
        const dataDuration = durationBtn?.getAttribute('data-duration');
        duration = dataDuration || '15';
    }
    
    // Get selected resolution
    const resolutionBtn = document.querySelector('.resolution-btn[style*="7C3AED"]');
    const resolution = resolutionBtn?.getAttribute('data-resolution') || '720x1280';
    
    // Get selected platforms
    const platforms = [];
    document.querySelectorAll('#campaignModal input[type="checkbox"]:checked').forEach(checkbox => {
        const platformLabel = checkbox.parentElement.querySelector('strong')?.textContent;
        if (platformLabel) {
            platforms.push(platformLabel.toLowerCase());
        }
    });
    
    // Get test mode
    const testMode = document.getElementById('testMode')?.checked || false;
    
    // Show loading state
    const createBtn = event.target;
    const originalText = createBtn.textContent;
    createBtn.disabled = true;
    createBtn.textContent = 'Generando video...';
    createBtn.style.opacity = '0.6';
    
    // Preparar datos para enviar
    const requestData = {
        campaignName,
        description,
        videoFormat,
        duration,
        resolution,
        platforms,
        testMode
    };
    
    // Pintar en consola lo que se envía al backend
    console.log('='.repeat(60));
    console.log('📤 ENVIANDO DATOS AL BACKEND:');
    console.log('='.repeat(60));
    console.log('Campaign Name:', requestData.campaignName);
    console.log('Description:', requestData.description);
    console.log('Video Format:', requestData.videoFormat);
    console.log('Duration:', requestData.duration, 'seconds');
    console.log('Resolution:', requestData.resolution);
    console.log('Platforms:', requestData.platforms);
    console.log('Test Mode:', requestData.testMode ? '✅ ENABLED (using local video)' : '❌ Disabled (generating new)');
    console.log('='.repeat(60));
    console.log('JSON completo:', JSON.stringify(requestData, null, 2));
    console.log('='.repeat(60));
    
    try {
        const response = await fetch('/api/campaign/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Cerrar modal de creación
            closeCampaignModal();
            
            // Mostrar popup de previsualización
            showPreviewPopup(result.data);
        } else {
            alert(`Error al crear campaña: ${result.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert(`Error al crear campaña: ${error.message}`);
    } finally {
        createBtn.disabled = false;
        createBtn.textContent = originalText;
        createBtn.style.opacity = '1';
    }
}

// Popup de previsualización del video con marco y botones
function showPreviewPopup(videoData) {
    // Guardar datos del video para publicar después
    window.pendingVideoData = videoData;
    
    // Crear popup si no existe
    let popup = document.getElementById('publishPreviewPopup');
    if (!popup) {
        popup = document.createElement('div');
        popup.id = 'publishPreviewPopup';
        popup.innerHTML = `
            <div class="publish-preview-overlay" onclick="cancelPublish()"></div>
            <div class="publish-preview-container">
                <button class="publish-preview-close" onclick="cancelPublish()">&times;</button>
                <h2 class="publish-preview-title">📺 Previsualización del Video</h2>
                <p class="publish-preview-subtitle" id="previewCampaignName"></p>
                <div class="publish-preview-video-wrapper">
                    <video id="publishPreviewVideo" controls autoplay>
                        Tu navegador no soporta video HTML5.
                    </video>
                </div>
                <div class="publish-preview-info">
                    <span id="previewDuration"></span>
                    <span id="previewResolution"></span>
                    <span id="previewFormat"></span>
                </div>
                <div class="publish-preview-actions">
                    <button class="btn-cancel" onclick="cancelPublish()">
                        ❌ Cancelar
                    </button>
                    <button class="btn-publish" id="publishBtn" onclick="confirmPublish()">
                        🚀 Publicar
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(popup);
        addPublishPreviewStyles();
    }
    
    // Rellenar datos
    document.getElementById('previewCampaignName').textContent = videoData.campaignName;
    document.getElementById('previewDuration').textContent = `⏱️ ${videoData.duration}s`;
    document.getElementById('previewResolution').textContent = `📐 ${videoData.resolution}`;
    document.getElementById('previewFormat').textContent = `📹 ${videoData.videoFormat === 'long' ? 'Largo' : 'Corto'}`;
    
    // Configurar video
    const video = document.getElementById('publishPreviewVideo');
    video.src = videoData.localPreviewUrl || videoData.videoUrl;
    video.load();
    
    // Mostrar popup
    popup.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function cancelPublish() {
    const popup = document.getElementById('publishPreviewPopup');
    if (popup) {
        popup.classList.remove('active');
        document.body.style.overflow = 'auto';
        
        // Pausar video
        const video = document.getElementById('publishPreviewVideo');
        if (video) {
            video.pause();
            video.src = '';
        }
    }
    
    // Limpiar datos pendientes
    window.pendingVideoData = null;
}

async function confirmPublish() {
    const videoData = window.pendingVideoData;
    if (!videoData) return;
    
    const publishBtn = document.getElementById('publishBtn');
    const originalText = publishBtn.innerHTML;
    
    publishBtn.disabled = true;
    publishBtn.innerHTML = '⏳ Publicando...';
    
    try {
        const response = await fetch('/api/campaign/publish', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                videoUrl: videoData.videoUrl,
                videoFormat: videoData.videoFormat,
                campaignName: videoData.campaignName
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('🎉 ¡Campaña publicada exitosamente!');
            cancelPublish();
            window.location.reload();
        } else {
            alert(`Error al publicar: ${result.error}`);
            publishBtn.disabled = false;
            publishBtn.innerHTML = originalText;
        }
    } catch (error) {
        console.error('Error:', error);
        alert(`Error al publicar: ${error.message}`);
        publishBtn.disabled = false;
        publishBtn.innerHTML = originalText;
    }
}

function addPublishPreviewStyles() {
    if (document.getElementById('publishPreviewStyles')) return;
    
    const style = document.createElement('style');
    style.id = 'publishPreviewStyles';
    style.textContent = `
        #publishPreviewPopup {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10000;
        }
        
        #publishPreviewPopup.active {
            display: block;
        }
        
        .publish-preview-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
        }
        
        .publish-preview-container {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            border-radius: 20px;
            padding: 32px;
            max-width: 700px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.4);
        }
        
        .publish-preview-close {
            position: absolute;
            top: 16px;
            right: 16px;
            background: #f0f0f0;
            border: none;
            font-size: 24px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
            color: #666;
        }
        
        .publish-preview-close:hover {
            background: #e0e0e0;
        }
        
        .publish-preview-title {
            margin: 0 0 8px 0;
            font-size: 26px;
            color: #333;
        }
        
        .publish-preview-subtitle {
            margin: 0 0 20px 0;
            color: #666;
            font-size: 16px;
        }
        
        .publish-preview-video-wrapper {
            background: #000;
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        
        #publishPreviewVideo {
            width: 100%;
            max-height: 400px;
            display: block;
            object-fit: contain;
        }
        
        .publish-preview-info {
            display: flex;
            gap: 12px;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }
        
        .publish-preview-info span {
            background: #f5f3ff;
            color: #7C3AED;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
        }
        
        .publish-preview-actions {
            display: flex;
            gap: 12px;
            justify-content: flex-end;
        }
        
        .publish-preview-actions .btn-cancel,
        .publish-preview-actions .btn-publish {
            padding: 14px 28px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            border: none;
        }
        
        .publish-preview-actions .btn-cancel {
            background: #f0f0f0;
            color: #666;
        }
        
        .publish-preview-actions .btn-cancel:hover {
            background: #e0e0e0;
        }
        
        .publish-preview-actions .btn-publish {
            background: linear-gradient(135deg, #7C3AED, #9F67FF);
            color: white;
        }
        
        .publish-preview-actions .btn-publish:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
        }
        
        .publish-preview-actions .btn-publish:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
    `;
    document.head.appendChild(style);
}

// Función para cargar el saldo de OpenAI
async function loadOpenAIBalance() {
    const balanceElement = document.getElementById('openaiBalance');
    const amountElement = document.getElementById('balanceAmount');
    
    if (!balanceElement || !amountElement) return;
    
    balanceElement.classList.add('loading');
    amountElement.textContent = '...';
    
    try {
        const response = await fetch('/api/openai/balance');
        const data = await response.json();
        
        if (data.success && data.balance !== 'N/A') {
            const balance = parseFloat(data.balance);
            amountElement.textContent = `$${balance.toFixed(2)}`;
            
            // Cambiar color según el saldo
            balanceElement.classList.remove('loading', 'low', 'critical');
            if (balance < 5) {
                balanceElement.classList.add('critical');
            } else if (balance < 20) {
                balanceElement.classList.add('low');
            }
            
            // Actualizar tooltip
            balanceElement.title = `Saldo: $${balance.toFixed(2)} | Usado: $${data.used} | Límite: $${data.limit}`;
        } else {
            amountElement.textContent = 'N/A';
            balanceElement.classList.remove('loading');
        }
    } catch (error) {
        console.error('Error al cargar saldo OpenAI:', error);
        amountElement.textContent = 'Error';
        balanceElement.classList.remove('loading');
        balanceElement.classList.add('critical');
    }
}
