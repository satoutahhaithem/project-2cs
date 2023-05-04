import cv2
from kafka import KafkaProducer

topic = 'test'

producer = KafkaProducer(bootstrap_servers=['192.168.43.33:9092'])

vc = cv2.VideoCapture(0)
vc.set(cv2.CAP_PROP_FPS, 30)
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = vc.read()
    if not ret:
        print("Video stream not available!")
        break

    # Convert the frame to bytes
    is_success, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
    if not is_success:
        print("Error converting frame to bytes!")
        break

    # Send the frame as a message to Kafka
    producer.send(topic, buffer.tobytes())