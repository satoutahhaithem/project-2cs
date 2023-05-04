from kafka import KafkaConsumer

consumer = KafkaConsumer('test', bootstrap_servers=['192.168.43.33:9092'])

for message in consumer:
    print(message.value.decode('utf-8'))
