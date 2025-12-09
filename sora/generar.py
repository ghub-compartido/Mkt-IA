import os
import time
import base64
import pathlib
import requests
import webbrowser
from dotenv import load_dotenv
from openai import OpenAI

# Cargar .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GHUB_TOKENv2")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")

if not OPENAI_API_KEY:
    raise ValueError("Falta OPENAI_API_KEY en .env")
if not all([GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO]):
    raise ValueError("Faltan variables de GitHub en .env")

client = OpenAI(api_key=OPENAI_API_KEY)


def generar_video_sora(prompt: str, seconds: int = 8, size: str = "1280x720", model: str = "sora-2") -> str:
    """
    Crea un job de vídeo con Sora y espera a que termine.
    Devuelve el ID del vídeo.
    """
    video = client.videos.create(
        model=model,
        prompt=prompt,
        seconds=str(seconds),
        size=size,
    )
    video_id = video.id
    print(f"Job creado: {video_id}, estado inicial: {video.status}")

    while video.status not in ("completed", "failed", "cancelled"):
        time.sleep(5)
        video = client.videos.retrieve(video_id)
        print(f"Estado: {video.status}, progreso: {video.progress}")

    if video.status != "completed":
        raise RuntimeError(f"El vídeo falló: {video.status}, error: {video.error}")

    print("Vídeo generado correctamente.")
    return video_id


def descargar_video(video_id: str, filename: str = "video_sora.mp4") -> pathlib.Path:
    """
    Descarga el vídeo de Sora y lo guarda localmente.
    """
    response = client.videos.download_content(video_id=video_id)
    content = response.read()

    path = pathlib.Path(filename).absolute()
    with open(path, "wb") as f:
        f.write(content)

    print(f"Vídeo guardado en: {path}")
    return path


def subir_a_github(path: pathlib.Path, repo_path: str) -> str:
    """
    Sube el archivo a GitHub usando la API de contenidos.
    repo_path: ruta dentro del repo (por ejemplo 'videos/video_sora.mp4')
    Devuelve la URL raw pública.
    """
    with open(path, "rb") as f:
        file_bytes = f.read()

    if len(file_bytes) > 100 * 1024 * 1024:
        raise ValueError("El archivo supera los 100 MB, GitHub no lo acepta sin LFS.")

    content_b64 = base64.b64encode(file_bytes).decode("utf-8")

    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{repo_path}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    data = {
        "message": f"Subir vídeo {repo_path}",
        "content": content_b64,
        "branch": GITHUB_BRANCH,
    }

    print("Subiendo archivo a GitHub…")
    resp = requests.put(url, headers=headers, json=data)
    if resp.status_code not in (201, 200):
        raise RuntimeError(f"Error al subir a GitHub: {resp.status_code} {resp.text}")

    # Construir URL raw
    raw_url = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{repo_path}"
    print("Archivo subido. URL raw pública:\n", raw_url)
    return raw_url


def abrir_en_navegador(url: str):
    print("Abriendo URL en el navegador…")
    webbrowser.open(url)


def main():
    prompt = "un plano aéreo de una ciudad futurista con luces de neón, estilo tráiler de película"
    local_filename = "sora_github_demo.mp4"
    repo_path = f"videos-sora/{local_filename}"  # carpeta 'videos' dentro del repo

    # # 1) Generar video con Sora
    # video_id = generar_video_sora(prompt, seconds=4, size="720x1280", model="sora-2")

    # # 2) Descargarlo localmente
    # path = descargar_video(video_id, local_filename)

    # 3) Subirlo a GitHub y obtener URL raw
    raw_url = subir_a_github('sora_github_demo.mp4', repo_path)

    # 4) Opcional: abrirlo en navegador
    abrir_en_navegador(raw_url)

    print("\n✅ Proceso completado.")
    print("URL pública HTTPS del vídeo:")
    print(raw_url)


if __name__ == "__main__":
    main()
