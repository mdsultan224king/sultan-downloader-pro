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

        # ইউটিউবের নতুন সিকিউরিটি এড়াতে শক্তিশালী সেটিংস
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'no_color': True,
            # এটি ইউটিউবকে আসল ব্রাউজার হিসেবে বোঝাবে
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ভিডিওর আসল তথ্য বের করা
            info = ydl.extract_info(url, download=False)
            
            # সরাসরি ডাউনলোড লিঙ্কটি খুঁজে বের করা
            video_url = info.get('url')
            if not video_url:
                formats = info.get('formats', [])
                for f in reversed(formats): # সবচেয়ে ভালো কোয়ালিটি আগে দেখার জন্য
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        video_url = f.get('url')
                        break

            return jsonify({
                "success": True,
                "title": info.get('title', 'Sultan Downloader Video'),
                "download_link": video_url
            })

    except Exception as e:
        # এরর মেসেজ যাতে ব্লগে স্পষ্ট দেখা যায়
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
