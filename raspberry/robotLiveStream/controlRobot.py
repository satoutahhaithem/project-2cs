from kafka import KafkaConsumer
import RPi.GPIO as GPIO
from time import sleep
import json


in1 = 18
in2 = 19
in3 = 20
in4 = 16
enB = 26
enA = 21

# Set up GPIO pins

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)

p1=GPIO.PWM(enA,1000)
p2=GPIO.PWM(enB,1000)

p1.start(25)
p2.start(25)
speedF=100
speedB=100
speedRL=100
# Define functions to control the car
def forward(p1,p2):
    p1.ChangeDutyCycle(speedF)
    p2.ChangeDutyCycle(speedF)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)

def backward(p1,p2):
    p1.ChangeDutyCycle(speedB)
    p2.ChangeDutyCycle(speedB)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)

def right(p1,p2):
    p1.ChangeDutyCycle(speedRL)
    p2.ChangeDutyCycle(speedRL)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)

def left(p1,p2):
    p1.ChangeDutyCycle(speedRL)
    p2.ChangeDutyCycle(speedRL)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)

def stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

# Set up Kafka consumer
consumer = KafkaConsumer('carControl',bootstrap_servers=['192.168.43.33:9092'],value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Listen for messages from Kafka
delayFB=1
delayRL=1
for message in consumer:
    direction = message.value
    if direction == 'forward':
        forward(p1,p2)
    elif direction == 'backward':
        backward(p1,p2)
    elif direction == 'left':
        left(p1,p2)

    elif direction == 'right':
        right(p1,p2)
    elif direction == 'stop':
        stop()
