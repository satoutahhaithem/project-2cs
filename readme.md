# 2CS project
In this groundbreaking project, we focused on creating a versatile system that can operate in standalone mode as well as a dedicated server mode. Let's delve into the key features and achievements of our project. 📝💡

🔹 Standalone Mode:
In the standalone mode, our project offers a comprehensive set of features. The web application, built using Flask, provides seamless request handling. We utilized TensorFlow Lite on a Raspberry Pi for real-time object detection during live video streaming. The system allows remote operation through web server commands and Raspberry Pi control. Additionally, we integrated an ultrasonic sensor for automatic actions based on proximity readings. Kafka was employed to enable the streaming of video frames from the Raspberry Pi to the web server, ensuring real-time video streaming with overlayed object detection information.

🔹 Dedicated Server Mode:
In the dedicated server mode, our project maintains consistent functionalities. The web application facilitates remote control and video streaming. Video frames captured by the Raspberry Pi are streamed to an external server, where the object detection process takes place using the YOLOv5 model. Kafka is employed to enable the communication and streaming of video frames between the Raspberry Pi and the external server. The remote and autonomous control system functionalities remain intact in this mode.
