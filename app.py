import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app) # এটি আপনার ব্লগার সাইট থেকে সার্ভারে রিকোয়েস্ট পাঠাতে সাহায্য করবে

@app.route('/')
def home():
    return "Sultan Downloader Server is Active! Developed by Md Sultan Shekh"

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"success": False, "error": "No URL provided"})

    # ডাউনলোড অপশন: শুধু লিঙ্ক বের করার জন্য
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ভিডিওর ইনফরমেশন বের করা (ডাউনলোড না করেই)
            info = ydl.extract_info(url, download=False)
            
            # সরাসরি ডাউনলোড লিঙ্ক
            video_url = info.get('url')
            title = info.get('title')
            
            return jsonify({
                "success": True, 
                "title": title,
                "download_link": video_url,
                "audio_link": video_url, # বেস্ট ফরম্যাটে অডিও-ভিডিও একসাথেই থাকে
                "developer": "Md Sultan Shekh"
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    # Render বা অন্য সার্ভারের পোর্ট হ্যান্ডেল করার জন্য
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
