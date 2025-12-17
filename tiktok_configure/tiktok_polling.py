import requests
import time

ACCESS_TOKEN = "act.1I6EOYgQjm1g0u1A41eTWiMYMVaAfgtkWFo2IDCLINSiRh48LMcVFfgscvOX!4856.e1"
PUBLISH_ID = "v_pub_url~v2-1.7584543579541047318"

STATUS_URL = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json; charset=UTF-8",
}

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
