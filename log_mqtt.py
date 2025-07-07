import paho.mqtt.client as mqtt
import config
import logging
import json
import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        # New format: type == 'text' and payload['text']
        if data.get("type") == "text" and "payload" in data and "text" in data["payload"]:
            text = data["payload"]["text"]
            from_id = data.get("from")
            to_id = data.get("to")
            sender = data.get("sender")
            rssi = data.get("rssi")
            hop_start = data.get("hop_start")
            hops_away = data.get("hops_away")
            timestamp = data.get("timestamp")
            if timestamp:
                ts_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            else:
                ts_str = "N/A"
            logging.info(f"Text message from {from_id} ({sender}) to {to_id}: {text} | RSSI: {rssi} | Hop start: {hop_start} | Hops away: {hops_away} | Time: {ts_str}")
        # Old format (if encountered)
        elif "decoded" in data:
            decoded = data["decoded"]
            portnum = decoded.get("portnum")
            if portnum == 1 or portnum == "TEXT_MESSAGE_APP":
                text = decoded.get("payload")
                from_id = data.get("from")
                to_id = data.get("to")
                rssi = data.get("rssi")
                hop_start = data.get("hop_start")
                hops_away = data.get("hops_away")
                timestamp = data.get("timestamp")
                if timestamp:
                    ts_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    ts_str = "N/A"
                logging.info(f"Text message from {from_id} to {to_id}: {text} | RSSI: {rssi} | Hop start: {hop_start} | Hops away: {hops_away} | Time: {ts_str}")
    except Exception:
        pass

def main():
    client = mqtt.Client()
    client.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
    client.on_message = on_message
    client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
    topic = config.MQTT_JSON_TOPIC
    client.subscribe(topic)
    logging.info(f"Subscribed to topic: {topic}")
    logging.info("Started Meshtastic JSON text message logger.")
    client.loop_forever()

if __name__ == "__main__":
    main() 