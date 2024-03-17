import paho.mqtt.client as mqtt


HOST = "localhost"
PORT = 1884
USER = "admin"
PASS = "Adm1n"

TOPIC = "fromRabbitMQ/someCompany/someDatabase/someDataKey"

client = mqtt.Client(client_id="mqtt-subscriber-abc123", clean_session=True)


def on_connect(client, userdata, flags, rc):
    print("on_connect")
    print(client)
    print(userdata)
    print(flags)
    print(rc)
    print()

    client.subscribe(TOPIC, qos=0)
    # client.subscribe(TOPIC, qos=1)


def on_message(client, userdata, message):
    print("on_message")
    print(client)
    print(userdata)
    print(message.topic)
    print(message.payload)
    print()


if __name__ == "__main__":
    print("started")
    try:
        client.on_connect = on_connect
        client.on_message = on_message

        client.username_pw_set(username=USER, password=PASS)
        client.connect(host=HOST, port=PORT)
        print("finished connecting")

        client.loop_forever()

    except KeyboardInterrupt:
        print("\nreceived keyboard interuption. exiting..")
        client.disconnect()
