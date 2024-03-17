from datetime import datetime
import json
import time

import pika

EXCHANGE = "amq.topic"
MQTT_TOPIC = "fromRabbitMQ.someCompany.someDatabase.someDataKey"  # routing-key: '.' will auto convert to '/' by MQTT Plugin
HOST = "localhost"
PORT = 5673
USER = "admin"
PASS = "Adm1n"
MSG_DURABLE = True

if __name__ == "__main__":
    print("started")
    try:
        creds = pika.PlainCredentials(username=USER, password=PASS)
        params = pika.ConnectionParameters(host=HOST, port=PORT, credentials=creds)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        print("finished connecting")

        counter = 0
        while True:
            time.sleep(0.5)
            counter += 1
            now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
            data = {"counter": counter, "timestamp": now}

            delivery_mode = 2 if MSG_DURABLE else 1
            properties = pika.BasicProperties(delivery_mode=delivery_mode)
            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=MQTT_TOPIC,
                body=json.dumps(data),
                properties=properties,
            )
            print(data)

    except KeyboardInterrupt as e:
        print("\nreceived keyboard interuption. exiting..")
        channel.stop_consuming()
        channel.close()
        connection.close()
