from flask import Flask, render_template, request, jsonify, send_from_directory
from video_generator import crear_video_campana
import os
import json
import requests

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
            "message": "Campaña creada - pendiente de aprobación",
            "awaiting_approval": result.get("awaiting_approval", True),
            "data": {
                "campaignName": campaign_name,
                "videoId": result["video_id"],
                "videoUrl": result["video_url"],
                "localPreviewUrl": "/" + result.get("local_preview_path", "").replace("\\", "/"),
                "filename": result["filename"],
                "duration": campaign_data["duration"],
                "resolution": campaign_data["resolution"],
                "platforms": campaign_data["platforms"],
                "videoFormat": result.get("video_format", campaign_data["videoFormat"])
            }
        })
        
    except Exception as e:
        print(f"❌ Error al crear campaña: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/campaign/publish", methods=["POST"])
def publish_campaign_api():
    """Endpoint para publicar campaña a Mulesoft después de aprobación"""
    try:
        data = request.get_json()
        
        video_url = data.get("videoUrl", "")
        video_format = data.get("videoFormat", "short")
        campaign_name = data.get("campaignName", "")
        platforms = data.get("platforms", [])
        
        if not video_url:
            return jsonify({
                "success": False,
                "error": "URL del video es requerida"
            }), 400
        
        print(f"\n{'='*60}")
        print(f"📤 Publicando campaña: {campaign_name}")
        print(f"📱 Plataformas: {platforms}")
        print(f"{'='*60}")
        
        # Construir URL de Mulesoft
        mulesoft_url = f"https://instagramreels-i6qmxs.cgxe76.usa-e2.cloudhub.io/api/data?url={video_url}"
        
        # Añadir formato de media
        if video_format == "long":
            mulesoft_url += "&media=REELS"
        else:
            mulesoft_url += "&media=STORIES"
        
        # Añadir plataforma: tiktok, insta, o all
        platforms_lower = [p.lower() for p in platforms]
        has_instagram = "instagram" in platforms_lower
        has_tiktok = "tiktok" in platforms_lower
        
        if has_instagram and has_tiktok:
            mulesoft_url += "&platform=all"
        elif has_tiktok:
            mulesoft_url += "&platform=tiktok"
        elif has_instagram:
            mulesoft_url += "&platform=insta"
        else:
            mulesoft_url += "&platform=all"  # Por defecto si no hay ninguna
        
        print(f"📤 Enviando petición POST a Mulesoft:")
        print(f"   URL: {mulesoft_url}")
        
        response = requests.post(mulesoft_url)
        print(f"✅ Status code: {response.status_code}")
        print(f"📩 Respuesta: {response.text}")
        
        print(f"{'='*60}")
        print(f"✅ Campaña publicada exitosamente!")
        print(f"{'='*60}\n")
        
        return jsonify({
            "success": True,
            "message": "Campaña publicada exitosamente",
            "mulesoft_status": response.status_code,
            "mulesoft_response": response.text
        })
        
    except Exception as e:
        print(f"❌ Error al publicar campaña: {str(e)}")
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


@app.route("/api/openai/balance")
def get_openai_balance():
    """
    Obtiene el saldo/créditos disponibles de OpenAI
    Nota: OpenAI no tiene un endpoint directo para saldo, 
    usamos el billing dashboard API
    """
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return jsonify({
                "success": False,
                "error": "OPENAI_API_KEY no configurada"
            }), 400
        
        # Obtener información de la organización y uso
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Obtener límites de uso (subscription)
        response = requests.get(
            "https://api.openai.com/v1/dashboard/billing/subscription",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            hard_limit = data.get("hard_limit_usd", 0)
            
            # Obtener uso del mes actual
            from datetime import datetime, timedelta
            today = datetime.now()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = (today + timedelta(days=1)).strftime("%Y-%m-%d")
            
            usage_response = requests.get(
                f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}",
                headers=headers
            )
            
            if usage_response.status_code == 200:
                usage_data = usage_response.json()
                total_usage = usage_data.get("total_usage", 0) / 100  # Convertir centavos a dólares
                remaining = hard_limit - total_usage
                
                return jsonify({
                    "success": True,
                    "balance": round(remaining, 2),
                    "used": round(total_usage, 2),
                    "limit": hard_limit
                })
        
        # Si falla, intentar con el endpoint de modelos como fallback
        return jsonify({
            "success": True,
            "balance": "N/A",
            "message": "No se pudo obtener el saldo exacto"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
