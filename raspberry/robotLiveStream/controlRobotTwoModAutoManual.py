from kafka import KafkaConsumer
import RPi.GPIO as GPIO
from time import sleep
import json
import time

in1 = 18
in2 = 19
in3 = 20
in4 = 16
enB = 26
enA = 21

trig = 23
echo = 27

# Set up GPIO pins

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

p1=GPIO.PWM(enA,100)
p2=GPIO.PWM(enB,100)

p1.start(25)
p2.start(25)
speedF=70
speedB=60
speedRL=100
# Define functions to control the car
def forward(p1,p2):
    p1.ChangeDutyCycle(speedF)
    p2.ChangeDutyCycle(speedF)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
def forwardAuto(p1,p2):
    p1.ChangeDutyCycle(40)
    p2.ChangeDutyCycle(40)
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

def distance():
    # Send a signal to the sensor to start measuring distance
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)

    # Wait for the sensor to respond
    while GPIO.input(echo) == 0:
        pulse_start = time.time()

    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    # Calculate distance based on time measurement
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

# Listen for messages from Kafka
delayFB=1
delayRL=1

def run(isAuto):
    while isAuto:
        dist = distance()
        if dist < 30:
            stop()
            sleep(1)
            backward(p1, p2)
            sleep(0.5)
            left(p1, p2)
            time.sleep(0.5)
            stop()
            time.sleep(1)
        else:
            forwardAuto(p1, p2)
            message = None
            for tp, msgs in consumer.poll(timeout_ms=1000).items():
                for msg in msgs:
                    message = msg.value
            if message and message != "auto":
                isAuto = False
                stop()
                break
            elif message == "auto":
                isAuto = True
                break






# Set up Kafka consumer
consumer = KafkaConsumer('carControl',bootstrap_servers=['192.168.43.33:9092'],value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Listen for messages from Kafka
delayFB=1
delayRL=1
def move(direction):
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



import sys

def manual_mode():
    isAuto = False
    for message in consumer:
        direction = message.value
        print("the direction is ",direction)
        if direction == 'auto':
            isAuto = True
            print('Switching to auto mode', flush=True)
            run(isAuto)


        else:
            isAuto = False
            print('manual:', direction, flush=True)
            move(direction)

manual_mode()

