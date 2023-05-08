from kafka import KafkaConsumer
import cv2
import numpy as np
from flask import Flask, render_template, request, Response, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)

topic1 = 'test'
topic = 'carControl'
consumer = KafkaConsumer(
    topic1,
    bootstrap_servers=['192.168.43.33:9092'],
    auto_offset_reset='latest'
)
producer = KafkaProducer(bootstrap_servers=['192.168.43.33:9092'], value_serializer=lambda x: json.dumps(x).encode('utf-8'))


#_______________________________ the functions car control __________________________
def forward():
    producer.send(topic, 'forward')

def backward():
    producer.send(topic, 'backward')

def left():
    producer.send(topic, 'left')

def right():
    producer.send(topic, 'right')

def stop():
    producer.send(topic, 'stop')

def auto():
    producer.send(topic, 'auto')

def manual():
    producer.send(topic, 'manual')

#_____________________________________________________________________
#_______________________________ the functions live stream __________________________
def gen_frames():
    for msg in consumer:
        nparr = np.frombuffer(msg.value, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # resize the frame to a smaller size
        frame = cv2.resize(frame, (640, 480))
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])[1].tobytes() + b'\r\n')

#_____________________________________________________________________


#_______________________________ Routes __________________________
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/", methods=["POST", "GET"])
def control():
    if request.method == "POST":
        data = request.get_json()
        command = data.get('command')

        if command == 'forward':
            forward()
        elif command == 'backward':
            backward()
        elif command == 'left':
            left()
        elif command == 'right':
            right()
        elif command == 'stop':
            stop()
        elif command == 'auto':
            auto()
        elif command ==  'manual':
            manual()


        return jsonify({'status': 'success'})
    
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
