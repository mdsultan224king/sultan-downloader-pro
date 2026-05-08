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

        # ইউটিউব ব্লকিং এড়াতে উন্নত সেটিংস
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'no_color': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ভিডিও তথ্য সংগ্রহ
            info = ydl.extract_info(url, download=False)
            
            # সরাসরি ডাউনলোড লিঙ্ক খুঁজে বের করা
            video_url = info.get('url')
            if not video_url:
                # যদি সরাসরি লিঙ্ক না পাওয়া যায়, তবে ফরম্যাট লিস্ট থেকে দেখা
                formats = info.get('formats', [])
                for f in formats:
                    if f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                        video_url = f.get('url')
                        break

            return jsonify({
                "success": True,
                "title": info.get('title', 'Video File'),
                "download_link": video_url
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
