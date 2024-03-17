import pika


EXCHANGE = "amq.topic"
HOST = "localhost"
PORT = 5673
USER = "admin"
PASS = "Adm1n"

# RMQ routing key. MQTT publisher publish to fromMQTT/someCompany/someDatabase/someDataKey
SUBSCRIBED_TOPIC = "fromMQTT.someCompany.someDatabase.someDataKey"
QUEUE = "mqtt2rmq-queue"


def callback(channel, method, properties, body):
    data = body.decode("utf-8")
    print(data)


if __name__ == "__main__":
    print("started")
    try:
        creds = pika.PlainCredentials(username=USER, password=PASS)
        params = pika.ConnectionParameters(host=HOST, port=PORT, credentials=creds)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(QUEUE)
        channel.queue_bind(queue=QUEUE, exchange=EXCHANGE, routing_key=SUBSCRIBED_TOPIC)
        channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)
        print("finished connecting")

        channel.start_consuming()

    except KeyboardInterrupt as e:
        print("\nreceived keyboard interuption. exiting..")
        channel.stop_consuming()
        channel.close()
        connection.close()
