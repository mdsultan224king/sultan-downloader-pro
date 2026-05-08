import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Sultan Downloader Server is Active! Developed by Md Sultan Shekh"

@app.route('/download', methods=['POST', 'GET'])
def download_video():
    if request.method == 'GET':
        return jsonify({"message": "Please use POST method to download"})
        
    data = request.json
    if not data:
        return jsonify({"success": False, "error": "No data received"})
        
    url = data.get('url')
    if not url:
        return jsonify({"success": False, "error": "No URL provided"})

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title')
            
            return jsonify({
                "success": True, 
                "title": title,
                "download_link": video_url,
                "developer": "Md Sultan Shekh"
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
