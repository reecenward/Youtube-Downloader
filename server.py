from flask import send_from_directory
from flask import Flask, request, send_file
from pytube import YouTube
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_lowest_resolution()
    try:
        name = youtubeObject.download()
    except Exception as e:
        logging.error("Error in downloading youtube video: ", e)
    logging.info("Download completed successfully")
    return name

@app.route("/", methods=['POST'])
def handle_post():
    data = request.get_json()
    link = data.get("fname")
    logging.info("Received request for video download: %s", link)
    try:
        p = Download(link)
    except Exception as e:
        logging.error("Error in downloading video: %s", str(e))
        return "Error in downloading video", 500
    logging.info("Sending file: %s", p)
    try:
        return send_file(p, as_attachment=True)
    except Exception as e:
        logging.error("Error in sending file: %s", str(e))
        return "Error in sending file", 500

@app.route("/")
def index():
    return send_from_directory("public", "index.html")

@app.route('/public/<path:path>')
def send_public(path):
    return send_from_directory('public', path)

if __name__ == '__main__':
    app.run(debug=True)