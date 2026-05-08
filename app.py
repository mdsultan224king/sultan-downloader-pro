import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Sultan Downloader Server is Active! Developed by Md Sultan Shekh"

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"success": False, "error": "No URL provided"}), 400

        # ইউটিউব ব্লকিং এড়াতে শক্তিশালী সেটিংস
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ভিডিও তথ্য সংগ্রহ
            info = ydl.extract_info(url, download=False)
            
            # সরাসরি ডাউনলোড লিঙ্ক খুঁজে বের করা
            video_url = info.get('url')
            if not video_url:
                formats = info.get('formats', [])
                for f in reversed(formats):
                    if f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                        video_url = f.get('url')
                        break

            if not video_url:
                return jsonify({"success": False, "error": "Could not extract direct link."}), 404

            return jsonify({
                "success": True,
                "title": info.get('title', 'Sultan Video'),
                "download_link": video_url
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    # Render এর জন্য পোর্টের সঠিক কনফিগারেশন
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
