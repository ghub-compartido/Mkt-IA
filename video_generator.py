"""
Módulo para generar videos con Sora AI y subirlos a GitHub
Utiliza las funciones de sora/generar.py
"""
import os
import sys
import requests
import time
from tiktok_configure.aws_uploder import uoploader_aws


# Agregar el directorio sora al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'sora'))

# Intentar importar las funciones de generación de sora/generar.py
try:
    import generar
    generar_video_sora = generar.generar_video_sora
    descargar_video = generar.descargar_video
    subir_a_github = generar.subir_a_github
    SORA_AVAILABLE = True
except ImportError as e:
    SORA_AVAILABLE = False
    print(f"Warning: Módulo de generación Sora no disponible - {e}")


def crear_video_campana(campaign_data: dict) -> dict:
    """
    Crea un video para una campaña usando Sora AI
    
    Args:
        campaign_data: Diccionario con datos de la campaña
            - campaignName: Nombre de la campaña
            - description: Descripción del video
            - videoFormat: 'short' o 'long'
            - duration: Duración en segundos (string)
            - resolution: '720p', '1080p' o '4k'
            - platforms: Lista de plataformas
    
    Returns:
        dict con:
            - success: bool
            - video_url: URL del video en GitHub
            - video_id: ID del video de Sora
            - error: mensaje de error si falló
    """
    if not SORA_AVAILABLE:
        return {
            "success": False,
            "error": "Módulo de generación Sora no está disponible"
        }
    
    try:
        campaign_name = campaign_data.get("campaignName", "campaign")
        description = campaign_data.get("description", "")
        video_format = campaign_data.get("videoFormat", "short")
        resolution = campaign_data.get("resolution", "1080p")
        duration_str = campaign_data.get("duration", "15")
        test_mode = campaign_data.get("testMode", False)
        
        # MODO PRUEBA: Usar primer video existente
        if test_mode:
            import json
            import shutil
            from datetime import datetime
            
            print("🧪 MODO PRUEBA ACTIVADO - Copiando video existente")
            videos_dir = "videos-sora"
            if not os.path.exists(videos_dir):
                return {
                    "success": False,
                    "error": "No existe la carpeta videos-sora/"
                }
            
            # Buscar primera carpeta de campaña
            folders = [f for f in os.listdir(videos_dir) if os.path.isdir(os.path.join(videos_dir, f))]
            if not folders:
                return {
                    "success": False,
                    "error": "No hay campañas en videos-sora/"
                }
            
            first_folder = folders[0]
            source_folder_path = os.path.join(videos_dir, first_folder)
            
            # Leer metadata del video original
            metadata_path = os.path.join(source_folder_path, "metadata.json")
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    source_metadata = json.load(f)
                source_video = source_metadata.get("videoFile", "")
            else:
                # Buscar primer .mp4 en la carpeta
                videos = [f for f in os.listdir(source_folder_path) if f.endswith('.mp4')]
                if not videos:
                    return {
                        "success": False,
                        "error": f"No hay videos en {first_folder}"
                    }
                source_video = videos[0]
            
            source_video_path = os.path.join(source_folder_path, source_video)
            
            # Crear nueva carpeta para la campaña de prueba
            test_campaign_id = f"test_{int(datetime.now().timestamp())}"
            new_folder_name = f"{campaign_name.replace(' ', '_').lower()}_{test_campaign_id}"
            new_folder_path = os.path.join(videos_dir, new_folder_name)
            os.makedirs(new_folder_path, exist_ok=True)
            
            # Copiar video a la nueva carpeta
            new_video_filename = f"{campaign_name.replace(' ', '_').lower()}_{test_campaign_id}.mp4"
            new_video_path = os.path.join(new_folder_path, new_video_filename)
            shutil.copy2(source_video_path, new_video_path)
            print(f"📋 Video copiado: {source_video} -> {new_video_filename}")
            
            # Crear metadata.json para la nueva campaña
            new_metadata = {
                "campaignName": campaign_name,
                "description": description,
                "platforms": campaign_data.get("platforms", []),
                "videoFormat": video_format,
                "resolution": resolution,
                "duration": duration_str,
                "published": False,
                "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "videoFile": new_video_filename,
                "videoId": test_campaign_id,
                "testMode": True,
                "sourceVideo": source_video
            }
            
            new_metadata_path = os.path.join(new_folder_path, "metadata.json")
            with open(new_metadata_path, 'w', encoding='utf-8') as f:
                json.dump(new_metadata, f, indent=2, ensure_ascii=False)
            
            print(f"📝 Metadata guardada en: {new_metadata_path}")
            
            # Subir a AWS PRIMERO
            repo_path = f"videos-sora/{new_folder_name}/{new_video_filename}"
            print(f"☁️  Subiendo video de prueba a AWS: {repo_path}")
            try:
                # video_url = subir_a_github(new_video_path, repo_path)
                video_url = uoploader_aws(new_video_path)
            except Exception as e:
                # Si ya existe en GitHub, construir la URL manualmente
                # video_url = f"https://raw.githubusercontent.com/{os.getenv('GITHUB_OWNER')}/{os.getenv('GITHUB_REPO')}/{os.getenv('GITHUB_BRANCH', 'main')}/{repo_path}"
                print(f"⚠️  Video probablemente ya existe en GitHub, usando URL: {video_url}")
            
            print(f"💾 Video de prueba guardado en: {video_url}")
            print(f"✅ Modo prueba completado - Nueva campaña creada: {new_folder_name}")
            print(f"⏸️  Esperando previsualización del usuario antes de publicar...")
            
            # Ruta local para previsualización (relativa a videos-sora)
            local_preview_path = f"videos-sora/{new_folder_name}/{new_video_filename}"
            
            # NO enviar a Mulesoft automáticamente - esperar confirmación del usuario
            return {
                "success": True,
                "video_url": video_url,
                "video_id": test_campaign_id,
                "filename": new_video_filename,
                "test_mode": True,
                "campaign_folder": new_folder_path,
                "video_format": video_format,
                "awaiting_approval": True,
                "local_preview_path": local_preview_path
            }
        
        # Convertir duración a entero
        try:
            duration = int(duration_str)
        except (ValueError, TypeError):
            duration = 15
        
        # Limitar duración según restricciones de Sora
        duration = min(max(duration, 4), 60)
        
        # Mapear resolución a tamaño
        size_map = {
            "720p": "1280x720" if video_format == "long" else "720x1280",
            "720x1280": "720x1280",  # Vertical HD
            "1080p": "1920x1080" if video_format == "long" else "1080x1920",
            "4k": "3840x2160" if video_format == "long" else "2160x3840"
        }
        
        size = size_map.get(resolution, "720x1280")
        
        # Crear prompt para Sora
        if description.strip():
            prompt = description
        else:
            prompt = f"Professional promotional video for {campaign_name}. Engaging and high-quality content for social media marketing."
        
        # Generar video
        print(f"🎬 Generando video con Sora...")
        print(f"   Prompt: {prompt[:80]}...")
        print(f"   Duración: {duration}s, Tamaño: {size}")
        
        video_id = generar_video_sora(
            prompt=prompt,
            seconds=duration,
            size=size,
            model="sora-2"
        )
        
        # Descargar video
        import json
        from datetime import datetime
        
        filename = f"{campaign_name.replace(' ', '_').lower()}_{video_id[:8]}.mp4"
        campaign_folder = os.path.join("videos-sora", campaign_name.replace(' ', '_').lower() + "_" + video_id[:8])
        
        # Crear carpeta de campaña
        os.makedirs(campaign_folder, exist_ok=True)
        
        local_filename = os.path.join(campaign_folder, filename)
        
        print(f"📥 Descargando video: {local_filename}")
        local_path = descargar_video(video_id, local_filename)
        
        # Crear metadata.json
        metadata = {
            "campaignName": campaign_name,
            "description": description,
            "platforms": campaign_data.get("platforms", []),
            "videoFormat": video_format,
            "resolution": resolution,
            "duration": str(duration),
            "published": False,
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "videoFile": filename,
            "videoId": video_id
        }
        
        metadata_path = os.path.join(campaign_folder, "metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"📝 Metadata guardada en: {metadata_path}")
        
        # Subir a GitHub
        repo_path = f"videos-sora/{os.path.basename(campaign_folder)}/{filename}"
        print(f"☁️  Subiendo a AWS: {repo_path}")
        # video_url = subir_a_github(local_path, repo_path)
        video_url = uoploader_aws(local_path)
        
        # NO eliminar archivo local - mantenerlo en videos-sora
        print(f"💾 Video guardado localmente en: {local_path}")
        print(f"✅ Video generado exitosamente!")
        print(f"⏸️  Esperando previsualización del usuario antes de publicar...")
        
        # Ruta local para previsualización
        local_preview_path = f"videos-sora/{os.path.basename(campaign_folder)}/{filename}"
        
        # NO enviar a Mulesoft automáticamente - esperar confirmación del usuario
        return {
            "success": True,
            "video_url": video_url,
            "video_id": video_id,
            "filename": filename,
            "campaign_folder": campaign_folder,
            "video_format": video_format,
            "awaiting_approval": True,
            "local_preview_path": local_preview_path
        }
        
    except Exception as e:
        print(f"❌ Error al generar video: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
