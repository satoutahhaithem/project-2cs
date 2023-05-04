from kafka import KafkaConsumer
import cv2
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)

topic = 'test'
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=['192.168.43.33:9092'],
    auto_offset_reset='latest'
)

def gen_frames():
    for msg in consumer:
        nparr = np.frombuffer(msg.value, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # resize the frame to a smaller size
        frame = cv2.resize(frame, (640, 480))
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])[1].tobytes() + b'\r\n')
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
