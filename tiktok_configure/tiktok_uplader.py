import requests
import time

ACCESS_TOKEN = "act.1I6EOYgQjm1g0u1A41eTWiMYMVaAfgtkWFo2IDCLINSiRh48LMcVFfgscvOX!4856.e1"
VIDEO_URL = "https://tiktokapi-vfran.s3.us-east-1.amazonaws.com/videos/sora_github_demo.mp4"

# 1) creator_info para obtener privacy_level permitido
r = requests.post(
    "https://open.tiktokapis.com/v2/post/publish/creator_info/query/",
    headers={
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json; charset=UTF-8",
    },
    json={}
)
print("creator_info:", r.status_code, r.text)

data = r.json().get("data", {})
privacy_options = data.get("privacy_level_options", [])
privacy_level = privacy_options[0] if privacy_options else "PUBLIC"  # fallback

# 2) init de publicación directa con PULL_FROM_URL
payload = {
    "post_info": {
        "title": "Video desde S3 🚀",
        "privacy_level": "SELF_ONLY"
    },
    "source": "PULL_FROM_URL",
    "video_url": VIDEO_URL
}

r = requests.post(
    "https://open.tiktokapis.com/v2/post/publish/video/init/",
    headers={
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json; charset=UTF-8",
    },
    json=payload
)

print("init:", r.status_code, r.text)
publish_id = r.json().get("data", {}).get("publish_id")

if not publish_id:
    raise SystemExit("No publish_id. Revisa el error en la respuesta de init.")

# 3) polling del estado
for i in range(60):  # hasta ~5 min si duermes 5s
    try:
        s = requests.post(
            STATUS_URL,
            headers=HEADERS,
            json={"publish_id": PUBLISH_ID},
            timeout=15,  # 👈 clave: evita cuelgues
        )
        print("status:", s.status_code, s.text)

        js = s.json()
        st = js.get("data", {}).get("status")

        if st in ("SUCCESS", "FAILED"):
            break

    except requests.exceptions.Timeout:
        print("⚠️ Timeout hablando con TikTok. Reintentando…")
    except requests.exceptions.RequestException as e:
        print("⚠️ Error de red:", e)

    time.sleep(5)
