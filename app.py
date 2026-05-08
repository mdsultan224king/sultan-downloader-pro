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
            return jsonify({"success": False, "error": "URL missing"}), 400

        # ইউটিউব ব্লকিং এড়ানোর জন্য প্রো-লেভেল সেটিংস
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            # ইউটিউবকে আসল ব্রাউজার হিসেবে দেখানোর জন্য নিচের অংশটি জরুরি
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ভিডিওর ডাটা বের করা
            try:
                info = ydl.extract_info(url, download=False)
            except Exception as e:
                # যদি ইউটিউব ব্লক করে, তবে অন্য একটি পদ্ধতিতে চেষ্টা করা
                return jsonify({"success": False, "error": "YouTube blocked this request. Try again later."}), 403
            
            video_url = info.get('url')
            
            # যদি সরাসরি লিঙ্ক না পাওয়া যায় তবে ফরম্যাট চেক করা
            if not video_url:
                formats = info.get('formats', [])
                for f in reversed(formats):
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        video_url = f.get('url')
                        break

            if not video_url:
                return jsonify({"success": False, "error": "Link extraction failed."}), 404

            return jsonify({
                "success": True,
                "title": info.get('title', 'Sultan Video'),
                "download_link": video_url
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
