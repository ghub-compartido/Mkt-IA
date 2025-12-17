import requests

ACCESS_TOKEN = "act.1I6EOYgQjm1g0u1A41eTWiMYMVaAfgtkWFo2IDCLINSiRh48LMcVFfgscvOX!4856.e1"

r = requests.post(
    "https://open.tiktokapis.com/v2/post/publish/creator_info/query/",
    headers={
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json; charset=UTF-8",
    },
    json={}
)

print(r.status_code)
print(r.text)
