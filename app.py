from flask import Flask, render_template, request, jsonify, send_from_directory
from video_generator import crear_video_campana
import os
import json

app = Flask(__name__)


def get_dashboard_context():
    """
    Carga las campañas desde las carpetas de videos-sora/
    Cada carpeta contiene un metadata.json y un video
    """
    campaigns = []
    videos_dir = "videos-sora"
    
    if os.path.exists(videos_dir):
        # Listar todas las carpetas
        for folder_name in os.listdir(videos_dir):
            folder_path = os.path.join(videos_dir, folder_name)
            if not os.path.isdir(folder_path):
                continue
            
            metadata_path = os.path.join(folder_path, "metadata.json")
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    # Buscar el archivo de video
                    video_file = metadata.get("videoFile", "")
                    video_path = os.path.join(folder_path, video_file)
                    
                    if os.path.exists(video_path):
                        # Convertir metadata a formato de campaign
                        campaign = {
                            "title": metadata.get("campaignName", folder_name),
                            "platforms": [p.capitalize() for p in metadata.get("platforms", [])],
                            "status": "Publicado" if metadata.get("published", False) else "Borrador",
                            "views": "0",  # Placeholder
                            "likes": "0",  # Placeholder
                            "videoFile": video_file,
                            "videoPath": f"videos-sora/{folder_name}/{video_file}",
                            "format": metadata.get("videoFormat", "short"),
                            "resolution": metadata.get("resolution", "720x1280"),
                            "duration": metadata.get("duration", "15") + "s"
                        }
                        campaigns.append(campaign)
                except Exception as e:
                    print(f"Error loading campaign {folder_name}: {e}")
    
    return {
        "campaigns": campaigns,
        "formats": [
            {
                "name": "TikTok (9:16)",
                "description": "Formato vertical optimizado para máxima interacción.",
                "duration": "15 segundos",
                "platform": "Red social",
            },
            {
                "name": "Reels (9:16)",
                "description": "Formato vertical para stories y reels.",
                "duration": "30 segundos",
                "platform": "Red social",
            },
        ],
    }


@app.route("/")
def dashboard():
    context = get_dashboard_context()
    return render_template("dashboard.html",  **context)


@app.route("/api/campaign/create", methods=["POST"])
def create_campaign_api():
    """Endpoint para crear campaña y generar video"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        campaign_name = data.get("campaignName", "").strip()
        if not campaign_name:
            return jsonify({
                "success": False,
                "error": "El nombre de la campaña es requerido"
            }), 400
        
        # Extraer datos del formulario
        campaign_data = {
            "campaignName": campaign_name,
            "description": data.get("description", ""),
            "videoFormat": data.get("videoFormat", "short"),
            "duration": data.get("duration", "15"),
            "resolution": data.get("resolution", "1080p"),
            "platforms": data.get("platforms", []),
            "testMode": data.get("testMode", False)
        }
        
        print(f"\n{'='*60}")
        print(f"🎬 Creando campaña: {campaign_name}")
        print(f"{'='*60}")
        
        # Generar video usando el módulo
        result = crear_video_campana(campaign_data);
        
        if not result["success"]:
            return jsonify({
                "success": False,
                "error": result.get("error", "Error desconocido")
            }), 500
        
        print(f"{'='*60}")
        print(f"✅ Campaña creada exitosamente!")
        print(f"{'='*60}\n")
        
        return jsonify({
            "success": True,
            "message": "Campaña creada exitosamente",
            "data": {
                "campaignName": campaign_name,
                "videoId": result["video_id"],
                "videoUrl": result["video_url"],
                "filename": result["filename"],
                "duration": campaign_data["duration"],
                "resolution": campaign_data["resolution"],
                "platforms": campaign_data["platforms"]
            }
        })
        
    except Exception as e:
        print(f"❌ Error al crear campaña: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/videos-sora/<path:filepath>")
def serve_video(filepath):
    """
    Sirve videos desde la carpeta videos-sora/
    filepath será algo como: campaign_name_xyz/campaign_name_xyz.mp4
    """
    videos_dir = os.path.join(os.getcwd(), "videos-sora")
    return send_from_directory(videos_dir, filepath)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
