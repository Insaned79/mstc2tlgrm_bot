import paho.mqtt.client as mqtt
import config
import logging
import base64
from Crypto.Cipher import AES
import datetime

try:
    from meshtastic import mesh_pb2, portnums_pb2, mqtt_pb2
except ImportError:
    import meshtastic.mesh_pb2 as mesh_pb2
    import meshtastic.portnums_pb2 as portnums_pb2
    import meshtastic.mqtt_pb2 as mqtt_pb2

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

BROADCAST_KEY = b'\x01' * 16


def decrypt_payload_ctr(encrypted, packet_id, from_id, key=BROADCAST_KEY):
    try:
        # nonce = id (8 bytes LE) + from (8 bytes LE)
        nonce = packet_id.to_bytes(8, 'little') + from_id.to_bytes(8, 'little')
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        decrypted = cipher.decrypt(encrypted)
        return decrypted
    except Exception as e:
        logging.warning(f"Decryption error (CTR): {e}")
        return None


def parse_and_log_message(packet):
    try:
        logging.info(f"Protobuf packet structure:\n{packet}")
        if packet.HasField("decoded"):
            decoded = packet.decoded
            if decoded.portnum == portnums_pb2.TEXT_MESSAGE_APP:
                text = decoded.payload.decode(errors='replace')
                from_id = getattr(packet, 'from')
                to_id = packet.to
                rssi = packet.rx_rssi
                hop_start = packet.hop_start
                hops_away = getattr(packet, 'hops_away', None)
                timestamp = packet.rx_time
                if timestamp:
                    ts_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    ts_str = "N/A"
                logging.info(f"Text message from {from_id} to {to_id}: {text} | RSSI: {rssi} | Hop start: {hop_start} | Hops away: {hops_away} | Time: {ts_str}")
            else:
                logging.info(f"Not a text message, portnum={decoded.portnum}")
        else:
            logging.info("No 'decoded' field in packet")
    except Exception as e:
        logging.warning(f"Protobuf parsing error: {e}")


def on_mqtt_message(client, userdata, msg):
    logging.info(f"Received binary message from topic {msg.topic}, length: {len(msg.payload)} bytes")
    # 1. Parse as ServiceEnvelope
    service_envelope = mqtt_pb2.ServiceEnvelope()
    try:
        service_envelope.ParseFromString(msg.payload)
        packet = service_envelope.packet
        # 2. If encrypted, decrypt via AES-CTR
        if packet.HasField("encrypted") and not packet.HasField("decoded"):
            encrypted = packet.encrypted
            packet_id = packet.id if packet.HasField("id") else 0
            from_id = getattr(packet, 'from') if packet.HasField("from") else 0
            decrypted_payload = decrypt_payload_ctr(encrypted, packet_id, from_id)
            if decrypted_payload:
                try:
                    decoded = mesh_pb2.DecodedPacket()
                    decoded.ParseFromString(decrypted_payload)
                    packet.decoded.CopyFrom(decoded)
                    parse_and_log_message(packet)
                except Exception as e:
                    logging.warning(f"Error parsing decrypted payload: {e}")
            else:
                logging.info("Failed to decrypt payload.")
        else:
            # If not encrypted or already has decoded
            parse_and_log_message(packet)
    except Exception as e:
        logging.warning(f"ServiceEnvelope parsing error: {e}")


def main():
    client = mqtt.Client()
    client.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
    client.on_message = on_mqtt_message
    client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
    topic = config.MQTT_TOPIC
    client.subscribe(topic)
    logging.info(f"Subscribed to binary topic: {topic}")
    logging.info("Started Meshtastic binary message logger.")
    client.loop_forever()

if __name__ == "__main__":
    main() 