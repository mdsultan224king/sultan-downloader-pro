import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Sultan Pro Downloader Server is Active!"

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"success": False, "error": "URL missing"}), 400

        # ইউটিউব ব্লকিং এড়ানোর জন্য নতুন শক্তিশালী সেটিংস
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            # ইউটিউবকে মনে করাবে এটি একটি মোবাইল অ্যাপ থেকে রিকোয়েস্ট আসছে
            'youtube_include_dash_manifest': False,
            'http_headers': {
                'User-Agent': 'com.google.android.youtube/19.11.38 (Linux; U; Android 14; en_US; Pixel 8 Pro) gzip',
            }
        }
        
        # আপনার আপলোড করা cookies.txt ফাইলটি যদি থেকে থাকে তবে এটি যোগ করুন
        if os.path.exists('cookies.txt'):
            ydl_opts['cookiefile'] = 'cookies.txt'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            
            if not video_url:
                formats = info.get('formats', [])
                for f in reversed(formats):
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        video_url = f.get('url')
                        break

            if not video_url:
                return jsonify({"success": False, "error": "ভিডিও লিঙ্ক পাওয়া যায়নি।"}), 404

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
