/**
 * Clase para manejar modales de previsualización de videos
 * Reutilizable para cualquier video en la aplicación
 */
class VideoPreviewModal {
    constructor() {
        this.modalId = 'videoPreviewModal';
        this.loadStyles();
        this.createModal();
        this.setupEventListeners();
    }

    loadStyles() {
        // Cargar CSS externo
        if (!document.getElementById('videoPreviewCSS')) {
            const link = document.createElement('link');
            link.id = 'videoPreviewCSS';
            link.rel = 'stylesheet';
            link.href = '/static/css/video-preview.css';
            document.head.appendChild(link);
        }
    }

    createModal() {
        // Crear modal HTML
        const modal = document.createElement('div');
        modal.id = this.modalId;
        modal.className = 'video-preview-modal';
        modal.innerHTML = `
            <div class="video-preview-overlay">
                <div class="video-preview-content">
                    <button class="video-preview-close" aria-label="Cerrar">&times;</button>
                    <video 
                        id="previewVideo"
                        class="video-preview-player"
                        controls
                        autoplay
                    ></video>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    setupEventListeners() {
        const modal = document.getElementById(this.modalId);
        const closeBtn = modal.querySelector('.video-preview-close');
        const overlay = modal.querySelector('.video-preview-overlay');

        // Cerrar con botón
        closeBtn.addEventListener('click', () => this.close());

        // Cerrar al hacer click fuera del video
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                this.close();
            }
        });

        // Cerrar con ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('active')) {
                this.close();
            }
        });
    }

    /**
     * Abre el modal con un video
     * @param {string} videoUrl - URL del video a mostrar
     * @param {string} title - Título opcional (para logging)
     */
    open(videoUrl, title = 'Video') {
        const modal = document.getElementById(this.modalId);
        const videoElement = modal.querySelector('#previewVideo');

        videoElement.src = videoUrl;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';

        console.log(`📹 Abriendo previsualización: ${title}`);
    }

    /**
     * Cierra el modal
     */
    close() {
        const modal = document.getElementById(this.modalId);
        const videoElement = modal.querySelector('#previewVideo');

        modal.classList.remove('active');
        videoElement.src = '';
        videoElement.pause();
        document.body.style.overflow = 'auto';

        console.log('🔚 Cerrada previsualización');
    }

    /**
     * Crea un botón de play para un contenedor
     * @param {HTMLElement} container - Elemento padre donde agregar el botón
     * @param {string} videoUrl - URL del video
     * @param {string} title - Título opcional
     */
    createPlayButton(container, videoUrl, title = 'Video') {
        // Asegurar que el contenedor es posicionado relativamente
        container.style.position = 'relative';
        
        const playBtn = document.createElement('button');
        playBtn.className = 'video-play-button';
        playBtn.innerHTML = '▶️';
        playBtn.setAttribute('aria-label', `Reproducir ${title}`);
        
        playBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            e.preventDefault();
            this.open(videoUrl, title);
        });

        container.appendChild(playBtn);
        return playBtn;
    }
}

// Crear instancia global y exponerla
const videoPreview = new VideoPreviewModal();
window.videoPreview = videoPreview;

console.log('✅ VideoPreviewModal inicializado');
