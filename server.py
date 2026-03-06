from flask import Flask, request, jsonify, send_from_directory
import requests
from user_agent import generate_user_agent as zzz

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/generate", methods=["POST"])
def generate_image():

    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "prompt required"}), 400

    session = requests.Session()
    session.headers.update({
        'User-Agent': zzz(),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
        'Content-Type': 'application/json',
        'Origin': 'https://aifreeforever.com',
        'Referer': 'https://aifreeforever.com/image-generators'
    })

    url = "https://aifreeforever.com/api/generate-image"

    payload = {
        "prompt": prompt,
        "resolution": "1024 × 1024 (Square)",
        "speed_mode": "Unsqueezed 🍋 (highest quality)",
        "output_format": "webp",
        "output_quality": 100,
        "seed": -1,
        "model_type": "fast"
    }

    try:
        r = session.post(url, json=payload)
        result = r.json()

        if "images" in result:
            return jsonify({"image": result["images"][0]})

        if "imageUrl" in result:
            return jsonify({"image": result["imageUrl"]})

        return jsonify({"error": "no image returned"})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
