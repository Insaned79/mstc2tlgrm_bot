import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import config
import os
import threading
import paho.mqtt.client as mqtt
import base64
from Crypto.Cipher import AES
import datetime
import queue
import asyncio
from collections import OrderedDict
import re

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

# Suppress verbose Telegram HTTP logs and hide token
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram.vendor.ptb_urllib3.urllib3.connectionpool").setLevel(logging.WARNING)
logging.getLogger("telegram.request").setLevel(logging.WARNING)
logging.getLogger("telegram.bot").setLevel(logging.WARNING)

SUBSCRIBERS_FILE = "subscribers.txt"
BROADCAST_KEY = b'\x01' * 16

# Queue for passing messages between MQTT and Telegram
message_queue = queue.Queue()

# Cache for recent message ids to prevent duplicates
recent_ids = OrderedDict()
RECENT_IDS_MAX = 500

def load_subscribers():
    if not os.path.exists(SUBSCRIBERS_FILE):
        return set()
    with open(SUBSCRIBERS_FILE, "r") as f:
        return set(int(line.strip()) for line in f if line.strip())

def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, "w") as f:
        for chat_id in subscribers:
            f.write(f"{chat_id}\n")

subscribers = load_subscribers()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in subscribers:
        subscribers.add(chat_id)
        save_subscribers(subscribers)
        await update.message.reply_text("You are now subscribed to Meshtastic messages!")
        logging.info(f"User {chat_id} subscribed.")
    else:
        await update.message.reply_text("You are already subscribed.")

# --- MQTT and Meshtastic message handling ---
def decrypt_payload_ctr(encrypted, packet_id, from_id, key=BROADCAST_KEY):
    try:
        nonce = packet_id.to_bytes(8, 'little') + from_id.to_bytes(8, 'little')
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        decrypted = cipher.decrypt(encrypted)
        return decrypted
    except Exception as e:
        logging.warning(f"Decryption error (CTR): {e}")
        return None

def format_meshtastic_message(packet):
    try:
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
                # Format text for HTML
                text_html = f"<b>{text}</b>"
                return f"Text message from {from_id} to {to_id}: {text_html}\nRSSI: {rssi} | Hop start: {hop_start} | Hops away: {hops_away} | Time: {ts_str}", 'HTML'
    except Exception as e:
        logging.warning(f"Protobuf parsing error: {e}")
    return None, None

def is_duplicate(packet_id, max_size=RECENT_IDS_MAX):
    if packet_id in recent_ids:
        return True
    recent_ids[packet_id] = True
    if len(recent_ids) > max_size:
        recent_ids.popitem(last=False)
    return False

def on_mqtt_message(client, userdata, msg):
    service_envelope = mqtt_pb2.ServiceEnvelope()
    try:
        service_envelope.ParseFromString(msg.payload)
        packet = service_envelope.packet
        # Log every received MQTT message (id, from, to, portnum, length)
        try:
            log_id = getattr(packet, 'id', None)
            log_from = getattr(packet, 'from', None)
            log_to = getattr(packet, 'to', None)
            log_portnum = packet.decoded.portnum if packet.HasField('decoded') else None
            logging.info(f"MQTT received: id={log_id}, from={log_from}, to={log_to}, portnum={log_portnum}, len={len(msg.payload)}")
        except Exception as e:
            logging.warning(f"Failed to log MQTT message meta: {e}")
        # Check for duplicate by id
        packet_id = packet.id if hasattr(packet, 'id') else None
        if packet_id is not None and is_duplicate(packet_id):
            logging.info(f"Duplicate message id {packet_id}, skipping.")
            return
        if packet.HasField("encrypted") and not packet.HasField("decoded"):
            encrypted = packet.encrypted
            packet_id = getattr(packet, 'id', 0)
            from_id = getattr(packet, 'from') if packet.HasField("from") else 0
            decrypted_payload = decrypt_payload_ctr(encrypted, packet_id, from_id)
            if decrypted_payload:
                try:
                    decoded = mesh_pb2.DecodedPacket()
                    decoded.ParseFromString(decrypted_payload)
                    packet.decoded.CopyFrom(decoded)
                except Exception as e:
                    logging.warning(f"Error parsing decrypted payload: {e}")
                    logging.info(f"MQTT message id={packet_id} not sent: failed to parse decrypted payload.")
                    return
            else:
                logging.info("Failed to decrypt payload.")
                logging.info(f"MQTT message id={packet_id} not sent: failed to decrypt payload.")
                return
        # Format text for Telegram
        text, parse_mode = format_meshtastic_message(packet)
        if text:
            message_queue.put((text, parse_mode))
        else:
            logging.info(f"MQTT message id={packet_id} not sent: not a text message or failed to format.")
    except Exception as e:
        logging.warning(f"ServiceEnvelope parsing error: {e}")
        logging.info(f"MQTT message not sent: ServiceEnvelope parsing error.")

def mqtt_thread():
    client = mqtt.Client()
    client.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
    client.on_message = on_mqtt_message
    client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
    topic = config.MQTT_TOPIC
    client.subscribe(topic)
    logging.info(f"Subscribed to binary topic: {topic}")
    logging.info("Started Meshtastic binary message forwarder (MQTT thread).")
    client.loop_forever()

async def telegram_forwarder(app):
    while True:
        try:
            text, parse_mode = None, None
            # Wait for a new message from the queue (blocking, but with timeout for graceful shutdown)
            msg = await asyncio.get_event_loop().run_in_executor(None, message_queue.get)
            if isinstance(msg, tuple):
                text, parse_mode = msg
            else:
                text = msg
            sent = False
            for chat_id in load_subscribers():
                try:
                    await app.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
                    logging.info(f"Sent to {chat_id}: {text}")
                    sent = True
                except Exception as e:
                    logging.warning(f"Failed to send message to {chat_id}: {e}")
            if not sent:
                logging.info(f"Message was not sent to any subscriber: {text}")
        except Exception as e:
            logging.warning(f"Error in telegram_forwarder: {e}")
        await asyncio.sleep(0.1)

async def post_init(app):
    app.create_task(telegram_forwarder(app))


def main():
    # Start MQTT in a separate thread
    threading.Thread(target=mqtt_thread, daemon=True).start()
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    logging.info("Telegram bot started.")
    app.run_polling()

if __name__ == "__main__":
    main() 