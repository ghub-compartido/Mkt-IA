from flask import Flask, render_template

app = Flask(__name__)


def get_dashboard_context():
    campaigns = [
        {
            "title": "Promoción Verano 2024",
            "platforms": ["TikTok", "YouTube"],
            "status": "Publicado",
            "views": "1.2M",
            "likes": "210K",
        },
        {
            "title": "Black Friday Special",
            "platforms": ["Instagram", "TikTok"],
            "status": "En revisión",
            "views": "920K",
            "likes": "180K",
        },
        {
            "title": "Lanzamiento Producto",
            "platforms": ["TikTok", "YouTube"],
            "status": "Borrador",
            "views": "220K",
            "likes": "45K",
        },
    ]
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
    return render_template("dashboard.html", **context)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
