from kafka import KafkaProducer
import json

# Define the Kafka server and topic
kafka_server = 'localhost:9092'
kafka_topic = 'test'

# Create a Kafka producer instance
producer = KafkaProducer(
    bootstrap_servers=[kafka_server],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Send a message to Kafka
message = {'key': 'value'}
producer.send(kafka_topic, value=message)

# Wait for any outstanding messages to be delivered and delivery reports received
producer.flush()

# Close the producer connection
producer.close()
