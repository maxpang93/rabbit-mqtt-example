from datetime import datetime
import json
import time

import paho.mqtt.client as mqtt


HOST = "localhost"
PORT = 1884
USER = "admin"
PASS = "Adm1n"

TOPIC = "fromMQTT/someCompany/someDatabase/someDataKey"
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print("on_connect")
    print(client)
    print(userdata)
    print(flags)
    print(rc)
    print()


if __name__ == "__main__":
    print("started")
    try:
        client.on_connect = on_connect

        client.username_pw_set(username=USER, password=PASS)
        client.connect(host=HOST, port=PORT)
        print("finished connecting")

        counter = 0
        while True:
            time.sleep(0.1)
            counter += 1
            now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
            data = {"counter": counter, "timestamp": now}
            # qos=1
            qos = 0
            client.publish(TOPIC, payload=json.dumps(data), qos=qos)
            print(data)

    except KeyboardInterrupt:
        print("\nreceived keyboard interuption. exiting..")
        client.disconnect()
