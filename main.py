from flask import Flask, render_template, Response, request
from app.core.stream_handler import process_video_stream
from app.settings.streams import RTSP_URLS

app = Flask(__name__)

current_stream_index = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    global current_stream_index
    rtsp_url = RTSP_URLS[current_stream_index]
    return Response(process_video_stream(rtsp_url), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/switch_stream', methods=['POST'])
def switch_stream():
    global current_stream_index
    current_stream_index = (current_stream_index + 1) % len(RTSP_URLS)
    return {'status': 'success', 'current_stream': current_stream_index}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
