from flask import Flask, jsonify, render_template
import threading
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# Data storage for received messages
data_store = {}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("your/mqtt/topic")

def on_message(client, userdata, msg):
    global data_store
    print(f"Received message: {msg.payload}")
    try:
        message_data = json.loads(msg.payload.decode('utf-8'))
        data_store.update(message_data)  # This merges new data with existing keys, updating values
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")


def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(ca_certs="./AmazonRootCA1.pem", certfile="./certificate.pem.crt", keyfile="./private.pem.key")
    client.connect("a2u9gyfv7s162-ats.iot.ap-south-1.amazonaws.com", 8883, 60)
    client.loop_forever()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(data_store)

if __name__ == '__main__':
    threading.Thread(target=start_mqtt, daemon=True).start()
    app.run(debug=True, host='127.0.0.1', port=5000)
